-- =====================================================
-- Script SQL para Tabela de Logs do Sistema
-- Sistema de Relatório de Salários de Garçons
-- =====================================================

-- =====================================================
-- 1. CRIAÇÃO DA TABELA DE LOGS
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
-- 2. ÍNDICES PARA MELHORAR PERFORMANCE
-- =====================================================
CREATE INDEX idx_logs_tabela ON public.logs(tabela);
CREATE INDEX idx_logs_acao ON public.logs(acao);
CREATE INDEX idx_logs_created_at ON public.logs(created_at DESC);

-- =====================================================
-- 3. HABILITAR ROW LEVEL SECURITY (RLS)
-- =====================================================
ALTER TABLE public.logs ENABLE ROW LEVEL SECURITY;

-- =====================================================
-- 4. POLÍTICAS RLS PARA LOGS
-- =====================================================
CREATE POLICY "Permitir tudo para anon em logs"
ON public.logs FOR ALL
TO anon
USING (true)
WITH CHECK (true);

-- =====================================================
-- 5. COMENTÁRIOS
-- =====================================================
COMMENT ON TABLE public.logs IS 'Tabela de logs do sistema para auditoria';
COMMENT ON COLUMN public.logs.acao IS 'Tipo de ação: CRIAR, ATUALIZAR, DELETAR, VISUALIZAR, ENVIAR_EMAIL';
COMMENT ON COLUMN public.logs.tabela IS 'Nome da tabela afetada: funcionarios, configuracoes, etc';
COMMENT ON COLUMN public.logs.registro_id IS 'ID do registro afetado';
COMMENT ON COLUMN public.logs.dados_anteriores IS 'Dados antes da alteração (JSON)';
COMMENT ON COLUMN public.logs.dados_novos IS 'Dados após a alteração (JSON)';

-- =====================================================
-- 6. VIEW PARA RELATÓRIO DE LOGS
-- =====================================================
CREATE OR REPLACE VIEW public.vw_logs_recentes AS
SELECT 
    id,
    acao,
    tabela,
    registro_id,
    usuario,
    ip_origem,
    created_at,
    CASE 
        WHEN acao = 'CRIAR' THEN '✅ Registro criado'
        WHEN acao = 'ATUALIZAR' THEN '✏️ Registro atualizado'
        WHEN acao = 'DELETAR' THEN '🗑️ Registro deletado'
        WHEN acao = 'VISUALIZAR' THEN '👁️ Registro visualizado'
        WHEN acao = 'ENVIAR_EMAIL' THEN '📧 E-mail enviado'
        ELSE acao
    END as descricao_formatada
FROM public.logs
ORDER BY created_at DESC
LIMIT 100;
