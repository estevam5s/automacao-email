-- Adicionar coluna nome_funcionario e outras colunas que faltam
ALTER TABLE public.registros_diarios 
ADD COLUMN IF NOT EXISTS nome_funcionario TEXT;

-- Atualizar registros existentes com nomes
UPDATE public.registros_diarios rd
SET nome_funcionario = fb.nome
FROM public.funcionarios_base fb
WHERE rd.funcionarios_base_id = fb.id;
