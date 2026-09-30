# Icebreaker API (observed)

Base URL: `https://joinicebreaker.com/api/v1` · JSON over HTTPS · FastAPI-style errors (`{"detail": "..."}` or `{"detail":[{"loc","msg","type"}]}` for 422).

This document describes interfaces **observed** in network traffic or in the website's shipped JavaScript. It contains no tokens, cookies or secrets. Response examples use made-up values.

## Authentication

The web client uses httpOnly cookies. The API **also accepts `Authorization: Bearer <access_token>`** (verified), which is what the mobile app uses.

| Aspect | Value |
|---|---|
| Access token | JWT (Supabase-issued claims: `sub`, `email`, `role`, `session_id`, …), lifetime **4 h** |
| Refresh token | Short opaque string, **rotates** on every refresh |
| Missing auth | `401 {"detail":"Could not validate credentials"}` |
| Bad/expired token | `401 {"detail":"Invalid or expired authentication token"}` |

### POST /auth/signin
Request `{ "email": "user@example.com", "password": "…" }`
Response 200:
```json
{
  "user": { "id": "uuid", "email": "user@example.com", "full_name": "…", "is_email_verified": true, "created_at": "ISO" },
  "access_token": "<jwt>", "refresh_token": "<opaque>",
  "needs_email_verification": false, "message": null
}
```
Errors: 401 `Invalid email or password` (same for unknown email).

### POST /auth/refresh
Request `{ "refresh_token": "<opaque>" }` (web sends it via cookie instead). Response: same shape as sign-in with new tokens. Errors: 401.

### POST /auth/signout
Ends the server session. Body `{}`.

### POST /auth/forgot-password
`{ "email": "…" }` → sends a reset link (bundle; not exercised).

### POST /auth/change-password
`{ "current_password": "…", "new_password": "…" }`. 401 = wrong current password. Client rules: ≥ 8 chars, upper, lower, digit, differs from current. The web re-signs-in with the new password afterwards.

### GET /auth/me
`{ "user_id": "uuid", "email": "…", "token_expires": "…" }`

### DELETE /auth/delete-account (bundle)

## Profile

### GET /profile — signed-in user
Key fields: `id, photo_url, first_name, last_name, city, city_display_name, hometown_display_name, mba_school_id, mba_grad_year, current_company, current_title, current_industry, my_icebreaker, hobbies[], my_projects, project_brief, linkedin_url, what_brings_you[], excited_cities[], passionate_about[], help_others[], affinity_tags[], experiences[], school_info{id,name,alias,domain}, is_profile_complete, is_verified, agent_beta_enabled, channels_enabled, created_at, updated_at` (plus structured city/hometown geo fields).

### PUT /profile, POST /profile, POST /profile/photo/upload (multipart `file`), POST/PUT/DELETE /profile/experiences[/{id}] (bundle)

### GET /profile/options
Option lists `{value,label[,description|category|group]}` for: `networking_goals, mba_focus_areas, industries, areas_of_expertise, hobbies, what_brings_you_options, excited_city_options, passionate_about_options, help_others_options, affinity_tag_options`.

### GET /schools
Array of ~800 `{id, name, alias, city, state, country, domain, is_active}`. `GET /schools/search?q=IIM&limit=10` → `{schools[], total_count, query}`.

### GET /cities/predictions?q=…&limit=8 → `[{place_id, description}]`; GET /cities/details?place_id=…

## Discovery

### GET /discovery/search/faceted
Query params (all optional, lists comma-separated): `q, schools, min_year, max_year, focus, industries, hobbies, expertise, desired_expertise, what_brings_you, passionate_about, help_others, affinity_tags, excited_cities, companies, cities` (or geo `city_lats, city_lngs, …`), `sort_by` (`relevance` default | `recent`), `page` (1-based), `limit` (web uses 50).
Headers used by web for analytics: `X-Search-Session-ID`, `X-Previous-Search-ID` (optional).
Response:
```json
{ "profiles": [ProfileSummary], "total_count": 6120, "page": 1, "limit": 50,
  "has_next_page": true, "has_previous_page": false, "total_pages": 123, "search_id": "uuid" }
```
`ProfileSummary`: `id, first_name, last_name, photo_url, city, mba_school_name, mba_school_alias, mba_school_id, mba_grad_year, current_company, current_title, current_industry, my_icebreaker, hobbies[], is_verified, relevance_score, is_connected, has_messaged, is_new, is_active`.

