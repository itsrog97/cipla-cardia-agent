"""
LAYER 5 — LLM NARRATION  (Google AI Studio / Gemini, with Claude fallback)

The LLM never computes a ranking. It receives the metric table produced by
engine.py and turns it into an answer. That guardrail is a slide bullet:
"the agent's reasoning is grounded — the model reads computed metrics, it
does not recall pharma facts."

Provider is chosen automatically:
  GOOGLE_API_KEY set    -> Gemini  (Google AI Studio)
  ANTHROPIC_API_KEY set -> Claude
Force one with  PROVIDER=gemini  or  PROVIDER=claude  in .env

MODEL RESOLUTION
Google retires model IDs for new API keys, so nothing is hardcoded. On first
call the code asks your own key which models it can access and picks the best
available one. Override in .env with:   GEMINI_MODEL=gemini-flash-latest
"""

import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()  # reads the .env file sitting next to this script

CLAUDE_MODEL = "claude-sonnet-4-6"

# Preference order, best first. The first one your key supports wins.
# '-latest' aliases track Google's current generation without code edits.
GEMINI_PREFERENCE = [
    "gemini-flash-latest",
    "gemini-3-flash",
    "gemini-3-pro-preview",
    "gemini-pro-latest",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
]

_RESOLVED = None  # cache so we only list models once per session

SYSTEM = """You are the reasoning layer of CARDIA-PRIORITISE, an opportunity-
prioritisation agent for Cipla's India Cardiac portfolio.

RULES
1. Use ONLY the metric table provided. Never introduce a market number from
   your own knowledge. If a number is not in the table, say it is not available.
2. Every claim must name the metric that supports it.
3. Cipla holds ~0.09% share of this Rs 23,244 Cr market, so 'right to win'
   means transferable capability (chronic-care detailing, solid-oral FDC
   development, brand building), not incumbency. Never imply Cipla is a leader.
4. Answer like a strategy consultant briefing a CEO: verdict first, then the
   two or three numbers that drive it. No preamble.
"""


# ------------------------------------------------------------------
def provider() -> str:
    forced = os.environ.get("PROVIDER", "").lower()
    if forced in ("gemini", "claude"):
        return forced
    if os.environ.get("GOOGLE_API_KEY"):
        return "gemini"
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "claude"
    return "none"


def _gemini_client():
    from google import genai
    return genai.Client(api_key=os.environ["GOOGLE_API_KEY"])


def list_gemini_models() -> list:
    """Every model this API key can call generateContent on."""
    out = []
    for m in _gemini_client().models.list():
        actions = getattr(m, "supported_actions", None) or []
        if not actions or "generateContent" in actions:
            out.append(m.name.replace("models/", ""))
    return out


def resolve_gemini_model(force_refresh: bool = False) -> str:
    """Pick a model that actually works with this key. Cached per session."""
    global _RESOLVED
    if _RESOLVED and not force_refresh:
        return _RESOLVED

    # 1. explicit override always wins
    override = os.environ.get("GEMINI_MODEL", "").strip()
    if override:
        _RESOLVED = override
        return _RESOLVED

    # 2. ask the key what it has, then apply our preference order
    try:
        available = list_gemini_models()
    except Exception:
        available = []

    for want in GEMINI_PREFERENCE:
        if want in available:
            _RESOLVED = want
            return _RESOLVED

    # 3. nothing matched by name — take any flash model, else any model at all
    flash = [m for m in available if "flash" in m and "image" not in m
             and "tts" not in m and "audio" not in m and "embedding" not in m]
    if flash:
        _RESOLVED = flash[0]
        return _RESOLVED
    usable = [m for m in available if "embedding" not in m and "image" not in m]
    _RESOLVED = usable[0] if usable else GEMINI_PREFERENCE[0]
    return _RESOLVED


def active_model() -> str:
    """What the UI should display."""
    p = provider()
    if p == "gemini":
        try:
            return resolve_gemini_model()
        except Exception:
            return "unresolved"
    return CLAUDE_MODEL if p == "claude" else "none"


def _table(df: pd.DataFrame, n: int = 15) -> str:
    cols = ["size", "val_cagr", "vol_cagr", "price_contrib", "HHI",
            "n_companies", "leader_share", "cipla_share", "tailwind",
            "nlem", "score", "verdict", "signal_note"]
    cols = [c for c in cols if c in df.columns]
    return df.head(n)[cols].round(3).to_markdown()


# ------------------------------------------------------------------
def _ask_gemini(prompt: str, model: str = None) -> str:
    from google.genai import types

    client = _gemini_client()
    cfg = types.GenerateContentConfig(
        system_instruction=SYSTEM,
        temperature=0.2,          # low: this is analysis, not creative writing
        max_output_tokens=1500,
    )
    chosen = model or resolve_gemini_model()
    try:
        return client.models.generate_content(
            model=chosen, contents=prompt, config=cfg).text
    except Exception as e:
        # a retired / unavailable model -> re-resolve once and retry
        if "404" in str(e) or "NOT_FOUND" in str(e):
            retry = resolve_gemini_model(force_refresh=True)
            if retry != chosen:
                return client.models.generate_content(
                    model=retry, contents=prompt, config=cfg).text
            avail = ", ".join(list_gemini_models()[:12]) or "none returned"
            raise RuntimeError(
                f"Gemini rejected '{chosen}'. Models your key can use: {avail}. "
                f"Put one of these in .env as GEMINI_MODEL=..."
            ) from e
        raise


def _ask_claude(prompt: str, model: str = None) -> str:
    from anthropic import Anthropic

    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    msg = client.messages.create(
        model=model or CLAUDE_MODEL,
        max_tokens=1500,
        system=SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(b.text for b in msg.content if b.type == "text")


# ------------------------------------------------------------------
def ask(df: pd.DataFrame, question: str, model: str = None) -> str:
    """Answer a judge's question against the computed table."""
    prompt = (f"METRIC TABLE (top ranked opportunity spaces):\n\n{_table(df)}\n\n"
              f"QUESTION: {question}")
    p = provider()
    if p == "gemini":
        return _ask_gemini(prompt, model)
    if p == "claude":
        return _ask_claude(prompt, model)
    return "No API key found. Set GOOGLE_API_KEY (or ANTHROPIC_API_KEY) in your .env file."


def slide_bullets(df: pd.DataFrame, model: str = None) -> str:
    """Generate the recommendation slide copy from the ranked output."""
    return ask(df,
               "Write slide copy for a 3-slide first-round deck: "
               "Slide 1 = the agent (objective, inputs, framework, metrics, trade-off rules). "
               "Slide 2 = top 5 opportunities with the 2-3 to prioritise, and the trade-offs "
               "resolved. Slide 3 = right to win vs competitors, underpenetrated spaces, and "
               "the enter / build / selective / avoid verdicts. "
               "Max 6 bullets per slide, every bullet carrying a number.",
               model=model)


# ------------------------------------------------------------------
# Diagnostics:  python llm.py
if __name__ == "__main__":
    print(f"Provider : {provider()}")
    if provider() == "gemini":
        try:
            models = list_gemini_models()
            print(f"Models your key can use ({len(models)}):")
            for m in models:
                print("  -", m)
        except Exception as e:
            print("Could not list models:", e)
        print(f"\nSelected : {resolve_gemini_model()}")

    try:
        import engine as E, signals as S
        d = E.score(E.apply_signals(E.build_metrics(E.load()), S.SIGNALS))
        print("\n--- test answer ---")
        print(ask(d, "Which 2-3 spaces should Cipla prioritise and why?"))
    except Exception as e:
        print("Test call failed:", e)
