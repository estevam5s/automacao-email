-- =====================================================
-- Script SQL para Criação das Tabelas no Supabase
-- Automação de Relatório de Salários de Garçons
-- =====================================================

-- =====================================================
-- 1. CRIAÇÃO DA TABELA FUNCIONARIOS
-- =====================================================
CREATE TABLE IF NOT EXISTS public.funcionarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome TEXT NOT NULL,
    valor_10_percent DECIMAL(10, 2) NOT NULL,
    hora_entrada TIME NOT NULL,
    hora_saida TIME NOT NULL,
    dia_trabalho DATE NOT NULL,
    observacao TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- 2. CRIAÇÃO DA TABELA CONFIGURACOES (para e-mail)
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
-- 3. CRIAÇÃO DA TABELA REGISTROS_TRABALHO
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
-- 4. HABILITAR ROW LEVEL SECURITY (RLS)
-- =====================================================
ALTER TABLE public.funcionarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.configuracoes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.registros_trabalho ENABLE ROW LEVEL SECURITY;

-- =====================================================
-- 5. POLÍTICAS RLS PARA FUNCIONARIOS
-- =====================================================
CREATE POLICY "Permitir tudo para anon em funcionarios"
ON public.funcionarios FOR ALL
TO anon
USING (true)
WITH CHECK (true);

-- =====================================================
-- 6. POLÍTICAS RLS PARA CONFIGURACOES
-- =====================================================
CREATE POLICY "Permitir tudo para anon em configuracoes"
ON public.configuracoes FOR ALL
TO anon
USING (true)
WITH CHECK (true);

-- =====================================================
-- 7. POLÍTICAS RLS PARA REGISTROS_TRABALHO
-- =====================================================
CREATE POLICY "Permitir tudo para anon em registros_trabalho"
ON public.registros_trabalho FOR ALL
TO anon
USING (true)
WITH CHECK (true);

-- =====================================================
-- 8. ÍNDICES PARA MELHORAR PERFORMANCE
-- =====================================================
CREATE INDEX idx_funcionarios_dia_trabalho 
ON public.funcionarios(dia_trabalho);

CREATE INDEX idx_funcionarios_nome 
ON public.funcionarios(nome);

CREATE INDEX idx_registros_trabalho_dia 
ON public.registros_trabalho(dia_trabalho);

-- =====================================================
-- 9. FUNÇÃO PARA ATUALIZAR TIMESTAMP AUTOMÁTICO
-- =====================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para funcionarios
CREATE TRIGGER update_funcionarios_updated_at
    BEFORE UPDATE ON public.funcionarios
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger para configuracoes
CREATE TRIGGER update_configuracoes_updated_at
    BEFORE UPDATE ON public.configuracoes
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- 10. INSERIR CONFIGURAÇÃO PADRÃO
-- =====================================================
INSERT INTO public.configuracoes (email_destinatario, email_remetente, senha_app)
VALUES ('estevams186@gmail.com', 'estevamsouzalaureth@gmail.com', 'dcbz odag occl qwqq')
ON CONFLICT DO NOTHING;

-- Para atualizar se já existir:
-- UPDATE public.configuracoes SET 
--     email_destinatario = 'estevams186@gmail.com',
--     email_remetente = 'estevamsouzalaureth@gmail.com',
--     senha_app = 'dcbz odag occl qwqq'
-- WHERE id IS NOT NULL;

-- =====================================================
-- 11. CRIAR VIEW PARA RELATÓRIO DIÁRIO
-- =====================================================
CREATE OR REPLACE VIEW public.vw_relatorio_diario AS
SELECT 
    dia_trabalho,
    COUNT(*) as total_funcionarios,
    SUM(valor_10_percent) as total_valores,
    ARRAY_AGG(
        JSON_BUILD_OBJECT(
            'nome', nome,
            'valor_10_percent', valor_10_percent,
            'hora_entrada', hora_entrada,
            'hora_saida', hora_saida,
            'observacao', observacao
        )
    ) as funcionarios
FROM public.funcionarios
GROUP BY dia_trabalho
ORDER BY dia_trabalho DESC;
