"""
CARDIA-PRIORITISE  |  Layer 1 + 2 + 4
Deterministic scoring engine for the Cipla Ascend S4 Cardiac case.

No LLM here on purpose. Every number a judge can ask about is computed
in pandas and is reproducible. The LLM layer (llm.py) only narrates
what this file computes.
"""

import numpy as np
import pandas as pd

# ----- column constants (exactly as they appear in the Cipla file) -----
V24, V25, V26 = "MAT FEB'24", "MAT FEB'25", "MAT FEB'26"
CP25, CP26 = "MAT CP FEB'25", "MAT CP FEB'26"
Q24, Q25, Q26 = "QTY MAT FEB'24", "QTY MAT FEB'25", "QTY MAT FEB'26"
CO = "COMPANY CLUSTER"
CIPLA = "CIPLA*"


# =====================================================================
# LAYER 1 — INGEST
# =====================================================================
def load(path: str = "data.xlsx") -> pd.DataFrame:
    """Read the Cardiac sheet and derive the archetype fields."""
    df = pd.read_excel(path, sheet_name="Cardiac")
    df.columns = [c.strip() for c in df.columns]

    df["SUBGROUP"] = df["SUBGROUP"].astype(str).str.strip()
    # 'C02F06 AMLODIPINE+TELMISARTAN' -> code / molecule string
    df["ATC"] = df["SUBGROUP"].str.split(" ").str[0]
    df["MOL_SET"] = df["SUBGROUP"].str.split(" ", n=1).str[1].fillna("")
    # combo order = how many molecules in the FDC (1 = plain, 3+ = poly)
    df["COMBO_ORDER"] = df["MOL_SET"].str.count(r"\+") + 1
    df["ARCHETYPE"] = df["COMBO_ORDER"].map(
        {1: "Mono", 2: "Dual FDC", 3: "Triple FDC"}
    ).fillna("Poly FDC")
    return df


# =====================================================================
# LAYER 2 — METRICS
# =====================================================================
def build_metrics(df: pd.DataFrame, level: str = "SUBGROUP") -> pd.DataFrame:
    """Aggregate to an opportunity-space level and compute every raw metric."""
    g = df.groupby(level)
    m = g[[V24, V25, V26, CP26, Q24, Q25, Q26]].sum()

    # --- growth: value vs volume vs price -----------------------------
    m["val_cagr"] = _cagr(m[V26], m[V24], 2)
    m["vol_cagr"] = _cagr(m[Q26], m[Q24], 2)
    m["val_yoy"] = m[V26] / m[V25] - 1
    m["accel"] = (m[V26] / m[V25]) - (m[V25] / m[V24])       # growth accelerating?
    # MAT CP holds prior-year prices, so the value/CP gap is pure price effect
    m["price_growth"] = np.where(m[CP26] > 0, m[V26] / m[CP26] - 1, 0)
    m["price_contrib"] = np.where(
        m["val_cagr"] > 0, (m["val_cagr"] - m["vol_cagr"]) / m["val_cagr"], 1.0
    ).clip(0, 1)

    # --- competitive intensity ---------------------------------------
    share = df.groupby([level, CO])[V26].sum()
    tot = share.groupby(level).sum()
    frac = share / tot.reindex(share.index.get_level_values(0)).values
    m["HHI"] = (frac ** 2).groupby(level).sum() * 10000
    m["n_companies"] = g[CO].nunique()
    m["n_brands"] = g["BRANDS"].nunique()
    m["leader_share"] = frac.groupby(level).max() * 100

    # --- Cipla position ----------------------------------------------
    cip = df[df[CO] == CIPLA].groupby(level)[V26].sum()
    m["cipla_val"] = cip.reindex(m.index).fillna(0)
    m["cipla_share"] = 100 * m["cipla_val"] / m[V26]
    m["cipla_rank"] = share.groupby(level).rank(ascending=False).reindex(
        [(i, CIPLA) for i in m.index]
    ).values
    m["cipla_rank"] = pd.Series(m["cipla_rank"], index=m.index).fillna(999)

    # --- context -----------------------------------------------------
    m["archetype"] = g["ARCHETYPE"].agg(lambda s: s.mode().iat[0])
    m["segment"] = g["CARDIAC SEGMENT"].agg(lambda s: s.mode().iat[0])
    m["sub_segment"] = g["CARDIAC SUB SEGMENTS"].agg(lambda s: s.mode().iat[0])
    m["mnc_share"] = 100 * df[df["INDIAN_MNC"] == "MNC"].groupby(level)[V26].sum().reindex(
        m.index).fillna(0) / m[V26]

    return m.rename(columns={V26: "size", V24: "size_24"})


def _cagr(end, start, yrs):
    return np.where(start > 0, (end / start.replace(0, np.nan)) ** (1 / yrs) - 1, np.nan)


# =====================================================================
# LAYER 3 — EXTERNAL SIGNALS  (see signals.py for the mapped table)
# =====================================================================
def apply_signals(m: pd.DataFrame, signals: dict) -> pd.DataFrame:
    """
    signals = { 'C02F0O': {'tailwind': +2, 'nlem': -1, 'note': '...'} , ... }
    tailwind: -3..+3  guideline / prevalence / LOE pull
    nlem:     -3..0   price-control exposure
    """
    m = m.copy()
    m["tailwind"] = 0.0
    m["nlem"] = 0.0
    m["signal_note"] = ""
    for key, s in signals.items():
        hit = m.index.astype(str).str.contains(key, regex=False)
        m.loc[hit, "tailwind"] = s.get("tailwind", 0)
        m.loc[hit, "nlem"] = s.get("nlem", 0)
        m.loc[hit, "signal_note"] = s.get("note", "")
    return m


