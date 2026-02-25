import { createClient, SupabaseClient, Session } from '@supabase/supabase-js';
import * as SecureStore from 'expo-secure-store';
import { 
  Funcionario, 
  Configuracao, 
  ObservacaoGeral, 
  Log, 
  RegistroTrabalho,
  TotalFuncionarios,
  RankingPagamento,
  HistoricoPresenca,
  HistoricoPagamento,
  DataCadastramento
} from '../types';

const supabaseUrl = process.env.EXPO_PUBLIC_SUPABASE_URL || 'https://seu-projeto.supabase.co';
const supabaseAnonKey = process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY || 'sua-chave-anon';

class AsyncStorageAdapter {
  async getItem(key: string): Promise<string | null> {
    return await SecureStore.getItemAsync(key);
  }
  async setItem(key: string, value: string): Promise<void> {
    await SecureStore.setItemAsync(key, value);
  }
  async removeItem(key: string): Promise<void> {
    await SecureStore.deleteItemAsync(key);
  }
}

export const supabase: SupabaseClient = createClient(
  supabaseUrl,
  supabaseAnonKey,
  {
    auth: {
      storage: new AsyncStorageAdapter(),
      autoRefreshToken: true,
      persistSession: true,
    },
  }
);

export const getSession = async (): Promise<Session | null> => {
  const { data } = await supabase.auth.getSession();
  return data.session;
};

export const signIn = async (email: string, password: string) => {
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });
  if (error) throw error;
  return data;
};

export const signUp = async (email: string, password: string) => {
  const { data, error } = await supabase.auth.signUp({
    email,
    password,
  });
  if (error) throw error;
  return data;
};

export const signOut = async () => {
  const { error } = await supabase.auth.signOut();
  if (error) throw error;
};

export const resetPassword = async (email: string) => {
  const { error } = await supabase.auth.resetPasswordForEmail(email);
  if (error) throw error;
};

// ============ FUNCIONÁRIOS ============
export const cadastrarFuncionario = async (func: Funcionario): Promise<Funcionario> => {
  const { data, error } = await supabase
    .from('funcionarios')
    .insert(func)
    .select()
    .single();
  
  if (error) throw error;
  return data as Funcionario;
};

export const listarFuncionarios = async (diaTrabalho?: string): Promise<Funcionario[]> => {
  let query = supabase.from('funcionarios').select('*').order('nome');
  
  if (diaTrabalho) {
    query = query.eq('dia_trabalho', diaTrabalho);
  }
  
  const { data, error } = await query;
  if (error) throw error;
  return data as Funcionario[];
};

export const listarTodosFuncionarios = async (): Promise<Funcionario[]> => {
  const { data, error } = await supabase
    .from('funcionarios')
    .select('*')
    .order('nome');
  
  if (error) throw error;
  return data as Funcionario[];
};

export const atualizarFuncionario = async (func: Funcionario): Promise<Funcionario> => {
  const { data, error } = await supabase
    .from('funcionarios')
    .update(func)
    .eq('id', func.id)
    .select()
    .single();
  
  if (error) throw error;
  return data as Funcionario;
};

export const deletarFuncionario = async (id: string): Promise<boolean> => {
  const { error } = await supabase
    .from('funcionarios')
    .delete()
    .eq('id', id);
  
  if (error) throw error;
  return true;
};

export const buscarFuncionarioPorNomeEData = async (nome: string, diaTrabalho: string): Promise<Funcionario | null> => {
  const { data, error } = await supabase
    .from('funcionarios')
    .select('*')
    .eq('nome', nome)
    .eq('dia_trabalho', diaTrabalho)
    .single();
  
  if (error) return null;
  return data as Funcionario;
};

export const getNomesUnicosFuncionarios = async (): Promise<string[]> => {
  const { data, error } = await supabase
    .from('funcionarios')
    .select('nome');
  
  if (error) throw error;
  const nomesUnicos = [...new Set(data.map(item => item.nome))];
  return nomesUnicos;
};

// ============ CONFIGURAÇÕES ============
export const getConfiguracao = async (): Promise<Configuracao | null> => {
  const { data, error } = await supabase
    .from('configuracoes')
    .select('*')
    .limit(1)
    .single();
  
  if (error) return null;
  return data as Configuracao;
};

