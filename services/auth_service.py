import os
from supabase import create_client, Client
from config.settings import settings

class AuthService:
    def __init__(self):
        self.supabase: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        self.session = None
        self.user = None
    
    def sign_in(self, email: str, password: str) -> dict:
        """Realiza login com e-mail e senha"""
        try:
            response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            self.session = response.session
            self.user = response.user
            return {
                "success": True,
                "user": response.user,
                "session": response.session
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def sign_up(self, email: str, password: str) -> dict:
        """Cria uma nova conta"""
        try:
            response = self.supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            return {
                "success": True,
                "user": response.user
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def sign_out(self):
        """Realiza logout"""
        try:
            self.supabase.auth.sign_out()
            self.session = None
            self.user = None
            return True
        except:
            return False
    
    def get_session(self):
        """Retorna a sessão atual"""
        try:
            return self.supabase.auth.get_session()
        except:
            return None
    
    def is_authenticated(self) -> bool:
        """Verifica se está autenticado"""
        return self.user is not None
    
    def reset_password(self, email: str) -> dict:
        """Envia e-mail para recuperação de senha"""
        try:
            self.supabase.auth.reset_password_for_email(email)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}


auth_service = AuthService()
