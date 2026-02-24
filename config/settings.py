import os

class Settings:
    SUPABASE_URL: str = "https://igmnzakdeacfddjeduoc.supabase.co"
    SUPABASE_KEY: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlnbW56YWtkZWFjZmRkamVkdW9jIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE4ODIyMTEsImV4cCI6MjA4NzQ1ODIxMX0.TartlYEE7N5WrXVOjHcVwHS-ypj8QJcWqSDb2jX7llQ"
    
    EMAIL_DEFAULT: str = "estevamsouzalaureth@gmail.com"
    SENHA_APP: str = "dcbz odag occl qqwq"
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    
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
