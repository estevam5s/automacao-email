import React, { useState, useEffect } from 'react';
import { View, StyleSheet, ScrollView, Alert } from 'react-native';
import { Text, TextInput, Button, Card, List, Divider, DataTable } from 'react-native-paper';
import DateTimePicker from '@react-native-community/datetimepicker';
import * as MailComposer from 'expo-mail-composer';
import { colors, spacing, fontSize, DIAS_SEMANA } from '../../src/constants/theme';
import { Funcionario, ObservacaoGeral } from '../../src/types';
import * as api from '../../src/services/supabase';
import { useAppStore } from '../../src/store/useAppStore';

export default function RelatorioScreen() {
  const { configuracao, loadConfiguracao } = useAppStore();
  
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [showDatePicker, setShowDatePicker] = useState(false);
  const [funcionariosDoDia, setFuncionariosDoDia] = useState<Funcionario[]>([]);
  const [observacaoGeral, setObservacaoGeral] = useState('');
  const [loading, setLoading] = useState(false);
  const [emailDestinatario, setEmailDestinatario] = useState('');

  useEffect(() => {
    loadConfiguracao();
    loadDadosDoDia();
  }, []);

  useEffect(() => {
    loadDadosDoDia();
  }, [selectedDate]);

  useEffect(() => {
    if (configuracao?.email_destinatario) {
      setEmailDestinatario(configuracao.email_destinatario);
    }
  }, [configuracao]);

  const loadDadosDoDia = async () => {
    try {
      const data = await api.listarFuncionarios(selectedDate.toISOString().split('T')[0]);
      setFuncionariosDoDia(data);
      
      const obs = await api.getObservacaoGeral(selectedDate.toISOString().split('T')[0]);
      if (obs) {
        setObservacaoGeral(obs.observacao);
      }
    } catch (error) {
      console.log('Erro ao carregar dados:', error);
    }
  };

  const handleDateChange = (event: any, date?: Date) => {
    setShowDatePicker(false);
    if (date) {
      setSelectedDate(date);
    }
  };

  const handleSalvarObservacao = async () => {
    setLoading(true);
    try {
      const obs: ObservacaoGeral = {
        dia_trabalho: selectedDate.toISOString().split('T')[0],
        observacao: observacaoGeral,
      };
      await api.salvarObservacaoGeral(obs);
      Alert.alert('Sucesso', 'Observação salva!');
    } catch (error: any) {
      Alert.alert('Erro', error.message || 'Erro ao salvar');
    } finally {
      setLoading(false);
    }
  };

  const handleEnviarEmail = async () => {
    if (!emailDestinatario) {
      Alert.alert('Erro', 'Informe o e-mail do destinatário');
      return;
    }

    if (funcionariosDoDia.length === 0) {
      Alert.alert('Erro', 'Nenhum funcionário para enviar');
      return;
    }

    setLoading(true);
    try {
      const diaSemana = DIAS_SEMANA[selectedDate.getDay()];
      const dataFormatada = selectedDate.toLocaleDateString('pt-BR');
      
      let htmlContent = `
        <h2>Relatório de Salários - ${dataFormatada}</h2>
        <p><strong>Dia:</strong> ${diaSemana}</p>
        <p><strong>Total de Funcionários:</strong> ${funcionariosDoDia.length}</p>
        <p><strong>Total a Pagar:</strong> R$ ${totalDia.toFixed(2)}</p>
        ${observacaoGeral ? `<p><strong>Observação:</strong> ${observacaoGeral}</p>` : ''}
        <table border="1" cellpadding="5" style="border-collapse: collapse; width: 100%;">
          <tr style="background-color: #00d4ff;">
            <th>Nome</th>
            <th>10% Vendas</th>
            <th>Entrada</th>
            <th>Saída</th>
            <th>Vale</th>
            <th>Pago</th>
          </tr>
      `;

      funcionariosDoDia.forEach(func => {
        htmlContent += `
          <tr>
            <td>${func.nome}</td>
            <td>R$ ${func.valor_10_percent.toFixed(2)}</td>
            <td>${func.hora_entrada}</td>
            <td>${func.hora_saida}</td>
            <td>${func.vale ? 'R$ ' + func.vale.toFixed(2) : '-'}</td>
            <td>${func.pago ? 'Sim' : 'Não'}</td>
          </tr>
        `;
      });

      htmlContent += '</table>';

      const isAvailable = await MailComposer.isAvailableAsync();
      
      if (isAvailable) {
        await MailComposer.composeAsync({
          recipients: [emailDestinatario],
          subject: `Relatório de Salários - ${dataFormatada}`,
          body: htmlContent,
          isHtml: true,
        });
        Alert.alert('Sucesso', 'E-mail aberto para envio!');
      } else {
        Alert.alert('Erro', 'E-mail não disponível neste dispositivo');
      }
    } catch (error: any) {
      Alert.alert('Erro', error.message || 'Erro ao enviar');
    } finally {
      setLoading(false);
    }
  };

  const handleGerarRelatorio = () => {
    if (funcionariosDoDia.length === 0) {
      Alert.alert('Erro', 'Nenhum funcionário para gerar relatório');
      return;
    }

    const diaSemana = DIAS_SEMANA[selectedDate.getDay()];
    const dataFormatada = selectedDate.toLocaleDateString('pt-BR');
    
    let relatorio = `RELATÓRIO DE SALÁRIOS - ${dataFormatada}\n`;
    relatorio += `${'='.repeat(40)}\n\n`;
    relatorio += `Dia: ${diaSemana}\n`;
    relatorio += `Total de Funcionários: ${funcionariosDoDia.length}\n`;
    relatorio += `Total a Pagar: R$ ${totalDia.toFixed(2)}\n`;
    
    if (observacaoGeral) {
      relatorio += `\nObservação: ${observacaoGeral}\n`;
    }
    
    relatorio += `\n${'─'.repeat(40)}\n`;
    relatorio += `FUNCIONÁRIOS:\n`;
    relatorio += `${'─'.repeat(40)}\n\n`;

    funcionariosDoDia.forEach((func, index) => {
      relatorio += `${index + 1}. ${func.nome}\n`;
      relatorio += `   10% das Vendas: R$ ${func.valor_10_percent.toFixed(2)}\n`;
      relatorio += `   Horário: ${func.hora_entrada} - ${func.hora_saida}\n`;
      relatorio += `   Vale: ${func.vale ? 'R$ ' + func.vale.toFixed(2) : 'Nenhum'}\n`;
      relatorio += `   Pago: ${func.pago ? 'Sim' : 'Não'}\n`;
      if (func.observacao) {
        relatorio += `   Obs: ${func.observacao}\n`;
      }
      relatorio += '\n';
    });

    Alert.alert('Relatório Gerado', 'O relatório foi gerado. Configure o e-mail para enviar.');
  };

  const totalDia = funcionariosDoDia.reduce((acc, func) => acc + func.valor_10_percent, 0);

  return (
    <ScrollView style={styles.container}>
      <View style={styles.content}>
        <Card style={styles.card}>
          <Card.Content>
            <Text style={styles.sectionTitle}>Selecionar Data</Text>
            
            <Button
              mode="outlined"
              onPress={() => setShowDatePicker(true)}
              style={styles.dateButton}
              textColor={colors.primary}
            >
              {selectedDate.toLocaleDateString('pt-BR')} ({DIAS_SEMANA[selectedDate.getDay()]})
            </Button>

            {showDatePicker && (
              <DateTimePicker
                value={selectedDate}
                mode="date"
                onChange={handleDateChange}
              />
            )}
          </Card.Content>
        </Card>

        <Card style={styles.card}>
          <Card.Content>
            <Text style={styles.sectionTitle}>Observação Geral do Dia</Text>
            
            <TextInput
              value={observacaoGeral}
              onChangeText={setObservacaoGeral}
              mode="outlined"
              multiline
              numberOfLines={4}
              style={styles.input}
              outlineColor={colors.border}
              activeOutlineColor={colors.primary}
              textColor={colors.text}
              placeholder="Adicione observações gerais sobre o dia..."
            />
            
            <Button
              mode="contained"
              onPress={handleSalvarObservacao}
              loading={loading}
              disabled={loading}
              style={styles.button}
              buttonColor={colors.success}
            >
              Salvar Observação
            </Button>
          </Card.Content>
        </Card>

        <Card style={styles.totalCard}>
          <Card.Content style={styles.totalContent}>
            <View>
              <Text style={styles.totalLabel}>Total do Dia</Text>
              <Text style={styles.totalSubLabel}>{funcionariosDoDia.length} funcionários</Text>
            </View>
            <Text style={styles.totalValue}>R$ {totalDia.toFixed(2)}</Text>
          </Card.Content>
        </Card>

        <Text style={styles.sectionTitle}>Funcionários do Dia</Text>

        {funcionariosDoDia.length === 0 ? (
          <Card style={styles.card}>
            <Card.Content>
              <Text style={styles.emptyText}>Nenhum registro para esta data</Text>
            </Card.Content>
          </Card>
        ) : (
          <Card style={styles.card}>
            {funcionariosDoDia.map((func, index) => (
              <React.Fragment key={func.id || index}>
                <List.Item
                  title={func.nome}
                  description={`10%: R$ ${func.valor_10_percent.toFixed(2)} | ${func.hora_entrada} - ${func.hora_saida}`}
                  left={props => (
                    <List.Icon 
                      {...props} 
                      icon={func.pago ? 'check-circle' : 'clock-outline'} 
                      color={func.pago ? colors.success : colors.warning} 
                    />
                  )}
                  titleStyle={styles.listTitle}
                  descriptionStyle={styles.listDescription}
                />
                {index < funcionariosDoDia.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </Card>
        )}

        <Card style={styles.card}>
          <Card.Content>
            <Text style={styles.sectionTitle}>Enviar E-mail</Text>
            
            <TextInput
              label="E-mail do Destinatário"
              value={emailDestinatario}
              onChangeText={setEmailDestinatario}
              mode="outlined"
              keyboardType="email-address"
              autoCapitalize="none"
              style={styles.input}
              outlineColor={colors.border}
              activeOutlineColor={colors.primary}
              textColor={colors.text}
            />
            
            <Button
              mode="contained"
              onPress={handleEnviarEmail}
              loading={loading}
              disabled={loading}
              style={styles.button}
              buttonColor={colors.info}
              icon="email-send"
            >
              Abrir E-mail
            </Button>

            <Button
              mode="outlined"
              onPress={handleGerarRelatorio}
              style={[styles.button, { marginTop: spacing.sm }]}
              textColor={colors.primary}
              icon="file-document"
            >
              Gerar Relatório
            </Button>
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
  sectionTitle: {
    fontSize: fontSize.lg,
    fontWeight: 'bold',
    color: colors.primary,
    marginBottom: spacing.md,
  },
  dateButton: {
    marginBottom: spacing.md,
  },
  input: {
    marginBottom: spacing.md,
    backgroundColor: colors.card,
  },
  button: {
    marginTop: spacing.sm,
  },
  totalCard: {
    backgroundColor: colors.card,
    marginBottom: spacing.md,
  },
  totalContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  totalLabel: {
    fontSize: fontSize.lg,
    color: colors.text,
    fontWeight: 'bold',
  },
  totalSubLabel: {
    fontSize: fontSize.sm,
    color: colors.textSecondary,
  },
  totalValue: {
    fontSize: fontSize.xxl,
    fontWeight: 'bold',
    color: colors.primary,
  },
  emptyText: {
    textAlign: 'center',
    color: colors.textSecondary,
  },
  listTitle: {
    color: colors.text,
  },
  listDescription: {
    color: colors.textSecondary,
  },
});
