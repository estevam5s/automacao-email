import React, { useState } from 'react';
import { View, StyleSheet, KeyboardAvoidingView, Platform, ScrollView } from 'react-native';
import { TextInput, Button, Text, HelperText } from 'react-native-paper';
import { useRouter } from 'expo-router';
import { colors, spacing, fontSize } from '../../src/constants/theme';
import { signIn } from '../../src/services/supabase';
import { useAppStore } from '../../src/store/useAppStore';

export default function LoginScreen() {
  const router = useRouter();
  const setUser = useAppStore((state) => state.setUser);
  const setLoading = useAppStore((state) => state.setLoading);
  
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoadingLocal] = useState(false);
  const [error, setError] = useState('');

  const handleLogin = async () => {
    if (!email || !password) {
      setError('Por favor, preencha todos os campos');
      return;
    }

    setLoadingLocal(true);
    setError('');

    try {
      const data = await signIn(email, password);
      setUser(data.user);
      router.replace('/(drawer)/home');
    } catch (err: any) {
      setError(err.message || 'Erro ao fazer login');
    } finally {
      setLoadingLocal(false);
    }
  };

  return (
    <KeyboardAvoidingView 
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.header}>
          <Text style={styles.title}>Sistema de Salários</Text>
          <Text style={styles.subtitle}>Garçons</Text>
        </View>

        <View style={styles.form}>
          <TextInput
            label="E-mail"
            value={email}
            onChangeText={setEmail}
            mode="outlined"
            keyboardType="email-address"
            autoCapitalize="none"
            style={styles.input}
            outlineColor={colors.border}
            activeOutlineColor={colors.primary}
            textColor={colors.text}
          />

          <TextInput
            label="Senha"
            value={password}
            onChangeText={setPassword}
            mode="outlined"
            secureTextEntry={!showPassword}
            style={styles.input}
            outlineColor={colors.border}
            activeOutlineColor={colors.primary}
            textColor={colors.text}
            right={
              <TextInput.Icon 
                icon={showPassword ? 'eye-off' : 'eye'} 
                onPress={() => setShowPassword(!showPassword)}
              />
            }
          />

          {error ? (
            <HelperText type="error" visible={!!error}>
              {error}
            </HelperText>
          ) : null}

          <Button
            mode="contained"
            onPress={handleLogin}
            loading={loading}
            disabled={loading}
            style={styles.button}
            buttonColor={colors.primary}
            textColor={colors.black}
          >
            Entrar
          </Button>

          <Button
            mode="text"
            onPress={() => router.push('/(auth)/register')}
            style={styles.linkButton}
            textColor={colors.primary}
          >
            Não tem conta? Cadastre-se
          </Button>
        </View>

        <View style={styles.footer}>
          <Text style={styles.footerText}>
            Desenvolvido por Estevam Souza
          </Text>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  scrollContent: {
    flexGrow: 1,
    justifyContent: 'center',
    padding: spacing.lg,
  },
  header: {
    alignItems: 'center',
    marginBottom: spacing.xxl,
  },
  title: {
    fontSize: fontSize.title,
    fontWeight: 'bold',
    color: colors.primary,
  },
  subtitle: {
    fontSize: fontSize.xxl,
    color: colors.text,
    marginTop: spacing.xs,
  },
  form: {
    backgroundColor: colors.surface,
    borderRadius: 16,
    padding: spacing.lg,
  },
  input: {
    marginBottom: spacing.md,
    backgroundColor: colors.card,
  },
  button: {
    marginTop: spacing.md,
    paddingVertical: spacing.xs,
  },
  linkButton: {
    marginTop: spacing.md,
  },
  footer: {
    marginTop: spacing.xxl,
    alignItems: 'center',
  },
  footerText: {
    color: colors.textSecondary,
    fontSize: fontSize.sm,
  },
});
