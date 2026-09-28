# Backend Assumptions & Integration Plan (pre-build)

**Phase:** pre-build input to Phases 13–15
**Date:** 2026-09-28
**Status:** Every backend capability in the MVP is **[MOCKED]** until Icebreaker authorises API access. Everything that requires Icebreaker's systems is **[PENDING BACKEND]**.

---

## 1. What is known about Icebreaker's backend

Only public surfaces were used. No API was called or reverse-engineered.

| Fact | Evidence | Label |
|---|---|---|
| Accounts use email + password; password reset uses an emailed link | `/login`, `/signup`, `/forgot-password` [E2–E4] | OBSERVED |
| Sign-up accepts an optional invite code and requires consent to Terms/Privacy | `/signup` [E3] | OBSERVED |
| Email verification exists, and its link opens the app | Universal-link path `/app/verified*` [E11]; "check your spam folder" [E7] | INFERRED |
| iOS universal links handle `/m/*`, `/app/open`, `/app/verified*`, `/auth/reset-password*` | [E11] | OBSERVED (semantics of `/m/*` UNKNOWN) |
| A **staging** iOS app exists alongside production | Second app ID with `.staging` suffix in [E11] | OBSERVED. A staging backend is likely [INFERRED] |
| No Android App Links file is hosted | `/.well-known/assetlinks.json` → 404 [E11] | OBSERVED |
| AI features run server-side through third-party LLM and embedding providers (OpenAI, Anthropic, and a third provider named "TypeSafe") | Privacy Policy §3.5 [E8] | OBSERVED |
| Semantic search uses profile embeddings stored on Icebreaker's infrastructure | [E8] | OBSERVED |
| Before profile text goes to AI providers, contact details, links and precise location are stripped | [E8] | OBSERVED |
| Push notifications are opt-in and use device identifiers | [E8] | OBSERVED |
| Payment processing exists for premium features | [E8] | OBSERVED mention |
| The website is Next.js (probably on Vercel) | Asset paths, Open Graph host [E1] | OBSERVED |
| Web app routes are protected client-side with a redirect parameter | `/home` → `/login?redirect=%2Fhome` [E6] | OBSERVED |
| API style, auth token format, realtime transport, push provider, media storage, rate limits | — | **UNKNOWN** |

---

## 2. Assumptions the MVP is built on

Each assumption is isolated behind the service layer (§3), so a wrong assumption changes one service, not the UI.

| ID | Assumption | Why | If wrong, what changes | Confirm with Icebreaker |
|---|---|---|---|---|
| **A-01** | There is no public or authorised API available to this project, so the MVP uses an in-app **mock service layer** with fictional data. | No API is documented; private APIs must not be used without authorisation. | Swap mock adapters for HTTP adapters. | API docs / OpenAPI, staging access |
| **A-02** | Auth is email + password, returning an access token plus a refresh mechanism usable by a native client. | Web shows email + password [E2]. | `authService` adapter only (for example, cookie session → token exchange). | Token model, expiry, refresh, sign-out semantics |
| **A-03** | Sign-up requires email verification before full access. | [E11], [E7] | Sign-up flow screens. | Verification flow; `.edu` or vetting rules (E16 is unverified) |
| **A-04** | The profile shape matches the fields visible in the app screenshots (§4). | [S3, S4, E13] | `Profile` type + mappers. | Canonical schema |
| **A-05** | Home is **server-driven**: one Match of the Day plus N titled sections of profile summaries, each with a server-provided title. | Section titles are personalised ("People from Northwestern who know Product Management") [S1, S2]. | `discoveryService` mapper. | Home payload shape |
| **A-06** | **Break the Ice opens a direct 1:1 conversation.** There is no accept/decline step. The first message may be a suggested opener. | "Stop sending cold connection requests" [E12]; message button on Search cards [S4]. | Add a request state machine (pending → accepted/declined) in `networkService` and a "request sent" UI state. | Actual Break the Ice semantics |
| **A-07** | Messaging is 1:1, text-first, with a delivery status ("Sent" observed [S6]). Realtime transport is unknown, so the client depends on a `subscribe()` interface, not a transport. | [S5, S6] | `messageService` adapter (WebSocket, SSE or polling). | Transport, read receipts, attachments, message limits |
| **A-08** | Push notifications carry a deep-link target, and the Alerts tab is a server-side list. | Alerts tab [S1]; push opt-in [E8]. | `notificationService` adapter. | Alert types, push provider (APNs/FCM directly or via a service), token registration |
| **A-09** | The MVP uses its **own route scheme** (for example, `/profile/:id`, `/messages/:conversationId`). Mapping to Icebreaker's `/m/*` universal-link paths is pending. Android App Links would require Icebreaker to host `assetlinks.json` on its domain. | `/m/*` semantics are unknown [E11]. | A single link-mapping table in the router. | Meaning of `/m/*`; willingness to publish `assetlinks.json` |
| **A-10** | **AI suggestions come from Icebreaker's backend.** The mobile client never calls LLM providers directly and never holds AI keys. | The Privacy Policy describes server-side processing with PII stripping [E8]. | None; this is a security invariant. | Suggestion endpoint shape; labelling requirements |
| **A-11** | Search runs server-side (query + filters + sort, paginated). | Semantic search [E8]; filters [E7, S4]. | `searchService` adapter. | Available facets, sort options, pagination |
| **A-12** | Saved is a per-user bookmark set with toggle semantics. | [S3, S1] | `networkService.save/unsave`. | Limits; whether saved people are notified (assumed: no) |
| **A-13** | Profile photos are served as CDN URLs; uploads use a signed URL or multipart. | Photo-led profiles [S1–S6]. | `profileService.uploadPhoto` adapter. | Upload mechanism, size and format limits |
| **A-14** | Report and Block exist as backend actions, or will. | Email reporting today [E7]; "•••" menus [S3, S6]. | UI stays; the adapter is added. | Existence and API of in-app safety actions |
| **A-15** | Lists use cursor pagination; the client caches server state (a query cache) and never treats the cache as the source of truth. | Common practice; nothing observed. | API client pagination helper. | Pagination style |
| **A-16** | The API client maps failures to typed errors: `Network`, `Timeout`, `Unauthorized`, `Forbidden`, `NotFound`, `RateLimited`, `Validation`, `Server`. | Needed for honest error states (MVP §5). | Mapping table only. | Error format, rate limits |

