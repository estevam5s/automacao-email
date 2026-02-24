-- =====================================================
-- Script SQL para Adicionar Campo tipo_pagamento
-- Sistema de Relatório de Salários de Garçons
-- =====================================================

-- Adicionar coluna tipo_pagamento se não existir
ALTER TABLE public.funcionarios 
ADD COLUMN IF NOT EXISTS tipo_pagamento TEXT DEFAULT 'pix';

-- Atualizar registros existentes para ter pix como padrão
UPDATE public.funcionarios 
SET tipo_pagamento = 'pix' 
WHERE tipo_pagamento IS NULL;

-- Adicionar comentário para documentar
COMMENT ON COLUMN public.funcionarios.tipo_pagamento IS 'Tipo de pagamento do salário: pix, dinheiro';

-- Verificar se a coluna foi adicionada
SELECT column_name, data_type, column_default 
FROM information_schema.columns 
WHERE table_name = 'funcionarios' 
AND column_name IN ('tipo_pagamento', 'tipo_vale', 'pago');