### GET /discovery/profiles/{id}
Full profile of another member (`ProfileDetail` = summary + `experiences[]`, `undergrad_school`, `hometown`, `what_brings_you[]`, `excited_cities[]`, `passionate_about[]`, `help_others[]`, `affinity_tags[]`, `linkedin_url`, `can_message`). Optional query `source_carousel_row_id`.
### POST /discovery/profiles/{id}/view (analytics) · POST /discovery/search/interactions (analytics)

### GET /profiles/{id}/commonalities
```json
{ "commonalities": [{ "category": "school", "label": "School", "items": ["…"] }],
  "reasons_to_connect": [{ "type": "complementary_need_help", "text": "Get their help with …" }] }
```

## Home

### GET /home/carousels (slow: 6–14 s observed)
```json
{ "featured_profile": { "profile_id", "first_name", "last_name", "photo_url", "school_alias", "mba_grad_year",
                         "current_title", "current_company", "shared_context": ["…"], "match_id", "is_new", "is_active", "is_saved" },
  "carousels": [{ "id", "carousel_type", "primary_card_type": "profile|project|notable_icebreaker",
                  "title", "subtitle", "cards": [{ "id", "card_type", "position", "data": { … } }], "has_more" }],
  "generated_at": "ISO", "failed_carousel_count": 0 }
```
Observed `carousel_type`s: `projects_carousel, notable_icebreakers_carousel, people_near_you, bidirectional_investing, bidirectional_mentorship, excited_city, goals_near_you, expertise_near_you, new_to_your_city, similar_expertise, similar_goals, school_near_you, passion_near_you`.
### GET /home/carousels/{carousel_type}?cursor=… (next page; bundle) · POST /home/carousel/analytics/batch
### GET/POST /home/saved-profiles (`{profile_id}`) · DELETE /home/saved-profiles/{id} → `{profiles[], total_count}`

## Messaging (direct)

| Method | Path | Notes |
|---|---|---|
| GET | `/messaging/conversations?limit=200` | `{conversations[], total, limit, offset, has_more}`; each has `other_participant` (ProfileSummary), `last_message`, `last_message_at`, `last_message_sender_id`, `unread_count`, `marked_unread` |
| POST | `/messaging/conversations` | `{other_user_id}` → conversation (get-or-create) |
| GET | `/messaging/conversations/{id}` | single conversation |
| GET | `/messaging/conversations/{id}/messages?limit=100` | `{messages[], total, limit, before_id, has_more}`; message: `id, conversation_id, sender_id, content, created_at, is_read, read_at, message_type, deleted_at, edited_at, edit_count, sender_profile, reactions` |
| POST | `/messaging/conversations/{id}/messages` | `{content, message_type:"text"}` |
| PUT | `/messaging/conversations/{id}/read` | mark read |
| POST | `/messaging/conversations/{id}/mark-unread` | |
| DELETE | `/messaging/conversations/{id}` | (bundle) |
| PATCH/DELETE | `/messaging/messages/{id}` | edit / delete (bundle) |
| POST/DELETE | `/messaging/messages/{id}/reactions[/{emoji}]` | (bundle) |
| GET | `/messaging/unread-count` | `{unread_count, conversations_with_unread}` |

## Channels

