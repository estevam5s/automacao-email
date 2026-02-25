import React, { useState, useEffect } from 'react';
import { View, StyleSheet, ScrollView, Alert } from 'react-native';
import { Text, Card, Button, SegmentedButtons, Chip, List, Divider } from 'react-native-paper';
import { colors, spacing, fontSize } from '../../src/constants/theme';
import { useAppStore } from '../../src/store/useAppStore';
import * as api from '../../src/services/supabase';
import { Log } from '../../src/types';

export default function LogsScreen() {
  const { logs, loadLogs, clearLogs } = useAppStore();
  
  const [filterAcao, setFilterAcao] = useState('Todos');
  const [filterTabela, setFilterTabela] = useState('Todas');
  const [loading, setLoading] = useState(false);
  const [filteredLogs, setFilteredLogs] = useState<Log[]>([]);

  useEffect(() => {
    loadLogs();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [logs, filterAcao, filterTabela]);

  const applyFilters = () => {
    let filtered = [...logs];
    
    if (filterAcao !== 'Todos') {
      filtered = filtered.filter(log => log.acao === filterAcao);
    }
    
    if (filterTabela !== 'Todas') {
      filtered = filtered.filter(log => log.tabela === filterTabela);
    }
    
    setFilteredLogs(filtered);
  };

  const handleAtualizar = async () => {
    setLoading(true);
    try {
      await loadLogs();
    } finally {
      setLoading(false);
    }
  };

  const handleLimpar = () => {
    Alert.alert(
      'Confirmar',
      'Deseja limpar TODOS os logs? Esta ação não pode ser desfeita.',
      [
        { text: 'Cancelar', style: 'cancel' },
        {
          text: 'Limpar',
          style: 'destructive',
          onPress: async () => {
            try {
              await clearLogs();
              Alert.alert('Sucesso', 'Logs limpos!');
            } catch (error: any) {
              Alert.alert('Erro', error.message || 'Erro ao limpar');
            }
          }
        },
      ]
    );
  };

  const getAcaoIcon = (acao: string) => {
    switch (acao) {
      case 'CRIAR': return 'plus-circle';
      case 'ATUALIZAR': return 'pencil';
      case 'DELETAR': return 'delete';
      case 'VISUALIZAR': return 'eye';
      case 'ENVIAR_EMAIL': return 'email-send';
      default: return 'information';
    }
  };

  const getAcaoColor = (acao: string) => {
    switch (acao) {
      case 'CRIAR': return colors.success;
      case 'ATUALIZAR': return colors.warning;
      case 'DELETAR': return colors.error;
      case 'VISUALIZAR': return colors.info;
      case 'ENVIAR_EMAIL': return colors.secondary;
      default: return colors.textSecondary;
    }
  };

  const formatDate = (dateStr?: string) => {
    if (!dateStr) return '-';
    const date = new Date(dateStr);
    return date.toLocaleString('pt-BR');
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.content}>
        <View style={styles.filtersRow}>
          <SegmentedButtons
            value={filterAcao}
            onValueChange={setFilterAcao}
            buttons={[
              { value: 'Todos', label: 'Todos' },
              { value: 'CRIAR', label: 'Criar' },
              { value: 'ATUALIZAR', label: 'Atualizar' },
              { value: 'DELETAR', label: 'Deletar' },
            ]}
            style={styles.segmented}
          />
        </View>

        <View style={styles.filtersRow}>
          <SegmentedButtons
            value={filterTabela}
            onValueChange={setFilterTabela}
            buttons={[
              { value: 'Todas', label: 'Todas' },
              { value: 'funcionarios', label: 'Func.' },
              { value: 'configuracoes', label: 'Config.' },
            ]}
            style={styles.segmented}
          />
        </View>

        <View style={styles.actionsRow}>
          <Button
            mode="contained"
            onPress={handleAtualizar}
            loading={loading}
            style={styles.actionButton}
            buttonColor={colors.info}
            icon="refresh"
          >
            Atualizar
          </Button>
          
          <Button
            mode="outlined"
            onPress={handleLimpar}
            style={styles.actionButton}
            textColor={colors.error}
            icon="delete"
          >
            Limpar
          </Button>
        </View>

        <Text style={styles.sectionTitle}>
          Logs ({filteredLogs.length})
        </Text>

        {filteredLogs.length === 0 ? (
          <Card style={styles.card}>
            <Card.Content>
              <Text style={styles.emptyText}>Nenhum log encontrado</Text>
            </Card.Content>
          </Card>
        ) : (
          filteredLogs.map((log, index) => (
            <Card key={log.id || index} style={styles.card}>
              <Card.Content>
                <View style={styles.logHeader}>
                  <View style={styles.logAcao}>
                    <Chip
                      icon={getAcaoIcon(log.acao)}
                      style={[styles.acaoChip, { backgroundColor: getAcaoColor(log.acao) }]}
                      textStyle={styles.acaoChipText}
                    >
                      {log.acao}
                    </Chip>
                  </View>
                  <Text style={styles.logTabela}>{log.tabela}</Text>
                </View>
                
                <View style={styles.logDetails}>
                  <Text style={styles.logLabel}>Data:</Text>
                  <Text style={styles.logValue}>{formatDate(log.created_at)}</Text>
                </View>
                
                <View style={styles.logDetails}>
                  <Text style={styles.logLabel}>Usuário:</Text>
                  <Text style={styles.logValue}>{log.usuario}</Text>
                </View>
                
                {log.registro_id && (
                  <View style={styles.logDetails}>
                    <Text style={styles.logLabel}>ID:</Text>
                    <Text style={styles.logValue} numberOfLines={1}>
                      {log.registro_id.substring(0, 8)}...
                    </Text>
                  </View>
                )}
              </Card.Content>
            </Card>
          ))
        )}
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
  filtersRow: {
    marginBottom: spacing.md,
  },
  segmented: {
    backgroundColor: colors.surface,
  },
  actionsRow: {
    flexDirection: 'row',
    marginBottom: spacing.lg,
  },
  actionButton: {
    flex: 1,
    marginHorizontal: spacing.xs,
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
  logHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.sm,
  },
  logAcao: {
    flexDirection: 'row',
  },
  acaoChip: {
    height: 28,
  },
  acaoChipText: {
    fontSize: fontSize.xs,
    color: colors.white,
    fontWeight: 'bold',
  },
  logTabela: {
    fontSize: fontSize.sm,
    color: colors.textSecondary,
    fontWeight: 'bold',
  },
  logDetails: {
    flexDirection: 'row',
    marginBottom: spacing.xs,
  },
  logLabel: {
    fontSize: fontSize.sm,
    color: colors.textSecondary,
    marginRight: spacing.sm,
    width: 60,
  },
  logValue: {
    fontSize: fontSize.sm,
    color: colors.text,
    flex: 1,
  },
  emptyText: {
    textAlign: 'center',
    color: colors.textSecondary,
  },
});
