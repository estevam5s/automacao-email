-- =====================================================
-- Script SQL para Histórico e Rankings
-- Sistema de Relatório de Salários de Garçons
-- =====================================================

-- =====================================================
-- 1. VIEW - Histórico de Presença no Trabalho
-- =====================================================
CREATE OR REPLACE VIEW public.vw_historico_presenca AS
SELECT 
    id,
    nome,
    dia_trabalho,
    hora_entrada,
    hora_saida,
    valor_10_percent,
    observacao,
    created_at,
    CASE 
        WHEN dia_trabalho = CURRENT_DATE THEN 'Hoje'
        WHEN dia_trabalho = CURRENT_DATE - 1 THEN 'Ontem'
        ELSE TO_CHAR(dia_trabalho, 'DD/MM/YYYY')
    END as dia_formatado
FROM public.funcionarios
ORDER BY dia_trabalho DESC, nome ASC;

-- =====================================================
-- 2. VIEW - Histórico de Pagamentos por Funcionário
-- =====================================================
CREATE OR REPLACE VIEW public.vw_historico_pagamentos AS
SELECT 
    id,
    nome,
    dia_trabalho,
    valor_10_percent,
    vale,
    tipo_pagamento,
    pago,
    updated_at as data_pagamento,
    CASE 
        WHEN pago = true THEN 'Pago'
        ELSE 'Pendente'
    END as status_pagamento,
    ROW_NUMBER() OVER (PARTITION BY nome ORDER BY dia_trabalho DESC) as numero_parcela
FROM public.funcionarios
ORDER BY nome, dia_trabalho DESC;

-- =====================================================
-- 3. VIEW - Total de Funcionários
-- =====================================================
CREATE OR REPLACE VIEW public.vw_total_funcionarios AS
SELECT 
    COUNT(DISTINCT nome) as total_cadastrados,
    COUNT(*) as total_registros,
    COUNT(DISTINCT dia_trabalho) as total_dias_trabalhados,
    SUM(valor_10_percent) as total_geral_pago,
    SUM(CASE WHEN pago = true THEN valor_10_percent ELSE 0 END) as total_pago,
    SUM(CASE WHEN pago = false THEN valor_10_percent ELSE 0 END) as total_pendente,
    MIN(dia_trabalho) as primeiro_registro,
    MAX(dia_trabalho) as ultimo_registro
FROM public.funcionarios;

-- =====================================================
-- 4. VIEW - Data de Cadastramento de Cada Funcionário
-- =====================================================
CREATE OR REPLACE VIEW public.vw_data_cadastramento AS
SELECT 
    nome,
    MIN(dia_trabalho) as primeiro_dia_trabalho,
    MAX(dia_trabalho) as ultimo_dia_trabalho,
    COUNT(*) as total_dias_trabalhados,
    SUM(valor_10_percent) as total_recebido,
    MIN(created_at) as data_cadastro_banco,
    ARRAY_AGG(DISTINCT dia_trabalho ORDER BY dia_trabalho) as dias_trabalhados
FROM public.funcionarios
GROUP BY nome
ORDER BY primeiro_dia_trabalho DESC;

-- =====================================================
-- 5. VIEW - Ranking de Melhores Pagamentos
-- =====================================================
CREATE OR REPLACE VIEW public.vw_ranking_pagamentos AS
SELECT 
    ROW_NUMBER() OVER (ORDER BY SUM(valor_10_percent) DESC) as posicao,
    nome,
    COUNT(*) as dias_trabalhados,
    SUM(valor_10_percent) as total_recebido,
    AVG(valor_10_percent) as media_diaria,
    MAX(valor_10_percent) as maior_diaria,
    MIN(valor_10_percent) as menor_diaria,
    SUM(CASE WHEN pago = true THEN valor_10_percent ELSE 0 END) as total_pago,
    SUM(CASE WHEN pago = false THEN valor_10_percent ELSE 0 END) as total_pendente
FROM public.funcionarios
GROUP BY nome
ORDER BY total_recebido DESC;

-- =====================================================
-- 6. VIEW - Estatísticas por Mês
-- =====================================================
CREATE OR REPLACE VIEW public.vw_estatisticas_mensais AS
SELECT 
    TO_CHAR(dia_trabalho, 'YYYY-MM') as ano_mes,
    TO_CHAR(dia_trabalho, 'MMMM/YYYY') as mes_ano,
    COUNT(DISTINCT nome) as funcionarios_unicos,
    COUNT(*) as total_registros,
    SUM(valor_10_percent) as total_valores,
    AVG(valor_10_percent) as media_diaria
FROM public.funcionarios
GROUP BY TO_CHAR(dia_trabalho, 'YYYY-MM'), TO_CHAR(dia_trabalho, 'MMMM/YYYY')
ORDER BY ano_mes DESC;

-- =====================================================
-- 7. VIEW - Funcionários Atúltivos (imos 30 dias)
-- =====================================================
CREATE OR REPLACE VIEW public.vw_funcionarios_ativos AS
SELECT 
    nome,
    COUNT(*) as dias_trabalhados_30_dias,
    SUM(valor_10_percent) as total_30_dias,
    MAX(dia_trabalho) as ultimo_dia_trabalho
FROM public.funcionarios
WHERE dia_trabalho >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY nome
ORDER BY total_30_dias DESC;

-- =====================================================
-- 8. VIEW - Resumo por Dia da Semana
-- =====================================================
CREATE OR REPLACE VIEW public.vw_resumo_dia_semana AS
SELECT 
    TO_CHAR(dia_trabalho, 'TMDay') as dia_semana,
    COUNT(*) as total_registros,
    COUNT(DISTINCT nome) as funcionarios_presentes,
    SUM(valor_10_percent) as total_valores,
    AVG(valor_10_percent) as media_por_funcionario
FROM public.funcionarios
GROUP BY TO_CHAR(dia_trabalho, 'TMDay'), EXTRACT(DOW FROM dia_trabalho)
ORDER BY EXTRACT(DOW FROM dia_trabalho);

-- =====================================================
-- 9. Função para buscar histórico de um funcionário específico
-- =====================================================
CREATE OR REPLACE FUNCTION public.buscar_historico_funcionario(nome_funcionario TEXT)
RETURNS TABLE (
    dia_trabalho DATE,
    valor_10_percent NUMERIC,
    hora_entrada TIME,
    hora_saida TIME,
    pago BOOLEAN,
    tipo_pagamento TEXT,
    vale NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        f.dia_trabalho,
        f.valor_10_percent,
        f.hora_entrada,
        f.hora_saida,
        f.pago,
        f.tipo_pagamento,
        f.vale
    FROM public.funcionarios f
    WHERE f.nome ILIKE '%' || nome_funcionario || '%'
    ORDER BY f.dia_trabalho DESC;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- 10. Função para verificar se há registros duplicados
-- =====================================================
CREATE OR REPLACE FUNCTION public.verificar_duplicatas()
RETURNS TABLE (
    nome TEXT,
    dia_trabalho DATE,
    quantidade INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        f.nome,
        f.dia_trabalho,
        COUNT(*) as quantidade
    FROM public.funcionarios f
    GROUP BY f.nome, f.dia_trabalho
    HAVING COUNT(*) > 1
    ORDER BY quantidade DESC;
END;
$$ LANGUAGE plpgsql;

-- Verificar criação
SELECT 'Views e funções criadas com sucesso!' as resultado;

-- Testar as views
-- SELECT * FROM public.vw_ranking_pagamentos LIMIT 10;
-- SELECT * FROM public.vw_total_funcionarios;
-- SELECT * FROM public.vw_data_cadastramento;
