import React from 'react';
import { Stack } from 'expo-router';
import { Drawer } from 'expo-router/drawer';
import { View, StyleSheet } from 'react-native';
import { IconButton } from 'react-native-paper';
import { colors } from '../../src/constants/theme';

export default function DrawerLayout() {
  return (
    <Drawer
      screenOptions={{
        headerStyle: {
          backgroundColor: colors.surface,
        },
        headerTintColor: colors.text,
        headerRight: () => (
          <View style={styles.headerRight}>
            <IconButton
              icon="menu"
              iconColor={colors.primary}
              onPress={() => {}}
            />
          </View>
        ),
        drawerStyle: {
          backgroundColor: colors.surface,
        },
        drawerActiveTintColor: colors.primary,
        drawerInactiveTintColor: colors.textSecondary,
        drawerLabelStyle: {
          marginLeft: -20,
          fontSize: 14,
        },
      }}
    >
      <Drawer.Screen
        name="home"
        options={{
          title: 'Início',
          drawerIcon: ({ color, size }) => (
            <IconButton icon="home" iconColor={color} size={size} />
          ),
          headerTitle: 'Sistema de Salários',
        }}
      />
      <Drawer.Screen
        name="cadastro"
        options={{
          title: 'Cadastrar Funcionários',
          drawerIcon: ({ color, size }) => (
            <IconButton icon="account-plus" iconColor={color} size={size} />
          ),
          headerTitle: 'Cadastro',
        }}
      />
      <Drawer.Screen
        name="registro"
        options={{
          title: 'Registro Diário',
          drawerIcon: ({ color, size }) => (
            <IconButton icon="calendar-edit" iconColor={color} size={size} />
          ),
          headerTitle: 'Registro',
        }}
      />
      <Drawer.Screen
        name="relatorio"
        options={{
          title: 'Enviar E-mail / Relatório',
          drawerIcon: ({ color, size }) => (
            <IconButton icon="send" iconColor={color} size={size} />
          ),
          headerTitle: 'Relatório',
        }}
      />
      <Drawer.Screen
        name="historico"
        options={{
          title: 'Histórico e Estatísticas',
          drawerIcon: ({ color, size }) => (
            <IconButton icon="chart-bar" iconColor={color} size={size} />
          ),
          headerTitle: 'Histórico',
        }}
      />
      <Drawer.Screen
        name="logs"
        options={{
          title: 'Logs do Sistema',
          drawerIcon: ({ color, size }) => (
            <IconButton icon="format-list-bulleted" iconColor={color} size={size} />
          ),
          headerTitle: 'Logs',
        }}
      />
      <Drawer.Screen
        name="configuracoes"
        options={{
          title: 'Configurações',
          drawerIcon: ({ color, size }) => (
            <IconButton icon="cog" iconColor={color} size={size} />
          ),
          headerTitle: 'Configurações',
        }}
      />
    </Drawer>
  );
}

const styles = StyleSheet.create({
  headerRight: {
    marginRight: 8,
  },
});
