# Icebreaker Mobile: product exploration

An independent exploration of what **Icebreaker** ([joinicebreaker.com](https://joinicebreaker.com)) could become as a mobile-first, multi-platform product. It is intended to be presented to the Icebreaker founding team.

> **Not affiliated with or endorsed by Icebreaker Connect, Inc.**
> - No Icebreaker member data, private APIs or credentials are used.
> - Icebreaker's logos and screenshots are not copied into this repository; they are referenced by URL.
> - Any future app build uses fictional personas and a mock backend, labelled **[MOCKED]** / **[PENDING BACKEND]**.

## Status

| Phase | Deliverable | Status |
|---|---|---|
| 0 | Workspace structure | ✅ |
| 1–2 | Website discovery + UX audit | ✅ [`docs/ux-audit/`](docs/ux-audit/) |
| 3 | Mobile product opportunity | ✅ [`MOBILE_PRODUCT_OPPORTUNITY.md`](docs/product-strategy/MOBILE_PRODUCT_OPPORTUNITY.md) |
| 4 | Core vs enhancement vs future matrix | ✅ [`CORE_VS_INNOVATION_MATRIX.md`](docs/product-strategy/CORE_VS_INNOVATION_MATRIX.md) |
| 5 | MVP scope + scoring | ✅ [`MVP_SCOPE.md`](docs/product-strategy/MVP_SCOPE.md) |
| — | Hypothesis register | ✅ [`HYPOTHESES.md`](docs/product-strategy/HYPOTHESES.md) |
| — | Backend assumptions + provisional data models | ✅ [`BACKEND_ASSUMPTIONS.md`](docs/api/BACKEND_ASSUMPTIONS.md) |
| 6 | Information architecture (phone / tablet / desktop) | ⏳ next |
| 7–8 | Design system + prototype specification | ⏳ |
| 10–20 | React Native / Expo MVP | ⏳ No app code yet (by design) |
| 21–25 | Testing, visual QA, analytics, demo mode, founder script | ⏳ |

## The key finding

The brief assumed that Icebreaker is a web product that needs a mobile app. **It already has one.** Icebreaker ships a native **iPhone** app (App Store: "Icebreaker Connect — Networking for MBAs", "Only for iPhone"), and the website mostly funnels visitors into it.

- There is **no Android app**, no iPad-optimised layout, and the web app sits behind sign-in.
- The opportunity is therefore **"iPhone-only → every device its MBA audience uses, from one codebase"**. It centres on the core loop Icebreaker already has: **Match of the Day → Profile → Break the Ice → Conversation → notification → back into the conversation**.

Details: [`docs/ux-audit/ICEBREAKER_UX_AUDIT.md`](docs/ux-audit/ICEBREAKER_UX_AUDIT.md) §0.

## Document map

```
icebreaker-mobile/
├── docs/
│   ├── ux-audit/
│   │   ├── ICEBREAKER_UX_AUDIT.md          overview, screen inventory, nav map, journeys, friction analysis
│   │   └── DISCOVERY_LOG.md                method, evidence index (E#/S#), what was not inspected
│   ├── product-strategy/
│   │   ├── MOBILE_PRODUCT_OPPORTUNITY.md   why mobile / multi-platform, specifically for Icebreaker
│   │   ├── CORE_VS_INNOVATION_MATRIX.md    existing core | mobile enhancement | future hypothesis
│   │   ├── MVP_SCOPE.md                    killer journey, scored backlog, quality bar, definition of done
│   │   └── HYPOTHESES.md                   H-01…H-13 with validation plans and metrics
│   ├── api/
│   │   └── BACKEND_ASSUMPTIONS.md          known facts, assumptions A-01…A-16, service layer, data models
│   ├── architecture/  testing/  founder-demo/     (later phases)
├── design/  design-system/  screens/  prototype/  (later phases)
├── app/                                          (Expo app, later phase)
├── assets/
└── scripts/discovery/audit-public-pages.mjs     reproducible public-page audit
```

## Evidence labels used in every document

| Label | Meaning |
|---|---|
| **[OBSERVED]** | Seen directly on a public Icebreaker surface |
| **[INFERRED]** | A reasonable interpretation of observed evidence |
| **[HYPOTHESIS]** | A proposed opportunity, to be validated |
| **[UNKNOWN]** | Not observable publicly; needs the authenticated product or the Icebreaker team |
| **[UNVERIFIED]** | Seen only in a secondary source and absent from the live site |
| **[IMPLEMENTED]** | Actually working in the MVP (later phases) |
| **[MOCKED]** | Implemented with simulated data (later phases) |
| **[PENDING BACKEND]** | Requires authorised Icebreaker backend/API access |

## Reproducing the discovery

```bash
cd icebreaker-mobile
npm i -D playwright && npx playwright install chromium
node scripts/discovery/audit-public-pages.mjs            # add --screenshots for local captures
```

The script only renders public pages. It never logs in or submits forms. Output goes to `scripts/discovery/out/` (gitignored, because captures contain third-party content).

## Open decisions (before the build phase)

1. **Confirm the corrected premise.** Should the MVP be built as the "iPhone-only → all platforms" story, around Icebreaker's real four-tab app?
2. **Where the build should live.** This repository is **public** and also contains an unrelated project. Icebreaker's Terms of Use (§2.2) restrict using the site to build "a similar or competitive" product.
   - This work is framed as a proposal *for* Icebreaker.
   - Even so, a **private, dedicated repository** is recommended before building a branded MVP.
3. **Authenticated review.** The signed-in web app and the live iOS app could not be inspected here. Options:
   - an authenticated pass in a browser you control, where you enter your own credentials;
   - your own screenshots, with other members' data redacted;
   - proceeding on public evidence only.
