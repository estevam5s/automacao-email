-- =====================================================
-- Script SQL Completo para Supabase
-- Sistema de Relatório de Salários de Garçons
-- =====================================================

-- =====================================================
-- 1. TABELA DE FUNCIONÁRIOS
-- =====================================================
CREATE TABLE IF NOT EXISTS public.funcionarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome TEXT NOT NULL,
    valor_10_percent DECIMAL(10, 2) NOT NULL DEFAULT 0,
    hora_entrada TIME NOT NULL DEFAULT '08:00',
    hora_saida TIME NOT NULL DEFAULT '16:00',
    dia_trabalho DATE NOT NULL,
    observacao TEXT,
    vale DECIMAL(10, 2),
    tipo_vale TEXT DEFAULT 'pix',
    pago BOOLEAN DEFAULT FALSE,
    tipo_pagamento TEXT DEFAULT 'pix',
    pix TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- 2. TABELA DE CONFIGURAÇÕES
-- =====================================================
CREATE TABLE IF NOT EXISTS public.configuracoes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email_destinatario TEXT NOT NULL,
    email_remetente TEXT NOT NULL,
    senha_app TEXT NOT NULL,
    smtp_host TEXT DEFAULT 'smtp.gmail.com',
    smtp_port INTEGER DEFAULT 587,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- 3. TABELA DE REGISTROS DE TRABALHO
