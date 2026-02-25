import React from 'react';
import { View, StyleSheet, TouchableOpacity } from 'react-native';
import { useRouter, usePathname } from 'expo-router';
import { IconButton } from 'react-native-paper';
import { colors, spacing } from '../constants/theme';

interface TabItem {
  name: string;
  icon: string;
  route: string;
}

export default function BottomBar() {
  const router = useRouter();
  const pathname = usePathname();

  const tabs: TabItem[] = [
    { name: 'home', icon: 'home', label: 'Início', route: '/home' },
    { name: 'registro', icon: 'calendar-edit', label: 'Registro', route: '/registro' },
    { name: 'historico', icon: 'chart-bar', label: 'Histórico', route: '/historico' },
  ];

  return (
    <View style={styles.container}>
      <View style={styles.tabsContainer}>
        {tabs.map((tab) => {
          const isActive = pathname === tab.route || pathname === tab.route.replace('/(drawer)', '');
          return (
            <TouchableOpacity
              key={tab.name}
              style={styles.tab}
              onPress={() => router.push(tab.route as any)}
            >
              <IconButton
                icon={tab.icon}
                iconColor={isActive ? colors.primary : colors.textSecondary}
                size={28}
              />
            </TouchableOpacity>
          );
        })}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    backgroundColor: colors.surface,
    borderTopWidth: 1,
    borderTopColor: colors.border,
    paddingBottom: spacing.md,
  },
  tabsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
    paddingVertical: spacing.sm,
  },
  tab: {
    alignItems: 'center',
    justifyContent: 'center',
  },
});
