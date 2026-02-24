-- =====================================================
-- Script completo para criar as tabelas necessárias
-- Execute no SQL Editor do Supabase
-- =====================================================

-- 1. Criar tabela de funcionários base (fixos)
CREATE TABLE IF NOT EXISTS public.funcionarios_base (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome TEXT NOT NULL UNIQUE,
    pix TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Criar tabela de registros diários
CREATE TABLE IF NOT EXISTS public.registros_diarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    funcionario_id UUID REFERENCES public.funcionarios_base(id),
    dia_trabalho DATE NOT NULL,
    valor_10_percent DECIMAL(10, 2) NOT NULL DEFAULT 0,
    hora_entrada TIME NOT NULL DEFAULT '08:00',
    hora_saida TIME NOT NULL DEFAULT '16:00',
    vale DECIMAL(10, 2),
    tipo_vale TEXT DEFAULT 'pix',
    pago BOOLEAN DEFAULT FALSE,
    observacao TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(funcionario_id, dia_trabalho)
);

-- 3. Criar tabela de observações gerais
CREATE TABLE IF NOT EXISTS public.observacoes_gerais (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dia_trabalho DATE NOT NULL UNIQUE,
    observacao TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Habilitar RLS
ALTER TABLE public.funcionarios_base ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.registros_diarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.observacoes_gerais ENABLE ROW LEVEL SECURITY;

-- 5. Criar políticas RLS
CREATE POLICY "Allow all on funcionarios_base" ON public.funcionarios_base FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY "Allow all on registros_diarios" ON public.registros_diarios FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY "Allow all on observacoes_gerais" ON public.observacoes_gerais FOR ALL TO anon USING (true) WITH CHECK (true);

-- 6. Criar função trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 7. Criar triggers
CREATE TRIGGER update_funcionarios_base_updated_at
    BEFORE UPDATE ON public.funcionarios_base
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_registros_diarios_updated_at
    BEFORE UPDATE ON public.registros_diarios
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_observacoes_gerais_updated_at
    BEFORE UPDATE ON public.observacoes_gerais
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Verificar criação
SELECT 'funcionarios_base' as tabela, COUNT(*) as existe FROM information_schema.tables WHERE table_name = 'funcionarios_base'
UNION ALL
SELECT 'registros_diarios', COUNT(*) FROM information_schema.tables WHERE table_name = 'registros_diarios'
UNION ALL
SELECT 'observacoes_gerais', COUNT(*) FROM information_schema.tables WHERE table_name = 'observacoes_gerais';
