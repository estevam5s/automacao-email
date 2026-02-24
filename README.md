# Sistema de Relatório de Salários de Garçons

Aplicação desktop e web para gerenciamento e envio de relatórios de salários de garçons (10% das vendas), com armazenamento em banco de dados Supabase e envio de e-mails automatizados.

## Índice

1. [Visão Geral](#visão-geral)
2. [Arquitetura do Projeto](#arquitetura-do-projeto)
3. [Pré-requisitos](#pré-requisitos)
4. [Instalação](#instalação)
5. [Configuração](#configuração)
6. [Executando a Aplicação](#executando-a-aplicação)
7. [Estrutura de Arquivos](#estrutura-de-arquivos)
8. [Uso da Aplicação Desktop (Tkinter)](#uso-da-aplicação-desktop-tkinter)
   - [Aba Cadastrar](#aba-cadastrar)
   - [Aba Registrar Dia](#aba-registrar-dia)
   - [Aba Enviar E-mail](#aba-enviar-e-mail)
   - [Aba Configurações](#aba-configurações)
9. [Uso da Aplicação Web (Streamlit)](#uso-da-aplicação-web-streamlit)
10. [Geração de Relatórios](#geração-de-relatórios)
11. [Banco de Dados Supabase](#banco-de-dados-supabase)
12. [Solução de Problemas](#solução-de-problemas)
13. [Licença](#licença)

---

## Visão Geral

Este sistema foi desenvolvido para automatizar o processo de cálculo e envio de relatórios de salários de garçons. O garçom recebe 10% das vendas do dia como comissão, e o sistema facilita o registro diário, cálculo automático e envio de relatório por e-mail.

### Principais Funcionalidades

- **Cadastro de Funcionários**: Gerencie a lista de garçons
- **Registro Diário**: Registre vendas, horas trabalhadas, vales e observações
- **Cálculo Automático**: Cálculo automático de 10% sobre vendas
- **Relatórios em Múltiplos Formatos**: DOCX, Excel, CSV, JSON, XML, HTML
- **Envio Automatizado por E-mail**: Relatórios enviados automaticamente para o gerente
- **Interface Desktop (Tkinter)**: Aplicação desktop completa
- **Interface Web (Streamlit)**: Alternativa web para acesso remoto

---

## Arquitetura do Projeto

```
automacao/
├── config/                  # Configurações da aplicação
│   └── settings.py          # Parâmetros de configuração
├── data/                    # Camada de dados
│   ├── models/              # Modelos de dados
│   │   └── funcionario.py  # Classes de domínio
│   └── repositories/        # Repositórios de dados
│       └── supabase_repository.py
├── services/                # Serviços de negócio
│   ├── email_service.py     # Envio de e-mails
│   └── report_generator.py  # Geração de relatórios
├── ui/                      # Interfaces de usuário
│   ├── desktop/             # Aplicação Tkinter
│   │   └── app_tkinter.py
│   └── web/                 # Aplicação Streamlit
│       └── app_streamlit.py
├── sql/                     # Scripts SQL para banco de dados
├── domain/                  # Camada de domínio (use cases)
├── doc/                     # Documentação adicional
├── requirements.txt         # Dependências Python
└── run_tkinter.sh          # Script de inicialização
```

### Padrão de Arquitetura

O projeto segue uma arquitetura em camadas:

1. **UI Layer** (`ui/`): Interfacesgráficas (Tkinter, Streamlit)
2. **Service Layer** (`services/`): Lógicas de negócio
3. **Data Layer** (`data/`): Modelos e repositórios
4. **Config Layer** (`config/`): Configurações globais

---

## Pré-requisitos

- **Python 3.10+**
- **Supabase**: Conta criada e projeto configurado
- **Gmail**: Conta com senha de app configurada (para envio de e-mails)
- **Sistema Operacional**: macOS, Linux ou Windows

---

## Instalação

### 1. Clone o Repositório

```bash
cd /caminho/para/projeto
```

### 2. Crie um Ambiente Virtual

```bash
python -m venv venv
```

### 3. Ative o Ambiente Virtual

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Instale as Dependências

```bash
pip install -r requirements.txt
```

---

## Configuração

### Configurações do Banco de Dados (Supabase)

As configurações do banco de dados estão em `config/settings.py`:

```python
SUPABASE_URL: str = "https://seu-projeto.supabase.co"
SUPABASE_KEY: str = "sua-chave-api"
```

### Configurações de E-mail

```python
EMAIL_DEFAULT: str = "seu-email@gmail.com"
SENHA_APP: str = "sua-senha-de-app"
SMTP_HOST: str = "smtp.gmail.com"
SMTP_PORT: int = 587
```

### Criando uma Senha de App no Gmail

1. Acesse: https://myaccount.google.com/apppasswords
2. Faça login com sua conta Google
3. Em "Selecione o app", escolha **E-mail**
4. Em "Selecione o dispositivo", escolha **Outro** e digite um nome
5. Clique em **Gerar**
6. Copie a senha gerada (16 caracteres)

### Configuração do Banco de Dados

Execute os scripts SQL em `sql/scripts.sql` no editor SQL do Supabase para criar as tabelas necessárias:

```sql
-- Tabela principal de funcionários
CREATE TABLE public.funcionarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome TEXT NOT NULL,
    valor_10_percent DECIMAL(10, 2) NOT NULL,
    hora_entrada TIME NOT NULL,
    hora_saida TIME NOT NULL,
    dia_trabalho DATE NOT NULL,
    observacao TEXT,
    vale DECIMAL(10, 2),
    tipo_vale TEXT,
    pago BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de configurações
CREATE TABLE public.configuracoes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email_destinatario TEXT NOT NULL,
    email_remetente TEXT NOT NULL,
    senha_app TEXT NOT NULL,
    smtp_host TEXT DEFAULT 'smtp.gmail.com',
    smtp_port INTEGER DEFAULT 587
);

-- Tabela de observações gerais
CREATE TABLE public.observacoes_gerais (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dia_trabalho DATE NOT NULL UNIQUE,
    observacao TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## Executando a Aplicação

### Aplicação Desktop (Tkinter)

```bash
# Usando o script shell
./run_tkinter.sh

# Ou manualmente
source venv/bin/activate
export PYTHONPATH=.
python ui/desktop/app_tkinter.py
```

### Aplicação Web (Streamlit)

```bash
source venv/bin/activate
streamlit run ui/web/app_streamlit.py
```

A aplicação web estará disponível em: http://localhost:8501

---

## Estrutura de Arquivos

### config/settings.py

Arquivo principal de configurações da aplicação.

| Parâmetro | Descrição |
|-----------|------------|
| `SUPABASE_URL` | URL do projeto Supabase |
| `SUPABASE_KEY` | Chave API do Supabase |
| `EMAIL_DEFAULT` | E-mail remetente padrão |
| `SENHA_APP` | Senha de app do Gmail |
| `SMTP_HOST` | Servidor SMTP |
| `SMTP_PORT` | Porta SMTP (587 para TLS) |

### data/models/funcionario.py

Modelos de dados da aplicação:

- **Funcionario**: Dados de um funcionário
- **ObservacaoGeral**: Observações gerais do dia
- **Configuracao**: Configurações de e-mail

### data/repositories/supabase_repository.py

Repositório para operações com o banco de dados Supabase:

- `cadastrar_funcionario()`: Cadastra novo funcionário
- `listar_funcionarios()`: Lista funcionários por data
- `listar_todos_funcionarios()`: Lista todos os funcionários
- `atualizar_funcionario()`: Atualiza dados de funcionário
- `deletar_funcionario()`: Remove funcionário
- `salvar_configuracao()`: Salva configurações
- `get_configuracao()`: Recupera configurações
- `salvar_observacao_geral()`: Salva observação geral

### services/email_service.py

Serviço de envio de e-mails:

- `enviar_relatorio()`: Envia relatório com/opcionalmente anexos
- `enviar_relatorio_com_anexos()`: Envia relatório com todos os formatos

### services/report_generator.py

Gerador de relatórios em múltiplos formatos:

- `generate_docx()`: Gera relatório em Word
- `generate_excel()`: Gera relatório em Excel
- `generate_csv()`: Gera relatório em CSV
- `generate_json()`: Gera relatório em JSON
- `generate_xml()`: Gera relatório em XML
- `generate_html()`: Gera relatório em HTML
- `generate_all()`: Gera todos os formatos

### ui/desktop/app_tkinter.py

Aplicação desktop com interface Tkinter.

### ui/web/app_streamlit.py

Aplicação web com interface Streamlit.

---

## Uso da Aplicação Desktop (Tkinter)

A aplicação possui 4 abas principais:

### Aba Cadastrar

Funcionalidades:
- **Cadastrar novo funcionário**: Digite o nome e clique em "Cadastrar"
- **Listar funcionários**: Visualize todos os funcionários cadastrados
- **Deletar funcionário**: Selecione um funcionário e clique em "Deletar"

### Aba Registrar Dia

Funcionalidades:
- **Selecionar data**: Escolha a data de trabalho no formato YYYY-MM-DD
- **Carregar dados**: Clique em "Carregar" para ver registros existentes
- **Registrar funcionário**:
  - Selecione o funcionário na lista suspensa
  - Digite o valor de 10% das vendas
  - Informe hora de entrada (formato HH:MM)
  - Informe hora de saída (formato HH:MM)
  - (Opcional) Digite o valor do vale
  - (Opcional) Selecione o tipo de vale (pix/dinheiro)
  - (Opcional) Marque "Pago" se já pagou
  - (Opcional) Adicione uma observação
- **Salvar registros**: Clique em "Salvar"

### Aba Enviar E-mail

Funcionalidades:
- **Selecionar data**: Escolha a data do relatório
- **Carregar dados**: Carregue os registros do dia
- **Editar observação geral**: Adicione observações gerais do dia
- **Visualizar registros**: See todos os funcionários e valores
- **Gerar relatórios**: Selecione o formato desejado e clique em "Gerar"
- **Enviar e-mail**: Clique em "Enviar E-mail" para enviar ao destinatário

### Aba Configurações

Funcionalidades:
- **E-mail remetente**: Configure o e-mail que envia
- **E-mail destinatário**: Configure o e-mail que recebe
- **Senha**: Configure a senha de app do Gmail

---

## Uso da Aplicação Web (Streamlit)

### Página Inicial

1. **Título e Informações**: Visualize o título do sistema
2. **Navegação**: Use o menu lateral para navegar entre as seções

### Seção Registro

- Selecione a data de trabalho
- Preencha os dados do funcionário:
  - Nome
  - Valor de 10% das vendas
  - Hora de entrada
  - Hora de saída
  - Vale (opcional)
  - Tipo de vale (opcional)
  - Pago (checkbox)
  - Observação (opcional)
- Clique em "Registrar"

### Seção Listar

- Selecione a data desejada
- Visualize a tabela com todos os registros
- See o total a pagar

### Seção Relatório

- Selecione a data
- Escolha o formato do relatório
- Clique em "Gerar Relatório"
- Faça o download do arquivo

### Seção Enviar E-mail

- Selecione a data
- Carregue os dados
- Confirme o e-mail do destinatário
- Clique em "Enviar E-mail"

---

## Geração de Relatórios

A aplicação gera relatórios nos seguintes formatos:

| Formato | Extensão | Descrição |
|---------|----------|------------|
| Word | .docx | Documento formatado do Microsoft Word |
| Excel | .xlsx | Planilha do Microsoft Excel |
| CSV | .csv | Arquivo separado por vírgulas |
| JSON | .json | Formato JavaScript Object Notation |
| XML | .xml | Extensible Markup Language |
| HTML | .html | Página web formatada |

### Conteúdo do Relatório

Cada relatório contém:
- Data de trabalho e dia da semana
- Total de funcionários
- Total a pagar (soma de 10%)
- Tabela com cada funcionário:
  - Nome
  - Valor de 10%
  - Hora de entrada
  - Hora de saída
  - Vale
  - Tipo de vale
  - Pago (sim/não)
  - Observação

---

## Banco de Dados Supabase

### Tabelas

#### public.funcionarios

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id | UUID | Identificador único |
| nome | TEXT | Nome do funcionário |
| valor_10_percent | DECIMAL | Valor de 10% das vendas |
| hora_entrada | TIME | Hora de entrada |
| hora_saida | TIME | Hora de saída |
| dia_trabalho | DATE | Data do trabalho |
| observacao | TEXT | Observação do dia |
| vale | DECIMAL | Valor do vale |
| tipo_vale | TEXT | Tipo do vale (pix/dinheiro) |
| pago | BOOLEAN | Se foi pago |
| created_at | TIMESTAMP | Data de criação |
| updated_at | TIMESTAMP | Data de atualização |

#### public.configuracoes

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id | UUID | Identificador único |
| email_destinatario | TEXT | E-mail do destinatário |
| email_remetente | TEXT | E-mail do remetente |
| senha_app | TEXT | Senha de app do Gmail |
| smtp_host | TEXT | Servidor SMTP |
| smtp_port | INTEGER | Porta SMTP |

#### public.observacoes_gerais

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id | UUID | Identificador único |
| dia_trabalho | DATE | Data (único) |
| observacao | TEXT | Observação geral |
| created_at | TIMESTAMP | Data de criação |

---

## Solução de Problemas

### Erro ao Conectar ao Supabase

```
Erro: conexão falhou
```

**Solução**:
1. Verifique se a URL e chave do Supabase estão corretas em `config/settings.py`
2. Verifique se o projeto Supabase está ativo
3. Verifique a conexão de internet

### Erro ao Enviar E-mail

```
Erro ao enviar e-mail: (535, b'5.7.8 Username and Password not accepted')
```

**Solução**:
1. A senha de app pode ter expirado - gere uma nova em https://myaccount.google.com/apppasswords
2. Verifique se o e-mail remetente está correto
3. Certifique-se de que a senha não contém espaços extras

### Erro ao Salvar Dados

```
invalid input syntax for type time
```

**Solução**:
1. Use o formato HH:MM para hora (ex: 08:00, 16:30)
2. O sistema agora converte automaticamente se você digitar apenas "8" para "8:00"

### Interface Não Aparece

**Solução**:
1. Verifique se o Tkinter está instalado: `python -c "import tkinter; print(tkinter.TkVersion)"`
2. No Windows, talvez seja necessário instalar o Python com suporte a Tkinter
3. No macOS, use: `brew install python-tk`

###DependênciasFaltantes

```
ModuleNotFoundError: No module named 'xxx'
```

**Solução**:
```bash
pip install -r requirements.txt
```

---

## Rotas da Aplicação Tkinter

### Estrutura de Rotas/Abas

```
AppTkinter
├── Tab 1: Cadastrar (👥)
│   ├── Form: Novo Funcionário
│   │   ├── entry_nome (Entrada de texto)
│   │   └── btn_cadastrar (Botão)
│   └── Table: Funcionários
│       ├── tree_cadastro (Treeview)
│       └── btn_deletar (Botão)
│
├── Tab 2: Registrar Dia (📝)
│   ├── Frame: Data do Trabalho
│   │   ├── entry_dia (Data)
│   │   └── btn_carregar (Botão)
│   ├── Frame: Registrar
│   │   ├── combo_funcionarios (Combobox)
│   │   ├── entry_10 (10% valor)
│   │   ├── entry_entrada (Hora)
│   │   ├── entry_saida (Hora)
│   │   ├── btn_add (Botão Adicionar)
│   │   ├── entry_vale (Vale)
│   │   ├── combo_tipo (Tipo vale)
│   │   ├── checkbutton_pago (Pago)
│   │   ├── entry_obs (Observação)
│   │   ├── btn_salvar (Botão)
│   │   └── tree_registrar (Tabela)
│
├── Tab 3: Enviar E-mail (📧)
│   ├── Frame: Data
│   │   ├── entry_dia_envio (Data)
│   │   └── btn_carregar (Botão)
│   ├── Frame: Observação Geral
│   │   └── txt_obs (Texto)
│   ├── Frame: Funcionários
│   │   └── tree_envio (Tabela)
│   ├── Frame: Enviar E-mail
│   │   ├── entry_email (E-mail)
│   │   ├── btn_enviar (Botão)
│   │   └── lbl_total (Label)
│   └── Frame: Gerar
│       ├── combo_formato (Formato)
│       └── btn_gerar (Botão)
│
└── Tab 4: Configurações (⚙️)
    ├── entry_remetente (E-mail)
    ├── entry_dest (E-mail)
    ├── entry_senha (Senha)
    └── btn_salvar (Botão)
```

### Métodos Principais

| Método | Descrição |
|--------|-----------|
| `__init__` | Inicializa a aplicação |
| `setup_styles` | Configura estilos da interface |
| `create_widgets` | Cria todos os widgets |
| `create_tab_cadastro` | Cria aba de cadastro |
| `create_tab_registrar` | Cria aba de registro |
| `create_tab_envio` | Cria aba de envio |
| `create_tab_config` | Cria aba de configurações |
| `cadastrar_funcionario` | Cadastra novo funcionário |
| `deletar_funcionario` | Remove funcionário |
| `carregar_dia` | Carrega registros do dia |
| `adicionar_registro` | Adiciona registro |
| `salvar_registros` | Salva registros |
| `carregar_dia_envio` | Carrega dados para envio |
| `atualizar_tree_envio` | Atualiza tabela de envio |
| `salvar_obs_geral` | Salva observação geral |
| `gerar_relatorio` | Gera relatório |
| `enviar_email` | Envia e-mail |
| `salvar_config` | Salva configurações |

---

## Contribuição

Para contribuir com o projeto:

1. Fork o repositório
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Crie um Pull Request

---

## Licença

Este projeto está sob licença MIT. Veja o arquivo LICENSE para mais detalhes.

---

## Contato

Para dúvidas ou problemas, entre em contato com o desenvolvedor.

---

Desenvolvido com ❤️ usando Python, Tkinter, Streamlit e Supabase