export const salvarConfiguracao = async (config: Configuracao): Promise<Configuracao> => {
  const existente = await getConfiguracao();
  
  let data;
  if (existente) {
    const { data: updateData, error } = await supabase
      .from('configuracoes')
      .update({
        email_destinatario: config.email_destinatario,
        email_remetente: config.email_remetente,
        senha_app: config.senha_app,
      })
      .eq('id', existente.id)
      .select()
      .single();
    
    if (error) throw error;
    data = updateData;
  } else {
    const { data: insertData, error } = await supabase
      .from('configuracoes')
      .insert(config)
      .select()
      .single();
    
    if (error) throw error;
    data = insertData;
  }
  
  return data as Configuracao;
};

// ============ OBSERVAÇÕES GERAIS ============
export const salvarObservacaoGeral = async (obs: ObservacaoGeral): Promise<ObservacaoGeral> => {
  const existente = await getObservacaoGeral(obs.dia_trabalho);
  
  let data;
  if (existente) {
    const { data: updateData, error } = await supabase
      .from('observacoes_gerais')
      .update({ observacao: obs.observacao })
      .eq('dia_trabalho', obs.dia_trabalho)
      .select()
      .single();
    
    if (error) throw error;
    data = updateData;
  } else {
    const { data: insertData, error } = await supabase
      .from('observacoes_gerais')
      .insert(obs)
      .select()
      .single();
    
    if (error) throw error;
    data = insertData;
  }
  
  return data as ObservacaoGeral;
};

export const getObservacaoGeral = async (diaTrabalho: string): Promise<ObservacaoGeral | null> => {
  const { data, error } = await supabase
    .from('observacoes_gerais')
    .select('*')
    .eq('dia_trabalho', diaTrabalho)
    .single();
  
  if (error) return null;
  return data as ObservacaoGeral;
};

// ============ REGISTROS DE TRABALHO ============
export const registrarEnvio = async (registro: RegistroTrabalho): Promise<RegistroTrabalho> => {
  const { data, error } = await supabase
    .from('registros_trabalho')
    .insert(registro)
    .select()
    .single();
  
  if (error) throw error;
  return data as RegistroTrabalho;
};

export const listarRegistros = async (): Promise<RegistroTrabalho[]> => {
  const { data, error } = await supabase
    .from('registros_trabalho')
    .select('*')
    .order('dia_trabalho', { ascending: false });
  
  if (error) throw error;
  return data as RegistroTrabalho[];
};

// ============ LOGS ============
export const salvarLog = async (log: Log): Promise<Log | null> => {
  const { data, error } = await supabase
    .from('logs')
    .insert(log)
    .select()
    .single();
  
  if (error) {
    console.log('Erro ao salvar log:', error);
    return null;
  }
  return data as Log;
};

export const listarLogs = async (limite: number = 100): Promise<Log[]> => {
  const { data, error } = await supabase
    .from('logs')
    .select('*')
    .order('created_at', { ascending: false })
    .limit(limite);
  
  if (error) return [];
  return data as Log[];
};

export const listarLogsPorTabela = async (tabela: string, limite: number = 100): Promise<Log[]> => {
  const { data, error } = await supabase
    .from('logs')
    .select('*')
    .eq('tabela', tabela)
    .order('created_at', { ascending: false })
    .limit(limite);
  
  if (error) return [];
  return data as Log[];
};

export const listarLogsPorAcao = async (acao: string, limite: number = 100): Promise<Log[]> => {
  const { data, error } = await supabase
    .from('logs')
    .select('*')
    .eq('acao', acao)
    .order('created_at', { ascending: false })
    .limit(limite);
  
  if (error) return [];
  return data as Log[];
};

export const limparLogs = async (): Promise<boolean> => {
  const { error } = await supabase.from('logs').delete().neq('id', '00000000-0000-0000-0000-000000000000');
  if (error) return false;
  return true;
};

// ============ ESTATÍSTICAS ============
export const getTotalFuncionarios = async (): Promise<TotalFuncionarios> => {
  const { data, error } = await supabase
    .from('funcionarios')
    .select('nome, dia_trabalho, valor_10_percent, pago');
  
  if (error || !data) {
    return {
      total_cadastrados: 0,
      total_registros: 0,
      total_dias_trabalhados: 0,
      total_geral_pago: 0,
      total_pago: 0,
      total_pendente: 0,
    };
  }
  
  const nomesUnicos = new Set(data.map(item => item.nome));
  const diasTrabalhados = new Set(data.map(item => item.dia_trabalho));
  
  let totalValores = 0;
  let totalPago = 0;
  let totalPendente = 0;
  
  data.forEach(item => {
    const valor = parseFloat(item.valor_10_percent) || 0;
    totalValores += valor;
    if (item.pago) {
      totalPago += valor;
    } else {
      totalPendente += valor;
    }
  });
  
  return {
    total_cadastrados: nomesUnicos.size,
    total_registros: data.length,
    total_dias_trabalhados: diasTrabalhados.size,
    total_geral_pago: totalValores,
    total_pago: totalPago,
    total_pendente: totalPendente,
  };
};

