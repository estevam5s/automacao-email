import { create } from 'zustand';
import { supabase } from './supabase';

interface Funcionario {
  id?: string;
  nome: string;
  valor_10_percent: number;
  hora_entrada: string;
  hora_saida: string;
  dia_trabalho: string;
  observacao?: string;
  vale?: number;
  tipo_vale?: string;
  pago?: boolean;
  tipo_pagamento?: string;
  pix?: string;
}

interface Configuracao {
  id?: string;
  email_destinatario: string;
  email_remetente: string;
  senha_app: string;
  smtp_host?: string;
  smtp_port?: number;
}

interface Log {
  id?: string;
  acao: string;
  tabela: string;
  registro_id?: string;
  usuario?: string;
  dados_anteriores?: Record<string, unknown>;
  dados_novos?: Record<string, unknown>;
  created_at?: string;
}

interface AppStore {
  user: Record<string, unknown> | null;
  loading: boolean;
  error: string | null;

  signIn: (email: string, password: string) => Promise<boolean>;
  signOut: () => Promise<void>;
  checkAuth: () => Promise<void>;
  setError: (err: string | null) => void;

  listarFuncionarios: (dia?: string) => Promise<Funcionario[]>;
  cadastrarFuncionario: (f: Funcionario) => Promise<void>;
  deletarFuncionario: (id: string) => Promise<void>;

  getConfiguracao: () => Promise<Configuracao | null>;
  salvarConfiguracao: (c: Configuracao) => Promise<void>;

  salvarLog: (l: Log) => Promise<void>;
}

export const useAppStore = create<AppStore>((set) => ({
  user: null,
  loading: false,
  error: null,

  setError: (err) => set({ error: err }),

  checkAuth: async () => {
    const { data: { session } } = await supabase.auth.getSession();
    set({ user: session?.user ?? null });
  },

  signIn: async (email, password) => {
    set({ loading: true, error: null });
    const { data, error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) {
      set({ loading: false, error: error.message });
      return false;
    }
    set({ user: data.user, loading: false });
    return true;
  },

  signOut: async () => {
    await supabase.auth.signOut();
    set({ user: null });
  },

  listarFuncionarios: async (dia) => {
    let query = supabase.from('funcionarios').select('*').order('nome');
    if (dia) query = query.eq('dia_trabalho', dia);
    const { data } = await query;
    return (data ?? []) as Funcionario[];
  },

  cadastrarFuncionario: async (f) => {
    await supabase.from('funcionarios').insert(f);
  },

  deletarFuncionario: async (id) => {
    await supabase.from('funcionarios').delete().eq('id', id);
  },

  getConfiguracao: async () => {
    const { data } = await supabase.from('configuracoes').select('*').limit(1).single();
    return data as Configuracao | null;
  },

  salvarConfiguracao: async (c) => {
    const { data: existing } = await supabase.from('configuracoes').select('id').limit(1).single();
    if (existing?.id) {
      await supabase.from('configuracoes').update(c).eq('id', existing.id);
    } else {
      await supabase.from('configuracoes').insert(c);
    }
  },

  salvarLog: async (l) => {
    await supabase.from('logs').insert(l);
  },
}));
