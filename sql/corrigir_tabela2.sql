-- =====================================================
-- CORRIGIR TABELA REGISTROS_DIARIOS
-- Execute no SQL Editor do Supabase
-- =====================================================

-- Verificar estrutura atual
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'registros_diarios';

-- Adicionar coluna nome_funcionario se não existir
ALTER TABLE public.registros_diarios 
ADD COLUMN IF NOT EXISTS nome_funcionario TEXT;

-- Se a coluna funcionario_id existir, atualizar nome_funcionario
UPDATE public.registros_diarios rd
SET nome_funcionario = (
    SELECT fb.nome 
    FROM public.funcionarios_base fb 
    WHERE fb.id = rd.funcionario_id
)
WHERE rd.nome_funcionario IS NULL;
