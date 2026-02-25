import { create } from 'zustand';
import { Funcionario, Configuracao, Log, TotalFuncionarios, RankingPagamento } from '../types';
import * as api from '../services/supabase';

interface AppState {
  // Auth
  user: any;
  isLoading: boolean;
  isAuthenticated: boolean;
  
  // Data
  funcionarios: Funcionario[];
  nomesFuncionarios: string[];
  configuracao: Configuracao | null;
  logs: Log[];
  
  // Stats
  totalFuncionarios: TotalFuncionarios | null;
  ranking: RankingPagamento[];
  
  // UI
  isOnline: boolean;
  isSyncing: boolean;
  
  // Actions
  setUser: (user: any | null) => void;
  setLoading: (loading: boolean) => void;
  setOnline: (online: boolean) => void;
  
  // Data actions
  loadFuncionarios: (diaTrabalho?: string) => Promise<void>;
  loadNomesFuncionarios: () => Promise<void>;
  loadConfiguracao: () => Promise<void>;
  loadLogs: (limite?: number) => Promise<void>;
  loadTotalFuncionarios: () => Promise<void>;
  loadRanking: () => Promise<void>;
  
  addFuncionario: (func: Funcionario) => Promise<void>;
  updateFuncionario: (func: Funcionario) => Promise<void>;
  deleteFuncionario: (id: string) => Promise<void>;
  
  saveConfiguracao: (config: Configuracao) => Promise<void>;
  clearLogs: () => Promise<void>;
}

export const useAppStore = create<AppState>((set, get) => ({
  // Initial state
  user: null,
  isLoading: true,
  isAuthenticated: false,
  funcionarios: [],
  nomesFuncionarios: [],
  configuracao: null,
  logs: [],
  totalFuncionarios: null,
  ranking: [],
  isOnline: true,
  isSyncing: false,
  
  // Basic setters
  setUser: (user) => set({ user, isAuthenticated: !!user }),
  setLoading: (isLoading) => set({ isLoading }),
  setOnline: (isOnline) => set({ isOnline }),
  
  // Load data functions
  loadFuncionarios: async (diaTrabalho?: string) => {
    try {
      const funcionarios = diaTrabalho 
        ? await api.listarFuncionarios(diaTrabalho)
        : await api.listarTodosFuncionarios();
      set({ funcionarios });
    } catch (error) {
      console.log('Erro ao carregar funcionários:', error);
    }
  },
  
  loadNomesFuncionarios: async () => {
    try {
      const nomes = await api.getNomesUnicosFuncionarios();
      set({ nomesFuncionarios: nomes });
    } catch (error) {
      console.log('Erro ao carregar nomes:', error);
    }
  },
  
  loadConfiguracao: async () => {
    try {
      const config = await api.getConfiguracao();
      set({ configuracao: config });
    } catch (error) {
      console.log('Erro ao carregar configuração:', error);
    }
  },
  
  loadLogs: async (limite: number = 100) => {
    try {
      const logs = await api.listarLogs(limite);
      set({ logs });
    } catch (error) {
      console.log('Erro ao carregar logs:', error);
    }
  },
  
  loadTotalFuncionarios: async () => {
    try {
      const total = await api.getTotalFuncionarios();
      set({ totalFuncionarios: total });
    } catch (error) {
      console.log('Erro ao carregar total:', error);
    }
  },
  
  loadRanking: async () => {
    try {
      const ranking = await api.listarRankingPagamentos();
      set({ ranking });
    } catch (error) {
      console.log('Erro ao carregar ranking:', error);
    }
  },
  
  // CRUD operations
  addFuncionario: async (func: Funcionario) => {
    set({ isSyncing: true });
    try {
      await api.cadastrarFuncionario(func);
      await api.salvarLog({
        acao: 'CRIAR',
        tabela: 'funcionarios',
        usuario: get().user?.email || 'sistema',
      });
      await get().loadFuncionarios();
      await get().loadNomesFuncionarios();
      await get().loadTotalFuncionarios();
    } catch (error) {
      console.log('Erro ao adicionar funcionário:', error);
      throw error;
    } finally {
      set({ isSyncing: false });
    }
  },
  
  updateFuncionario: async (func: Funcionario) => {
    set({ isSyncing: true });
    try {
      await api.atualizarFuncionario(func);
      await api.salvarLog({
        acao: 'ATUALIZAR',
        tabela: 'funcionarios',
        registro_id: func.id,
        usuario: get().user?.email || 'sistema',
      });
      await get().loadFuncionarios();
      await get().loadTotalFuncionarios();
    } catch (error) {
      console.log('Erro ao atualizar funcionário:', error);
      throw error;
    } finally {
      set({ isSyncing: false });
    }
  },
  
  deleteFuncionario: async (id: string) => {
    set({ isSyncing: true });
    try {
      await api.deletarFuncionario(id);
      await api.salvarLog({
        acao: 'DELETAR',
        tabela: 'funcionarios',
        registro_id: id,
        usuario: get().user?.email || 'sistema',
      });
      await get().loadFuncionarios();
      await get().loadNomesFuncionarios();
      await get().loadTotalFuncionarios();
    } catch (error) {
      console.log('Erro ao deletar funcionário:', error);
      throw error;
    } finally {
      set({ isSyncing: false });
    }
  },
  
  saveConfiguracao: async (config: Configuracao) => {
    set({ isSyncing: true });
    try {
      await api.salvarConfiguracao(config);
      await get().loadConfiguracao();
    } catch (error) {
      console.log('Erro ao salvar configuração:', error);
      throw error;
    } finally {
      set({ isSyncing: false });
    }
  },
  
  clearLogs: async () => {
    try {
      await api.limparLogs();
      set({ logs: [] });
    } catch (error) {
      console.log('Erro ao limpar logs:', error);
    }
  },
}));
