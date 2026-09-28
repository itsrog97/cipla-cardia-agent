# Icebreaker — UX Audit

**Phase:** 1–2 (Website discovery + UX audit)
**Date:** 2026-09-28
**Author role:** Product / UX research
**Method and sources:** see [`DISCOVERY_LOG.md`](./DISCOVERY_LOG.md). Evidence is cited as `[E#]`, App Store screenshots as `[S#]`.

## Evidence labels

| Label | Meaning |
|---|---|
| **[OBSERVED]** | Seen directly on a public Icebreaker surface (website, App Store listing, published policy, public config file) |
| **[INFERRED]** | A reasonable interpretation of observed evidence, not directly confirmed |
| **[HYPOTHESIS]** | A proposed product opportunity or belief to be tested |
| **[UNKNOWN]** | Not observable from public surfaces. Needs an authenticated review or input from the Icebreaker team |
| **[UNVERIFIED]** | Seen only in a secondary source (for example, a search snippet) and contradicted or absent on the live site |

Later phases add **[IMPLEMENTED]**, **[MOCKED]** and **[PENDING BACKEND]**.

---

## 0. Executive summary

1. **Icebreaker is already a mobile product.** [OBSERVED] It ships a native iPhone app, "Icebreaker Connect — Networking for MBAs" (v1.6.7, Sep 2026, 5.0★ from 13 ratings) [E12]. The website is mostly an acquisition funnel into that app, plus a web sign-in and sign-up surface. The web app at `/home` is behind authentication [E1–E6].
2. **The brief's premise needs adjusting.** This is not a "web product → mobile app" conversion. The evidence points to a different opportunity: **iPhone-only → every device its audience uses** (Android phones, iPad and Android tablets, Chromebook and desktop web), from one codebase. Tied to that is a tighter **web → app → back-into-a-conversation** loop through deep links and notifications.
   - [OBSERVED] The listing says "Only for iPhone" [E12].
   - [OBSERVED] No Google Play listing was found [E15].
   - [OBSERVED] No Android App Links file is published [E11].
3. **The core loop is clear and already mobile-native.** [OBSERVED S1–S6]
   - Home shows a **Match of the Day**, **My Saved Icebreakers** and themed discovery carousels.
   - A member **Profile** offers two actions: **Saved** and **Break the Ice**.
   - **Messages** holds the conversations. **Alerts** is the fourth tab.
4. **Icebreaker's most distinctive features barely appear on its public surfaces.** [OBSERVED in policy text; INFERRED gap]
   - The Terms and Privacy Policy describe an AI networking assistant (**Spark**), AI conversation starters and suggested replies, "**Imagine the Conversation**" and AI-assisted semantic search [E8, E9].
   - None of these appears in the App Store screenshots or on the landing page.
5. **Mobile friction on public surfaces is specific, not broad.** Most public pages are responsive, with labelled inputs and 16 px input text. The problems are concentrated in the **download/invite page (`/auth`)**, the **iOS-only download paths** and a few **inconsistencies** (for example, the supported iOS version).

---

## 2.1 Product overview

### What Icebreaker is

