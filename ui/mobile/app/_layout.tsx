import React, { useEffect, useState } from 'react';
import { Stack } from 'expo-router';
import { View, ActivityIndicator, StyleSheet } from 'react-native';
import { PaperProvider, MD3DarkTheme } from 'react-native-paper';
import { colors } from '../src/constants/theme';
import { useAppStore } from '../src/store/useAppStore';
import { getSession } from '../src/services/supabase';

const theme = {
  ...MD3DarkTheme,
  colors: {
    ...MD3DarkTheme.colors,
    primary: colors.primary,
    background: colors.background,
    surface: colors.surface,
  },
};

export default function RootLayout() {
  const setUser = useAppStore((state) => state.setUser);
  const setLoading = useAppStore((state) => state.setLoading);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const session = await getSession();
        if (session?.user) {
          setUser(session.user);
        }
      } catch (error) {
        console.log('Erro ao verificar sessão:', error);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  return (
    <PaperProvider theme={theme}>
      <Stack
        screenOptions={{
          headerShown: false,
          contentStyle: { backgroundColor: colors.background },
        }}
      >
        <Stack.Screen name="(auth)/login" />
        <Stack.Screen name="(auth)/register" />
        <Stack.Screen name="(drawer)" />
      </Stack>
    </PaperProvider>
  );
}
