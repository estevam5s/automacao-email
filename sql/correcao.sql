-- =====================================================
-- Script de Correção para Supabase
-- Execute este script no SQL Editor do Supabase
-- =====================================================

-- 1. Corrigir a coluna ID para gerar UUID automaticamente
ALTER TABLE public.funcionarios 
ALTER COLUMN id SET DEFAULT gen_random_uuid();

-- 2. Se a tabela já tiver dados sem ID, você precisa excluí-la e recriar
-- Execute apenas se não conseguir inserir (primeira opção acima)

-- Para recriar a tabela (cuidado: apaga todos os dados):
-- DROP TABLE IF EXISTS public.funcionarios CASCADE;
-- CREATE TABLE IF NOT EXISTS public.funcionarios (
--     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
--     nome TEXT NOT NULL,
--     valor_10_percent DECIMAL(10, 2) NOT NULL,
--     hora_entrada TIME NOT NULL,
--     hora_saida TIME NOT NULL,
--     dia_trabalho DATE NOT NULL,
--     observacao TEXT,
--     created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
--     updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
-- );

-- Habilitar RLS novamente se necessário
-- ALTER TABLE public.funcionarios ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY "Permitir tudo para anon em funcionarios"
-- ON public.funcionarios FOR ALL TO anon USING (true) WITH CHECK (true);
