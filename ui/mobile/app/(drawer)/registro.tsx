import React, { useState, useEffect } from 'react';
import { View, StyleSheet, ScrollView, Alert } from 'react-native';
import { Text, TextInput, Button, Card, SegmentedButtons, Switch, List, Divider } from 'react-native-paper';
import DateTimePicker from '@react-native-community/datetimepicker';
import { colors, spacing, fontSize, DIAS_SEMANA } from '../../src/constants/theme';
import { useAppStore } from '../../src/store/useAppStore';
import { Funcionario } from '../../src/types';
import * as api from '../../src/services/supabase';
import BottomBar from '../../src/components/BottomBar';

export default function RegistroScreen() {
  const { nomesFuncionarios, loadNomesFuncionarios, addFuncionario, updateFuncionario, deleteFuncionario, loadFuncionarios } = useAppStore();
  
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [showDatePicker, setShowDatePicker] = useState(false);
  const [selectedFuncionario, setSelectedFuncionario] = useState('');
  const [valor10, setValor10] = useState('');
  const [horaEntrada, setHoraEntrada] = useState('08:00');
  const [horaSaida, setHoraSaida] = useState('16:00');
  const [vale, setVale] = useState('');
  const [tipoVale, setTipoVale] = useState<'pix' | 'dinheiro'>('pix');
  const [pago, setPago] = useState(false);
  const [observacao, setObservacao] = useState('');
  const [loading, setLoading] = useState(false);
  const [registrosDoDia, setRegistrosDoDia] = useState<Funcionario[]>([]);

  useEffect(() => {
    loadNomesFuncionarios();
    loadRegistrosDoDia();
  }, []);

  useEffect(() => {
    loadRegistrosDoDia();
  }, [selectedDate]);

  const loadRegistrosDoDia = async () => {
    try {
      const data = await api.listarFuncionarios(selectedDate.toISOString().split('T')[0]);
      setRegistrosDoDia(data);
    } catch (error) {
      console.log('Erro ao carregar registros:', error);
    }
  };

  const handleDateChange = (event: any, date?: Date) => {
    setShowDatePicker(false);
    if (date) {
      setSelectedDate(date);
    }
  };

  const handleSalvar = async () => {
    if (!selectedFuncionario) {
      Alert.alert('Erro', 'Selecione um funcionário');
      return;
    }

    const valor = parseFloat(valor10);
    if (isNaN(valor) || valor <= 0) {
      Alert.alert('Erro', 'Informe o valor de 10% das vendas');
      return;
    }

    setLoading(true);
    try {
      const diaTrabalho = selectedDate.toISOString().split('T')[0];
      
      const existente = await api.buscarFuncionarioPorNomeEData(selectedFuncionario, diaTrabalho);
      
      if (existente) {
        await updateFuncionario({
          ...existente,
          valor_10_percent: valor,
          hora_entrada: horaEntrada,
          hora_saida: horaSaida,
          vale: vale ? parseFloat(vale) : undefined,
          tipo_vale: vale ? tipoVale : undefined,
          tipo_pagamento: tipoVale,
          pago,
          observacao,
        });
        Alert.alert('Sucesso', 'Registro atualizado!');
      } else {
        const func: Funcionario = {
          nome: selectedFuncionario,
          valor_10_percent: valor,
          hora_entrada: horaEntrada,
          hora_saida: horaSaida,
          dia_trabalho: diaTrabalho,
          vale: vale ? parseFloat(vale) : undefined,
          tipo_vale: vale ? tipoVale : undefined,
          tipo_pagamento: tipoVale,
          pago,
          observacao,
        };
        
        await addFuncionario(func);
        Alert.alert('Sucesso', 'Registro salvo!');
      }
      
      await loadRegistrosDoDia();
      limparCampos();
    } catch (error: any) {
      Alert.alert('Erro', error.message || 'Erro ao salvar');
    } finally {
      setLoading(false);
    }
  };

  const limparCampos = () => {
    setValor10('');
    setHoraEntrada('08:00');
    setHoraSaida('16:00');
    setVale('');
    setPago(false);
    setObservacao('');
  };

  const handleDeletar = (id: string) => {
    Alert.alert(
      'Confirmar',
      'Deseja deletar este registro?',
      [
        { text: 'Cancelar', style: 'cancel' },
        { 
          text: 'Deletar', 
          style: 'destructive',
          onPress: async () => {
            try {
              await deleteFuncionario(id);
              await loadRegistrosDoDia();
              Alert.alert('Sucesso', 'Registro deletado!');
            } catch (error: any) {
              Alert.alert('Erro', error.message || 'Erro ao deletar');
            }
          }
        },
      ]
    );
  };

  const handleSelectRegistro = (func: Funcionario) => {
    setSelectedFuncionario(func.nome);
    setValor10(func.valor_10_percent.toString());
    setHoraEntrada(func.hora_entrada);
    setHoraSaida(func.hora_saida);
    setVale(func.vale?.toString() || '');
    setTipoVale(func.tipo_vale || 'pix');
    setPago(func.pago);
    setObservacao(func.observacao || '');
  };

  const totalDia = registrosDoDia.reduce((acc, func) => acc + func.valor_10_percent, 0);

  return (
    <>
    <View style={styles.container}>
      <ScrollView style={styles.scrollView} contentContainerStyle={styles.scrollContent}>
        <Card style={styles.card}>
          <Card.Content>
            <Text style={styles.sectionTitle}>Data do Trabalho</Text>
            
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
            <Text style={styles.sectionTitle}>Dados do Funcionário</Text>
            
            <View style={styles.pickerContainer}>
              <ScrollView horizontal showsHorizontalScrollIndicator={false}>
                {nomesFuncionarios.map((nome) => (
                  <Button
                    key={nome}
                    mode={selectedFuncionario === nome ? 'contained' : 'outlined'}
                    onPress={() => setSelectedFuncionario(nome)}
                    style={styles.nameChip}
                    buttonColor={selectedFuncionario === nome ? colors.primary : 'transparent'}
                    textColor={selectedFuncionario === nome ? colors.black : colors.primary}
                  >
                    {nome}
                  </Button>
                ))}
              </ScrollView>
            </View>

            <TextInput
              label="10% das Vendas (R$)"
              value={valor10}
              onChangeText={setValor10}
              mode="outlined"
              keyboardType="numeric"
              style={styles.input}
              outlineColor={colors.border}
              activeOutlineColor={colors.primary}
              textColor={colors.text}
            />

            <View style={styles.row}>
              <TextInput
                label="Entrada"
                value={horaEntrada}
                onChangeText={setHoraEntrada}
                mode="outlined"
                style={[styles.input, { flex: 1, marginRight: spacing.sm }]}
                outlineColor={colors.border}
                activeOutlineColor={colors.primary}
                textColor={colors.text}
                placeholder="08:00"
              />
              <TextInput
                label="Saída"
                value={horaSaida}
                onChangeText={setHoraSaida}
                mode="outlined"
                style={[styles.input, { flex: 1, marginLeft: spacing.sm }]}
                outlineColor={colors.border}
                activeOutlineColor={colors.primary}
                textColor={colors.text}
                placeholder="16:00"
              />
            </View>

            <Text style={styles.sectionSubTitle}>Vale (Opcional)</Text>
            
            <View style={styles.row}>
              <TextInput
                label="Valor do Vale"
                value={vale}
                onChangeText={setVale}
                mode="outlined"
                keyboardType="numeric"
                style={[styles.input, { flex: 1, marginRight: spacing.sm }]}
                outlineColor={colors.border}
                activeOutlineColor={colors.primary}
                textColor={colors.text}
              />
              <SegmentedButtons
                value={tipoVale}
                onValueChange={(value) => setTipoVale(value as 'pix' | 'dinheiro')}
                buttons={[
                  { value: 'pix', label: 'PIX' },
                  { value: 'dinheiro', label: 'Dinheiro' },
                ]}
                style={styles.segmented}
              />
            </View>

            <View style={styles.switchRow}>
              <Text style={styles.switchLabel}>Salário Pago</Text>
              <Switch
                value={pago}
                onValueChange={setPago}
                color={colors.success}
              />
            </View>

            <TextInput
              label="Observação"
              value={observacao}
              onChangeText={setObservacao}
              mode="outlined"
              multiline
              numberOfLines={3}
              style={styles.input}
              outlineColor={colors.border}
              activeOutlineColor={colors.primary}
              textColor={colors.text}
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
              Salvar Registro
            </Button>
          </Card.Content>
        </Card>

        <Card style={styles.totalCard}>
          <Card.Content style={styles.totalContent}>
            <Text style={styles.totalLabel}>Total do Dia</Text>
            <Text style={styles.totalValue}>R$ {totalDia.toFixed(2)}</Text>
          </Card.Content>
        </Card>

        <Text style={styles.sectionTitle}>Registros do Dia ({registrosDoDia.length})</Text>

        {registrosDoDia.length === 0 ? (
          <Card style={styles.card}>
            <Card.Content>
              <Text style={styles.emptyText}>Nenhum registro para esta data</Text>
            </Card.Content>
          </Card>
        ) : (
          <Card style={styles.card}>
            {registrosDoDia.map((func, index) => (
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
                  right={props => (
                    <View style={styles.listActions}>
                      <Button
                        mode="text"
                        onPress={() => func.id && handleDeletar(func.id)}
                        textColor={colors.error}
                      >
                        Deletar
                      </Button>
                    </View>
                  )}
                  onPress={() => handleSelectRegistro(func)}
                  titleStyle={styles.listTitle}
                  descriptionStyle={styles.listDescription}
                />
                {index < registrosDoDia.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </Card>
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
  sectionSubTitle: {
    fontSize: fontSize.md,
    fontWeight: 'bold',
    color: colors.textSecondary,
    marginTop: spacing.md,
    marginBottom: spacing.sm,
  },
  dateButton: {
    marginBottom: spacing.md,
  },
  pickerContainer: {
    marginBottom: spacing.md,
  },
  nameChip: {
    marginRight: spacing.sm,
    marginBottom: spacing.sm,
  },
  input: {
    marginBottom: spacing.md,
    backgroundColor: colors.card,
  },
  row: {
    flexDirection: 'row',
    marginBottom: spacing.md,
  },
  segmented: {
    flex: 1,
  },
  switchRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.md,
    paddingVertical: spacing.sm,
  },
  switchLabel: {
    fontSize: fontSize.md,
    color: colors.text,
  },
  button: {
    marginTop: spacing.md,
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
  listActions: {
    justifyContent: 'center',
  },
});
