-- =====================================================
-- NOVAS TABELAS PARA SISTEMA DE SALÁRIOS
-- Execute este script no SQL Editor do Supabase
-- =====================================================

-- 1. Tabela de funcionários fixos
CREATE TABLE IF NOT EXISTS public.funcionarios_base (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome TEXT NOT NULL UNIQUE,
    pix TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Tabela de registros diários de trabalho
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

-- 3. Tabela de observações gerais
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

-- 5. Políticas RLS
DROP POLICY IF EXISTS "Allow all on funcionarios_base" ON public.funcionarios_base;
CREATE POLICY "Allow all on funcionarios_base" ON public.funcionarios_base FOR ALL TO anon USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all on registros_diarios" ON public.registros_diarios;
CREATE POLICY "Allow all on registros_diarios" ON public.registros_diarios FOR ALL TO anon USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all on observacoes_gerais" ON public.observacoes_gerais;
CREATE POLICY "Allow all on observacoes_gerais" ON public.observacoes_gerais FOR ALL TO anon USING (true) WITH CHECK (true);

-- 6. Função e triggers
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_funcionarios_base_updated_at ON public.funcionarios_base;
CREATE TRIGGER update_funcionarios_base_updated_at
    BEFORE UPDATE ON public.funcionarios_base
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_registros_diarios_updated_at ON public.registros_diarios;
CREATE TRIGGER update_registros_diarios_updated_at
    BEFORE UPDATE ON public.registros_diarios
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_observacoes_gerais_updated_at ON public.observacoes_gerais;
CREATE TRIGGER update_observacoes_gerais_updated_at
    BEFORE UPDATE ON public.observacoes_gerais
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Verificar
SELECT 'Tabelas criadas com sucesso!' as resultado;
