# Sistema de Relatório de Salários de Garçons

Sistema para gerenciamento de salários de garçons com cálculo automático de 10% das vendas.

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [ Tecnologias](#-tecnologias)
- [Aplicações](#aplicações)
  - [Desktop (Tkinter)](#desktop-tkinter)
  - [Web (Streamlit)](#web-streamlit)
  - [Mobile (React Native/Expo)](#mobile-react-native-expo)
- [Instalação](#instalação)
- [Executando as Aplicações](#executando-as-aplicações)
- [Build Executável Desktop](#build-executável-desktop)
  - [macOS](#macos)
  - [Windows](#windows)
- [Autenticação](#autenticação)
- [Funcionalidades](#funcionalidades)
- [Banco de Dados](#banco-de-dados)
- [Licença](#licença)

---

## 📝 Sobre o Projeto

O Sistema de Relatório de Salários de Garçons automatiza o cálculo e envio de relatórios de comissões (10% das vendas) para garçons. O sistema conta com três interfaces diferentes:

- **Desktop**: Aplicação Python com Tkinter
- **Web**: Aplicação Python com Streamlit  
- **Mobile**: Aplicação React Native/Expo

Todas as aplicações compartilham o mesmo banco de dados Supabase e sistema de autenticação.

---

## 🛠 Tecnologias

| Componente | Tecnologia |
|------------|------------|
| Backend | Python 3.10+ |
| Banco de Dados | Supabase (PostgreSQL) |
| Autenticação | Supabase Auth |
| Desktop | Tkinter |
| Web | Streamlit |
| Mobile | React Native / Expo |
| Build Desktop | PyInstaller |

---

## 📱 Aplicações

### Desktop (Tkinter)

Aplicação desktop com interface gráfica completa:

```bash
cd ui/desktop
pip install -r requirements.txt
python app_tkinter.py
```

**Funcionalidades:**
- Cadastro de funcionários
- Registro diário de vendas
- Cálculo automático de 10%
- Envio de e-mail com relatórios
- Histórico e estatísticas
- Logs do sistema
- Configurações

### Web (Streamlit)

Aplicação web acessível via navegador:

```bash
cd ui/web
pip install -r requirements.txt
streamlit run app_streamlit.py
```

**Acesse:** `http://localhost:8501`

### Mobile (React Native/Expo)

Aplicação mobile para iOS e Android:

```bash
cd ui/mobile
npm install
npx expo start
```

**Funcionalidades:**
- Autenticação Supabase
- Cadastro de funcionários
- Registro diário
- Envio de e-mail
- Histórico e estatísticas
- Interface mobile otimizada

---

## 💻 Instalação

### 1. Clone o repositório

```bash
git clone <repositorio>
cd automacao
```

### 2. Configure o ambiente

#### Variáveis de Ambiente (.env)

Crie um arquivo `.env` na raiz do projeto:

```env
# Supabase
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-supabase

# E-mail (opcional)
EMAIL_DEFAULT=seu-email@gmail.com
SENHA_APP=senha-app-gmail
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```

### 3. Instale as dependências

```bash
# Python
pip install -r requirements.txt

# Node.js (para mobile)
cd ui/mobile
npm install
```

---

## 🚀 Executando as Aplicações

### Aplicação Desktop

```bash
cd ui/desktop
python app_tkinter.py
```

### Aplicação Web

```bash
cd ui/web
streamlit run app_streamlit.py
```

### Aplicação Mobile

```bash
cd ui/mobile
npx expo start
```

---

## 📦 Build Executável Desktop

### macOS

O build já está configurado. Execute:

```bash
cd ui/desktop
pyinstaller --clean app.spec
```

O executável será criado em:
```
ui/desktop/dist/SistemaSalariosGarcons
```

Para criar um arquivo compactado:

```bash
cd ui/desktop/dist
zip -r SistemaSalariosGarcons-Mac.zip SistemaSalariosGarcons
```

### Windows

Para compilar o executável no Windows:

1. **Instale Python 3.10+** no Windows
2. **Copie a pasta do projeto** para o Windows
3. **Execute o script de build:**

```bash
cd ui\desktop
build_windows.bat
```

Ou manualmente:

```cmd
pip install -r requirements.txt
pip install pyinstaller

pyinstaller --onedir --windowed --name SistemaSalariosGarcons ^
    --add-data "config;config" ^
    --hidden-import=supabase ^
    --hidden-import=tkinter ^
    --hidden-import=pandas ^
    --hidden-import=openpyxl ^
    --hidden-import=python_docx ^
    app_tkinter.py
```

O executável estará em: `dist\SistemaSalariosGarcons\SistemaSalariosGarcons.exe`

---

## 🔐 Autenticação

O sistema usa **Supabase Auth** para autenticação. As três aplicações (Desktop, Web, Mobile) compartilham o mesmo sistema de login.

### Credenciais

Use as mesmas credenciais em todas as aplicações:
- **E-mail**: Seu e-mail cadastrado
- **Senha**: Sua senha do Supabase Auth

### Criar Novo Usuário

Você pode criar novos usuários através do:
1. Aplicativo mobile (tela de registro)
2. Painel do Supabase (Authentication > Users)

---

## ⚙️ Funcionalidades

### Cadastro de Funcionários
- Adicionar novos funcionários
- Listar funcionários cadastrados
- Excluir funcionários

### Registro Diário
- Data do trabalho
- Nome do funcionário
- 10% das vendas (R$)
- Hora de entrada
- Hora de saída
- Vale (PIX/Dinheiro)
- Status de pagamento
- Observações

### Relatórios
- Geração em múltiplos formatos (DOCX, Excel, CSV, JSON, XML, HTML)
- Envio por e-mail com anexos

### Histórico e Estatísticas
- Total de funcionários
- Total de registros
- Total de dias trabalhados
- Total pago / pendente
- Ranking de pagamentos
- Histórico de presença
- Data de cadastramento

### Logs do Sistema
- Registro de todas as operações
- Filtragem por ação e tabela
- Limpeza de logs

### Configurações
- E-mail remetente
- E-mail destinatário
- Senha de app Gmail

---

## 🗄 Banco de Dados

### Tabelas

| Tabela | Descrição |
|---------|------------|
| `funcionarios` | Registro de funcionários e dias trabalhados |
| `configuracoes` | Configurações de e-mail |
| `observacoes_gerais` | Observações gerais por dia |
| `logs` | Histórico de ações no sistema |

### Configuração Supabase

1. Crie um projeto em [supabase.com](https://supabase.com)
2. Execute os scripts SQL em `sql/` para criar as tabelas
3. Configure as variáveis de ambiente com as credenciais

---

## 📄 Licença

Desenvolvido por **Estevam Souza**

---

## ❓ Suporte

Para dúvidas ou problemas:
1. Verifique as configurações do Supabase
2. Confirme as variáveis de ambiente
3. Verifique os logs do sistema
