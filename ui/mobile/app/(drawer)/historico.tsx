import React, { useState, useEffect } from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Text, Card, SegmentedButtons } from 'react-native-paper';
import { colors, spacing, fontSize } from '../../src/constants/theme';
import { useAppStore } from '../../src/store/useAppStore';
import * as api from '../../src/services/supabase';
import { RankingPagamento, HistoricoPresenca, HistoricoPagamento, DataCadastramento } from '../../src/types';
import BottomBar from '../../src/components/BottomBar';

export default function HistoricoScreen() {
  const { loadTotalFuncionarios, loadRanking, totalFuncionarios, ranking } = useAppStore();
  
  const [tab, setTab] = useState('ranking');
  const [historicoPresenca, setHistoricoPresenca] = useState<HistoricoPresenca[]>([]);
  const [historicoPagamentos, setHistoricoPagamentos] = useState<HistoricoPagamento[]>([]);
  const [dataCadastramento, setDataCadastramento] = useState<DataCadastramento[]>([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    await Promise.all([
      loadTotalFuncionarios(),
      loadRanking(),
    ]);
    await loadDadosTab(tab);
  };

  const loadDadosTab = async (tabName: string) => {
    if (tabName === 'presenca') {
      const data = await api.listarHistoricoPresenca();
      setHistoricoPresenca(data);
    } else if (tabName === 'pagamentos') {
      const data = await api.listarHistoricoPagamentos();
      setHistoricoPagamentos(data);
    } else if (tabName === 'cadastro') {
      const data = await api.listarDataCadastramento();
      setDataCadastramento(data);
    }
  };

  const handleTabChange = async (value: string) => {
    setTab(value);
    await loadDadosTab(value);
  };

  return (
    <>
    <View style={styles.container}>
      <ScrollView style={styles.scrollView} contentContainerStyle={styles.scrollContent}>
        <View style={styles.statsRow}>
          <Card style={[styles.statCard, { flex: 1, marginRight: spacing.sm }]}>
            <Card.Content>
              <Text style={styles.statValue}>{totalFuncionarios?.total_cadastrados || 0}</Text>
              <Text style={styles.statLabel}>Funcionários</Text>
            </Card.Content>
          </Card>
          
          <Card style={[styles.statCard, { flex: 1, marginLeft: spacing.sm }]}>
            <Card.Content>
              <Text style={styles.statValue}>{totalFuncionarios?.total_registros || 0}</Text>
              <Text style={styles.statLabel}>Registros</Text>
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

        <SegmentedButtons
          value={tab}
          onValueChange={handleTabChange}
          buttons={[
            { value: 'ranking', label: 'Ranking' },
            { value: 'presenca', label: 'Presença' },
            { value: 'pagamentos', label: 'Pagamentos' },
            { value: 'cadastro', label: 'Cadastro' },
          ]}
          style={styles.tabs}
        />

        {tab === 'ranking' && (
          <>
            <Text style={styles.sectionTitle}>🏆 Ranking de Pagamentos</Text>
            
            {ranking && ranking.length > 0 ? (
              ranking.map((item: RankingPagamento, index: number) => (
                <Card key={index} style={styles.card}>
                  <Card.Content style={styles.rankingContent}>
                    <View style={[styles.positionBadge, { 
                      backgroundColor: item.posicao <= 3 ? colors.primary : colors.card 
                    }]}>
                      <Text style={styles.positionText}>#{item.posicao}</Text>
                    </View>
                    <View style={styles.rankingInfo}>
                      <Text style={styles.rankingName}>{item.nome}</Text>
                      <Text style={styles.rankingDetails}>
                        {item.dias_trabalhados} dias trabalhados | Média: R$ {item.media_diaria.toFixed(2)}
                      </Text>
                    </View>
                    <View style={styles.rankingValues}>
                      <Text style={styles.rankingTotal}>R$ {item.total_recebido.toFixed(2)}</Text>
                      <Text style={styles.rankingPago}>
                        Pago: R$ {item.total_pago.toFixed(2)}
                      </Text>
                    </View>
                  </Card.Content>
                </Card>
              ))
            ) : (
              <Card style={styles.card}>
                <Card.Content>
                  <Text style={styles.emptyText}>Nenhum dado disponível</Text>
                </Card.Content>
              </Card>
            )}
          </>
        )}

        {tab === 'presenca' && (
          <>
            <Text style={styles.sectionTitle}>📅 Histórico de Presença</Text>
            
            {historicoPresenca.length > 0 ? (
              historicoPresenca.slice(0, 20).map((item, index) => (
                <Card key={index} style={styles.card}>
                  <Card.Content>
                    <View style={styles.presencaRow}>
                      <View style={styles.presencaDate}>
                        <Text style={styles.presencaDia}>{item.dia_formatado}</Text>
                      </View>
                      <View style={styles.presencaInfo}>
                        <Text style={styles.presencaName}>{item.nome}</Text>
                        <Text style={styles.presencaHora}>
                          {item.hora_entrada} - {item.hora_saida}
                        </Text>
                      </View>
                      <View style={styles.presencaValor}>
                        <Text style={styles.presencaValueText}>R$ {item.valor_10_percent.toFixed(2)}</Text>
                      </View>
                    </View>
                  </Card.Content>
                </Card>
              ))
            ) : (
              <Card style={styles.card}>
                <Card.Content>
                  <Text style={styles.emptyText}>Nenhum dado disponível</Text>
                </Card.Content>
              </Card>
            )}
          </>
        )}

        {tab === 'pagamentos' && (
          <>
            <Text style={styles.sectionTitle}>💵 Histórico de Pagamentos</Text>
            
            {historicoPagamentos.length > 0 ? (
              historicoPagamentos.slice(0, 20).map((item, index) => (
                <Card key={index} style={styles.card}>
                  <Card.Content>
                    <View style={styles.pagamentoRow}>
                      <View style={styles.pagamentoInfo}>
                        <Text style={styles.pagamentoName}>{item.nome}</Text>
                        <Text style={styles.pagamentoData}>{item.dia_trabalho}</Text>
                      </View>
                      <View style={styles.pagamentoValores}>
                        <Text style={styles.pagamentoValor}>R$ {item.valor_10_percent.toFixed(2)}</Text>
                        <Text style={[
                          styles.pagamentoStatus,
                          { color: item.pago ? colors.success : colors.warning }
                        ]}>
                          {item.status_pagamento}
                        </Text>
                      </View>
                    </View>
                  </Card.Content>
                </Card>
              ))
            ) : (
              <Card style={styles.card}>
                <Card.Content>
                  <Text style={styles.emptyText}>Nenhum dado disponível</Text>
                </Card.Content>
              </Card>
            )}
          </>
        )}

        {tab === 'cadastro' && (
          <>
            <Text style={styles.sectionTitle}>📋 Data de Cadastramento</Text>
            
            {dataCadastramento.length > 0 ? (
              dataCadastramento.map((item, index) => (
                <Card key={index} style={styles.card}>
                  <Card.Content>
                    <View style={styles.cadastroRow}>
                      <View style={styles.cadastroInfo}>
                        <Text style={styles.cadastroName}>{item.nome}</Text>
                        <Text style={styles.cadastroDias}>
                          Primeiro: {item.primeiro_dia_trabalho || '-'} | Último: {item.ultimo_dia_trabalho || '-'}
                        </Text>
                      </View>
                      <View style={styles.cadastroValores}>
                        <Text style={styles.cadastroDiasText}>{item.total_dias_trabalhados} dias</Text>
                        <Text style={styles.cadastroTotal}>R$ {item.total_recebido.toFixed(2)}</Text>
                      </View>
                    </View>
                  </Card.Content>
                </Card>
              ))
            ) : (
              <Card style={styles.card}>
                <Card.Content>
                  <Text style={styles.emptyText}>Nenhum dado disponível</Text>
                </Card.Content>
              </Card>
            )}
          </>
        )}
      </ScrollView>
    </View>
    <BottomBar />
    </>
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
  statsRow: {
    flexDirection: 'row',
    marginBottom: spacing.md,
  },
  statCard: {
    backgroundColor: colors.surface,
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
  tabs: {
    marginBottom: spacing.lg,
  },
  sectionTitle: {
    fontSize: fontSize.lg,
    fontWeight: 'bold',
    color: colors.primary,
    marginBottom: spacing.md,
  },
  card: {
    backgroundColor: colors.surface,
    marginBottom: spacing.sm,
  },
  rankingContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  positionBadge: {
    width: 45,
    height: 45,
    borderRadius: 22.5,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: spacing.md,
  },
  positionText: {
    fontSize: fontSize.md,
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
  rankingValues: {
    alignItems: 'flex-end',
  },
  rankingTotal: {
    fontSize: fontSize.lg,
    fontWeight: 'bold',
    color: colors.primary,
  },
  rankingPago: {
    fontSize: fontSize.sm,
    color: colors.success,
  },
  emptyText: {
    textAlign: 'center',
    color: colors.textSecondary,
  },
  presencaRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  presencaDate: {
    width: 70,
  },
  presencaDia: {
    fontSize: fontSize.sm,
    color: colors.primary,
    fontWeight: 'bold',
  },
  presencaInfo: {
    flex: 1,
  },
  presencaName: {
    fontSize: fontSize.md,
    color: colors.text,
    fontWeight: 'bold',
  },
  presencaHora: {
    fontSize: fontSize.sm,
    color: colors.textSecondary,
  },
  presencaValor: {
    alignItems: 'flex-end',
  },
  presencaValueText: {
    fontSize: fontSize.md,
    color: colors.primary,
    fontWeight: 'bold',
  },
  pagamentoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  pagamentoInfo: {
    flex: 1,
  },
  pagamentoName: {
    fontSize: fontSize.md,
    color: colors.text,
    fontWeight: 'bold',
  },
  pagamentoData: {
    fontSize: fontSize.sm,
    color: colors.textSecondary,
  },
  pagamentoValores: {
    alignItems: 'flex-end',
  },
  pagamentoValor: {
    fontSize: fontSize.md,
    color: colors.primary,
    fontWeight: 'bold',
  },
  pagamentoStatus: {
    fontSize: fontSize.sm,
  },
  cadastroRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  cadastroInfo: {
    flex: 1,
  },
  cadastroName: {
    fontSize: fontSize.md,
    color: colors.text,
    fontWeight: 'bold',
  },
  cadastroDias: {
    fontSize: fontSize.sm,
    color: colors.textSecondary,
  },
  cadastroValores: {
    alignItems: 'flex-end',
  },
  cadastroDiasText: {
    fontSize: fontSize.sm,
    color: colors.primary,
  },
  cadastroTotal: {
    fontSize: fontSize.md,
    color: colors.primary,
    fontWeight: 'bold',
  },
});
