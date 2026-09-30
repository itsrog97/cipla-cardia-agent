import Constants from 'expo-constants';

/** Backend origin. Override with EXPO_PUBLIC_API_BASE_URL (see .env.example). */
export const API_BASE_URL = (process.env.EXPO_PUBLIC_API_BASE_URL || 'https://joinicebreaker.com').replace(/\/$/, '');

export const WEB_BASE_URL = 'https://joinicebreaker.com';

export const APP_VERSION: string = Constants.expoConfig?.version ?? '0.1.0';

/** Mirrors the web client's default request timeout. */
export const REQUEST_TIMEOUT_MS = 15_000;

/** Polling intervals observed in the web client (React Query refetchInterval). */
export const POLL = {
  unreadCounts: 30_000,
  conversations: 30_000,
  notifications: 60_000,
  openThread: 4_000,
} as const;

export const LINKS = {
  terms: `${WEB_BASE_URL}/terms`,
  privacy: `${WEB_BASE_URL}/privacy`,
  support: `${WEB_BASE_URL}/support`,
  signup: `${WEB_BASE_URL}/signup`,
} as const;
