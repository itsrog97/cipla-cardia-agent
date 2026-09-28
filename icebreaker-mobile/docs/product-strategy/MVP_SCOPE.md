# MVP Scope

**Phase:** 5
**Date:** 2026-09-28
**Inputs:** [`../ux-audit/ICEBREAKER_UX_AUDIT.md`](../ux-audit/ICEBREAKER_UX_AUDIT.md), [`MOBILE_PRODUCT_OPPORTUNITY.md`](./MOBILE_PRODUCT_OPPORTUNITY.md), [`CORE_VS_INNOVATION_MATRIX.md`](./CORE_VS_INNOVATION_MATRIX.md), [`HYPOTHESES.md`](./HYPOTHESES.md), [`../api/BACKEND_ASSUMPTIONS.md`](../api/BACKEND_ASSUMPTIONS.md)

---

## 1. MVP goal

> Show Icebreaker's **existing core loop** (Match of the Day → Profile → Break the Ice → Conversation → notification → back into the conversation) running natively on **iPhone, Android phone, iPad/Android tablet and Chromebook/web from one codebase**, with a layout designed for each device class. Use fictional data and a mock service layer that can be swapped for Icebreaker's real API.

The MVP optimises for **one excellent journey**, not feature count.

### Non-goals

- Replacing or cloning the current iOS app feature for feature.
- Using real Icebreaker data, accounts or private APIs.
- Recreating features whose real UI has not been seen (Spark chat, Imagine the Conversation, Polls) as if they were Icebreaker's design.
- Proving any hypothesis. The MVP *demonstrates* experiences; proof needs Icebreaker's users.

---

## 2. The killer journey

This is the demo spine. Every MUST item below exists to make this path excellent.

| # | Step | What the user sees | Platform notes | Status in MVP |
|---|---|---|---|---|
| 1 | Open app | Splash → sign-in with **"Continue with demo account"** | Same on all platforms | [MOCKED] auth |
| 2 | Home | **Match of the Day** card, **My Saved Icebreakers**, 2–3 themed carousels | Phone: carousels. Tablet/desktop: grids | [MOCKED] data |
| 3 | View person | Profile: photo, icebreaker quote, education, experience, goal chips; **Saved** and **Break the Ice** | Phone: sheet. Tablet/desktop: side panel | [MOCKED] data |
| 4 | Interact | **Break the Ice** → composer with an editable suggested opener, labelled "Suggested · Prototype" → Send | Success haptic on native | [MOCKED] AI suggestion |
| 5 | System response | "Sent" status. Contextual prompt: *"Get notified when [name] replies"* → OS permission request | Native: OS dialog. Web: in-app alerts only | Permission prompt [IMPLEMENTED on native]; reply simulated |
| 6 | Notification | A simulated reply arrives after a few seconds → local notification (native) or in-app toast plus an Alerts badge (web) | Android: notification channel | [MOCKED] reply + local notification |
| 7 | Return to app | Tap the notification → **deep link** opens that exact conversation | The same link format works on every platform | Deep-link routing [IMPLEMENTED] |
| 8 | Continue | Read the reply → respond | Desktop: `Enter` to send | [MOCKED] messaging |
| 9 | Adaptive | The same account on tablet or Chromebook: Messages list + thread split view; Search results + profile side by side | Resize live on web to show breakpoints | Layouts [IMPLEMENTED] |

**Assumption to confirm (A-06 in the backend doc):** Break the Ice opens a direct conversation with no accept step. If Icebreaker uses an accept step, steps 4–6 become "request sent → accepted → conversation", and the journey keeps the same shape.

---

## 3. Prioritisation method (MVP score)

Each candidate is scored from 1 to 5 on four dimensions:

