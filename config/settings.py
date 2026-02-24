import os
from dotenv import load_dotenv

load_dotenv()

def get_secret(key: str, default: str = "") -> str:
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
    return os.environ.get(key, default)

class Settings:
    SUPABASE_URL: str = get_secret("SUPABASE_URL", "")
    SUPABASE_KEY: str = get_secret("SUPABASE_KEY", "")
    
    EMAIL_DEFAULT: str = get_secret("EMAIL_DEFAULT", "")
    SENHA_APP: str = get_secret("SENHA_APP", "")
    SMTP_HOST: str = get_secret("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(get_secret("SMTP_PORT", "587") or "587")
    
    REPORT_FORMATS: list = ["docx", "excel", "csv", "json", "xml", "html"]
    
    DIAS_SEMANA: dict = {
        0: "Segunda-feira",
        1: "Terça-feira",
        2: "Quarta-feira",
        3: "Quinta-feira",
        4: "Sexta-feira",
        5: "Sábado",
        6: "Domingo"
    }

settings = Settings()
