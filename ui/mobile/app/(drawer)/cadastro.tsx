import React, { useState, useEffect } from 'react';
import { View, StyleSheet, ScrollView, Alert } from 'react-native';
import { Text, TextInput, Button, Card, List, IconButton, Divider } from 'react-native-paper';
import { colors, spacing, fontSize } from '../../src/constants/theme';
import { useAppStore } from '../../src/store/useAppStore';
import { Funcionario } from '../../src/types';

export default function CadastroScreen() {
  const { nomesFuncionarios, loadNomesFuncionarios, addFuncionario, deleteFuncionario } = useAppStore();
  
  const [nome, setNome] = useState('');
  const [loading, setLoading] = useState(false);
  const [funcionarios, setFuncionarios] = useState<string[]>([]);

  useEffect(() => {
    loadNomesFuncionarios();
  }, []);

  useEffect(() => {
    setFuncionarios(nomesFuncionarios);
  }, [nomesFuncionarios]);

  const handleCadastrar = async () => {
    if (!nome.trim()) {
      Alert.alert('Erro', 'Por favor, digite o nome do funcionário');
      return;
    }

    setLoading(true);
    try {
      const func: Funcionario = {
        nome: nome.trim(),
        valor_10_percent: 0,
        hora_entrada: '08:00',
        hora_saida: '16:00',
        dia_trabalho: new Date().toISOString().split('T')[0],
        pago: false,
      };
      
      await addFuncionario(func);
      Alert.alert('Sucesso', `${nome} cadastrado!`);
      setNome('');
      await loadNomesFuncionarios();
    } catch (error: any) {
      Alert.alert('Erro', error.message || 'Erro ao cadastrar');
    } finally {
      setLoading(false);
    }
  };

  const handleDeletar = (nomeFunc: string) => {
    Alert.alert(
      'Confirmar',
      `Deseja deletar ${nomeFunc}?`,
      [
        { text: 'Cancelar', style: 'cancel' },
        { 
          text: 'Deletar', 
          style: 'destructive',
          onPress: async () => {
            try {
              const funcs = useAppStore.getState().funcionarios;
              const funcToDelete = funcs.find(f => f.nome === nomeFunc);
              if (funcToDelete?.id) {
                await deleteFuncionario(funcToDelete.id);
                await loadNomesFuncionarios();
                Alert.alert('Sucesso', 'Funcionário deletado!');
              }
            } catch (error: any) {
              Alert.alert('Erro', error.message || 'Erro ao deletar');
            }
          }
        },
      ]
    );
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.content}>
        <Card style={styles.card}>
          <Card.Content>
            <Text style={styles.title}>Novo Funcionário</Text>
            
            <TextInput
              label="Nome do Funcionário"
              value={nome}
              onChangeText={setNome}
              mode="outlined"
              style={styles.input}
              outlineColor={colors.border}
              activeOutlineColor={colors.primary}
              textColor={colors.text}
            />
            
            <Button
              mode="contained"
              onPress={handleCadastrar}
              loading={loading}
              disabled={loading}
              style={styles.button}
              buttonColor={colors.primary}
              textColor={colors.black}
            >
              Cadastrar
            </Button>
          </Card.Content>
        </Card>

        <Text style={styles.sectionTitle}>
          Funcionários Cadastrados ({funcionarios.length})
        </Text>

        {funcionarios.length === 0 ? (
          <Card style={styles.emptyCard}>
            <Card.Content>
              <Text style={styles.emptyText}>
                Nenhum funcionário cadastrado
              </Text>
            </Card.Content>
          </Card>
        ) : (
          <Card style={styles.card}>
            {funcionarios.map((nomeFunc, index) => (
              <React.Fragment key={nomeFunc}>
                <List.Item
                  title={nomeFunc}
                  left={props => <List.Icon {...props} icon="account" color={colors.primary} />}
                  right={props => (
                    <IconButton
                      icon="delete"
                      iconColor={colors.error}
                      onPress={() => handleDeletar(nomeFunc)}
                    />
                  )}
                  titleStyle={styles.listTitle}
                />
                {index < funcionarios.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </Card>
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
  card: {
    backgroundColor: colors.surface,
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
    marginTop: spacing.sm,
  },
  sectionTitle: {
    fontSize: fontSize.lg,
    fontWeight: 'bold',
    color: colors.primary,
    marginBottom: spacing.md,
    marginTop: spacing.md,
  },
  emptyCard: {
    backgroundColor: colors.surface,
  },
  emptyText: {
    textAlign: 'center',
    color: colors.textSecondary,
    fontSize: fontSize.md,
  },
  listTitle: {
    color: colors.text,
  },
});
