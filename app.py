"""
CARDIA-PRIORITISE — Streamlit front end
Run:  streamlit run app.py
"""

import os
import pandas as pd
import plotly.express as px
import streamlit as st

import engine as E
import signals as S

st.set_page_config(page_title="CARDIA-PRIORITISE", layout="wide")


# ---------- cached data ----------
@st.cache_data
def get_data(path):
    df = E.load(path)
    return df, E.market_summary(df)


st.title("CARDIA-PRIORITISE")
st.caption("AI-enabled opportunity prioritisation | Cipla India Cardiac | Ascend Season 4")

# ---------- sidebar: the demo surface ----------
with st.sidebar:
    st.header("Agent controls")
    src = st.text_input("Dataset", "data.xlsx")
    level = st.selectbox("Opportunity space granularity",
                         ["SUBGROUP", "CARDIAC SUB SEGMENTS", "ARCHETYPE"], index=0)
    st.divider()
    st.subheader("Pillar weights")
    w1 = st.slider("Market attractiveness", 0.0, 1.0, 0.30, 0.05)
    w2 = st.slider("Future potential", 0.0, 1.0, 0.25, 0.05)
    w3 = st.slider("Competitive intensity", 0.0, 1.0, 0.20, 0.05)
    w4 = st.slider("Strategic fit / right to win", 0.0, 1.0, 0.25, 0.05)
    tot = w1 + w2 + w3 + w4
    st.caption(f"Weights normalise to 1.00 (currently {tot:.2f})")
    st.divider()
    min_size = st.slider("Minimum market size gate (Rs Cr)", 0, 800, 150, 25)
    price_pen = st.checkbox("Penalise price-led growth (>60% price)", True)
    use_rtw = st.checkbox("Include right-to-win in score", True)
    use_sig = st.checkbox("Overlay external signals", True)

df, summ = get_data(src)

# ---------- headline ----------
c = st.columns(5)
c[0].metric("Cardiac market", f"Rs {summ['size_26']:,.0f} Cr")
c[1].metric("Value CAGR", f"{summ['val_cagr']:.1%}")
c[2].metric("Volume CAGR", f"{summ['vol_cagr']:.1%}", "price-led growth", delta_color="inverse")
c[3].metric("Cipla share", f"{summ['cipla_share']:.2f}%")
c[4].metric("Opportunity spaces", summ["n_spaces"])

st.info(
    f"**Headline finding:** the market grows {summ['val_cagr']:.1%} in value but only "
    f"{summ['vol_cagr']:.1%} in volume — roughly "
    f"{(1 - summ['vol_cagr'] / summ['val_cagr']):.0%} of headline growth is price/mix. "
    f"Cipla participates at Rs {summ['cipla_val']:.0f} Cr ({summ['cipla_share']:.2f}% share), "
    "so right-to-win is an adjacency question, not a defence question."
)

# ---------- score ----------
m = E.build_metrics(df, level=level)
m = E.apply_signals(m, S.SIGNALS if use_sig else {})
weights = {"attractiveness": w1 / tot, "future": w2 / tot,
           "competition": w3 / tot, "fit": w4 / tot}
d = E.score(m, weights=weights, min_size=min_size,
            price_penalty=price_pen, use_rtw=use_rtw)

tab1, tab2, tab3, tab4 = st.tabs(
    ["Ranked opportunities", "Attractiveness x Right-to-win", "Why this rank?", "Ask the agent"])

# ---------- tab 1 ----------
with tab1:
    show = d.head(20)[["size", "val_cagr", "vol_cagr", "price_contrib", "HHI",
                       "n_companies", "leader_share", "cipla_share",
                       "tailwind", "score", "verdict"]]
    st.dataframe(
        show.style.format({
            "size": "{:,.0f}", "val_cagr": "{:.1%}", "vol_cagr": "{:.1%}",
            "price_contrib": "{:.0%}", "HHI": "{:,.0f}", "leader_share": "{:.0f}%",
            "cipla_share": "{:.2f}%", "score": "{:.1f}"}),
        use_container_width=True, height=560)
    st.download_button("Download ranked output (CSV)",
                       d.to_csv().encode(), "cardia_ranked.csv")

# ---------- tab 2 ----------
with tab2:
    p = d.copy()
    p["attractiveness"] = (p["P_attract"] + p["P_future"]) / 2 * 100
    p["right_to_win"] = p["P_fit"] * 100
    fig = px.scatter(p.reset_index(), x="right_to_win", y="attractiveness",
                     size="size", color="verdict", hover_name=p.index,
                     labels={"right_to_win": "Right to win (percentile)",
                             "attractiveness": "Attractiveness + future potential"},
                     height=620)
    fig.add_hline(y=p["attractiveness"].median(), line_dash="dot")
    fig.add_vline(x=p["right_to_win"].median(), line_dash="dot")
    st.plotly_chart(fig, use_container_width=True)

# ---------- tab 3 ----------
with tab3:
    pick = st.selectbox("Opportunity space", d.index.tolist())
    row = d.loc[pick]
    st.success(E.explain(row))
    if row.get("signal_note"):
        st.caption(f"External signal: {row['signal_note']}")
    cc = st.columns(4)
    cc[0].metric("Attractiveness", f"{row['P_attract']:.0%}")
    cc[1].metric("Future potential", f"{row['P_future']:.0%}")
    cc[2].metric("Competitive headroom", f"{row['P_compete']:.0%}")
    cc[3].metric("Right to win", f"{row['P_fit']:.0%}")
    st.dataframe(df[df[level] == pick].groupby("COMPANY CLUSTER")[E.V26]
                 .sum().sort_values(ascending=False).head(10).to_frame("MAT Feb'26 (Rs Cr)"))

# ---------- tab 4 ----------
with tab4:
    import llm
    prov = llm.provider()
    if prov == "none":
        st.warning("Add GOOGLE_API_KEY (or ANTHROPIC_API_KEY) to your .env file "
                   "to enable this tab. The ranking above works without it.")
    else:
        st.caption(f"Reasoning layer: **{prov}** / model `{llm.active_model()}`")
    q = st.text_input("Question", "Which 2-3 spaces should Cipla prioritise and why?")
    c1, c2 = st.columns([1, 1])
    if c1.button("Ask", disabled=prov == "none"):
        with st.spinner("Reasoning over the computed metric table..."):
            st.markdown(llm.ask(d, q))
    if c2.button("Generate slide copy", disabled=prov == "none"):
        with st.spinner("Drafting..."):
            st.markdown(llm.slide_bullets(d))

with st.expander("External data sources (deck Appendix)"):
    for s in S.SOURCES:
        st.write("-", s)
