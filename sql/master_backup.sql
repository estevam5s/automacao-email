-- ============================================================
-- AUTOMAÇÃO EMAIL — MASTER BACKUP SQL
-- Supabase Project: zqvqmqpdgsiyvlsewyyq
-- Generated: 2026-05-02
-- Run idempotently in Supabase SQL Editor
-- ============================================================

-- ============================================================
-- 1. TABELAS PRINCIPAIS
-- ============================================================

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

CREATE TABLE IF NOT EXISTS public.observacoes_gerais (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dia_trabalho DATE NOT NULL UNIQUE,
    observacao TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.funcionarios_base (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome TEXT NOT NULL UNIQUE,
    pix TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

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

-- ============================================================
-- 2. ÍNDICES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_funcionarios_dia ON public.funcionarios(dia_trabalho);
CREATE INDEX IF NOT EXISTS idx_funcionarios_nome ON public.funcionarios(nome);
CREATE INDEX IF NOT EXISTS idx_registros_diarios_dia ON public.registros_diarios(dia_trabalho);
CREATE INDEX IF NOT EXISTS idx_logs_tabela ON public.logs(tabela);
CREATE INDEX IF NOT EXISTS idx_logs_created_at ON public.logs(created_at DESC);

-- ============================================================
-- 3. ROW LEVEL SECURITY
-- ============================================================

ALTER TABLE public.funcionarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.configuracoes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.registros_trabalho ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.observacoes_gerais ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.funcionarios_base ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.registros_diarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.logs ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Allow all on funcionarios" ON public.funcionarios;
CREATE POLICY "Allow all on funcionarios" ON public.funcionarios FOR ALL TO anon USING (true) WITH CHECK (true);
DROP POLICY IF EXISTS "Allow auth on funcionarios" ON public.funcionarios;
CREATE POLICY "Allow auth on funcionarios" ON public.funcionarios FOR ALL TO authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all on configuracoes" ON public.configuracoes;
CREATE POLICY "Allow all on configuracoes" ON public.configuracoes FOR ALL TO anon USING (true) WITH CHECK (true);
DROP POLICY IF EXISTS "Allow auth on configuracoes" ON public.configuracoes;
CREATE POLICY "Allow auth on configuracoes" ON public.configuracoes FOR ALL TO authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all on registros_trabalho" ON public.registros_trabalho;
CREATE POLICY "Allow all on registros_trabalho" ON public.registros_trabalho FOR ALL TO anon USING (true) WITH CHECK (true);
DROP POLICY IF EXISTS "Allow auth on registros_trabalho" ON public.registros_trabalho;
CREATE POLICY "Allow auth on registros_trabalho" ON public.registros_trabalho FOR ALL TO authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all on observacoes_gerais" ON public.observacoes_gerais;
CREATE POLICY "Allow all on observacoes_gerais" ON public.observacoes_gerais FOR ALL TO anon USING (true) WITH CHECK (true);
DROP POLICY IF EXISTS "Allow auth on observacoes_gerais" ON public.observacoes_gerais;
CREATE POLICY "Allow auth on observacoes_gerais" ON public.observacoes_gerais FOR ALL TO authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all on funcionarios_base" ON public.funcionarios_base;
CREATE POLICY "Allow all on funcionarios_base" ON public.funcionarios_base FOR ALL TO anon USING (true) WITH CHECK (true);
DROP POLICY IF EXISTS "Allow auth on funcionarios_base" ON public.funcionarios_base;
CREATE POLICY "Allow auth on funcionarios_base" ON public.funcionarios_base FOR ALL TO authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all on registros_diarios" ON public.registros_diarios;
CREATE POLICY "Allow all on registros_diarios" ON public.registros_diarios FOR ALL TO anon USING (true) WITH CHECK (true);
DROP POLICY IF EXISTS "Allow auth on registros_diarios" ON public.registros_diarios;
CREATE POLICY "Allow auth on registros_diarios" ON public.registros_diarios FOR ALL TO authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all on logs" ON public.logs;
CREATE POLICY "Allow all on logs" ON public.logs FOR ALL TO anon USING (true) WITH CHECK (true);
DROP POLICY IF EXISTS "Allow auth on logs" ON public.logs;
CREATE POLICY "Allow auth on logs" ON public.logs FOR ALL TO authenticated USING (true) WITH CHECK (true);

-- ============================================================
-- 4. FUNCTIONS & TRIGGERS
-- ============================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

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

-- ============================================================
-- 5. VIEWS
-- ============================================================

CREATE OR REPLACE VIEW public.vw_relatorio_diario AS
SELECT
    dia_trabalho,
    COUNT(*) as total_funcionarios,
    SUM(valor_10_percent) as total_valores
FROM public.funcionarios
GROUP BY dia_trabalho
ORDER BY dia_trabalho DESC;

-- ============================================================
-- 6. CONFIGURAÇÃO PADRÃO
-- ============================================================

INSERT INTO public.configuracoes (email_destinatario, email_remetente, senha_app)
VALUES ('rebecaluize@gmail.com', 'estevamsouzalaureth@gmail.com', 'dcbzodagocclqwqq')
ON CONFLICT DO NOTHING;

-- ============================================================
-- 7. TABLE_CRON + PG_CRON
-- ============================================================

CREATE TABLE IF NOT EXISTS public.table_cron (num INT8);
ALTER TABLE public.table_cron ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "anon_all" ON public.table_cron;
CREATE POLICY "anon_all" ON public.table_cron FOR ALL USING (true) WITH CHECK (true);

CREATE EXTENSION IF NOT EXISTS pg_cron;

SELECT cron.unschedule(jobname) FROM cron.job WHERE jobname LIKE 'email-cron-%';

SELECT cron.schedule('email-cron-1-6h-heartbeat',   '0 */6 * * *',       $$INSERT INTO public.table_cron (num) VALUES (1)$$);
SELECT cron.schedule('email-cron-2-daily-cleanup',  '0 2 * * *',         $$INSERT INTO public.table_cron (num) VALUES (2)$$);
SELECT cron.schedule('email-cron-3-10min-status',   '*/10 * * * *',      $$INSERT INTO public.table_cron (num) VALUES (3)$$);
SELECT cron.schedule('email-cron-4-hourly-sync',    '0 * * * *',         $$INSERT INTO public.table_cron (num) VALUES (4)$$);
SELECT cron.schedule('email-cron-5-weekly-report',  '0 3 * * 1',         $$INSERT INTO public.table_cron (num) VALUES (5)$$);
SELECT cron.schedule('email-cron-6-monthly-close',  '0 0 1 * *',         $$INSERT INTO public.table_cron (num) VALUES (6)$$);
SELECT cron.schedule('email-cron-7-daily-purge',    '0 1 * * *',         $$INSERT INTO public.table_cron (num) VALUES (7)$$);
SELECT cron.schedule('email-cron-8-daily-backup',   '0 4 * * *',         $$INSERT INTO public.table_cron (num) VALUES (8)$$);
SELECT cron.schedule('email-cron-9-weekly-reindex', '0 4 * * 0',         $$INSERT INTO public.table_cron (num) VALUES (9)$$);
SELECT cron.schedule('email-cron-10-batch-process', '0 9,15,21 * * *',   $$INSERT INTO public.table_cron (num) VALUES (10)$$);

-- ============================================================
-- 8. ADMIN AUTH USER (criar via Supabase Auth Admin API)
-- POST /auth/v1/admin/users com service_role key:
--   { "email": "contato@estevamsouza.com.br",
--     "password": "Respira@110088", "email_confirm": true }
-- ============================================================

-- ============================================================
-- 9. VERIFICAÇÃO
-- ============================================================

SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN ('funcionarios','configuracoes','registros_trabalho',
                     'observacoes_gerais','funcionarios_base','registros_diarios',
                     'logs','table_cron')
ORDER BY table_name;
