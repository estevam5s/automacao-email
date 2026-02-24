# Sistema de Relatório de Salários de Garçons

## 📥 Download e Instalação

### macOS

#### Opção 1: Executável Direto
1. Baixe o arquivo `SistemaSalariosGarcons.zip`
2. Descompacte o arquivo
3. Vá para a pasta: `SistemaSalariosGarcons/`
4. Clique duas vezes em `SistemaSalariosGarcons`
5. Se aparecer aviso de segurança:
   - Clique com botão direito no arquivo → "Abrir"
   - Ou vá em Preferências do Sistema → Segurança e Privacidade → Allow

#### Opção 2: Via Terminal
```bash
cd ~/Downloads
unzip SistemaSalariosGarcons.zip
./SistemaSalariosGarcons/SistemaSalariosGarcons
```

---

### Windows

#### Requisitos
- Windows 10 ou superior
- Não precisa de Python instalado

#### Instalação
1. Baixe o arquivo `SistemaSalariosGarcons.zip`
2. Descompacte o arquivo (clique direito → Extrair tudo)
3. Entre na pasta: `SistemaSalariosGarcons/`
4. Clique duas vezes em `SistemaSalariosGarcons.exe`

#### Solução de Problemas
- **Erro de DLL**: Instale o [Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)
- **Antivírus bloqueando**: Adicione exceção ou desative temporariamente

---

## 🚀 Primeiros Passos

### 1. Configuração Inicial
Ao abrir o aplicativo pela primeira vez:

1. Vá para a aba **⚙️ Configurações**
2. Configure:
   - **Email Remetente**: seu email Gmail
   - **Email Destinatário**: email que receberá os relatórios
   - **Senha de App**: Senha de app do Gmail (não sua senha normal)
3. Clique em **Salvar Configurações**

### 2. Cadastrar Funcionários
1. Vá para a aba **👥 Cadastrar Funcionários**
2. Digite o nome do funcionário
3. Clique em **Cadastrar**

### 3. Registrar Dia de Trabalho
1. Vá para a aba **📝 Registrar Dia de Trabalho**
2. Selecione a data
3. Cada funcionário cadastrado aparecerá na lista
4. Preencha:
   - Valor 10% das vendas
   - Hora de entrada/saída
   - Vale (se houver)
5. Clique em **Salvar Registros**

### 4. Enviar Relatório por Email
1. Vá para a aba **📧 Enviar E-mail com Relatório**
2. Selecione a data desejada
3. Escolha o formato do relatório:
   - 📄 DOCX (Word)
   - 📊 Excel
   - 📋 CSV
   - 🌐 HTML
4. Clique em **Gerar Relatório** para visualizar
5. Clique em **Enviar por Email** para enviar

---

## 📊 Abas do Aplicativo

| Aba | Descrição |
|-----|-----------|
| 👥 Cadastrar | Gerenciar lista de funcionários |
| 📝 Registrar Dia | Registrar vendas e valores do dia |
| 📧 Enviar Email | Gerar e enviar relatórios |
| 🗄️ Supabase | Gerenciar banco de dados |
| 📋 Logs | Histórico de ações do sistema |
| 📊 Histórico | Estatísticas e rankings |
| 💻 Código Fonte | Baixar código do projeto |
| 📚 Documentação | Ver documentação |
| ⚙️ Configurações | Configurar email e sistema |

---

## 🔧 Configurando o Gmail para Envio de Emails

### Criar Senha de App
1. Acesse [myaccount.google.com](https://myaccount.google.com)
2. Vá em **Segurança**
3. Ative **Verificação em duas etapas**
4. Vá em **Senhas de App** (pesquise no campo de busca)
5. Selecione "Correio" e "Outro"
6. Copie a senha gerada (16 caracteres com espaços)
7. Use essa senha no aplicativo

### Solução de Problemas de Email
- **Erro de autenticação**: Verifique se a senha de app está correta
- **Email não recebido**: Verifique caixa de spam
- **Erro de conexão**: Verifique internet

---

## 📋 Formatos de Relatório

| Formato | Extensão | Uso |
|---------|----------|-----|
| Word | .docx | Documentos formais |
| Excel | .xlsx | Planilhas e análise |
| CSV | .csv | Importação em outros sistemas |
| JSON | .json | Integração com APIs |
| XML | .xml | Sistemas legados |
| HTML | .html | Publicação na web |

---

## 🗄️ Banco de Dados Supabase

O aplicativo usa **Supabase** como banco de dados na nuvem. Isso permite:
- Acessar dados de qualquer lugar
- Dados sincronizados em tempo real
- Backup automático

### Tabelas do Banco
- **funcionarios**: Cadastro de funcionários e registros diários
- **configuracoes**: Configurações do sistema
- **observacoes_gerais**: Observações por dia
- **registros_trabalho**: Controle de envios
- **logs**: Histórico de operações

---

## 🔒 Segurança

- Senhas armazenadas localmente no banco
- Conexão segura com Supabase (SSL)
- Recomendado usar senha de app do Gmail (não senha pessoal)

---

## 📞 Suporte

Para dúvidas ou problemas:
- Email: estevams186@gmail.com
- GitHub: [Abrir Issue](https://github.com/anomalyco/opencode/issues)

---

*Sistema de Relatório de Salários de Garçons - v1.0.0*
