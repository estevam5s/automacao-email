-- =====================================================
-- Script para criar tabela de funcionários fixos e registros diários
-- Execute este script no SQL Editor do Supabase
-- =====================================================

-- Tabela de funcionários fixos (cadastrados uma vez)
CREATE TABLE IF NOT EXISTS public.funcionarios_base (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome TEXT NOT NULL UNIQUE,
    pix TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de registros diários de trabalho
CREATE TABLE IF NOT EXISTS public.registros_diarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    funcionario_id UUID REFERENCES public.funcionarios_base(id),
    dia_trabalho DATE NOT NULL,
    valor_10_percent DECIMAL(10, 2) NOT NULL,
    hora_entrada TIME NOT NULL,
    hora_saida TIME NOT NULL,
    vale DECIMAL(10, 2),
    tipo_vale TEXT DEFAULT 'pix',
    pago BOOLEAN DEFAULT FALSE,
    observacao TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(funcionario_id, dia_trabalho)
);

-- Tabela de observações gerais (já criada anteriormente)
-- CREATE TABLE IF NOT EXISTS public.observacoes_gerais ...

-- Habilitar RLS
ALTER TABLE public.funcionarios_base ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.registros_diarios ENABLE ROW LEVEL SECURITY;

-- Políticas RLS
CREATE POLICY "Permitir tudo para anon em funcionarios_base"
ON public.funcionarios_base FOR ALL TO anon USING (true) WITH CHECK (true);

CREATE POLICY "Permitir tudo para anon em registros_diarios"
ON public.registros_diarios FOR ALL TO anon USING (true) WITH CHECK (true);

-- Trigger para updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_funcionarios_base_updated_at
    BEFORE UPDATE ON public.funcionarios_base
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_registros_diarios_updated_at
    BEFORE UPDATE ON public.registros_diarios
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
