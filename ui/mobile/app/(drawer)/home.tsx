import React, { useEffect } from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Text, Card, Button, Chip } from 'react-native-paper';
import { useRouter } from 'expo-router';
import { colors, spacing, fontSize } from '../../src/constants/theme';
import { useAppStore } from '../../src/store/useAppStore';
import BottomBar from '../../src/components/BottomBar';

export default function HomeScreen() {
  const router = useRouter();
  const { 
    loadFuncionarios, 
    loadNomesFuncionarios, 
    loadTotalFuncionarios,
    loadRanking,
    totalFuncionarios,
    ranking,
    isSyncing 
  } = useAppStore();

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    await Promise.all([
      loadFuncionarios(),
      loadNomesFuncionarios(),
      loadTotalFuncionarios(),
      loadRanking(),
    ]);
  };

  return (
    <View style={styles.container}>
      <ScrollView style={styles.scrollView} contentContainerStyle={styles.scrollContent}>
        <Card style={styles.welcomeCard}>
          <Card.Content>
            <Text style={styles.welcomeTitle}>Bem-vindo!</Text>
            <Text style={styles.welcomeSubtitle}>
              Sistema de Relatório de Salários de Garçons
            </Text>
          </Card.Content>
        </Card>

        <Text style={styles.sectionTitle}>Estatísticas</Text>
        
        <View style={styles.statsGrid}>
          <Card style={styles.statCard}>
            <Card.Content>
              <Text style={styles.statValue}>{totalFuncionarios?.total_cadastrados || 0}</Text>
              <Text style={styles.statLabel}>Funcionários</Text>
            </Card.Content>
          </Card>
          
          <Card style={styles.statCard}>
            <Card.Content>
              <Text style={styles.statValue}>{totalFuncionarios?.total_registros || 0}</Text>
              <Text style={styles.statLabel}>Registros</Text>
            </Card.Content>
          </Card>
          
          <Card style={styles.statCard}>
            <Card.Content>
              <Text style={styles.statValue}>{totalFuncionarios?.total_dias_trabalhados || 0}</Text>
              <Text style={styles.statLabel}>Dias Trab.</Text>
            </Card.Content>
          </Card>
        </View>

        <View style={styles.statsRow}>
          <Card style={[styles.statCard, { flex: 1, marginRight: spacing.sm }]}>
            <Card.Content>
              <Text style={[styles.statValue, { color: colors.success }]}>
                R$ {totalFuncionarios?.total_pago?.toFixed(2) || '0.00'}
              </Text>
              <Text style={styles.statLabel}>Total Pago</Text>
            </Card.Content>
          </Card>
          
          <Card style={[styles.statCard, { flex: 1, marginLeft: spacing.sm }]}>
            <Card.Content>
              <Text style={[styles.statValue, { color: colors.warning }]}>
                R$ {totalFuncionarios?.total_pendente?.toFixed(2) || '0.00'}
              </Text>
              <Text style={styles.statLabel}>Pendente</Text>
            </Card.Content>
          </Card>
        </View>

        <Card style={styles.totalCard}>
          <Card.Content>
            <Text style={styles.totalLabel}>Total Geral (10%)</Text>
            <Text style={styles.totalValue}>
              R$ {totalFuncionarios?.total_geral_pago?.toFixed(2) || '0.00'}
            </Text>
          </Card.Content>
        </Card>

        <Text style={styles.sectionTitle}>Ações Rápidas</Text>
        
        <View style={styles.actionsGrid}>
          <Button
            mode="contained"
            icon="account-plus"
            onPress={() => router.push('/(drawer)/cadastro')}
            style={styles.actionButton}
            buttonColor={colors.primary}
            textColor={colors.black}
          >
            Cadastrar
          </Button>
          
          <Button
            mode="contained"
            icon="calendar-edit"
            onPress={() => router.push('/(drawer)/registro')}
            style={styles.actionButton}
            buttonColor={colors.info}
            textColor={colors.white}
          >
            Registro
          </Button>
          
          <Button
            mode="contained"
            icon="email-send"
            onPress={() => router.push('/(drawer)/relatorio')}
            style={styles.actionButton}
            buttonColor={colors.secondary}
            textColor={colors.white}
          >
            E-mail
          </Button>
          
          <Button
            mode="contained"
            icon="chart-bar"
            onPress={() => router.push('/(drawer)/historico')}
            style={styles.actionButton}
            buttonColor={colors.success}
            textColor={colors.white}
          >
            Histórico
          </Button>
        </View>

        {ranking && ranking.length > 0 && (
          <>
            <Text style={styles.sectionTitle}>Top 5 - Ranking</Text>
            
            {ranking.slice(0, 5).map((item, index) => (
              <Card key={index} style={styles.rankingCard}>
                <Card.Content style={styles.rankingContent}>
                  <View style={styles.rankingPosition}>
                    <Text style={styles.positionText}>#{item.posicao}</Text>
                  </View>
                  <View style={styles.rankingInfo}>
                    <Text style={styles.rankingName}>{item.nome}</Text>
                    <Text style={styles.rankingDetails}>
                      {item.dias_trabalhados} dias | R$ {item.total_recebido.toFixed(2)}
                    </Text>
                  </View>
                </Card.Content>
              </Card>
            ))}
          </>
        )}

        {isSyncing && (
          <Chip style={styles.syncingChip} textStyle={styles.syncingText}>
            Sincronizando...
          </Chip>
        )}
      </ScrollView>
      <BottomBar />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    padding: spacing.md,
    paddingBottom: 100,
  },
  welcomeCard: {
    backgroundColor: colors.primary,
    marginBottom: spacing.lg,
  },
  welcomeTitle: {
    fontSize: fontSize.xxl,
    fontWeight: 'bold',
    color: colors.black,
  },
  welcomeSubtitle: {
    fontSize: fontSize.md,
    color: colors.black,
    opacity: 0.8,
  },
  sectionTitle: {
    fontSize: fontSize.lg,
    fontWeight: 'bold',
    color: colors.primary,
    marginBottom: spacing.md,
    marginTop: spacing.md,
  },
  statsGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  statsRow: {
    flexDirection: 'row',
    marginTop: spacing.md,
  },
  statCard: {
    backgroundColor: colors.surface,
    flex: 1,
    marginHorizontal: spacing.xs,
  },
  statValue: {
    fontSize: fontSize.xxl,
    fontWeight: 'bold',
    color: colors.primary,
    textAlign: 'center',
  },
  statLabel: {
    fontSize: fontSize.sm,
    color: colors.textSecondary,
    textAlign: 'center',
  },
  totalCard: {
    backgroundColor: colors.card,
    marginTop: spacing.md,
  },
  totalLabel: {
    fontSize: fontSize.md,
    color: colors.textSecondary,
    textAlign: 'center',
  },
  totalValue: {
    fontSize: fontSize.title,
    fontWeight: 'bold',
    color: colors.primary,
    textAlign: 'center',
  },
  actionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  actionButton: {
    width: '48%',
    marginBottom: spacing.md,
  },
  rankingCard: {
    backgroundColor: colors.surface,
    marginBottom: spacing.sm,
  },
  rankingContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  rankingPosition: {
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: colors.primary,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: spacing.md,
  },
  positionText: {
    fontSize: fontSize.lg,
    fontWeight: 'bold',
    color: colors.black,
  },
  rankingInfo: {
    flex: 1,
  },
  rankingName: {
    fontSize: fontSize.lg,
    fontWeight: 'bold',
    color: colors.text,
  },
  rankingDetails: {
    fontSize: fontSize.sm,
    color: colors.textSecondary,
  },
  syncingChip: {
    marginTop: spacing.md,
    alignSelf: 'center',
    backgroundColor: colors.warning,
  },
  syncingText: {
    color: colors.black,
  },
});