---

## 3. Service layer (contract the UI depends on)

```
UI (screens, components)
  ↓
Feature logic (hooks per feature: home, profile, breakTheIce, messages, alerts, search)
  ↓
Services (interfaces below)       ← the only thing features import
  ↓
Adapters: MockAdapter [MOCKED]  |  HttpAdapter [PENDING BACKEND]
  ↓
API client (fetch wrapper: auth header, retries, timeout, typed errors)
  ↓
Icebreaker backend (not connected)
```

| Service | Responsibilities (method intents) | Used by | MVP status |
|---|---|---|---|
| `authService` | sign in, sign out, restore session, sign up, request password reset | Sign-in, Settings | [MOCKED]. Session storage [IMPLEMENTED in build] |
| `profileService` | get my profile, get profile by id, update my profile, upload photo | Profile, Edit Profile | [MOCKED] |
| `discoveryService` | get home (Match of the Day + saved + sections), see all in a section | Home | [MOCKED] |
| `searchService` | search people (query, filters, sort, cursor), list available facets | Search | [MOCKED] |
| `networkService` | save / unsave, list saved, **break the ice** (returns a conversation), report, block | Profile, Home | [MOCKED] |
| `messageService` | list conversations, get messages (cursor), send message, subscribe to a conversation, mark read | Messages, Conversation | [MOCKED] (simulated replies) |
| `notificationService` | register device for push, list alerts, mark read, parse notification → deep link | Alerts, app root | Local notifications [IMPLEMENTED in build]; remote push [PENDING BACKEND] |
| `aiAssistService` | suggest opener for a profile, suggest reply for a conversation | Break the Ice composer | [MOCKED] canned suggestions, labelled "Suggested · Prototype" |

The build phase implements these as TypeScript interfaces. Only this document describes them before then.

---

## 4. Provisional data models

Fields are labelled **OBSERVED** (visible in a screenshot or public page), **INFERRED**, or **PROVISIONAL** (needed by the app but not observed). Entities that were never observed are deliberately **not modelled**.

### Profile

| Field | Type | Label | Evidence |
|---|---|---|---|
| `id` | string | PROVISIONAL | — |
| `firstName`, `lastName` | string | OBSERVED | [S3–S5] |
| `photoUrl` | string (URL) | OBSERVED | [S1–S6] |
| `icebreaker` | string (short personal line) | OBSERVED | "I worked for the Yankees" [S3]; quotes on Search cards [S4] |
| `currentRole` | `{ title, company }` | OBSERVED | "Financial Analyst at Tesla" [S1] |
| `education[]` | `{ degree, classYear, school, focusTags[] }` | OBSERVED | "MBA '20", school name, "Marketing" / "Strategy" [S3] |
| `undergraduate` | `{ school }` | OBSERVED | [S3] |
| `workExperience[]` | `{ title, company, startYear, endYear \| null, isCurrent, industryTags[] }` | OBSERVED | "VP Marketing · Pepsi · 2021 – Present · Current", "Technology & Software" [S3] |
| `goals[]` | `GoalId[]` | OBSERVED | [E13]. See the enumeration below |
| `interests[]` | `InterestId[]` | OBSERVED | [E13]. See the enumeration below |
| `city` | string | OBSERVED (policy + carousel titles) | [E8, S2] |
| `bio`, `skills[]` | string, string[] | OBSERVED (policy text only) | [E8] |
| `isSavedByMe` | boolean | INFERRED | Saved state on the profile [S3] |

