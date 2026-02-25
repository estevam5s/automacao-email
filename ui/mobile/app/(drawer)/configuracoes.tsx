import React, { useState, useEffect } from 'react';
import { View, StyleSheet, ScrollView, Alert } from 'react-native';
import { Text, TextInput, Button, Card } from 'react-native-paper';
import { colors, spacing, fontSize } from '../../src/constants/theme';
import { useAppStore } from '../../src/store/useAppStore';
import { Configuracao } from '../../src/types';

export default function ConfiguracoesScreen() {
  const { configuracao, loadConfiguracao, saveConfiguracao } = useAppStore();
  
  const [emailRemetente, setEmailRemetente] = useState('');
  const [emailDestinatario, setEmailDestinatario] = useState('');
  const [senhaApp, setSenhaApp] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadConfiguracao();
  }, []);

  useEffect(() => {
    if (configuracao) {
      setEmailRemetente(configuracao.email_remetente || '');
      setEmailDestinatario(configuracao.email_destinatario || '');
      setSenhaApp(configuracao.senha_app || '');
    }
  }, [configuracao]);

  const handleSalvar = async () => {
    if (!emailRemetente || !emailDestinatario || !senhaApp) {
      Alert.alert('Erro', 'Por favor, preencha todos os campos');
      return;
    }

    setLoading(true);
    try {
      const config: Configuracao = {
        email_remetente: emailRemetente,
        email_destinatario: emailDestinatario,
        senha_app: senhaApp,
      };
      
      await saveConfiguracao(config);
      Alert.alert('Sucesso', 'Configurações salvas!');
    } catch (error: any) {
      Alert.alert('Erro', error.message || 'Erro ao salvar');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.content}>
        <Card style={styles.card}>
          <Card.Content>
            <Text style={styles.title}>Configurações de E-mail</Text>
            
            <TextInput
              label="E-mail Remetente"
              value={emailRemetente}
              onChangeText={setEmailRemetente}
              mode="outlined"
              keyboardType="email-address"
              autoCapitalize="none"
              style={styles.input}
              outlineColor={colors.border}
              activeOutlineColor={colors.primary}
              textColor={colors.text}
              placeholder="seu-email@gmail.com"
            />
            
            <TextInput
              label="E-mail Destinatário"
              value={emailDestinatario}
              onChangeText={setEmailDestinatario}
              mode="outlined"
              keyboardType="email-address"
              autoCapitalize="none"
              style={styles.input}
              outlineColor={colors.border}
              activeOutlineColor={colors.primary}
              textColor={colors.text}
              placeholder="destinatario@email.com"
            />
            
            <TextInput
              label="Senha de App do Gmail"
              value={senhaApp}
              onChangeText={setSenhaApp}
              mode="outlined"
              secureTextEntry
              style={styles.input}
              outlineColor={colors.border}
              activeOutlineColor={colors.primary}
              textColor={colors.text}
              placeholder="Senha de 16 caracteres"
            />

            <Button
              mode="contained"
              onPress={handleSalvar}
              loading={loading}
              disabled={loading}
              style={styles.button}
              buttonColor={colors.primary}
              textColor={colors.black}
            >
              Salvar Configurações
            </Button>
          </Card.Content>
        </Card>

        <Card style={styles.infoCard}>
          <Card.Content>
            <Text style={styles.infoTitle}>Como obter a senha de app do Gmail:</Text>
            
            <View style={styles.infoList}>
              <Text style={styles.infoItem}>1. Acesse myaccount.google.com/apppasswords</Text>
              <Text style={styles.infoItem}>2. Faça login com sua conta Google</Text>
              <Text style={styles.infoItem}>3. Em "Selecione o app", escolha "E-mail"</Text>
              <Text style={styles.infoItem}>4. Em "Selecione o dispositivo", escolha "Outro"</Text>
              <Text style={styles.infoItem}>5. Digite um nome (ex: "App Salários")</Text>
              <Text style={styles.infoItem}>6. Clique em "Gerar"</Text>
              <Text style={styles.infoItem}>7. Copie a senha de 16 caracteres</Text>
            </View>
          </Card.Content>
        </Card>

        <Card style={styles.card}>
          <Card.Content>
            <Text style={styles.title}>Informações do Sistema</Text>
            
            <View style={styles.infoRow}>
              <Text style={styles.infoLabel}>Servidor SMTP:</Text>
              <Text style={styles.infoValue}>smtp.gmail.com</Text>
            </View>
            
            <View style={styles.infoRow}>
              <Text style={styles.infoLabel}>Porta SMTP:</Text>
              <Text style={styles.infoValue}>587</Text>
            </View>
            
            <View style={styles.infoRow}>
              <Text style={styles.infoLabel}>Segurança:</Text>
              <Text style={styles.infoValue}>TLS</Text>
            </View>
            
            <View style={styles.infoRow}>
              <Text style={styles.infoLabel}>Banco de Dados:</Text>
              <Text style={styles.infoValue}>Supabase</Text>
            </View>
          </Card.Content>
        </Card>

        <Card style={styles.card}>
          <Card.Content>
            <Text style={styles.title}>Sobre</Text>
            
            <Text style={styles.aboutText}>
              Sistema de Relatório de Salários de Garçons
            </Text>
            <Text style={styles.aboutText}>
              Versão 1.0.0
            </Text>
            <Text style={styles.aboutText}>
              Desenvolvido por Estevam Souza
            </Text>
          </Card.Content>
        </Card>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  content: {
    padding: spacing.md,
  },
  card: {
    backgroundColor: colors.surface,
    marginBottom: spacing.md,
  },
  infoCard: {
    backgroundColor: colors.card,
    marginBottom: spacing.md,
  },
  title: {
    fontSize: fontSize.lg,
    fontWeight: 'bold',
    color: colors.primary,
    marginBottom: spacing.md,
  },
  input: {
    marginBottom: spacing.md,
    backgroundColor: colors.card,
  },
  button: {
    marginTop: spacing.md,
  },
  infoTitle: {
    fontSize: fontSize.md,
    fontWeight: 'bold',
    color: colors.primary,
    marginBottom: spacing.md,
  },
  infoList: {
    marginLeft: spacing.sm,
  },
  infoItem: {
    fontSize: fontSize.sm,
    color: colors.text,
    marginBottom: spacing.xs,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: spacing.sm,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  infoLabel: {
    fontSize: fontSize.md,
    color: colors.textSecondary,
  },
  infoValue: {
    fontSize: fontSize.md,
    color: colors.text,
    fontWeight: 'bold',
  },
  aboutText: {
    fontSize: fontSize.md,
    color: colors.text,
    textAlign: 'center',
    marginBottom: spacing.xs,
  },
});
