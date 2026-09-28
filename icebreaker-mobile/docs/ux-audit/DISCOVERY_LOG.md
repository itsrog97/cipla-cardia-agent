# Discovery Log — Phase 1

**Date of discovery:** 2026-09-28
**Scope:** everything about Icebreaker that is publicly reachable without an account.
**Status:** Complete for public surfaces. The authenticated product has **not** been inspected (see "Not inspected").

This log records *how* each fact in the audit was obtained, so that every claim can be traced to a source. Other documents cite evidence as `[E#]` and App Store screenshots as `[S#]`.

---

## 1. Method

| Step | What was done | Tooling |
|---|---|---|
| 1 | Rendered every public page reachable from the home page (JavaScript executed, not raw HTML) and captured visible text, headings, links, form fields, computed styles and full-page screenshots | Headless Chromium (Playwright), `scripts/discovery/audit-public-pages.mjs` |
| 2 | Followed only links that appear on the site itself. No URL guessing, no form submission, no login attempts | Same |
| 3 | Re-rendered each public page with a fresh load at 320, 390, 768, 1024 and 1440 px, measuring horizontal overflow, tap-target size, input font size and input labelling | Same |
| 4 | Read the public App Store listing: metadata, description, ratings, reviews and the six store screenshots | Headless Chromium |
| 5 | Viewed the five product mock-up images the landing page itself displays | Image review |
| 6 | Read the public `/.well-known/apple-app-site-association` file (the deep-link configuration Apple fetches) | HTTP GET |
| 7 | Checked Google Play for an Android listing; read the public LinkedIn company page | Headless Chromium, web fetch |
| 8 | Extracted brand colours from computed CSS (Lab → sRGB) and from dominant colours in product screenshots | Script |

### Rules followed

- No credentials were requested, entered, stored or logged.
- No private or undocumented API was called. The only network requests were the ones a normal browser makes when viewing public pages.
- No CAPTCHA, rate limit or access control was bypassed.
- Icebreaker's images and screenshots are **not** copied into this repository (the repository is public). They are referenced by URL and described in text. Local captures stayed in a temporary working directory.

---

## 2. Evidence index

| ID | Source | Accessed | What it provided |
|---|---|---|---|
| E1 | `https://joinicebreaker.com/` (landing) | 2026-09-28 | Positioning, value proposition, feature sections, CTAs, testimonials, footer |
| E2 | `/login` | 2026-09-28 | Web sign-in form (email + password) |
| E3 | `/signup` | 2026-09-28 | Web sign-up form (email, password, optional invite code, terms consent) |
| E4 | `/forgot-password` | 2026-09-28 | Password reset request form |
| E5 | `/auth` (page title "Download Icebreaker") | 2026-09-28 | App download / invite landing page, QR code, school list |
| E6 | `/home` | 2026-09-28 | Auth-gated web app: blank render, then client-side redirect to `/login?redirect=%2Fhome` |
| E7 | `/support` | 2026-09-28 | Help centre: FAQ, feature descriptions, account deletion path, platform requirements, abuse reporting |
| E8 | `/privacy` (last updated 2026-09-20) | 2026-09-28 | Data collected, AI features, AI subprocessors, push notifications, premium payments |
| E9 | `/terms` (last revised 2026-06-14) | 2026-09-28 | AI features (Spark, Imagine the Conversation), user content, use restrictions |
| E10 | `/careers` | 2026-09-28 | Careers page, embedded third-party job board |
| E11 | `/.well-known/apple-app-site-association` | 2026-09-28 | iOS universal-link paths and shared web credentials |
| E12 | App Store listing `apps.apple.com/us/app/icebreaker-connect/id6748621869` | 2026-09-28 | Name, subtitle, platform support, version, ratings, reviews, description, privacy labels |
| E13 | Landing-page product images (`/personalized_networking.png`, `/what_looking_for.png`, `/most_passionate_about.png`, `/messaging.png`, `/home_tab_carousels.png`) | 2026-09-28 | Real app screens: Home, two onboarding steps, conversation |
| E14 | LinkedIn company page `linkedin.com/company/icebreakerconnect` | 2026-09-28 | Company self-description, size, founding year, HQ, recent posts |
| E15 | Google Play search for "Icebreaker Connect" | 2026-09-28 | No Icebreaker Connect listing found (the similarly named apps belong to other developers) |
| E16 | Search-engine result snippet (not the live page) | 2026-09-28 | Mentions a `.edu` email requirement. **Not present on the current `/support` page, so treated as UNVERIFIED / possibly outdated** |