| Dimension | 1 | 5 |
|---|---|---|
| **V**: Demo value (shows Icebreaker's core value in 3–5 minutes) | Peripheral | Central to the killer journey |
| **Ev**: Evidence it exists in Icebreaker today | Net-new idea | Observed with visible UI (3 = exists per text, UI unseen) |
| **M**: Mobile / multi-platform leverage | Same on every device | Transformed by being native or adaptive |
| **Ef**: Effort with a mocked backend | Hours | Weeks |

**Score = 2·V + Ev + M − Ef** (range −1 to 19). Bands: **≥ 13 → MUST · 8–12 → SHOULD · ≤ 7 → FUTURE**.

The following override rules apply regardless of score:

- **R1:** Anything that needs Icebreaker's backend or credentials (real auth, real push, real AI) is **[PENDING BACKEND]**. If it is on the killer journey, the MVP ships a mocked equivalent.
- **R2:** Net-new *product* features (Ev = 1 and not a platform convention or layout adaptation) go to **FUTURE**, to keep the MVP recognisably Icebreaker.
- **R3:** Features whose real UI is **UNKNOWN** and which are not on the killer journey go to **FUTURE**, so the MVP does not invent Icebreaker's design.
- **R4:** Quality requirements (states, accessibility, performance, labelling, security) are **MUST** and are not scored. See §5.

---

## 4. Scored backlog

| # | Feature | V | Ev | M | Ef | Score | Band | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | Adaptive navigation: bottom tabs (phone), side rail (tablet), sidebar (desktop). Home, Search, Messages, Alerts | 5 | 5 | 5 | 2 | **18** | **MUST** | Keeps the real four-tab IA |
| 2 | Profile: sheet (phone) / panel (tablet, desktop) with Saved + Break the Ice | 5 | 5 | 4 | 2 | **17** | **MUST** | |
| 3 | Home: Match of the Day, My Saved Icebreakers, themed carousels (grids on large screens) | 5 | 5 | 4 | 3 | **16** | **MUST** | "Polls for You" omitted (R3) |
| 4 | Messages list + thread; split view on tablet and desktop | 5 | 5 | 4 | 3 | **16** | **MUST** | Tab bar hidden in the thread on phone (F-14) |
| 5 | Simulated reply → local notification → deep link into the conversation | 5 | 3 | 5 | 3 | **15** | **MUST** | Real push is #23 (R1) |
| 6 | Deep-link routing (profile, conversation, match) on all platforms | 4 | 4 | 5 | 2 | **15** | **MUST** | Mapping to Icebreaker's `/m/*` paths pending (A-09) |
| 7 | Break the Ice composer with editable, labelled suggested opener | 5 | 3 | 4 | 3 | **14** | **MUST** | [MOCKED] suggestion; on the killer journey, so R3 does not apply |
| 8 | Demo sign-in + email/password form, secure session storage, sign-out | 4 | 5 | 3 | 2 | **14** | **MUST** | Real auth [PENDING BACKEND] (R1) |
| 9 | Alerts list (reply, saved-person, match alerts) with badges | 4 | 3 | 4 | 2 | **13** | **MUST** | Real alert types UNKNOWN. Labelled as prototype |
| 10 | Contextual push-permission prompt after the first Break the Ice | 3 | 3 | 5 | 1 | **13** | **MUST** | H-04 |
| 11 | Onboarding: Goals + Interests (the two observed steps) + photo picker | 3 | 5 | 3 | 2 | **12** | SHOULD | The other 11 steps are UNKNOWN |
| 12 | Search: query, quick chips, sort | 3 | 5 | 3 | 3 | **11** | SHOULD | |
| 13 | Daily Match of the Day local notification | 3 | 2 | 5 | 2 | **11** | SHOULD | H-03. [MOCKED] |
| 14 | Native share sheet for a profile or invite link | 2 | 4 | 4 | 1 | **11** | SHOULD | H-08 |
| 15 | Filters bottom sheet (phone) / sidebar (tablet, desktop) | 3 | 3 | 4 | 3 | **10** | SHOULD | H-09 |
| 16 | Haptics (Save, Send) + pull-to-refresh | 2 | 1 | 5 | 1 | **9** | SHOULD | Platform convention (R2 does not apply) |
| 17 | Report / Block in the "•••" menu (UI + mocked confirmation) | 2 | 3 | 3 | 1 | **9** | SHOULD | F-15 |
| 18 | Desktop keyboard shortcuts, hover and focus states | 3 | 1 | 4 | 2 | **9** | SHOULD | Layout/platform adaptation (R2 does not apply) |
| 19 | Edit own profile (fields + photo) | 2 | 5 | 3 | 3 | **9** | SHOULD | |
| 20 | Settings + delete account (UI) | 1 | 5 | 2 | 2 | **7** | FUTURE | **Required before any App Store release** (in-app account deletion) |
| 21 | Biometric unlock | 2 | 1 | 4 | 2 | **7** | FUTURE | |
| 22 | Imagine the Conversation | 3 | 3 | 2 | 4 | **7** | FUTURE | R3 |
| 23 | Real push notifications (APNs / FCM) | 4 | 4 | 5 | 4 | 13 | **PENDING BACKEND** | R1 |
| 24 | Spark AI assistant chat | 3 | 3 | 2 | 5 | **6** | FUTURE | R3 |
| 25 | Offline cache of profiles and conversations | 2 | 1 | 4 | 3 | **6** | FUTURE | An offline *banner and retry* is a MUST (§5) |
| 26 | Saved-person reminders | 2 | 1 | 3 | 2 | **6** | FUTURE | R2, H-11 |
| 27 | Polls | 2 | 2 | 2 | 3 | **5** | FUTURE | R3 |
| 28 | Event mode (profile QR show/scan) | 3 | 1 | 5 | 3 | 9 | **FUTURE** | R2, H-12 |
| 29 | Premium / paywall | 1 | 2 | 2 | 4 | **2** | FUTURE | Offer unknown |

**Outside the app (recommendation only):** a phone-first redesign of the `/auth` download/invite page (F-03, F-04, H-07). It will be delivered as a design specification in the prototype phase, not built in the app.

### Summary

- **MUST (10):** #1–#10.
- **SHOULD (9):** #11–#19, built in score order only after the MUST items pass QA.
- **FUTURE (9) + PENDING BACKEND (1).**

---

## 5. Quality requirements (MUST, not scored, per R4)

| Area | Requirement |
|---|---|
| **States** | Every data screen has skeleton loading, an empty state, and an error state with retry. A global offline banner. Send failure → retry on the message bubble. |
| **Accessibility** | Accessible role and label on every interactive element. Text scales with OS font size up to 200% on key screens without clipping. WCAG AA contrast from design tokens. Touch targets ≥ 44 pt (iOS) / 48 dp (Android). Visible keyboard focus and logical tab order on web. Respects reduced motion. |
| **Responsiveness** | Three layout classes (phone / tablet / desktop), tested at 320–430 px, 768–1024 px and ≥ 1024 px. No stretched phone layouts. Exact breakpoints are defined in the IA phase. |
| **Performance** | Virtualised lists; cached, appropriately sized images; memoised list rows; no blocking work on the JS thread during navigation. |
| **Honesty labelling** | A persistent "Prototype · backend integration pending" marker (sign-in screen + About). A "Suggested · Prototype" badge on every AI-like suggestion. Fictional personas only. |
| **Security** | No secrets in the repo; `.env.example` only; session tokens in the platform secure store (never plain storage); no credentials in logs. |
| **Brand & IP** | Icebreaker's logo files and screenshots are **not** copied into this public repository. The MVP uses a text wordmark and original placeholder imagery. Official assets can be swapped in with Icebreaker's permission. |

---

## 6. Definition of done

The MVP is done when all of the following hold:

1. The killer journey (§2) completes with no dead ends on an **iOS simulator, an Android emulator, and web at tablet and Chromebook widths**.
2. The journey can be demonstrated in **≤ 90 seconds** and the full demo in 3–5 minutes.
3. Every MUST item and every §5 requirement is met and recorded in the test report.
4. Every mocked capability is labelled in the UI and in the docs ([MOCKED] / [PENDING BACKEND]).
5. TypeScript strict mode, lint and unit tests (service layer, navigation, deep-link parsing) pass.
6. The founder demo script names what is real, what is mocked, and what is a proposal.

---

## 7. MVP readiness scorecard (for the go / no-go before the build)

| Pre-build prerequisite | Status |
|---|---|
| UX audit, screen inventory, navigation map, journeys | ✅ Done (Phase 1–2) |
| Mobile opportunity + hypotheses | ✅ Done (Phase 3) |
| Core vs enhancement vs future matrix | ✅ Done (Phase 4) |
| MVP scope + scoring | ✅ Done (this document) |
| Backend assumptions | ✅ Done ([`BACKEND_ASSUMPTIONS.md`](../api/BACKEND_ASSUMPTIONS.md)) |
| Information architecture (phone / tablet / desktop) | ⏳ Phase 6 |
| Design system tokens + components | ⏳ Phase 7 |
| Prototype specification (10–12 screens) | ⏳ Phase 8 |
| Authenticated review of the real product | ⚠️ Not possible in this environment. Recommended before the build (see audit §2.8) |
| Decision on repo visibility and positioning | ⚠️ Needs your decision (see README "Open decisions") |
