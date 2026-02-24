# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2026-02-24

### Added
- **Interface Web (Streamlit)** - Versão web completa do sistema
- **Página Home** - Introdução e tutorial do sistema
- **Sistema de Envio de E-mail** - Integrado com configurações do desktop
- **Download da Aplicação Desktop** - Link direto para baixar o executável
- **Menu Lateral** - Navegação completa entre todas as funcionalidades
- **Tema Dark** - Interface com gradiente e estilização profissional
- **Estatísticas em Tempo Real** - Métricas na página inicial

### Features Web

#### 🏠 Home
- Introdução ao sistema
- Passo a passo de uso
- Sistema de envio de e-mail explicado
- Download da aplicação desktop
- Estatísticas em tempo real

#### 📝 Registro Diário
- Seleção de data
- Registro de valores 10%
- Controle de vales
- Tipo de pagamento
- Marcação de pago/pendente

#### 👥 Cadastrar Funcionários
- Formulário completo
- Validação de duplicados
- Filtro por nome
- Ordenação por data/nome/valor
- Deleção em massa

#### 📧 Enviar E-mail
- Configuração automática (usa settings)
- Geração de relatórios em múltiplos formatos
- Download direto
- Envio por e-mail com um clique

#### 📊 Histórico
- Métricas gerais (funcionários, registros, total, pago, pendente)
- Ranking de pagamentos
- Histórico de presença
- Histórico de pagamentos
- Data de cadastramento

#### 🗄️ Banco de Dados
- Visualização de todas as tabelas
- Carregamento de dados
- Interface simples e intuitiva

#### 📋 Logs
- Histórico de operações
- Atualização em tempo real

#### 📥 Download App Desktop
- Link direto para ZIP (120 MB)
- Instruções de uso
- Recursos disponíveis

#### ⚙️ Configurações
- Informações do sistema
- Status do banco de dados
- Configurações de e-mail

---

## [1.0.0] - 2026-02-24

### Added
- **Interface Desktop (Tkinter)** - Aplicação completa com interface gráfica
- **Sistema de Cadastro** - Cadastro de funcionários do restaurante
- **Registro de Trabalho Diário** - Registro de vendas e cálculo de 10% para cada funcionário
- **Envio de Emails** - Envio automático de relatórios por email com templates HTML
- **Geração de Relatórios** - Relatórios em múltiplos formatos:
  - DOCX (Word)
  - Excel (XLSX)
  - CSV
  - JSON
  - XML
  - HTML
- **Banco de Dados Supabase** - Integração completa com SupSistema de Logs**abase
- ** - Histórico de todas as operações
- **Módulo de Histórico** - Estatísticas e rankings:
  - Histórico de presença
  - Histórico de pagamentos
  - Data de cadastramento
  - Ranking de melhores pagamentos
- **Gerenciamento de BD** - Interface completa para gerenciar banco de dados:
  - Visualizar tabelas
  - Inserir registros
  - Atualizar registros
  - Deletar registros
- **Download do Código Fonte** - Opção para baixar todo o código
- **Interface Dark Theme** - Visual moderno com tema escuro
- **Documentação** - Manual do usuário completo
- **Executável** - Geração de executável para macOS e Windows

### Features Detalhadas

#### 👥 Cadastro de Funcionários (Desktop)
- Lista de funcionários do restaurante
- Cadastro rápido de novos funcionários
- Remoção de funcionários

#### 📝 Registro de Trabalho (Desktop)
- Seleção de data
- Cálculo automático de 10% das vendas
- Controle de entrada/saída
- Registro de vales
- Tipo de pagamento (pix/dinheiro)
- Marcação de pagamento

#### 📧 Envio de Relatórios (Desktop)
- Template HTML profissional
- Total de funcionários do dia
- Informações de dias trabalhados
- Detalhamento por funcionário

#### 📊 Histórico e Estatísticas (Desktop)
- Total de funcionários cadastrados
- Total de registros
- Dias trabalhados
- Total geral pago/pendente
- Ranking de pagamentos
- Histórico de presença por data

#### 🗄️ Banco de Dados (Desktop)
- Tabela: funcionarios
- Tabela: configuracoes
- Tabela: observacoes_gerais
- Tabela: registros_trabalho
- Tabela: logs

---

## [0.0.1] - 2026-01-01

### Added
- Projeto inicial
- Estrutura base
- Configurações Supabase

---

## Versões Futuras Planejadas

### [1.2.0] - Planejado
- [ ] Exportar relatório em PDF
- [ ] Backup automático do banco
- [ ] Relatórios mensais
- [ ] Gráficos de evolução
- [ ] Interface Web Streamlit completa
- [ ] Dashboard online
- [ ] Acesso via navegador

### [2.0.0] - Planejado
- [ ] Aplicativo mobile
- [ ] Offline mode
- [ ] Sincronização automática

---

## Agradecimentos

- Supabase pelo banco de dados
- Comunidade Python
- Tkinter pela interface gráfica
- Streamlit pela interface web
- openpyxl pela geração de Excel
- python-docx pela geração de Word
