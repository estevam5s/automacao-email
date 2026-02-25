export interface Funcionario {
  id?: string;
  nome: string;
  valor_10_percent: number;
  hora_entrada: string;
  hora_saida: string;
  dia_trabalho: string;
  observacao?: string;
  vale?: number;
  tipo_vale?: 'pix' | 'dinheiro';
  tipo_pagamento?: 'pix' | 'dinheiro';
  pago: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface ObservacaoGeral {
  id?: string;
  dia_trabalho: string;
  observacao: string;
  created_at?: string;
}

export interface Configuracao {
  id?: string;
  email_destinatario: string;
  email_remetente: string;
  senha_app: string;
  smtp_host?: string;
  smtp_port?: number;
}

export interface Log {
  id?: string;
  acao: string;
  tabela: string;
  registro_id?: string;
  dados_anteriores?: string;
  dados_novos?: string;
  usuario: string;
  ip_origem?: string;
  created_at?: string;
}

export interface RegistroTrabalho {
  id?: string;
  dia_trabalho: string;
  dia_semana: string;
  total_funcionarios: number;
  total_valores: number;
  email_enviado: boolean;
  data_envio?: string;
}

export interface TotalFuncionarios {
  total_cadastrados: number;
  total_registros: number;
  total_dias_trabalhados: number;
  total_geral_pago: number;
  total_pago: number;
  total_pendente: number;
}

export interface RankingPagamento {
  posicao: number;
  nome: string;
  dias_trabalhados: number;
  total_recebido: number;
  media_diaria: number;
  maior_diaria: number;
  menor_diaria: number;
  total_pago: number;
  total_pendente: number;
}

export interface HistoricoPresenca {
  id?: string;
  nome: string;
  dia_trabalho: string | null;
  hora_entrada: string;
  hora_saida: string;
  valor_10_percent: number;
  observacao: string;
  created_at?: string;
  dia_formatado?: string;
}

export interface HistoricoPagamento {
  id?: string;
  nome: string;
  dia_trabalho: string | null;
  valor_10_percent: number;
  vale?: number;
  tipo_pagamento?: string;
  pago: boolean;
  data_pagamento?: string;
  status_pagamento?: string;
}

export interface DataCadastramento {
  nome: string;
  primeiro_dia_trabalho: string | null;
  ultimo_dia_trabalho: string | null;
  total_dias_trabalhados: number;
  total_recebido: number;
}

export interface User {
  id: string;
  email: string;
  created_at: string;
}

export interface AuthState {
  user: User | null;
  session: string | null;
  isLoading: boolean;
}
