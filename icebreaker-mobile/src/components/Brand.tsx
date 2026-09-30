import NetInfo from '@react-native-community/netinfo';
import { Image } from 'expo-image';
import React, { useEffect, useState } from 'react';
import { StyleSheet, View } from 'react-native';

import { spacing, useTheme } from '@/theme';
import { AppText } from './AppText';

const wordmark = require('../../assets/logo-wordmark.png');

/** Icebreaker wordmark; tinted for dark mode. Source aspect ratio 1930×460. */
export function Logo({ height = 30 }: { height?: number }) {
  const { scheme } = useTheme();
  return (
    <Image
      source={wordmark}
      style={{ height, width: height * (1930 / 460) }}
      contentFit="contain"
      tintColor={scheme === 'dark' ? '#eceff2' : undefined}
      accessibilityLabel="Icebreaker"
      accessibilityRole="image"
    />
  );
}

/** Thin banner shown while the device has no connectivity. */
export function OfflineBanner() {
  const { colors } = useTheme();
  const [offline, setOffline] = useState(false);
  useEffect(
    () =>
      NetInfo.addEventListener((s) => {
        setOffline(s.isConnected === false || s.isInternetReachable === false);
      }),
    [],
  );
  if (!offline) return null;
  return (
    <View style={[styles.banner, { backgroundColor: colors.warning }]} accessibilityRole="alert">
      <AppText variant="caption" color="#1a1300" align="center">
        You’re offline. Showing saved data where available.
      </AppText>
    </View>
  );
}

const styles = StyleSheet.create({
  banner: { paddingVertical: spacing.xs, paddingHorizontal: spacing.lg },
});
