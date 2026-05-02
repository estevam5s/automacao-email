-- =====================================================
-- Script para adicionar novos campos à tabela de funcionários
-- Execute este script no SQL Editor do Supabase
-- =====================================================

-- Adicionar novos campos à tabela funcionarios
ALTER TABLE public.funcionarios 
ADD COLUMN IF NOT EXISTS vale DECIMAL(10, 2) DEFAULT 0.00,
ADD COLUMN IF NOT EXISTS tipo_vale TEXT DEFAULT 'pix',
ADD COLUMN IF NOT EXISTS observacao_geral TEXT,
ADD COLUMN IF NOT EXISTS pago BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS data_pagamento TIMESTAMP WITH TIME ZONE;

-- Verificar se os campos foram adicionados
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'funcionarios' 
ORDER BY ordinal_position;
