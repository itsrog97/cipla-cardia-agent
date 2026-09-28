# Product Matrix: Existing Core vs Mobile Enhancement vs Future Hypothesis

**Phase:** 4
**Date:** 2026-09-28

The three columns in the matrix below:

- **Existing Icebreaker Core:** what Icebreaker has today, with its evidence label. The MVP must keep all of this recognisable.
- **Mobile Enhancement:** improves an existing capability on phone, tablet or desktop. It does not create a new product surface. Each has a hypothesis ID.
- **Future Hypothesis:** a new idea, clearly a **proposal**, kept out of the MVP.

| Area | Existing Icebreaker Core | Mobile Enhancement (proposal) | Future Hypothesis (proposal) |
|---|---|---|---|
| **Platforms** | Native iPhone app [OBSERVED E12]; web sign-in/sign-up and auth-gated web app [OBSERVED E2–E6] | One codebase for iPhone, Android, tablet and Chromebook/web with adaptive layouts (H-01, H-02, H-13) | Mac Catalyst / desktop wrapper; wearables |
| **Sign-in** | Email + password; password reset by email link [OBSERVED E2, E4]; shared iOS web credentials [OBSERVED E11] | Secure token storage; biometric unlock for returning sessions; system password autofill on Android and iOS | Passkeys; Sign in with Apple/Google (needs a product decision by Icebreaker) |
| **Sign-up & vetting** | Email, password, optional invite code, consent [OBSERVED E3]; email verification [INFERRED E11]; vetting mechanism [UNKNOWN] | Deep link from the verification email straight into the next onboarding step on any platform (H-08) | School-email or SSO verification flows (depends on UNKNOWN vetting rules) |
| **Onboarding / profile setup** | 13-step setup [OBSERVED E7]; Goals and Interests chip steps [OBSERVED E13] | Progressive profiling: minimum steps unlock the first match; the rest become nudges (H-05); native camera/photo picker with avatar crop | AI-drafted icebreaker line from the user's own inputs |
| **Home / Match of the Day** | Match of the Day card; My Saved Icebreakers; themed carousels by school, city, expertise and need; Polls for You [OBSERVED S1, S2] | Pull-to-refresh; skeleton loading; "See all" to a vertical list (H-10); grid layout on tablet and desktop | Daily match notification (H-03) and home-screen widget |
| **Search** | Search by profiles, schools, companies; quick chips (Same School, Different School, Similar Expertise); Sort [OBSERVED S4]; filters by school, year, focus area [OBSERVED text E7]; AI-assisted semantic search [OBSERVED text E8] | Filters bottom sheet (phone) or sidebar (tablet/desktop) exposing every facet (H-09); `/` keyboard shortcut on desktop; results + profile split view on tablet | Natural-language search ("PMs in NYC who switched from consulting") through the existing AI search |
| **Profile** | Sheet with photo, icebreaker quote, education, work experience, tags; **Saved** and **Break the Ice** actions; "•••" menu [OBSERVED S3] | Same content; sheet on phone, side panel on tablet and desktop; share-profile link through the native share sheet (H-08); haptic feedback on Save | "Why you might connect" explanation from Spark, on the profile |
| **Break the Ice** | Primary action [OBSERVED S3]; AI conversation starters exist [OBSERVED text E9]; resulting flow [UNKNOWN] | Composer bottom sheet over the profile with an editable, labelled suggested opener (H-06); success haptic; permission priming for push right after the first send (H-04) | "Imagine the Conversation" preview inside the composer (exists per Terms E9; its UI is UNKNOWN, so it is not recreated in the MVP) |
| **Messages** | Conversation list with search and filter; 1:1 thread with "Sent" status [OBSERVED S5, S6]; suggested replies [OBSERVED text E9] | List + thread split view on tablet and desktop; tab bar hidden in the thread on phone; keyboard-aware composer; `Enter` to send on desktop | Quick reply from the notification; offline outbox |
| **Alerts / notifications** | Alerts tab with badge [OBSERVED S1]; push opt-in [OBSERVED E8]; contents [UNKNOWN] | Every alert deep-links to its exact destination (H-03); contextual permission prompt (H-04); Android notification channels | Granular notification preferences; digest mode |
| **AI assistant** | Spark: chat to find people, explain fit, draft outreach; has memory [OBSERVED text E8] | Entry points in context: profile ("why connect") and composer ("draft opener"). **Shown only as clearly mocked UI** in the MVP | A full Spark chat surface on mobile, including voice input |
| **Polls** | "Polls for You" section header [OBSERVED S1]; mechanics [UNKNOWN] | — (unknown mechanics, so no enhancement proposed) | Poll cards on Home once mechanics are known |
| **Safety** | Abuse reporting by email [OBSERVED E7]; in-app tools [UNKNOWN] | Report and Block in the "•••" menu of Profile and Conversation, with confirmation | Automated abuse signals |
| **Settings / account** | Settings → Account → Delete Account; notification settings [OBSERVED text E7] | Native-feeling settings list; account deletion reachable in two taps | Data export in-app (the right exists per the Privacy Policy, E8) |
| **Invites & growth** | Invite code at sign-up [OBSERVED E3]; download page with QR [OBSERVED E5] | Native share sheet for invites; device-aware install links; phone-first invite page (H-07, H-08) | Referral tracking and rewards |
| **Monetisation** | Premium features mentioned [OBSERVED text E8]; offer [UNKNOWN] | — (out of scope) | Platform-native in-app purchase once the offer is known |
| **Offline / IRL** | In-person events [OBSERVED E14, outside the app] | — | Event mode: profile QR show/scan (H-12) |

## Guardrails

1. **Existing core stays recognisable.** The MVP keeps these as-is:
   - the four tabs (Home, Search, Messages, Alerts), with no new "Discover" tab;
   - the names "Match of the Day", "My Saved Icebreakers", "Break the Ice" and "Saved";
   - the navy/white visual identity.
2. **Enhancements improve something that already exists.** No enhancement introduces a new top-level product surface.
3. **Anything in the "Future" column** appears in the founder demo only as a labelled proposal (slide or roadmap), never as a working feature.
4. **Anything whose real UI is UNKNOWN** (Spark, Imagine the Conversation, Polls, Alerts contents) is either left out or shown as clearly **[MOCKED]** UI with an on-screen "Prototype" label. It is never presented as a copy of Icebreaker's actual design.