export const listarRankingPagamentos = async (): Promise<RankingPagamento[]> => {
  const { data, error } = await supabase
    .from('funcionarios')
    .select('nome, dia_trabalho, valor_10_percent, pago');
  
  if (error || !data) return [];
  
  const funcionariosDict: Record<string, any> = {};
  
  data.forEach(item => {
    const nome = item.nome;
    if (!funcionariosDict[nome]) {
      funcionariosDict[nome] = {
        nome,
        dias_trabalhados: 0,
        total_recebido: 0,
        maior_diaria: 0,
        menor_diaria: Infinity,
        total_pago: 0,
        total_pendente: 0,
      };
    }
    
    const func = funcionariosDict[nome];
    const valor = parseFloat(item.valor_10_percent) || 0;
    
    func.dias_trabalhados += 1;
    func.total_recebido += valor;
    if (valor > func.maior_diaria) func.maior_diaria = valor;
    if (valor < func.menor_diaria) func.menor_diaria = valor;
    if (item.pago) {
      func.total_pago += valor;
    } else {
      func.total_pendente += valor;
    }
  });
  
  const resultados: RankingPagamento[] = Object.values(funcionariosDict).map((func: any) => ({
    posicao: 0,
    nome: func.nome,
    dias_trabalhados: func.dias_trabalhados,
    total_recebido: func.total_recebido,
    media_diaria: func.total_recebido / func.dias_trabalhados,
    maior_diaria: func.maior_diaria,
    menor_diaria: func.menor_diaria === Infinity ? 0 : func.menor_diaria,
    total_pago: func.total_pago,
    total_pendente: func.total_pendente,
  }));
  
  resultados.sort((a, b) => b.total_recebido - a.total_recebido);
  
  return resultados.map((r, i) => ({ ...r, posicao: i + 1 }));
};

export const listarHistoricoPresenca = async (limite: number = 100): Promise<HistoricoPresenca[]> => {
  const { data, error } = await supabase
    .from('funcionarios')
    .select('*')
    .order('dia_trabalho', { ascending: false })
    .limit(limite);
  
  if (error || !data) return [];
  
  const today = new Date().toISOString().split('T')[0];
  const yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0];
  
  return data.map(item => ({
    ...item,
    dia_formatado: item.dia_trabalho === today ? 'Hoje' : 
                   item.dia_trabalho === yesterday ? 'Ontem' : 
                   item.dia_trabalho,
  })) as HistoricoPresenca[];
};

export const listarHistoricoPagamentos = async (limite: number = 100): Promise<HistoricoPagamento[]> => {
  const { data, error } = await supabase
    .from('funcionarios')
    .select('*')
    .order('dia_trabalho', { ascending: false })
    .limit(limite);
  
  if (error || !data) return [];
  
  return data.map(item => ({
    ...item,
    status_pagamento: item.pago ? 'Pago' : 'Pendente',
  })) as HistoricoPagamento[];
};

export const listarDataCadastramento = async (): Promise<DataCadastramento[]> => {
  const { data, error } = await supabase
    .from('funcionarios')
    .select('nome, dia_trabalho, valor_10_percent');
  
  if (error || !data) return [];
  
  const funcionariosDict: Record<string, any> = {};
  
  data.forEach(item => {
    const nome = item.nome;
    if (!funcionariosDict[nome]) {
      funcionariosDict[nome] = {
        nome,
        primeiro_dia_trabalho: item.dia_trabalho,
        ultimo_dia_trabalho: item.dia_trabalho,
        total_dias_trabalhados: 0,
        total_recebido: 0,
      };
    }
    
    const func = funcionariosDict[nome];
    func.total_dias_trabalhados += 1;
    func.total_recebido += parseFloat(item.valor_10_percent) || 0;
    
    if (item.dia_trabalho < func.primeiro_dia_trabalho) {
      func.primeiro_dia_trabalho = item.dia_trabalho;
    }
    if (item.dia_trabalho > func.ultimo_dia_trabalho) {
      func.ultimo_dia_trabalho = item.dia_trabalho;
    }
  });
  
  return Object.values(funcionariosDict) as DataCadastramento[];
};