`ProfileSummary` (carousel and search cards) contains `id`, `firstName`, `lastName?`, `photoUrl`, `school`, `classYear?`, `title?`, `company`, `icebreaker?` [S1, S2, S4].

### Goal options (OBSERVED, "What brings you to Icebreaker?" [E13])

| Group | Options |
|---|---|
| Career | Finding a new role · Exploring career paths · Want mentorship · Switching industries · Need advice · Preparing for recruiting / interviews |
| Entrepreneurship | Finding a co-founder · Building a startup · Fundraising · Exploring startups / VC |
| New in town | New to this city · New to this country |

Also seen as a chip on a Match of the Day card, from a step not observed: **"Willing to mentor"** [S1]. Its source step is UNKNOWN.

### Interest options (OBSERVED, "What are you most passionate about?" [E13])

AI / Machine Learning · Investment Banking · Consulting · Media & Entertainment · Data & Analytics · Marketing / Growth · Entrepreneurship · Product Management · Healthcare · Venture Capital · Nonprofit · Operations · Private Equity · Startups · Sustainability

### Home

| Entity | Fields | Label |
|---|---|---|
| `MatchOfTheDay` | `date`, `profile: ProfileSummary`, `highlightTags[]` (for example, "Willing to mentor", "Finding a cofounder", "+7") | OBSERVED [S1]. `reason` text UNKNOWN |
| `HomeSection` | `id`, `title` (server-provided), `profiles: ProfileSummary[]` | OBSERVED titles [S1, S2]; shape PROVISIONAL |
| `SavedEntry` | `profile: ProfileSummary`, `savedAt` | OBSERVED list [S1]; `savedAt` PROVISIONAL |

### Messaging

| Entity | Fields | Label |
|---|---|---|
| `Conversation` | `id`, `participant: ProfileSummary`, `lastMessagePreview`, `updatedAt`, `unreadCount` | Preview and time OBSERVED [S5]; `unreadCount` INFERRED from tab badges |
| `Message` | `id`, `conversationId`, `senderId`, `body`, `sentAt`, `status: 'sending' \| 'sent' \| 'failed'` | Body and "Sent" OBSERVED [S6]; `sending`/`failed` PROVISIONAL (client states); read receipts UNKNOWN |

### Alerts

| Entity | Fields | Label |
|---|---|---|
| `Alert` | `id`, `type`, `createdAt`, `readAt?`, `target` (deep link) | Tab and badge OBSERVED [S1]. **All fields PROVISIONAL.** MVP types (`new_message`, `match_of_the_day`, `saved_profile_update`) are **[MOCKED]** proposals, not Icebreaker's real alert types |

### Deliberately not modelled

| Entity | Reason |
|---|---|
| `Connection` (request/accept) | Not observed. A-06 assumes conversations are the connection. |
| `Poll` | Only a section header was observed [S1]. |
| `Event`, `Community` | Not observed in the product. Events appear only as offline activity on LinkedIn [E14]. |
| `Subscription` / premium | Offer unknown [E8]. |
| Spark chat / memory | UI unknown [E8]. |

---

## 5. What is needed from Icebreaker to integrate

1. API documentation (or OpenAPI spec) for the endpoints behind §3, plus a **staging** environment and test accounts. A staging app ID already exists [E11].
2. The auth model for native clients: token format, refresh, revocation.
3. The realtime messaging transport and the push provider setup (APNs keys / FCM project). These are configured by Icebreaker and never committed here.
4. The semantics of the universal-link paths (`/m/*`), and approval to host Android `assetlinks.json` on `joinicebreaker.com`.
5. Permission to use official brand assets (logo, app icon) in the proposal build.
6. Confirmation of A-06 (Break the Ice semantics) and of alert types (A-08).

---

## 6. Security invariants (hold now and after integration)

- No credentials, tokens, API keys or `.env` files are committed. Only `.env.example` with placeholder names.
- Session tokens live in the platform secure store on native (Keychain / Keystore). The web strategy is decided with Icebreaker (A-02); tokens are never stored in plain local storage.
- The client never talks to AI providers directly (A-10).
- Logs never include tokens, passwords, message bodies or email addresses.
- The mock layer ships only fictional personas. No real member data is scraped or reproduced.
