-- =====================================================
-- Script para adicionar tabela de observações gerais diárias
-- Execute este script no SQL Editor do Supabase
-- =====================================================

-- Criar tabela de observações gerais por dia
CREATE TABLE IF NOT EXISTS public.observacoes_gerais (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dia_trabalho DATE NOT NULL UNIQUE,
    observacao TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Habilitar RLS
ALTER TABLE public.observacoes_gerais ENABLE ROW LEVEL SECURITY;

-- Política RLS
CREATE POLICY "Permitir tudo para anon em observacoes_gerais"
ON public.observacoes_gerais FOR ALL TO anon USING (true) WITH CHECK (true);

-- Trigger para updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_observacoes_gerais_updated_at
    BEFORE UPDATE ON public.observacoes_gerais
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