| Aspect | Finding | Label | Source |
|---|---|---|---|
| Category | Professional networking app, App Store category "Social Networking" | OBSERVED | E12 |
| Positioning | "Networking, Reimagined." / "Finally, networking that's actually enjoyable and leads to connections that count." | OBSERVED | E1 |
| Community | "an exclusive network of top MBA students and alumni professionals", "vetted global MBA community", "Thousands of MBAs are connecting inside." | OBSERVED | E1, E3, E12 |
| Stated purposes | "Find cofounders, collaborators, mentors, investors, and more." (site meta description) | OBSERVED | E1 |
| Scale claim | "the fastest growing private MBA network in the world, connecting students and alumni across 300+ business schools. We help MBAs meet people outside their own program…" | OBSERVED (company's self-description, not independently verified) | E14 |
| Schools named | "Trusted by students & alumni from": Harvard, Stanford, UPenn, Northwestern, UChicago, Columbia, NYU, MIT, Dartmouth, Duke, Berkeley, Yale, Cornell, USC, UCLA, Emory, Rice, UT Austin, Oxford, INSEAD, HEC Paris, IESE, SDA Bocconi, IIM | OBSERVED | E5 |
| Company | Icebreaker Connect, Inc.; New York; 2–10 employees | OBSERVED (LinkedIn self-reported) | E14 |
| Founded | 2025 | UNVERIFIED (from a summarised fetch of the LinkedIn page; the year did not appear in the rendered page text) | E14 |
| Offline activity | LinkedIn posts mention an in-person NYC happy hour for MBA students and alumni | OBSERVED (outside the product) | E14 |

### Target users

- **MBA students and MBA alumni** [OBSERVED]
  - Login copy says "Sign in to continue networking with your MBA community" [E2]. The App Store subtitle is "Networking for MBAs" [E12].
  - The App Store description also addresses "business leader[s], or someone looking to make meaningful career connections" [E12]. The eligibility boundary for non-MBAs is **[UNKNOWN]**.
- **Age 18+** [OBSERVED] (Terms [E9], App Store [E12]). The Support page says 17+ [E7]. See friction item F-08.
- **Goals users bring** [OBSERVED from onboarding options, E13]:
  - Career: finding a new role, exploring career paths, wanting mentorship, switching industries, needing advice, preparing for recruiting and interviews.
  - Entrepreneurship: finding a co-founder, building a startup, fundraising, exploring startups/VC.
  - Relocation: new to this city, new to this country.

### Primary user problem

**[INFERRED from Icebreaker's own copy and reviews]:** Professional outreach is awkward and cold, and generic networks are noisy. MBAs want a trusted, relevant pool of peers and a low-pressure way to start a conversation that actually gets a reply.

- "Stop sending cold connection requests. Build genuine relationships with Icebreaker." [E12]
- "Start conversations that actually get responses" [E5]
- "experience the joy of networking without the awkwardness" [E1]
- A user review says it "cuts through the noise you see on LinkedIn" [E12, review, Apr 2026].

### Core value proposition

| Pillar | Evidence | Label |
|---|---|---|
| **Vetted, relevant community** (MBA-only) | "Our vetted community allows you to spend less time searching and more time connecting" [E1] | OBSERVED (the vetting mechanism is UNKNOWN) |
| **Goal- and interest-based matching** | "Tell Us What You're Looking For", "Connect Over Shared Interests", "Start with a curated match" [E1]; "Smart Matching" [E12] | OBSERVED |
| **Warm, human openers** | Each profile carries a personal "icebreaker" line (for example, *"I worked for the Yankees"*) [S3, S4]; "Warm Introductions: Share icebreakers and project highlights" [E12]; the primary action is "Break the Ice" [S3] | OBSERVED |
| **Unlimited connections** | "Unlimited Connections — Build relationships across industries and schools. Grow your network at your own pace." [E1] | OBSERVED |
| **AI assistance** | Spark assistant, conversation starters, suggested replies, Imagine the Conversation, AI-assisted search [E8, E9] | OBSERVED in policy text; UI UNKNOWN |

### Platforms and business model

| Item | Finding | Label |
|---|---|---|
| iOS | Native iPhone app; "Only for iPhone"; not verified for macOS; requires iOS 18.0+ [E12] | OBSERVED |
| iPad | No iPad-optimised version listed ("Only for iPhone") [E12] | OBSERVED |
| Android | No Google Play listing found [E15]; no `assetlinks.json` [E11] | OBSERVED (absence) |
| Web | Marketing site; web sign-in, sign-up and password reset; auth-gated web app at `/home` [E1–E6] | OBSERVED |
| Web ↔ iOS integration | Universal links for `/m/*`, `/app/open`, `/app/verified*`, `/auth/reset-password*`; shared web credentials [E11] | OBSERVED |
| Price | App is free [E12] | OBSERVED |
| Premium | Privacy Policy: "If you purchase premium features, we collect billing information…" [E8] | OBSERVED mention. Offer and pricing UNKNOWN |
| Invites | Sign-up has an "Invite code (optional)" field [E3] | OBSERVED |

### Main user journeys (detailed in §2.4)

1. **Discover → join**: visitor lands on web → downloads the iOS app or signs up on web.
2. **Onboard**: sign up → verify email → multi-step profile setup (goals, interests, role, icebreaker).
3. **Daily discovery → first conversation (core loop)**: Home → Match of the Day or a carousel → Profile → Break the Ice → conversation.
4. **Targeted search**: Search → filter chip or sort → profile or direct message.
5. **Conversation follow-through**: notification or Alerts → conversation → reply.
6. **Save for later**: Profile → Saved → My Saved Icebreakers on Home.
7. **Account housekeeping**: edit profile, notification settings, password reset, delete account.

---

## 2.2 Screen inventory

### A. Public web: observed directly [E1–E10]

| Screen | URL / route | Purpose | Components | Actions | Data |
|---|---|---|---|---|---|
| Landing | `/` | Explain the value; convert to download or sign-up | Header (logo, "Sign In", "Join Network", shortened to "Join" on phone); hero H1 "Networking, Reimagined."; App Store badge; hero photos; "exclusive network" section; rotating testimonial (Georgetown MBA, Duke MBA); four feature sections with phone mock-ups (Personalized Networking, Tell Us What You're Looking For, Connect Over Shared Interests, Unlimited Connections); closing CTA; footer | Sign In → `/login`; Join Network → `/signup`; App Store badge → App Store; footer → Support, Privacy, Terms, Careers | Static marketing content |
| Web app entry | `/home` | Authenticated web experience | Unauthenticated: blank page, then client redirect | Redirects to `/login?redirect=%2Fhome` | **[UNKNOWN]** behind auth |
| Sign in | `/login` | Return to the web app | Logo (→ home), H1 "Welcome Back", subtitle "Sign in to continue networking with your MBA community", Email Address, Password, "Sign In" button | Sign In; "Sign Up" → `/signup`; "Forgot Password?" → `/forgot-password` | Email, password. No social or SSO sign-in and no magic link [OBSERVED absence] |
| Sign up | `/signup` | Create an account on web | H1 "Join Icebreaker", "Thousands of MBAs are connecting inside.", Email Address, Password ("Create a password"), Invite code (optional), consent checkbox (Terms, Privacy), "Create Account" | Create Account; "Sign In" → `/login` | Email, password, invite code, consent |
| Reset password | `/forgot-password` | Request a reset email | H1 "Reset Password", "Enter your email and we'll send you a link to reset your password", Email Address, "Send Reset Link" | Send Reset Link; "Back to Sign In" | Email. The reset link opens `/auth/reset-password*`, which is a universal link into the iOS app [E11] |
| Download / invite page | `/auth` (title "Download Icebreaker") | Convert a visitor to an app install | App icon + wordmark; H1; three check-marked benefits; "Join Network" button; QR code "Scan for iOS app" (App Store link); "Trusted by students & alumni from…" list of 24 schools; footer | Join Network → `/signup`; QR / App Store link | Static. **[INFERRED]** likely the destination of shared or invite links (route name plus page title) |
| Support & Help Center | `/support` | Self-serve help | Contact (email, 24–48 h response, Mon–Fri 9–6 PST); 5 FAQs; Technical Support (app issues, login problems); App Features (Discovery, Messaging, Profile Creation); Policies; App Information; Report Issues or Abuse | Email links (support, report, security); links to Terms and Privacy | Static |
| Privacy Policy | `/privacy` | Legal. Last updated 2026-09-20 | Long-form policy, 15 sections | — | — |
| Terms of Use | `/terms` | Legal. Last revised 2026-06-14 | Long-form terms, 11 sections | — | — |
| Careers | `/careers` | Recruiting | Intro, embedded job board, "Send us your resume" email | Email | — |

### B. iOS app: observed from store and marketing screenshots [S1–S6, E13]

These are static images. Layout and content are observed; behaviour is inferred.

| # | Screen | Purpose | Components (observed) | Actions (observed → inferred behaviour) | Data shown |
|---|---|---|---|---|---|
| A1 | **Home**: top [S1, E13] | Daily entry point; curated discovery | Header: Icebreaker wordmark (left), own avatar (right). **Match of the Day** card: photo, name, "role at company", school, goal chips ("Willing to mentor", "Finding a cofounder", "+7"). **My Saved Icebreakers**: horizontal avatar carousel. Themed carousel ("People from Northwestern who know Product Management"). **Polls for You** section header. Bottom tab bar: Home, Search, Messages, Alerts, with badge counts on Messages and Alerts | Tap card or avatar → Profile [INFERRED]; tap own avatar → own profile or settings [INFERRED]; horizontal scroll | Name, photo, title, company, school, goal tags |
| A2 | **Home**: discovery carousels [S2] | Personalised browsing by theme | Carousels such as "Experts in Growth Marketing in NYC", "Your Northwestern Network", "People in NYC who need Machine Learning / AI Help". Each card: circular photo, first name, school, company | Tap → Profile [INFERRED] | First name, school, company. Carousels combine **city**, **school**, **expertise** and **need** [INFERRED from titles] |
| A3 | **Member Profile** [S3] | Evaluate a person; act | Presented as a sheet (grab handle), back chevron, "•••" menu. Large circular photo, name, italic icebreaker quote. Education (degree and year, school, focus chips such as "Marketing", "Strategy"). Undergraduate. Work Experience (title, company, dates, "Current", industry chip). Fixed bottom action bar: **Saved** (bookmark) and **Break the Ice** | Saved → toggles bookmark, appears in "My Saved Icebreakers" [INFERRED]. Break the Ice → starts a conversation, possibly with a suggested opener [INFERRED; the flow is UNKNOWN]. "•••" menu contents UNKNOWN | Full profile |
| A4 | **Search** [S4] | Find specific people or segments | Search field "Search profiles, schools, companies…". Horizontally scrollable quick-filter chips: "Same School", "Different School", "Similar Expertise" (more are cut off). "Sort" dropdown. Result cards: photo, name, school and class year, role, company, icebreaker quote, round message button | Type query; apply chip; sort; tap card → Profile [INFERRED]; tap message button → conversation [INFERRED] | Name, school, year, role, company, icebreaker |
| A5 | **Messages** [S5] | Manage conversations | Search field "Search conversations…", filter button, list rows (avatar, name, two-line preview, timestamp) | Tap → Conversation; search; filter (options UNKNOWN) | Conversation summaries |
| A6 | **Conversation** [S6, E13] | One-to-one chat | Header: back, avatar, name, "•••". Outgoing blue bubbles, incoming grey bubbles, "Sent" receipt. Composer "Type a message…" with round send button. The tab bar stays visible | Send message. "•••" contents UNKNOWN | Messages, delivery status |
| A7 | **Profile setup**: "What brings you to Icebreaker?" [E13] | Capture goals ("Select at least 1") | Modal with "Cancel", title "Edit Profile", progress bar, back chevron. Chips grouped into Career (6), Entrepreneurship (4), New in town (2). Round "next" button | Select chips → next | Goals |
| A8 | **Profile setup**: "What are you most passionate about?" [E13] | Capture interests ("Select at least 2") | 15 interest chips: AI / Machine Learning, Investment Banking, Consulting, Media & Entertainment, Data & Analytics, Marketing / Growth, Entrepreneurship, Product Management, Healthcare, Venture Capital, Nonprofit, Operations, Private Equity, Startups, Sustainability | Select chips → next | Interests |
| A9 | **Alerts** | Notifications inbox | Exists as the fourth tab with a badge count [S1, S2] | UNKNOWN | UNKNOWN |

### C. Referenced in text but never seen

| Screen / feature | Evidence (quoted) | Label |
|---|---|---|
| Edit Profile | "Tap the 'Profile' tab in the app, then tap 'Edit Profile.' You can update your photo, work experience, interests…" [E7] | OBSERVED text. There is no "Profile" tab in the current screenshots; the path is probably through the header avatar [INFERRED]. The help text may be outdated. |
| 13-step profile setup | "Complete your 13-step profile setup… Include your current role, MBA focus, networking goals, and personal icebreaker." [E7] | OBSERVED text; 2 of 13 steps seen |
| Email verification | Universal link path `/app/verified*` [E11]; "Check your spam folder for emails from us" [E7] | INFERRED |
| Discovery filters | "Use filters to find people by school, graduation year, or focus area." [E7] | OBSERVED text; only 3 chips seen |
| Settings → Account → Delete Account | "Settings > Account > Delete Account. This action is permanent…" [E7] | OBSERVED text |
| Notification settings | "Check your notification settings" [E7]; push is opt-in: "Device identifiers if you opt into push notifications" [E8] | OBSERVED text |
| Spark (AI assistant) | "Spark, our AI networking assistant, which you can chat with to find relevant people, understand why someone may be a good connection, and draft outreach." Has saved "memory" [E8] | OBSERVED text; UI UNKNOWN |
| AI openers and replies | "AI-generated conversation starters and suggested replies" [E9] | OBSERVED text; UI UNKNOWN |
| Imagine the Conversation | "a hypothetical, simulated preview of how a conversation with another member might unfold… to help you begin outreach with more confidence" [E9] | OBSERVED text; UI UNKNOWN |
| AI-assisted / semantic search | "embeddings… surface relevant matches through semantic search" [E8] | OBSERVED text |
| Project highlights / posting | "Share icebreakers and project highlights" [E12]; "Post content on the platform" [E8] | OBSERVED text; UI UNKNOWN |
| Polls | Section header "Polls for You" [S1] | OBSERVED header only |
| Premium features | [E8] | OBSERVED mention only |
| Reporting abuse | By email to a dedicated address [E7]. In-app block or report is not documented publicly. | OBSERVED email path; in-app UNKNOWN |

---

## 2.3 Navigation map

### Public web [OBSERVED]

```
joinicebreaker.com
├── /  Landing
│   ├── Sign In ─────────────► /login
│   │                           ├── Sign Up ─────────► /signup
│   │                           ├── Forgot Password? ► /forgot-password ─► (email link) /auth/reset-password* ⇒ iOS app (universal link)
│   │                           └── (success) ───────► /home or ?redirect target        [INFERRED]
│   ├── Join Network ────────► /signup
│   │                           ├── Terms / Privacy
│   │                           └── Sign In ─────────► /login
│   ├── App Store badge ─────► App Store (iPhone only)
│   └── Footer ──────────────► /support · /privacy · /terms · /careers  (each has "← Back to Home")
├── /auth  "Download Icebreaker" ─► Join Network (/signup) · QR / App Store
├── /home  (auth-gated) ─────────► /login?redirect=%2Fhome
└── Universal-link paths handled by the iOS app: /m/* · /app/open · /app/verified* · /auth/reset-password*
```

### iOS app

```
Icebreaker Connect (iPhone)
├── Auth ─ sign up / sign in ─► verify email (/app/verified*)          [INFERRED]
│          └─► Profile setup (13 steps; seen: Goals, Interests)         [OBSERVED 2/13]
│
├── Tab 1 · Home                                                         [OBSERVED]
│   ├── Match of the Day ───────────► Profile
│   ├── My Saved Icebreakers ───────► Profile
│   ├── Themed carousels ×N ────────► Profile                            (school / city / expertise / need)
│   └── Polls for You ──────────────► Poll                               [UNKNOWN]
├── Tab 2 · Search                                                       [OBSERVED]
│   ├── Query · filter chips · sort
│   └── Result card ──► Profile | ──► Message button → Conversation      [INFERRED]
├── Tab 3 · Messages                                                     [OBSERVED]
│   └── Conversation ──► ••• menu                                        [contents UNKNOWN]
├── Tab 4 · Alerts                                                       [contents UNKNOWN]
│
├── Header avatar ──► Own profile ──► Edit Profile · Settings            [INFERRED]
│                                     └── Account ► Delete Account       [OBSERVED in Support]
├── Profile (sheet) ─► Saved (bookmark) | Break the Ice ─► Conversation   [action OBSERVED, result INFERRED]
│                    └► ••• menu                                         [contents UNKNOWN]
└── Spark AI assistant · Imagine the Conversation                        [exist per Terms; entry points UNKNOWN]
```

**Structural observation [OBSERVED]:** discovery lives on **Home** as carousels. There is no separate "Discover" tab. **Search** is the directed-discovery tab. The MVP information architecture should keep this model and not invent a new "Discover" tab.

---

## 2.4 User journeys

Format: **START → ACTION → SYSTEM RESPONSE → NEXT SCREEN → SUCCESS STATE**, followed by failure states.

### J1. Visitor → member (acquisition)

| Step | Detail | Label |
|---|---|---|
| START | Visitor opens `joinicebreaker.com` or an `/auth` link on a phone or laptop | OBSERVED |
| ACTION | Taps "Join Network" **or** the App Store badge / QR code | OBSERVED |
| SYSTEM RESPONSE | Join Network → web `/signup`. Badge → App Store (iPhone only) | OBSERVED |
| NEXT SCREEN | `/signup` form, or the App Store listing | OBSERVED |
| SUCCESS | Account created, or app installed | INFERRED |

**Failure states:** an Android visitor has no app to install [OBSERVED absence]; a phone visitor on `/auth` sees a desktop layout and a QR code meant for another device (F-03); a web sign-up's next step (web app or "download the app") is UNKNOWN.

### J2. Sign-up → verified → profile ready (activation)

| Step | Detail | Label |
|---|---|---|
| START | New user on `/signup` or in the app | OBSERVED |
| ACTION | Enters email and password, optional invite code, accepts Terms | OBSERVED (web) |
| SYSTEM RESPONSE | Sends a verification email; link opens `/app/verified*` in the app | INFERRED (E11, E7) |
| NEXT SCREEN | 13-step profile setup: goals, interests, role, MBA focus, icebreaker, photo… | OBSERVED text + 2 screens |
| SUCCESS | Profile complete → first Match of the Day and personalised carousels | INFERRED |

**Failure states:** the verification email lands in spam (Support explicitly advises checking spam [E7]); a user abandons during the 13 steps [HYPOTHESIS]; incomplete profiles get fewer matches or messages (Support: "Make sure your profile is complete with a photo and all required information" [E7]).

### J3. Daily discovery → first conversation (core loop, the "killer journey")

| Step | Detail | Label |
|---|---|---|
| START | Member opens the app (directly or from a notification) | OBSERVED (app), INFERRED (notification entry) |
| ACTION | Views **Match of the Day**, or scrolls the themed carousels | OBSERVED |
| SYSTEM RESPONSE | Opens the Profile sheet with education, experience, goal chips and icebreaker quote | OBSERVED (S3) |
| ACTION | Taps **Break the Ice** | OBSERVED (button) |
| SYSTEM RESPONSE | Opens a conversation, possibly with an AI-suggested opener or "Imagine the Conversation" preview | INFERRED (E9) / UNKNOWN (actual UI) |
| NEXT SCREEN | Conversation thread | INFERRED |
| SUCCESS | First message sent; the other member replies | INFERRED |

**Failure states:** no Match of the Day or empty carousels for a thin profile [INFERRED from the Support FAQ]; the message is never answered; the recipient misses it because push is disabled (F-06); network error while sending (UNKNOWN handling).

**Open question for Icebreaker:** is there an accept/decline step (connection request) before messaging, or does "Break the Ice" open a direct conversation? The App Store copy ("Stop sending cold connection requests") and the Search card's message button suggest direct messaging [INFERRED], but this is **UNKNOWN**.

### J4. Targeted search

| Step | Detail | Label |
|---|---|---|
| START | Member has a specific need, for example "someone at Pepsi" | INFERRED |
| ACTION | Search tab → types a name, school or company; taps "Same School", "Different School" or "Similar Expertise"; sorts | OBSERVED (UI) |
| SYSTEM RESPONSE | Result cards with icebreaker quotes | OBSERVED |
| NEXT SCREEN | Profile, or a conversation through the message button | INFERRED |
| SUCCESS | Relevant person found and contacted | INFERRED |

**Failure states:** no results (empty state UNKNOWN); filters by graduation year or focus area [E7] are hidden behind the horizontal chip scroll or absent (F-10).

### J5. Conversation follow-through (return journey)

| Step | Detail | Label |
|---|---|---|
| START | Member receives a reply | INFERRED |
| ACTION | Gets a push notification (if opted in) or sees a badge on Messages or Alerts | OBSERVED (badges, push opt-in) |
| SYSTEM RESPONSE | Opens the app to the conversation (deep link) or to the Alerts list | UNKNOWN |
| NEXT SCREEN | Conversation | INFERRED |
| SUCCESS | Reply sent; meeting arranged | INFERRED (S6 shows scheduling talk) |

**Failure states:** push not enabled; a notification opens Home instead of the conversation (UNKNOWN); reply latency kills momentum [HYPOTHESIS].

### J6. Save for later

Profile → **Saved** (bookmark) → the person appears in **My Saved Icebreakers** on Home → later, tap → Profile → Break the Ice. [OBSERVED UI; link between them INFERRED]

**Failure state:** no reminder to revisit saved people [HYPOTHESIS].

### J7. Returning web user

`/home` → redirect to `/login?redirect=%2Fhome` → email + password → back to `/home` [OBSERVED redirect; post-login UNKNOWN]. **Failure states:** forgotten password → J8; no social sign-in or passkey on web [OBSERVED absence].

### J8. Password reset

`/forgot-password` → email → "Send Reset Link" → email link to `/auth/reset-password*` → opens the iOS app if installed (universal link), otherwise web [OBSERVED config, INFERRED behaviour]. **Failure state:** the user is on Android or desktop without the app, so the web reset page's behaviour matters (UNKNOWN).

### J9. Account deletion

Settings → Account → Delete Account → permanent removal [OBSERVED text, E7]. Only the path is known.

### J10. Safety / abuse report

Publicly documented path: **email** the report address [E7]. The profile and conversation "•••" menus exist [S3, S6], but whether they contain Block or Report is **UNKNOWN**.

---

## 2.5 UX friction analysis

Each item follows **OBSERVATION → IMPACT → MOBILE OPPORTUNITY**. Severity reflects the likely effect on the core loop; confidence reflects the evidence behind it. Items marked "UNKNOWN in app" may already be solved inside the authenticated product.

### What already works well on mobile [OBSERVED]

Recorded first, so the critique is balanced.

- **Bottom tab bar with four clear destinations** (Home, Search, Messages, Alerts) and badge counts [S1–S6]. This is a native, thumb-reachable information architecture.
- **Primary actions sit in the thumb zone.** "Saved" and "Break the Ice" are pinned to the bottom of the profile [S3].
- **Chip-based onboarding** with "select at least N" guidance and a single next button [E13]. Low typing, fast on a phone.
- **Profile sheet presentation** keeps context and is easy to dismiss [S3].
- **Web forms are phone-ready:**
  - Every input has a label.
  - Input text is 16 px, which avoids iOS zoom-on-focus.
  - There is no horizontal overflow at 320–1440 px on `/`, `/login`, `/signup`, `/forgot-password` and `/support` [E1–E4, E7].
- **Universal links and shared web credentials are already configured for iOS** [E11]. This is a strong base for deep linking.

### Friction items

| ID | Observation | Impact | Mobile opportunity | Severity / confidence |
|---|---|---|---|---|
| **F-01** | **iPhone-only distribution.** "Only for iPhone" [E12]; no Google Play listing [E15]; no Android App Links file [E11]. The site's only download CTA is the App Store [E1, E5]. | Prospective members on Android cannot use the native app. For a network-effect product, every excluded member lowers match quality for everyone. The schools listed include many outside the US (INSEAD, HEC Paris, IESE, SDA Bocconi, IIM, Oxford) [E5]. [HYPOTHESIS] Android share among those members is material. | One cross-platform codebase (React Native + Expo) that ships **Android** alongside iOS, with the same IA and brand. | High / High (absence observed; the effect is a hypothesis) |
| **F-02** | **No large-screen experience.** "Designed for iPhone. Not verified for macOS." [E12]. The web app exists, but it is behind auth and unassessed [E6]. | [HYPOTHESIS] Networking prep (researching people, writing thoughtful outreach, recruiting season) often happens on laptops and tablets. An iPhone-only layout on iPad is letterboxed and wastes the canvas. | Adaptive layouts: list + detail split views for Messages and Search, and grids instead of carousels on tablet and Chromebook. Keyboard and mouse support on desktop. | Medium / Medium |
| **F-03** | **The `/auth` "Download Icebreaker" page is not phone-responsive.** On a mobile viewport the layout is wider than the device, so the browser zooms out: 382 px on a 320 px screen, and 417–510 px on a 390 px screen (the width varied between runs). The desktop two-column layout persists: the phone mock-up is clipped and the benefit text wraps at one to three words per line [E5, measured]. | [INFERRED] This page is the likely landing for shared or invite links, which are mostly opened on phones. First impressions and install conversion suffer on exactly the device being targeted. | A single-column, phone-first invite page. On a phone, show a device-aware install button (App Store on iOS, Play Store on Android) instead of a QR code. Keep the QR code for desktop visitors. | High / High |
| **F-04** | **The QR code is the main download affordance, even on a phone** ("Scan for iOS app") [E5]. | A phone user cannot scan their own screen. They must find and tap the image to reach the App Store. | Detect the platform: show "Get the app" deep-link buttons on phones and a QR code on desktop. | Medium / High |
| **F-05** | **Two competing conversion paths.** Web "Join Network" goes to `/signup` (web account); the App Store badge goes to install [E1, E5]. What happens after a web sign-up is not visible [UNKNOWN]. | Users may create an account on web and then need to rediscover the app, or stay in a web experience of unknown parity. Activation can split across surfaces. | One continuous path: sign up on any surface, then deep-link into the same account on the device in hand (deferred deep links for fresh installs). | Medium / Medium |
| **F-06** | **Push is opt-in** [E8], and the Support FAQ's first answer for "not receiving matches or messages" is "Check your notification settings" [E7]. | [INFERRED] Notifications are critical to the conversation loop. If a recipient never sees "Break the Ice", the opener goes unanswered, which undermines the core promise ("conversations that actually get responses" [E5]). | Contextual permission priming: ask right after the user's first Break the Ice or first reply, and explain the value. Deep link each notification to the exact conversation. Offer granular notification preferences. Use Android notification channels. | High / Medium |
| **F-07** | **AI differentiators are invisible in public materials.** Spark, suggested openers and replies, Imagine the Conversation and AI search are defined in the Terms and Privacy Policy [E8, E9] but absent from the App Store screenshots and the landing page [E1, E12]. | [INFERRED] New users do not know about the features most likely to lower outreach anxiety. [UNKNOWN] how prominent they are inside the app. | Surface AI help at the moment of need: "Why you might connect" on the profile, and a suggested opener in the Break the Ice composer. Always keep it editable and labelled as AI. | Medium / Medium |
| **F-08** | **Inconsistent platform facts.** Support says "Requires: iOS 15.0 or later" and "Age Rating: 17+" [E7]. The App Store says "Requires iOS 18.0 or later" and "18+" [E12]. The Terms require 18+ [E9]. | Users on iOS 15–17 are told they are supported but cannot install the app. Also a small trust and compliance inconsistency. | Update the Support copy. A cross-platform build can also re-evaluate the minimum OS floor on purpose. | Low / High |
| **F-09** | **The Support page's help text may be outdated.** It refers to a "Profile" tab [E7]; the current tab bar is Home, Search, Messages, Alerts [S1–S6]. | Users following the help text will not find the tab. | Keep in-app help in sync with the IA. In the MVP, own-profile access is the header avatar, matching the current app. | Low / Medium |
| **F-10** | **Search filters are partly hidden.** Only three quick-filter chips are visible and the row is cut off at the edge [S4]. Support promises filters by "school, graduation year, or focus area" [E7]. | Horizontally scrolling chips hide most options. People may not discover graduation-year or focus-area filtering. | Phone: a "Filters" button opening a bottom sheet with every facet and a count of active filters. Tablet and desktop: a persistent filter sidebar. | Medium / Medium (UNKNOWN in app) |
| **F-11** | **Discovery relies on horizontal carousels, with about 3.5 cards visible per row** [S1, S2]. | Most people in each theme are off-screen. There is no visible "See all" affordance in the screenshots. The secondary metadata (school, company) is small grey text [INFERRED from screenshots], which may hurt legibility and contrast. | Keep carousels on phone (they suit quick browsing) but add a "See all" link to a vertical, filterable list. Use grids on tablet and desktop. Check metadata contrast against WCAG AA and support Dynamic Type / font scaling. | Medium / Medium |
| **F-12** | **Long onboarding before first value.** "13-step profile setup" [E7]. | [HYPOTHESIS] Thirteen screens on a phone before the first Match of the Day raises the risk of drop-off. Individual steps are well designed (chip-based; see "What already works well"), but the total count is the risk. | Progressive profiling: goals + interests + photo unlock the first Match of the Day; the other steps become profile-completion nudges (for example, "Add your icebreaker so people have something to reply to"). Whether this raises activation is a hypothesis to test (H-05). | Medium / Low (actual drop-off UNKNOWN) |
| **F-13** | **Password-only sign-in on web.** No Sign in with Apple, Google, passkey or magic link [E2, E3]. | Typing passwords on phones is slow and error-prone. Support lists login problems and password resets as common topics [E7]. | Passkeys or Sign in with Apple/Google, plus biometric unlock for returning sessions on mobile. The existing shared web credentials already help on iOS [E11]. | Low / Medium |
| **F-14** | **The tab bar stays visible inside a conversation** [S6]. | Less vertical room for the thread when the keyboard is open. The composer competes with navigation. | Hide the tab bar in the thread on phones (standard chat pattern); keep the back gesture. On tablet and desktop, the conversation sits in the right pane of a split view. | Low / Medium |
| **F-15** | **Safety actions are not publicly documented as in-app.** The documented abuse path is email [E7]. "•••" menus exist on Profile and Conversation, contents unknown [S3, S6]. | For a messaging product, reporting and blocking should be one tap away from the person or thread. | Report and Block in the "•••" menu of Profile and Conversation, with confirmation and an undo toast. | Medium / Low (may already exist in app) |
| **F-16** | **Web tap targets below 44 px.** Footer links, "Sign In" (49×20) and "Forgot Password?" (119×17) are under the 44 pt / 48 dp guideline [E1, E2, measured at 390 px]. | Minor mis-tap risk on phones. | Enlarge the hit areas (padding) without changing the visual design. | Low / High |
| **F-17** | **No accessibility features declared on the App Store** [E12]. | "Not declared" does not mean "not supported", but it signals that accessibility has not been audited or communicated. | Build accessibility into the MVP architecture: roles, labels, Dynamic Type, contrast tokens, focus order, reduced motion. Document support so it can be declared. | Low / Medium |

### Friction themes

1. **Reach:** F-01, F-02. The biggest gap is *where* Icebreaker can be used, not *how* it looks on iPhone.
2. **Handoff:** F-03, F-04, F-05, F-13. The web → app → account path has seams.
3. **Loop velocity:** F-06, F-07, F-12. Anything that slows the first reply weakens the core promise.
4. **Discoverability of depth:** F-10, F-11. Rich filtering and people lists are partly hidden behind horizontal scroll.
5. **Hygiene:** F-08, F-09, F-14, F-15, F-16, F-17.

---

## 2.6 Visual language observed (input to the design system)

| Token candidate | Value | Where observed | Label |
|---|---|---|---|
| Brand navy (primary action) | `#255B7D` (web button); about `#2F5B84` in app chips and next button | `/login` button, app selected chips, next button [E2, E13] | OBSERVED (computed CSS; screenshot sampling approximate) |
| Heading ink | `#101828` | Landing H1 [E1] | OBSERVED |
| Body text | `#27272A` | Web body [E1] | OBSERVED |
| Secondary text | `#364153` | Web nav links [E1] | OBSERVED |
| Chat outgoing bubble | iOS-style blue, about `#0A84FF` | [S6, E13] | OBSERVED (approximate) |
| App background (grouped) | about `#F0F0F4` | Search field, cards [S4] | OBSERVED (approximate) |
| Highlight card tint | about `#E4ECF8` | Match of the Day card [S1] | OBSERVED (approximate) |
| Success / check | green check icons | Landing bullets [E1] | OBSERVED (exact value not captured) |
| Store marketing violet | about `#5050E8` | App Store screenshot backgrounds only [E12] | OBSERVED. Marketing, **not** in-app UI |
| Web type | Inter; H1 96 px / 800 on desktop landing; H2 36 px / 700; body 18 px | [E1] | OBSERVED |
| App type | System font (SF Pro-like) | [S1–S6] | INFERRED |
| Shape | Buttons 14 px radius (web); pill chips; circular avatars; rounded cards; sheet modals | [E1, E2, S1–S6] | OBSERVED |
| Iconography | Outline tab icons with a filled active state; bookmark and cube "Break the Ice" icons | [S1–S6] | OBSERVED |
| Tone of voice | Warm, human, anti-awkward: "Break the Ice", "Icebreakers", "without the awkwardness" | [E1, E5, S3] | OBSERVED |

**Design implication [INFERRED]:** the product identity is *calm navy, generous white space, round human faces, pill chips*. A cross-platform MVP should keep this identity: navy primary, light grouped surfaces, round avatars and "icebreaker" language. It should add platform-appropriate navigation (Android Material conventions, tablet split views, desktop sidebar), not a new look.

---

## 2.7 Open questions for the Icebreaker team

Answers to these change the MVP.

1. After **Break the Ice**, is there an accept step, or is it direct messaging? Is an AI opener pre-filled?
2. What is in **Alerts**? Which events create notifications: new message, new match, saved person active, poll?
3. How does **vetting** work (school email, invite code, manual review)? Is `.edu` still required? (E16 says yes; the live Support page no longer says so.)
4. What stack is the iOS app built with? If it is already React Native / Expo, Android, tablet and web become incremental rather than a rebuild.
5. Is there an API the iOS app uses that could serve Android and web, and what is its authentication model?
6. How complete is the web app at `/home` compared with the iOS app?
7. Where do **Spark** and **Imagine the Conversation** live in the UI today, and how much are they used?
8. Is there any Android demand signal (waitlist, support emails, school partners)?

---

## 2.8 Limitations of this audit

- The authenticated web app and the live iOS app were **not** used. In-app claims rest on six App Store screenshots, five marketing mock-ups, and text in the Support page, Terms and Privacy Policy.
- Screenshots are marketing assets with demo personas and may be idealised or out of date (the Support text already disagrees with the current tab bar).
- Colour values from screenshots are approximations (compression, device colour space). Computed CSS values from the website are exact.
- No usage data, analytics or user interviews were available. Every impact statement about behaviour is an inference or a hypothesis. See [`../product-strategy/HYPOTHESES.md`](../product-strategy/HYPOTHESES.md).
