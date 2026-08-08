"""
LAYER 3 — EXTERNAL SIGNAL LIBRARY

Every signal is mapped to an ATC subgroup code so it CHANGES THE RANKING.
This is what makes it "integrated trend analytics" rather than a CAGR sort.

  tailwind : -3 .. +3   guideline shift / prevalence / LOE / pipeline pull
  nlem     : -3 .. 0    DPCO / NLEM ceiling-price exposure (value-pool risk)

>>> REPLACE the placeholder notes with your own verified citations and put
>>> them in the deck Appendix. The scores are yours to defend.
"""

SIGNALS = {
    # ---------------- Anti-hypertensives ----------------
    "C02F0O": {"tailwind": 3, "nlem": -1,
               "note": "Cilnidipine+Telmisartan: N/L-type CCB renal protection + "
                       "reduced pedal oedema; ISH/CSI single-pill-combination-first guidance."},
    "C01D0B": {"tailwind": 2, "nlem": -1,
               "note": "Cilnidipine mono: switching from amlodipine on oedema tolerability."},
    "C02I0B": {"tailwind": 3, "nlem": -1,
               "note": "Triple SPC (chlorthalidone+cilnidipine+telmisartan): guideline push to "
                       "early 3-drug combination in stage-2 HTN."},
    "C02I0D": {"tailwind": 3, "nlem": -1,
               "note": "Triple SPC with metoprolol: post-MI + HTN comorbidity archetype."},
    "C02I01": {"tailwind": 2, "nlem": -2, "note": "Amlo+HCT+Telmi: mature triple, NLEM exposed."},
    "C02F06": {"tailwind": 1, "nlem": -2,
               "note": "Amlodipine+Telmisartan: largest dual FDC, heavy NLEM ceiling exposure."},
    "C02G0U": {"tailwind": 2, "nlem": -1,
               "note": "Chlorthalidone preferred over HCTZ in recent HTN guidance."},
    "C02C04": {"tailwind": 1, "nlem": -2, "note": "Telmisartan mono: commoditised, price-controlled."},
    "C02F02": {"tailwind": -1, "nlem": -2, "note": "Atenolol+Amlodipine: beta-blocker de-prioritised as first line."},
    "C02B":   {"tailwind": -2, "nlem": -2, "note": "ACE inhibitors: structural decline vs ARBs (cough intolerance)."},

    # ---------------- Lipid regulators ----------------
    "C10A0S": {"tailwind": 3, "nlem": 0,
               "note": "Rosuvastatin+Ezetimibe: lower LDL-C targets (<55 mg/dL very-high risk) "
                       "drive combination-first over statin uptitration."},
    "C10A0G": {"tailwind": 2, "nlem": -1,
               "note": "Rosuva+Fenofibrate: Indian dyslipidaemia phenotype (high TG / low HDL), "
                       "residual-risk management."},
    "C10A04": {"tailwind": 2, "nlem": -2,
               "note": "Rosuvastatin: primary-prevention expansion, high NLEM exposure."},
    "C10A03": {"tailwind": -1, "nlem": -2, "note": "Atorvastatin: share ceding to rosuvastatin."},
    "C10A0I": {"tailwind": 2, "nlem": -1, "note": "Rosuva+Clopidogrel: secondary prevention polypill."},
    "C10A0K": {"tailwind": 1, "nlem": -1, "note": "Rosuva+Clopi+ASA: crowded secondary-prevention triple."},
    "C10C03": {"tailwind": 2, "nlem": 0,
               "note": "Saroglitazar: MASLD/NAFLD label expansion — high growth but a "
                       "3-company originator-locked market."},

    # ---------------- Others ----------------
    "C01G01": {"tailwind": 1, "nlem": 0, "note": "Nicorandil: chronic stable angina, refractory CAD."},
    "C01F03": {"tailwind": 0, "nlem": -1, "note": "Nitrates: mature, replacement-driven."},
    "C02D01": {"tailwind": 0, "nlem": 0, "note": "Prazosin: BPH crossover demand, ageing male cohort."},
}

# Sources to reproduce in the deck Appendix
SOURCES = [
    "ICMR-INDIAB Phase II (Lancet Diab Endo, 2023) - hypertension & dyslipidaemia prevalence",
    "NFHS-5 (2019-21) - measured BP prevalence by state",
    "Cardiological Society of India / ISH 2023 Global Hypertension Practice Guidelines - SPC-first",
    "ESC/EAS 2019 & 2023 dyslipidaemia guidelines - LDL-C targets by risk category",
    "NPPA / NLEM 2022 ceiling price notifications - cardiovascular molecules",
    "CDSCO new drug approvals list; US FDA Orange Book - patent expiry calendar",
    "GBD 2021 India CVD burden; CPCB AQI data - environment-linked CVD incidence",
]
