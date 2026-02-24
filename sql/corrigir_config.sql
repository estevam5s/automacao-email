-- Script para corrigir configuração de e-mail no Supabase
-- Execute este código no SQL Editor do Supabase

-- Atualizar a configuração existente
UPDATE public.configuracoes 
SET 
    email_destinatario = 'estevams186@gmail.com',
    email_remetente = 'estevamsouzalaureth@gmail.com',
    senha_app = 'dcbz odag occl qwqq'
WHERE id IS NOT NULL;

-- Se não existir, inserir novo registro
INSERT INTO public.configuracoes (email_destinatario, email_remetente, senha_app)
SELECT 'estevams186@gmail.com', 'estevamsouzalaureth@gmail.com', 'dcbz odag occl qwqq'
WHERE NOT EXISTS (SELECT 1 FROM public.configuracoes LIMIT 1);