-- =====================================================
CREATE TABLE IF NOT EXISTS public.registros_trabalho (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dia_trabalho DATE NOT NULL,
    dia_semana TEXT NOT NULL,
    total_funcionarios INTEGER DEFAULT 0,
    total_valores DECIMAL(10, 2) DEFAULT 0,
    email_enviado BOOLEAN DEFAULT FALSE,
    data_envio TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- 4. TABELA DE OBSERVAÇÕES GERAIS
-- =====================================================
CREATE TABLE IF NOT EXISTS public.observacoes_gerais (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dia_trabalho DATE NOT NULL UNIQUE,
    observacao TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- 5. TABELA DE FUNCIONÁRIOS BASE
-- =====================================================
CREATE TABLE IF NOT EXISTS public.funcionarios_base (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome TEXT NOT NULL UNIQUE,
    pix TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- 6. TABELA DE REGISTROS DIÁRIOS
-- =====================================================
CREATE TABLE IF NOT EXISTS public.registros_diarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome_funcionario TEXT NOT NULL,
    dia_trabalho DATE NOT NULL,
    valor_10_percent DECIMAL(10, 2) NOT NULL DEFAULT 0,
    hora_entrada TIME NOT NULL DEFAULT '08:00',
    hora_saida TIME NOT NULL DEFAULT '16:00',
    vale DECIMAL(10, 2),
    tipo_vale TEXT DEFAULT 'pix',
    pago BOOLEAN DEFAULT FALSE,
    observacao TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- 7. TABELA DE LOGS
-- =====================================================
CREATE TABLE IF NOT EXISTS public.logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    acao TEXT NOT NULL,
    tabela TEXT NOT NULL,
    registro_id TEXT,
    dados_anteriores JSONB,
    dados_novos JSONB,
    usuario TEXT DEFAULT 'sistema',
    ip_origem TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- 8. HABILITAR ROW LEVEL SECURITY (RLS)
-- =====================================================
ALTER TABLE public.funcionarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.configuracoes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.registros_trabalho ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.observacoes_gerais ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.funcionarios_base ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.registros_diarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.logs ENABLE ROW LEVEL SECURITY;

-- =====================================================
-- 9. POLÍTICAS RLS
-- =====================================================
-- Funcionarios
DROP POLICY IF EXISTS "Allow all on funcionarios" ON public.funcionarios;
CREATE POLICY "Allow all on funcionarios" ON public.funcionarios FOR ALL TO anon USING (true) WITH CHECK (true);

-- Configuracoes
DROP POLICY IF EXISTS "Allow all on configuracoes" ON public.configuracoes;
CREATE POLICY "Allow all on configuracoes" ON public.configuracoes FOR ALL TO anon USING (true) WITH CHECK (true);

-- Registros trabalho
DROP POLICY IF EXISTS "Allow all on registros_trabalho" ON public.registros_trabalho;
CREATE POLICY "Allow all on registros_trabalho" ON public.registros_trabalho FOR ALL TO anon USING (true) WITH CHECK (true);

-- Observacoes gerais
DROP POLICY IF EXISTS "Allow all on observacoes_gerais" ON public.observacoes_gerais;
CREATE POLICY "Allow all on observacoes_gerais" ON public.observacoes_gerais FOR ALL TO anon USING (true) WITH CHECK (true);

-- Funcionarios base
DROP POLICY IF EXISTS "Allow all on funcionarios_base" ON public.funcionarios_base;
CREATE POLICY "Allow all on funcionarios_base" ON public.funcionarios_base FOR ALL TO anon USING (true) WITH CHECK (true);

-- Registros diarios
DROP POLICY IF EXISTS "Allow all on registros_diarios" ON public.registros_diarios;
CREATE POLICY "Allow all on registros_diarios" ON public.registros_diarios FOR ALL TO anon USING (true) WITH CHECK (true);

-- Logs
DROP POLICY IF EXISTS "Allow all on logs" ON public.logs;
CREATE POLICY "Allow all on logs" ON public.logs FOR ALL TO anon USING (true) WITH CHECK (true);

-- =====================================================
-- 10. ÍNDICES
-- =====================================================
CREATE INDEX IF NOT EXISTS idx_funcionarios_dia ON public.funcionarios(dia_trabalho);
CREATE INDEX IF NOT EXISTS idx_funcionarios_nome ON public.funcionarios(nome);
CREATE INDEX IF NOT EXISTS idx_registros_diarios_dia ON public.registros_diarios(dia_trabalho);
CREATE INDEX IF NOT EXISTS idx_logs_tabela ON public.logs(tabela);
CREATE INDEX IF NOT EXISTS idx_logs_created_at ON public.logs(created_at DESC);

-- =====================================================
-- 11. FUNÇÃO PARA TIMESTAMP AUTOMÁTICO
-- =====================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers
DROP TRIGGER IF EXISTS update_funcionarios_updated_at ON public.funcionarios;
CREATE TRIGGER update_funcionarios_updated_at BEFORE UPDATE ON public.funcionarios FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_configuracoes_updated_at ON public.configuracoes;
CREATE TRIGGER update_configuracoes_updated_at BEFORE UPDATE ON public.configuracoes FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_observacoes_gerais_updated_at ON public.observacoes_gerais;
CREATE TRIGGER update_observacoes_gerais_updated_at BEFORE UPDATE ON public.observacoes_gerais FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_funcionarios_base_updated_at ON public.funcionarios_base;
CREATE TRIGGER update_funcionarios_base_updated_at BEFORE UPDATE ON public.funcionarios_base FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_registros_diarios_updated_at ON public.registros_diarios;
CREATE TRIGGER update_registros_diarios_updated_at BEFORE UPDATE ON public.registros_diarios FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- 12. INSERIR CONFIGURAÇÃO PADRÃO
-- =====================================================
INSERT INTO public.configuracoes (email_destinatario, email_remetente, senha_app)
VALUES ('estevams186@gmail.com', 'estevamsouzalaureth@gmail.com', 'dcbzodagocclqwqq')
ON CONFLICT DO NOTHING;

-- =====================================================
-- 13. VIEW PARA RELATÓRIO DIÁRIO
-- =====================================================
CREATE OR REPLACE VIEW public.vw_relatorio_diario AS
SELECT 
    dia_trabalho,
    COUNT(*) as total_funcionarios,
    SUM(valor_10_percent) as total_valores
FROM public.funcionarios
GROUP BY dia_trabalho
ORDER BY dia_trabalho DESC;

-- Verificar resultado
SELECT 'Tabelas criadas com sucesso!' as resultado;
