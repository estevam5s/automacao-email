import streamlit as st
import pandas as pd
from datetime import date, datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.models.funcionario import Funcionario, Configuracao
from data.repositories.supabase_repository import SupabaseRepository
from services.report_generator import ReportGenerator
from services.email_service import EmailService
from config.settings import settings

st.set_page_config(
    page_title="Sistema de Salários - Garçons",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main { background-color: #f5f5f5; }
    .stButton > button { 
        width: 100%; 
        border-radius: 8px;
        font-weight: bold;
    }
    .success-message { padding: 15px; border-radius: 8px; background: #E8F5E9; color: #2E7D32; }
    .error-message { padding: 15px; border-radius: 8px; background: #FFEBEE; color: #C62828; }
    .card { 
        background: white; 
        padding: 20px; 
        border-radius: 10px; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1 { color: #1B5E20; }
    h2 { color: #2E7D32; }
</style>
""", unsafe_allow_html=True)

if 'repository' not in st.session_state:
    st.session_state.repository = SupabaseRepository()

if 'funcionarios' not in st.session_state:
    st.session_state.funcionarios = []

def carregar_dados():
    st.session_state.funcionarios = st.session_state.repository.listar_funcionarios()

def get_funcionarios_do_dia(dia: date) -> list:
    return [f for f in st.session_state.funcionarios if f.dia_trabalho == dia]

def main():
    st.title("💼 Sistema de Relatório de Salários dos Garçons")
    
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        config = st.session_state.repository.get_configuracao()
        email_dest = st.text_input(
            "E-mail Destinatário", 
            value=config.email_destinatario if config else settings.EMAIL_DEFAULT
        )
        
        if st.button("💾 Salvar Configuração"):
            try:
                nova_config = Configuracao(
                    email_destinatario=email_dest,
                    email_remetente=settings.EMAIL_DEFAULT,
                    senha_app=settings.SENHA_APP
                )
                st.session_state.repository.salvar_configuracao(nova_config)
                st.success("Configuração salva!")
            except Exception as e:
                st.error(f"Erro: {e}")
        
        st.divider()
        
        st.info(f"📅 Data: {date.today().strftime('%d/%m/%Y')}")
        st.info(f"📆 Dia: {settings.DIAS_SEMANA.get(date.today().weekday())}")
        
        st.divider()
        
        st.subheader("📥 Exportar Relatório")
        formato = st.selectbox("Formato", ["HTML", "Excel", "DOCX", "CSV", "JSON", "XML"])
        
        if st.button("📊 Gerar Relatório"):
            funcs = get_funcionarios_do_dia(date.today())
            if funcs:
                report = ReportGenerator(funcs, date.today())
                
                if formato == "HTML":
                    st.download_button(
                        "📥 Download HTML",
                        report.generate_html(),
                        f"relatorio_{date.today()}.html",
                        "text/html"
                    )
                elif formato == "Excel":
                    st.download_button(
                        "📥 Download Excel",
                        report.generate_excel(),
                        f"relatorio_{date.today()}.xlsx",
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                elif formato == "DOCX":
                    st.download_button(
                        "📥 Download DOCX",
                        report.generate_docx(),
                        f"relatorio_{date.today()}.docx",
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                elif formato == "CSV":
                    st.download_button(
                        "📥 Download CSV",
                        report.generate_csv(),
                        f"relatorio_{date.today()}.csv",
                        "text/csv"
                    )
                elif formato == "JSON":
                    st.download_button(
                        "📥 Download JSON",
                        report.generate_json(),
                        f"relatorio_{date.today()}.json",
                        "application/json"
                    )
                elif formato == "XML":
                    st.download_button(
                        "📥 Download XML",
                        report.generate_xml(),
                        f"relatorio_{date.today()}.xml",
                        "application/xml"
                    )
            else:
                st.warning("Nenhum funcionário cadastrado para hoje")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("📝 Cadastrar Funcionário")
            
            with st.form("cadastro_form"):
                nome = st.text_input("Nome do Funcionário", placeholder="Digite o nome")
                valor = st.number_input("Valor 10% (R$)", min_value=0.0, step=0.01, format="%.2f")
                hora_entrada = st.time_input("Horário Entrada", datetime.strptime("08:00", "%H:%M"))
                hora_saida = st.time_input("Horário Saída", datetime.strptime("16:00", "%H:%M"))
                dia_trabalho = st.date_input("Dia de Trabalho", date.today())
                observacao = st.text_area("Observação", placeholder="Observações opcionais...")
                
                submitted = st.form_submit_button("✅ Cadastrar", type="primary")
                
                if submitted:
                    if nome and valor > 0:
                        try:
                            func = Funcionario(
                                nome=nome,
                                valor_10_percent=valor,
                                hora_entrada=hora_entrada.strftime("%H:%M"),
                                hora_saida=hora_saida.strftime("%H:%M"),
                                dia_trabalho=dia_trabalho,
                                observacao=observacao
                            )
                            st.session_state.repository.cadastrar_funcionario(func)
                            st.success("Funcionário cadastrado com sucesso!")
                            carregar_dados()
                        except Exception as e:
                            st.error(f"Erro ao cadastrar: {e}")
                    else:
                        st.error("Preencha o nome e o valor")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("📋 Funcionários Cadastrados")
            
            dia_selecionado = st.date_input("Filtrar por dia", date.today(), key="filtro_dia")
            
            carregar_dados()
            funcs_filtrados = get_funcionarios_do_dia(dia_selecionado)
            
            if funcs_filtrados:
                df = pd.DataFrame([
                    {
                        "Nome": f.nome,
                        "10% (R$)": f"R$ {f.valor_10_percent:.2f}",
                        "Entrada": f.hora_entrada,
                        "Saída": f.hora_saida,
                        "Observação": f.observacao or "-"
                    }
                    for f in funcs_filtrados
                ])
                
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                total = sum(f.valor_10_percent for f in funcs_filtrados)
                
                st.divider()
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Total Funcionários", len(funcs_filtrados))
                with col_b:
                    st.metric("Total a Pagar", f"R$ {total:.2f}")
                
                if st.button("🗑️ Deletar Funcionários do Dia", type="secondary"):
                    if st.session_state.repository:
                        try:
                            for f in funcs_filtrados:
                                st.session_state.repository.deletar_funcionario(str(f.id))
                            st.success("Funcionários deletados!")
                            carregar_dados()
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro: {e}")
            else:
                st.info(f"Nenhum funcionário cadastrado para {dia_selecionado.strftime('%d/%m/%Y')}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📧 Enviar Relatório por E-mail")
    
    col_e1, col_e2 = st.columns([3, 1])
    
    with col_e1:
        email_destino = st.text_input("E-mail Destinatário", value=email_dest)
    
    with col_e2:
        st.write("")
        st.write("")
        if st.button("📧 Enviar E-mail", type="primary"):
            funcs = get_funcionarios_do_dia(date.today())
            if funcs and email_destino:
                try:
                    config = st.session_state.repository.get_configuracao()
                    email_service = EmailService(
                        remetente=config.email_remetente if config else settings.EMAIL_DEFAULT,
                        senha=config.senha_app if config else settings.SENHA_APP
                    )
                    
                    report_gen = ReportGenerator(funcs, date.today())
                    dia_semana = settings.DIAS_SEMANA.get(date.today().weekday(), "")
                    
                    sucesso = email_service.enviar_relatorio_com_anexos(
                        email_destino, funcs, date.today(), dia_semana, report_gen
                    )
                    
                    if sucesso:
                        st.success(f"E-mail enviado com sucesso para {email_destino}!")
                    else:
                        st.error("Falha ao enviar e-mail")
                except Exception as e:
                    st.error(f"Erro: {e}")
            else:
                st.warning("Nenhum funcionário para hoje ou e-mail não configurado")
    
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
