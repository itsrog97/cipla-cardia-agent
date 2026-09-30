# Icebreaker Mobile (Android test build)

A native, mobile-first client for **Icebreaker** (joinicebreaker.com) — MBA networking: discover people, break the ice, chat 1:1 and in channels, and get help from the Spark AI assistant. It talks to the same backend as the website using the member's own account.

> Status: **ANDROID TEST BUILD v0.1.0 — not a final release.** See `CHANGELOG.md` and `docs/qa-report.md`.

## Tech stack
- React Native 0.86 + **Expo SDK 57**, **Expo Router** (file-based navigation, protected routes), **TypeScript** (strict)
- TanStack Query (caching, polling, retries), expo-secure-store (tokens), expo-image, NetInfo, Inter font, Ionicons
- Jest + jest-expo + React Native Testing Library

## Project structure
```
icebreaker-mobile/
├── src/
│   ├── app/                    # Routes (Expo Router)
│   │   ├── _layout.tsx         # Providers, fonts, splash, auth-protected stack
│   │   ├── login.tsx, forgot-password.tsx
│   │   └── (app)/              # Only reachable when signed in
│   │       ├── (tabs)/         # Home, Discover, Spark, Chat (messages), Profile
│   │       ├── person/[id].tsx, conversation/[id].tsx, channel/[id].tsx
│   │       └── notifications.tsx, settings.tsx, change-password.tsx
│   ├── api/                    # client.ts (fetch, bearer auth, refresh, timeouts) + endpoints.ts
│   ├── components/             # Design-system components
│   ├── constants/config.ts     # Base URL, timeouts, poll intervals, links
│   ├── hooks/                  # React Query hooks, Spark streaming hook
│   ├── services/               # SecureStore token storage, SSE parser
│   ├── store/AuthProvider.tsx  # Session state machine
│   ├── theme/                  # Tokens (from the website's CSS) + ThemeProvider (light/dark)
│   ├── types/api.ts            # API types
│   └── utils/                  # Formatting, validation, dialogs, notification routing
├── __tests__/                  # Unit & component tests
├── plugins/withReleaseSigning.js  # Uses android/keystore.properties for release signing if present
├── docs/                       # Audit, spec, flows, data model, API, design system, QA report
└── app.json                    # Expo config (package com.icebreaker.mobiletest)
```

## Prerequisites
- Node.js 20+ (tested with 22) and npm
- For native Android builds: JDK 17–21, Android SDK (platform 36, build-tools 36), `ANDROID_HOME` set. Android Studio is optional.

## Install & run
```bash
cd icebreaker-mobile
npm install
npx expo start            # dev server; press "a" for a connected Android device/emulator
npm run android           # = npx expo run:android (builds & installs a dev build)
npx expo start --web      # quick browser preview (see note below)
```
Note: the web preview is for development only. Browsers block the API's cross-origin requests from `localhost`, and tokens are kept in memory on web (a page reload signs you out).

## Tests & checks
```bash
npm test                  # Jest (39 tests)
npm run typecheck         # tsc --noEmit
npm run lint              # expo lint
npx expo-doctor           # dependency/config health
```

## Build an APK (test build)
```bash
npx expo prebuild --platform android --clean     # generates ./android (git-ignored)
cd android
./gradlew assembleRelease -PreactNativeArchitectures=arm64-v8a,armeabi-v7a,x86_64
# → android/app/build/outputs/apk/release/app-release.apk
```
Without `android/keystore.properties` the release APK is signed with the **debug key** — fine for side-loading test builds, not for the Play Store.

## Build an AAB (Google Play)
1. Create an upload key once (keep it and its passwords safe — never commit them):
   ```bash
   keytool -genkeypair -v -keystore ~/keys/icebreaker-upload.keystore -alias upload -keyalg RSA -keysize 2048 -validity 10000
   ```
2. After `npx expo prebuild`, create `android/keystore.properties` (git-ignored):
   ```properties
   storeFile=/home/you/keys/icebreaker-upload.keystore
   storePassword=…
   keyAlias=upload
   keyPassword=…
   ```
3. `cd android && ./gradlew bundleRelease` → `android/app/build/outputs/bundle/release/app-release.aab`
4. Bump `expo.version` and `expo.android.versionCode` in `app.json` for every upload.

Alternatively use EAS Build (`npx eas-cli@latest build -p android`), which manages keys in the cloud.

## Environment variables
| Variable | Default | Purpose |
|---|---|---|
| `EXPO_PUBLIC_API_BASE_URL` | `https://joinicebreaker.com` | Backend origin (e.g. a staging server) |

Copy `.env.example` to `.env.local` to override. `EXPO_PUBLIC_*` values are compiled into the app — **never put secrets or credentials in them**.

## Secure credential handling
- There are **no credentials in this repository**. Users sign in interactively in the app.
- The password is sent once to `POST /api/v1/auth/signin` over HTTPS and is never stored.
- The returned access/refresh tokens are stored only in **expo-secure-store** (Android Keystore-backed encryption; iOS Keychain), with `AFTER_FIRST_UNLOCK_THIS_DEVICE_ONLY`. `android:allowBackup` is disabled.
- Tokens are sent only in the `Authorization` header (`credentials: 'omit'`, no cookies) and are never logged.
- On logout or a rejected refresh, tokens are deleted and all cached data is cleared.
- `.gitignore` excludes `.env*`, keystores, `keystore.properties`, `credentials.json`, APK/AAB files.

## Known limitations (v0.1)
See `docs/qa-report.md` for the full list. Highlights: no push notifications yet; profile editing, threads, reactions, media posting and AI reply helpers open/remain on the website; not yet tested on a physical device (the build environment has no hardware-accelerated emulator) — the APK needs your on-device check.