| Method | Path | Notes |
|---|---|---|
| GET | `/channels` | directory `{channels:[{id, slug, name, emoji, description, category, audience, member_count, is_member}]}` |
| GET | `/channels/joined` | + `unread_count, last_message_at, last_message_preview, last_message_sender, notification_level` |
| POST/DELETE | `/channels/{id}/join` | join / leave |
| GET | `/channels/{id}/messages?before=&limit=` | `{messages[], has_more, joins[]}`; message: `id, channel_id, content, created_at, edited_at, deleted_at, is_pinned, sender{user_id,first_name,last_name,photo_url}, reactions[{emoji,count,reacted_by_me}], link_preview, media_type, media_url, media_width, media_height, mentioned_user_ids[], parent_message_id, thread{reply_count,last_reply_at,participants[],has_unread_replies}` |
| POST | `/channels/{id}/messages` | `{content, media?, mentioned_user_ids?}` |
| PUT | `/channels/{id}/read` | mark read |
| GET | `/channels/{id}/members` | `{members[], member_count, truncated}` |
| PUT | `/channels/{id}/notifications` | `{level}` |
| GET/POST/PUT | `/channels/messages/{id}/thread`, `/replies`, `/thread/read` | threads (bundle) |
| POST | `/channels/messages/{id}/reactions`, `/report`; PATCH/DELETE `/channels/messages/{id}` | (bundle) |
| POST | `/channels/media/sign`, `/channels/giphy/search`; GET `/channels/{id}/mentions/search` | (bundle) |

## Notifications

`GET /notifications` → array of `{id, notification_type, metadata{title, body, deep_link, sender_id, sender_name, sender_photo_url, conversation_id, …}, sent_at, read_at, opened_at, is_read, is_opened}` · `GET /notifications/unread-count` → `{count}` · `POST /notifications/{id}/mark-read` · `POST /notifications/mark-all-read` · `POST /notifications/matches/{id}/mark-read`.

## Settings

`GET /user-settings` → `{settings:{push_notifications, email_notifications, discovery_enabled, show_graduation_year, privacy_level, blocked_users[], theme_preference, has_shown_onboarding_tour, has_seen_welcome, match_eligible, terms_accepted_at, terms_version, …}, message}` · `PATCH /user-settings` (partial) · `GET /user-settings/blocked-users` · `POST/DELETE /user-settings/block/{id}`.

## Spark agent (SSE)

`GET /agent/interactions?scope=latest_session` → `{user_id, session_id, interactions:[{id, session_id, type:"message", details:{role, content}, created_at}]}`

`POST /agent/chat` with `Accept: text/event-stream`, body `{ "messages": [{role, content}], "session_id"?: "uuid" }` (empty `messages` → greeting). Stream of `event:`/`data:` blocks:

| event | data |
|---|---|
| `ready` | `{session_id, model, contract_version}` |
| `text` | `{delta}` — append to the current assistant message |
| `tool_call` | tool name (`search_network`, `get_commonalities`, `draft_icebreaker`, `get_profile`, `imagine_conversation`, `send_icebreaker`, …) |
| `profile_card`, `icebreaker`, `message_sent`, `imagined_conversation`, `goal_summary`, `resume_feedback`, `document_intake` | structured cards |
| `suggestions` | `{chips:[{id, label, send_text}]}` |
| `usage` | token accounting |
| `done` | `{session_id}` |
| `error` | error info |

Also `POST /agent/memory/reset`, `/agent/documents`, `/agent/resume/review` (bundle).

## Other
`POST /sessions` `{platform, app_version, os_version, device_model}` / `PUT /sessions/{id}` `{session_end}` (usage analytics) · `GET /referrals/my-code` → `{code, share_url}` · `POST /polls/{id}/vote` `{option_id}` · `/conversation-starters/generate`, `/conversation-movers/*` (AI assists).

## Media
Profile photos are Cloudinary URLs (`res.cloudinary.com/.../image/upload/v…/icebreaker/profiles/…`). Resize by inserting a transformation after `/upload/`, e.g. `c_fill,w_192,h_192,f_auto,q_auto/` (same as the website).

## Reliability notes
Observed intermittent `502 Bad Gateway` on several GET endpoints; `/home/carousels` latency 6–14 s. Clients should retry idempotent GETs and cache the home feed.