### App Store screenshots (from E12)

| ID | Store caption | Screen shown |
|---|---|---|
| S1 | "Grow Your Network" | Home tab: Match of the Day, My Saved Icebreakers, themed carousel, Polls for You |
| S2 | "Discover New People" | Home tab scrolled: themed discovery carousels |
| S3 | "Build Your Brand" | Member profile (sheet) with **Saved** and **Break the Ice** actions |
| S4 | "Search Members" | Search tab: search field, filter chips, sort, result cards |
| S5 | "Make Connections" | Messages tab: conversation list |
| S6 | "Open New Doors" | Conversation thread |

The screenshots are marketing images with demo personas. They show layout and information hierarchy, but not behaviour.

---

## 3. Key raw facts

### App Store listing [E12]

| Field | Value |
|---|---|
| Name / subtitle | Icebreaker Connect — "Networking for MBAs" |
| Platform | "Only for iPhone". "Designed for iPhone. Not verified for macOS." |
| Price | Free |
| Rating | 5.0 from 13 ratings |
| Age rating | 18+ |
| Category | Social Networking |
| Version | 1.6.7, released Sep 8 ("Fixed some bugs and made the app run better.") |
| Size | 50.2 MB |
| Compatibility | Requires iOS 18.0 or later |
| Privacy labels (linked to you) | Contact Info, User Content, Identifiers, Usage Data |
| Accessibility | "The developer has not yet indicated which accessibility features this app supports." |

### Deep-link configuration [E11]

- iOS universal-link paths: `/m/*`, `/app/open`, `/app/verified*`, `/auth/reset-password*`
- Two app IDs are configured: production and a `.staging` variant.
- `webcredentials` is configured, so saved passwords are shared between the website and the iOS app.
- `/.well-known/assetlinks.json` (Android App Links) returns **404**.

### Technology visible from the public site

These are [OBSERVED] from asset paths, metadata and network requests of public pages only:

- The website is a Next.js application (`/_next/` asset paths). Open Graph images reference a `*.vercel.app` host, suggesting Vercel hosting.
- The marketing pages load Google Tag Manager / Google Analytics and Amplitude.
- The careers page embeds a third-party job board (Dover).
- Web typography is Inter.
- The iOS app's technology stack, the backend and the API are **not observable** from public surfaces.

---

## 4. Not inspected, and why

| Surface | Reason | How to close the gap |
|---|---|---|
| Authenticated web app (`/home` and everything behind it) | Requires sign-in. This discovery ran in a headless cloud browser with no interactive window where you could enter credentials yourself, and credentials must never be pasted into chat. | Run an authenticated pass in a browser you control (for example, Claude in Chrome on your own machine), where you type the credentials. Or share your own screenshots, with other members' personal data redacted. |
| iOS app, interactive behaviour | No device available. Only static store and marketing screenshots were seen. | Screen recording of the core loop, or a walkthrough with the Icebreaker team |
| Alerts tab, Settings, Edit Profile, Spark, Imagine the Conversation, Polls, premium | Not shown in any public image. Known only from text in the Support page, Terms and Privacy Policy. | Same as above |
| Sign-up completion, email verification, the 13-step profile setup (11 of 13 steps) | Would require creating an account. Accounts were not created on the user's behalf. | Authenticated pass |

---

## 5. Environment notes (not product findings)

- During the first crawl, `/signup` and `/forgot-password` returned a gateway error once. Both loaded normally on retry. This is attributed to the discovery environment's network path, **not** to Icebreaker, and is not reported as a product finding.
- The landing page's lazy-loaded images need scrolling before a full-page capture. Captures that skipped scrolling showed empty image slots. That was a capture artefact, not a site defect.