# =====================================================================
# LAYER 4 — SCORE + VERDICT
# =====================================================================
DEFAULT_WEIGHTS = {
    "attractiveness": 0.30,
    "future": 0.25,
    "competition": 0.20,
    "fit": 0.25,
}

# adjacency: Cipla's transferable right-to-win by archetype / segment.
# Cipla holds ~0.09% Cardiac share, so current share alone scores everything
# to zero — RTW must be built from what actually transfers.
ADJACENCY = {
    "Statins Plain": 0.7,      # Lipvas legacy brand equity
    "Statins Comb.": 0.5,      # solid-oral FDC capability, no brand yet
    "AHT Dual Comb.": 0.6,     # Amlip franchise
    "AHT Triple / Poly Comb.": 0.5,
    "CCB": 0.6,
    "ARBs": 0.4,
    "AHT Diuretic Comb.": 0.4,
    "Oth. Lipid Red.": 0.3,    # specialty, needs new capability
    "Nitrates": 0.3,
    "ACEi": 0.3,
}


def score(m: pd.DataFrame,
          weights: dict = None,
          min_size: float = 150.0,
          price_penalty: bool = True,
          use_rtw: bool = True) -> pd.DataFrame:
    """Rank opportunity spaces. Returns a scored, sorted frame."""
    w = {**DEFAULT_WEIGHTS, **(weights or {})}
    d = m[m["size"] >= min_size].copy()          # TRADE-OFF 1: size gate

    pr = lambda s: s.rank(pct=True)              # percentile-rank normaliser

    # Pillar 1 — market attractiveness
    d["P_attract"] = (0.45 * pr(d["size"]) + 0.40 * pr(d["val_cagr"])
                      + 0.15 * pr(d["accel"]))

    # Pillar 2 — future potential (volume truth + external signals)
    d["P_future"] = (0.50 * pr(d["vol_cagr"]) + 0.35 * pr(d["tailwind"])
                     + 0.15 * pr(d["nlem"]))

    # Pillar 3 — competitive intensity (inverted: less crowded = better)
    d["P_compete"] = (0.50 * pr(-d["HHI"]) + 0.30 * pr(-d["leader_share"])
                      + 0.20 * pr(-d["n_brands"] / d["size"]))

    # Pillar 4 — strategic fit / right to win
    d["adjacency"] = d["sub_segment"].map(ADJACENCY).fillna(0.3)
    d["P_fit"] = (0.55 * pr(d["adjacency"]) + 0.25 * pr(d["cipla_share"])
                  + 0.20 * pr(-d["cipla_rank"]))

    d["score"] = (w["attractiveness"] * d["P_attract"]
                  + w["future"] * d["P_future"]
                  + w["competition"] * d["P_compete"]
                  + (w["fit"] * d["P_fit"] if use_rtw else 0))
    if not use_rtw:
        d["score"] /= (1 - w["fit"])

    # TRADE-OFF 2: growth that is price, not patients, gets discounted
    if price_penalty:
        d["price_flag"] = d["price_contrib"] > 0.60
        d["score"] *= np.where(d["price_flag"], 0.85, 1.0)
    else:
        d["price_flag"] = False

    # TRADE-OFF 3: attractiveness x right-to-win -> action verdict
    a_hi = d["P_attract"] + d["P_future"] > (d["P_attract"] + d["P_future"]).median()
    r_hi = d["P_fit"] > d["P_fit"].median()
    d["verdict"] = np.select(
        [a_hi & r_hi, a_hi & ~r_hi, ~a_hi & r_hi],
        ["ENTER & SCALE", "BUILD CAPABILITY", "SELECTIVE"],
        default="AVOID",
    )
    # closed markets are un-enterable regardless of growth
    d.loc[(d["HHI"] > 3000) & (d["cipla_share"] < 1), "verdict"] = "AVOID - CLOSED"

    d["score"] = (d["score"] * 100).round(1)
    return d.sort_values("score", ascending=False)


def explain(row: pd.Series) -> str:
    """Deterministic 'why this rank' string — the Finale answer."""
    return (
        f"Size Rs {row['size']:,.0f} Cr (pct {row['P_attract']:.0%} attractiveness) | "
        f"value CAGR {row['val_cagr']:.1%} vs volume CAGR {row['vol_cagr']:.1%} "
        f"({row['price_contrib']:.0%} of growth is price) | "
        f"HHI {row['HHI']:,.0f} across {row['n_companies']:.0f} companies, "
        f"leader {row['leader_share']:.0f}% | "
        f"Cipla share {row['cipla_share']:.2f}%, adjacency {row['adjacency']:.1f} "
        f"-> {row['verdict']}"
    )


def market_summary(df: pd.DataFrame) -> dict:
    return {
        "size_26": df[V26].sum(),
        "val_cagr": (df[V26].sum() / df[V24].sum()) ** 0.5 - 1,
        "vol_cagr": (df[Q26].sum() / df[Q24].sum()) ** 0.5 - 1,
        "cipla_val": df[df[CO] == CIPLA][V26].sum(),
        "cipla_share": 100 * df[df[CO] == CIPLA][V26].sum() / df[V26].sum(),
        "n_spaces": df["SUBGROUP"].nunique(),
    }
