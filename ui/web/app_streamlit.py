import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from data.models.funcionario import Funcionario, Configuracao, ObservacaoGeral
from data.repositories.supabase_repository import SupabaseRepository
from services.report_generator import ReportGenerator
from services.email_service import EmailService
from services.auth_service import auth_service
from config.settings import settings

st.set_page_config(
    page_title="Sistema de Salários - Garçons",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user = None

if not st.session_state.authenticated:
    st.markdown("""
    <style>
        .login-container {
            max-width: 400px;
            margin: 50px auto;
            padding: 40px;
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        .stApp { background: linear-gradient(135deg, #1e1e2f 0%, #2d2d44 100%); }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("### 🔐 Sistema de Salários")
        st.markdown("Faça login para continuar")
        
        email = st.text_input("E-mail", key="login_email")
        password = st.text_input("Senha", type="password", key="login_password")
        
        if st.button("Entrar", type="primary", use_container_width=True):
            if not email or not password:
                st.error("Preencha todos os campos")
            else:
                result = auth_service.sign_in(email, password)
                if result.get("success"):
                    st.session_state.authenticated = True
                    st.session_state.user = result.get("user")
                    st.rerun()
                else:
                    st.error(result.get("error", "Erro ao fazer login"))
        
        st.markdown("---")
        st.caption("Use as mesmas credenciais do app mobile")
    
    st.stop()

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #1e1e2f 0%, #2d2d44 100%); }
    .card { background: rgba(255,255,255,0.95); padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); margin: 10px 0; }
    h1, h2, h3, h4 { color: #00d4ff !important; font-weight: bold !important; }
    div[data-testid="stMetric"] { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 15px; border-radius: 10px; }
    div[data-testid="stMetricLabel"] { color: rgba(255,255,255,0.8) !important; }
    div[data-testid="stMetricValue"] { color: white !important; }
    .stButton > button { border-radius: 10px; font-weight: bold; }
    section[data-testid="stSidebar"] { background: rgba(0,0,0,0.3); }
    .stAlert { border-radius: 10px; }
    div[data-testid="stRadio"] > div { flex-direction: row; }
    div[data-testid="stRadio"] > div > label { margin-right: 15px; }
    .feature-icon { font-size: 48px; text-align: center; }
    .step-box { background: #2d2d44; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid #00d4ff; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 👤 Usuário")
    user_email = st.session_state.user.email if st.session_state.user else "Usuário"
    st.markdown(f"**{user_email}**")
    if st.button("Sair", use_container_width=True):
        auth_service.sign_out()
        st.session_state.authenticated = False
        st.session_state.user = None
        st.rerun()
    st.markdown("---")

if 'repository' not in st.session_state:
    st.session_state.repository = SupabaseRepository()

if 'funcionarios' not in st.session_state:
    st.session_state.funcionarios = []

def carregar_dados():
    st.session_state.funcionarios = st.session_state.repository.listar_todos_funcionarios()

def get_funcionarios_do_dia(dia: date) -> list:
    return [f for f in st.session_state.funcionarios if f.dia_trabalho == dia]

def main():
    st.title("💼 Sistema de Relatório de Salários dos Garçons")
    st.markdown("---")
    
    menu = st.sidebar.radio(
        "📋 Navegação",
        [
            "🏠 Home",
            "📝 Registro Diário",
            "👥 Cadastrar Funcionários", 
            "📧 Enviar E-mail",
            "📊 Histórico",
            "🗄️ Banco de Dados",
            "📋 Logs",
            "📥 Download App Desktop",
            "⚙️ Configurações"
        ]
    )
    
    with st.sidebar:
        st.markdown("---")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.metric("📅", date.today().strftime('%d/%m'))
        with col_s2:
            dia_semana = settings.DIAS_SEMANA.get(date.today().weekday(), "")
            st.metric("📆", dia_semana[:3] if dia_semana else "")
        st.markdown("---")
        st.caption("Desenvolvido por: Estevam Souza")
    
    if menu == "🏠 Home":
        pagina_home()
    elif menu == "📝 Registro Diário":
        pagina_registro_diario()
    elif menu == "👥 Cadastrar Funcionários":
        pagina_cadastro_funcionarios()
    elif menu == "📧 Enviar E-mail":
        pagina_enviar_email()
    elif menu == "📊 Histórico":
        pagina_historico()
    elif menu == "🗄️ Banco de Dados":
        pagina_banco_dados()
    elif menu == "📋 Logs":
        pagina_logs()
    elif menu == "📥 Download App Desktop":
        pagina_download_desktop()
    elif menu == "⚙️ Configurações":
        pagina_configuracoes()

def pagina_home():
    st.header("🏠 Bem-vindo ao Sistema!")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    ## 💼 Sistema de Relatório de Salários de Garçons
    
    Sistema completo para gerenciamento de salários de garçons baseado em 10% das vendas diárias.
    Gerencie funcionários, registre vendas, gere relatórios e envie por e-mail automaticamente.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("👥 Funcionários", "Cadastre")
    with col2: st.metric("📊 Relatórios", "Multi Formatos")
    with col3: st.metric("📧 E-mail", "Automático")
    
    st.markdown("---")
    
    st.header("🚀 Como Funciona")
    
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("### 1️⃣ Cadastre os Funcionários")
    st.markdown("""
    - Acesse a aba **Cadastrar Funcionários**
    - Adicione o nome e informações de cada funcionário
    - Defina o valor de 10% das vendas para cada um
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("### 2️⃣ Registre o Dia de Trabalho")
    st.markdown("""
    - Acesse a aba **Registro Diário**
    - Selecione a data desejada
    - Preencha os valores de vendas do dia
    - O sistema calcula automaticamente 10% para cada funcionário
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.markdown("### 3️⃣ Gere e Envie Relatórios")
    st.markdown("""
    - Acesse a aba **Enviar E-mail**
    - Escolha o formato desejado (Excel, Word, PDF, etc)
    - Gere para download ou envie diretamente por e-mail
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.header("📧 Sistema de Envio de E-mail")
    
    col_e1, col_e2 = st.columns(2)
    
    with col_e1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### ✉️ Como Enviar E-mail")
        st.markdown("""
        **Configuração Automática:**
        - O sistema já vem configurado com o e-mail do restaurante
        - Basta selecionar a data e clicar em "Enviar E-mail"
        
        **Relatório Enviado:**
        - Total de funcionários do dia
        - Valor de 10% de cada funcionário
        - Informações de entrada e saída
        - Dados de vales e pagamentos
        
        **Anexos:**
        - Excel (.xlsx)
        - Word (.docx)  
        - CSV, JSON, XML, HTML
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_e2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### ⚙️ Configurações de E-mail")
        st.markdown(f"""
        **E-mail Remetente:**
        - `{settings.EMAIL_DEFAULT}`
        
        **Servidor SMTP:**
        - Host: `{settings.SMTP_HOST}`
        - Porta: `{settings.SMTP_PORT}`
        - Segurança: TLS
        
        **Formato do E-mail:**
        - HTML profissional
        - Anexos automáticos
        - Relatório completo em tabela
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.header("📥 Download da Aplicação Desktop")
    
    col_d1, col_d2 = st.columns([2, 1])
    
    with col_d1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("""
        ### 🖥️ Aplicação Desktop (Tkinter)
        
        Você também pode usar a versão desktop do sistema que oferece:
        
        ✅ Interface completa e profissional
        ✅ Todas as funcionalidades da web
        ✅ Funciona offline (com internet para banco)
        ✅ Mais opções de configuração
        ✅ Visualização mais detalhada
        
        **Para baixar, vá na aba "📥 Download App Desktop" no menu lateral.**
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_d2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📊 Estatísticas")
        
        carregar_dados()
        todos = st.session_state.funcionarios
        nomes = len(set(f.nome for f in todos if f.nome))
        
        st.metric("Funcionários", nomes)
        st.metric("Registros", len(todos))
        st.metric("Total", f"R$ {sum(f.valor_10_percent for f in todos):.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.header("📋 Formatos de Relatório")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        st.markdown("""
        ### 📄 Documentos
        - **Word (.docx)**: Relatório formatado
        - **HTML (.html)**: Para web
        """)
    
    with col_f2:
        st.markdown("""
        ### 📊 Planilhas
        - **Excel (.xlsx)**: Com formatação
        - **CSV (.csv)**: Dados simples
        """)
    
    with col_f3:
        st.markdown("""
        ### 💾 Dados
        - **JSON**: Integração API
        - **XML**: Sistemas legados
        """)

def pagina_registro_diario():
    st.header("📝 Registro do Dia de Trabalho")
    
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 📅 Data do Trabalho")
            
            dia_selecionado = st.date_input("Selecione a data", date.today(), key="registro_dia")
            dia_semana = settings.DIAS_SEMANA.get(dia_selecionado.weekday(), "")
            
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.info(f"**{dia_semana}**")
            with col_d2:
                st.info(f"**{dia_selecionado.strftime('%d/%m/%Y')}**")
            
            carregar_dados()
            funcs_dia = get_funcionarios_do_dia(dia_selecionado)
            
            st.markdown("---")
            st.markdown("### 💵 Registrar Valores")
            
            if funcs_dia:
                for func in funcs_dia:
                    with st.expander(f"👤 {func.nome}"):
                        col_v1, col_v2 = st.columns(2)
                        with col_v1:
                            valor = st.number_input(f"10%", min_value=0.0, value=float(func.valor_10_percent), key=f"v_{func.id}", format="%.2f")
                        with col_v2:
                            vale = st.number_input("Vale", min_value=0.0, value=float(func.vale or 0), key=f"va_{func.id}", format="%.2f")
                        
                        col_p1, col_p2 = st.columns(2)
                        with col_p1:
                            tipo_pag = st.selectbox("Tipo", ["pix", "dinheiro"], index=0 if func.tipo_pagamento == "pix" else 1, key=f"tp_{func.id}")
                        with col_p2:
                            pago = st.checkbox("Pago", value=func.pago, key=f"pg_{func.id}")
                        
                        func.valor_10_percent = valor
                        func.vale = vale if vale > 0 else None
                        func.tipo_pagamento = tipo_pag
                        func.pago = pago
                        st.session_state.repository.atualizar_funcionario(func)
                
                st.success(f"✅ {len(funcs_dia)} registros atualizados!")
            else:
                st.warning("⚠️ Nenhum funcionário. Cadastre primeiro!")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f"### 📋 Registros de {dia_selecionado.strftime('%d/%m/%Y')}")
            
            carregar_dados()
            funcs_dia = get_funcionarios_do_dia(dia_selecionado)
            
            if funcs_dia:
                df = pd.DataFrame([
                    {"Nome": f.nome, "10%": f"R$ {f.valor_10_percent:.2f}", "Vale": f"R$ {f.vale:.2f}" if f.vale else "-", 
                     "Entrada": f.hora_entrada, "Saída": f.hora_saida, "Status": "✅" if f.pago else "⏳"}
                    for f in funcs_dia
                ])
                st.dataframe(df, hide_index=True)
                
                total = sum(f.valor_10_percent for f in funcs_dia)
                total_vale = sum(f.vale or 0 for f in funcs_dia)
                
                st.markdown("---")
                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1: st.metric("Funcionários", len(funcs_dia))
                with col_m2: st.metric("Total 10%", f"R$ {total:.2f}")
                with col_m3: st.metric("Total Vales", f"R$ {total_vale:.2f}")
            else:
                st.info(f"Nenhum registro")
            
            st.markdown('</div>', unsafe_allow_html=True)

def pagina_cadastro_funcionarios():
    st.header("👥 Cadastro de Funcionários")
    
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### ➕ Novo Funcionário")
            
            with st.form("cad_form"):
                nome = st.text_input("Nome *", placeholder="Nome completo")
                dia_trabalho = st.date_input("Data *", date.today())
                valor = st.number_input("Valor 10% *", min_value=0.0, step=0.01, format="%.2f", value=0.0)
                
                col_h1, col_h2 = st.columns(2)
                with col_h1: hora_entrada = st.time_input("Entrada", datetime.strptime("08:00", "%H:%M"))
                with col_h2: hora_saida = st.time_input("Saída", datetime.strptime("16:00", "%H:%M"))
                
                col_v1, col_v2 = st.columns(2)
                with col_v1: vale = st.number_input("Vale", min_value=0.0, step=0.01, format="%.2f", value=0.0)
                with col_v2: tipo_vale = st.selectbox("Tipo Vale", ["pix", "dinheiro"], index=0)
                
                observacao = st.text_area("Observação", placeholder="Opcional...")
                
                submitted = st.form_submit_button("✅ Cadastrar")
                
                if submitted:
                    if nome and valor > 0:
                        try:
                            existente = st.session_state.repository.buscar_funcionario_por_nome_e_data(nome, dia_trabalho)
                            if existente:
                                st.warning(f"⚠️ {nome} já cadastrado!")
                            else:
                                func = Funcionario(nome=nome, valor_10_percent=valor, hora_entrada=hora_entrada.strftime("%H:%M"),
                                    hora_saida=hora_saida.strftime("%H:%M"), dia_trabalho=dia_trabalho, vale=vale if vale > 0 else None,
                                    tipo_vale=tipo_vale, observacao=observacao)
                                st.session_state.repository.cadastrar_funcionario(func)
                                st.success("✅ Cadastrado!")
                                carregar_dados()
                        except Exception as e: st.error(f"❌ {e}")
                    else: st.error("⚠️ Nome e valor obrigatórios")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 📋 Todos os Funcionários")
            
            carregar_dados()
            todos = st.session_state.funcionarios
            
            if todos:
                nomes = sorted(list(set(f.nome for f in todos if f.nome)))
                col_f1, col_f2 = st.columns(2)
                with col_f1: filtro_nome = st.selectbox("Filtrar", ["Todos"] + nomes)
                with col_f2: ordenar = st.selectbox("Ordenar", ["Data", "Nome", "Valor"])
                
                if filtro_nome != "Todos": todos = [f for f in todos if f.nome == filtro_nome]
                
                if ordenar == "Data": todos = sorted(todos, key=lambda x: x.dia_trabalho or date.min, reverse=True)
                elif ordenar == "Nome": todos = sorted(todos, key=lambda x: x.nome or "")
                elif ordenar == "Valor": todos = sorted(todos, key=lambda x: x.valor_10_percent, reverse=True)
                
                df = pd.DataFrame([
                    {"Nome": f.nome, "Data": f.dia_trabalho.strftime('%d/%m/%Y') if f.dia_trabalho else "-",
                     "10%": f"R$ {f.valor_10_percent:.2f}", "Vale": f"R$ {f.vale:.2f}" if f.vale else "-",
                     "Entrada": f.hora_entrada, "Saída": f.hora_saida}
                    for f in todos
                ])
                st.dataframe(df, hide_index=True)
                
                st.markdown("---")
                col_t1, col_t2 = st.columns(2)
                with col_t1: st.metric("Total Geral", f"R$ {sum(f.valor_10_percent for f in todos):.2f}")
                with col_t2: st.metric("Registros", len(todos))
                
                if st.button("🗑️ Deletar Todos"):
                    try:
                        for f in todos: st.session_state.repository.deletar_funcionario(str(f.id))
                        st.success("Deletado!")
                        carregar_dados()
                        st.rerun()
                    except Exception as e: st.error(f"Erro: {e}")
            else: st.info("Nenhum funcionário")
            
            st.markdown('</div>', unsafe_allow_html=True)

def pagina_enviar_email():
    st.header("📧 Enviar Relatório por E-mail")
    
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 📤 Configuração do E-mail")
            
            config = st.session_state.repository.get_configuracao()
            
            st.info(f"""
            **E-mail Remetente:**
            - `{settings.EMAIL_DEFAULT}`
            
            **Status:** ✅ Configurado automaticamente
            
            O sistema usa as configurações do sistema desktop.
            """)
            
            data_rel = st.date_input("Data do Relatório", date.today())
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 📊 Gerar e Enviar Relatório")
            
            formato = st.selectbox("Formato", ["HTML", "Excel", "DOCX", "CSV", "JSON", "XML"], index=0)
            
            carregar_dados()
            funcs = get_funcionarios_do_dia(data_rel)
            
            if funcs:
                df = pd.DataFrame([{"Nome": f.nome, "10%": f.valor_10_percent, "Entrada": f.hora_entrada, "Saída": f.hora_saida, "Vale": f.vale or 0} for f in funcs])
                st.dataframe(df, hide_index=True)
                
                total = sum(f.valor_10_percent for f in funcs)
                st.metric("Total", f"R$ {total:.2f}")
                
                st.markdown("---")
                col_b1, col_b2 = st.columns(2)
                
                with col_b1:
                    if st.button("📥 Gerar Relatório"):
                        try:
                            report = ReportGenerator(funcs, data_rel)
                            if formato == "HTML": dados = report.generate_html(); st.download_button("📥 Download", dados, f"relatorio_{data_rel}.html", "text/html")
                            elif formato == "Excel": dados = report.generate_excel(); st.download_button("📥 Download", dados, f"relatorio_{data_rel}.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                            elif formato == "DOCX": dados = report.generate_docx(); st.download_button("📥 Download", dados, f"relatorio_{data_rel}.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                            elif formato == "CSV": dados = report.generate_csv(); st.download_button("📥 Download", dados, f"relatorio_{data_rel}.csv", "text/csv")
                            elif formato == "JSON": dados = report.generate_json(); st.download_button("📥 Download", dados, f"relatorio_{data_rel}.json", "application/json")
                            elif formato == "XML": dados = report.generate_xml(); st.download_button("📥 Download", dados, f"relatorio_{data_rel}.xml", "application/xml")
                            st.success("✅ Gerado!")
                        except Exception as e: st.error(f"❌ {e}")
                
                with col_b2:
                    email_dest = config.email_destinatario if config else "estevams186@gmail.com"
                    if st.button("📧 Enviar E-mail"):
                        try:
                            svc = EmailService(remetente=settings.EMAIL_DEFAULT, senha=settings.SENHA_APP)
                            report = ReportGenerator(funcs, data_rel)
                            dia = settings.DIAS_SEMANA.get(data_rel.weekday(), "")
                            ok = svc.enviar_relatorio_com_anexos(email_dest, funcs, data_rel, dia, report)
                            if ok: st.success(f"✅ Enviado para {email_dest}!")
                            else: st.error("❌ Falha")
                        except Exception as e: st.error(f"❌ {e}")
            else: st.warning(f"Nenhum para {data_rel.strftime('%d/%m/%Y')}")
            
            st.markdown('</div>', unsafe_allow_html=True)

def pagina_historico():
    st.header("📊 Histórico e Estatísticas")
    
    carregar_dados()
    todos = st.session_state.funcionarios
    
    if not todos: st.warning("Nenhum dado"); return
    
    nomes = list(set(f.nome for f in todos if f.nome))
    
    col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
    with col_m1: st.metric("👥", len(nomes))
    with col_m2: st.metric("📝", len(todos))
    with col_m3: st.metric("💰", f"R$ {sum(f.valor_10_percent for f in todos):.2f}")
    with col_m4: st.metric("✅", f"R$ {sum(f.valor_10_percent for f in todos if f.pago):.2f}")
    with col_m5: st.metric("⏳", f"R$ {sum(f.valor_10_percent for f in todos if not f.pago):.2f}")
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🏆 Ranking", "📅 Presença", "💵 Pagamentos", "📋 Cadastro"])
    
    with tab1:
        st.markdown("### 🏆 Ranking")
        dados = {}
        for f in todos:
            if f.nome not in dados: dados[f.nome] = {"dias": 0, "total": 0, "pago": 0, "pendente": 0}
            dados[f.nome]["dias"] += 1
            dados[f.nome]["total"] += f.valor_10_percent
            if f.pago: dados[f.nome]["pago"] += f.valor_10_percent
            else: dados[f.nome]["pendente"] += f.valor_10_percent
        
        ranking = [{"Pos": i+1, "Nome": n, "Dias": d["dias"], "Total": f"R$ {d['total']:.2f}", "Média": f"R$ {d['total']/d['dias']:.2f}", "Pago": f"R$ {d['pago']:.2f}", "Pendente": f"R$ {d['pendente']:.2f}"} for i, (n, d) in enumerate(sorted(dados.items(), key=lambda x: x[1]["total"], reverse=True))]
        if ranking: st.dataframe(pd.DataFrame(ranking), hide_index=True)
    
    with tab2:
        st.markdown("### 📅 Presença")
        filtro = st.date_input("Filtrar", value=None, key="f_pres")
        pres = todos if not filtro else [f for f in todos if f.dia_trabalho == filtro]
        df = pd.DataFrame([{"Data": f.dia_trabalho.strftime('%d/%m/%Y') if f.dia_trabalho else "-", "Nome": f.nome, "Entrada": f.hora_entrada, "Saída": f.hora_saida, "Valor": f"R$ {f.valor_10_percent:.2f}"} for f in pres])
        st.dataframe(df, hide_index=True)
    
    with tab3:
        st.markdown("### 💵 Pagamentos")
        fnome = st.selectbox("Funcionário", ["Todos"] + nomes, key="f_pag")
        pgts = todos if fnome == "Todos" else [f for f in todos if f.nome == fnome]
        df = pd.DataFrame([{"Nome": f.nome, "Data": f.dia_trabalho.strftime('%d/%m/%Y') if f.dia_trabalho else "-", "Valor": f"R$ {f.valor_10_percent:.2f}", "Tipo": f.tipo_pagamento, "Status": "✅" if f.pago else "⏳"} for f in pgts])
        st.dataframe(df, hide_index=True)
    
    with tab4:
        st.markdown("### 📋 Cadastro")
        cads = {}
        for f in todos:
            if f.nome not in cads: cads[f.nome] = {"prim": f.dia_trabalho, "ult": f.dia_trabalho, "dias": 0, "total": 0}
            cads[f.nome]["dias"] += 1; cads[f.nome]["total"] += f.valor_10_percent
            if f.dia_trabalho:
                if cads[f.nome]["prim"] is None or f.dia_trabalho < cads[f.nome]["prim"]: cads[f.nome]["prim"] = f.dia_trabalho
                if cads[f.nome]["ult"] is None or f.dia_trabalho > cads[f.nome]["ult"]: cads[f.nome]["ult"] = f.dia_trabalho
        df = pd.DataFrame([{"Nome": n, "Primeiro": d["prim"].strftime('%d/%m/%Y') if d["prim"] else "-", "Último": d["ult"].strftime('%d/%m/%Y') if d["ult"] else "-", "Dias": d["dias"], "Total": f"R$ {d['total']:.2f}"} for n, d in cads.items()])
        st.dataframe(df, hide_index=True)

def pagina_banco_dados():
    st.header("🗄️ Gerenciar Banco de Dados")
    
    tabela = st.selectbox("Tabela", ["funcionarios", "configuracoes", "observacoes_gerais", "registros_trabalho", "logs"])
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f"### 📋 {tabela}")
            
            if st.button("🔄 Carregar"):
                try:
                    dados = st.session_state.repository.client.table(tabela).select("*").execute()
                    st.session_state.dados = dados.data
                    st.success(f"{len(dados.data)} registros")
                except Exception as e: st.error(f"Erro: {e}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 📊 Dados")
            if 'dados' in st.session_state and st.session_state.dados:
                st.dataframe(pd.DataFrame(st.session_state.dados), hide_index=True)
            else: st.info("Carregue os dados")
            st.markdown('</div>', unsafe_allow_html=True)

def pagina_logs():
    st.header("📋 Logs do Sistema")
    
    col_l1, _ = st.columns([1, 4])
    with col_l1:
        if st.button("🔄 Atualizar"):
            try:
                logs = st.session_state.repository.listar_logs(limite=200)
                st.session_state.logs = logs
            except Exception as e: st.error(f"Erro: {e}")
    
    st.markdown("---")
    if 'logs' in st.session_state and st.session_state.logs:
        df = pd.DataFrame([{"Data": l.created_at[:19] if l.created_at else "-", "Ação": l.acao, "Tabela": l.tabela, "Usuário": l.usuario} for l in st.session_state.logs])
        st.dataframe(df, hide_index=True)
        st.metric("Total", len(st.session_state.logs))
    else: st.info("Nenhum log")

def pagina_download_desktop():
    st.header("📥 Download Aplicação Desktop")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    ### 🖥️ Aplicação Desktop (Tkinter)
    
    A versão desktop oferece uma experiência completa com interface rica em recursos.
    
    **Recursos disponíveis:**
    - ✅ Interface profissional com tema escuro
    - ✅ Registro diário de trabalho
    - ✅ Cadastro de funcionários
    - ✅ Envio de relatórios por e-mail
    - ✅ Histórico e estatísticas
    - ✅ Gerenciamento do banco de dados
    - ✅ Logs do sistema
    - ✅ Download do código fonte
    - ✅ Geração de executável
    
    **Para usar:**
    1. Baixe o arquivo abaixo
    2. Descompacte
    3. Execute o arquivo `SistemaSalariosGarcons`
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### 📦 Download")
    
    dist_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "dist", "SistemaSalariosGarcons.zip")
    
    if os.path.exists(dist_path):
        try:
            with open(dist_path, "rb") as f:
                st.download_button(
                    label="📥 Baixar Aplicação Desktop (ZIP)",
                    data=f,
                    file_name="SistemaSalariosGarcons.zip",
                    mime="application/zip"
                )
            st.success(f"✅ Arquivo disponível! Tamanho: {os.path.getsize(dist_path) / 1024 / 1024:.1f} MB")
        except Exception as e:
            st.error(f"Erro ao carregar: {e}")
    else:
        st.warning("⚠️ Arquivo não encontrado no servidor.")
        st.info("O arquivo precisa ser gerado primeiro. Execute o build no servidor.")
        
        st.markdown("---")
        st.markdown("### 🔧 Gerar Executável")
        
        st.markdown("""
        Para gerar o executável, execute no terminal:
        ```bash
        ./build_exe.sh
        ```
        
        O arquivo será criado em: `dist/SistemaSalariosGarcons.zip`
        """)

def pagina_configuracoes():
    st.header("⚙️ Configurações")
    
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 📧 E-mail")
            
            config = st.session_state.repository.get_configuracao()
            
            st.markdown(f"""
            **Remetente:** `{settings.EMAIL_DEFAULT}`
            
            **Destinatário:** `{config.email_destinatario if config else 'Não configurado'}`
            
            **Servidor SMTP:**
            - Host: `{settings.SMTP_HOST}`
            - Porta: `{settings.SMTP_PORT}`
            """)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### ℹ️ Informações")
            
            col_i1, col_i2 = st.columns(2)
            with col_i1: st.metric("📅", date.today().strftime('%d/%m/%Y'))
            with col_i2: st.metric("📆", settings.DIAS_SEMANA.get(date.today().weekday()))
            
            st.markdown("---")
            st.markdown("### 🔗 Supabase")
            st.code(f"{settings.SUPABASE_URL[:40]}...", language="text")
            
            st.markdown("---")
            st.markdown("### 📋 Tabelas")
            for t in ["funcionarios", "configuracoes", "observacoes_gerais", "registros_trabalho", "logs"]:
                try:
                    d = st.session_state.repository.client.table(t).select("*").execute()
                    st.write(f"📊 **{t}**: {len(d.data)}")
                except: st.write(f"📊 **{t}**: erro")
            
            st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
