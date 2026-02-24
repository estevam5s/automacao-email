from supabase import create_client, Client
from typing import List, Optional
from datetime import date
import uuid
from config.settings import settings
from data.models.funcionario import Funcionario, FuncionarioBase, RegistroDiario, ObservacaoGeral, Configuracao, RegistroTrabalho

class SupabaseRepository:
    def __init__(self):
        self._client: Optional[Client] = None

    @property
    def client(self) -> Client:
        if self._client is None:
            self._client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        return self._client

    # ===== FUNCIONÁRIOS (usa tabela funcionários) =====
    def cadastrar_funcionario(self, func: Funcionario) -> Funcionario:
        if not func.id:
            func.id = uuid.uuid4()
        data = self.client.table("funcionarios").insert(func.to_dict()).execute()
        if data.data:
            return Funcionario.from_dict(data.data[0])
        raise Exception("Erro ao cadastrar")

    def listar_funcionarios(self, dia_trabalho: date = None) -> List[Funcionario]:
        query = self.client.table("funcionarios").select("*")
        if dia_trabalho:
            query = query.eq("dia_trabalho", dia_trabalho.isoformat())
        data = query.execute()
        return [Funcionario.from_dict(item) for item in data.data]

    def listar_todos_funcionarios(self) -> List[Funcionario]:
        data = self.client.table("funcionarios").select("*").order("nome").execute()
        return [Funcionario.from_dict(item) for item in data.data]

    def atualizar_funcionario(self, func: Funcionario) -> Funcionario:
        data = self.client.table("funcionarios").update(func.to_dict()).eq("id", str(func.id)).execute()
        if data.data:
            return Funcionario.from_dict(data.data[0])
        raise Exception("Erro ao atualizar")

    def deletar_funcionario(self, func_id: str) -> bool:
        self.client.table("funcionarios").delete().eq("id", func_id).execute()
        return True

    def buscar_funcionario_por_nome(self, nome: str) -> Optional[Funcionario]:
        data = self.client.table("funcionarios").select("*").eq("nome", nome).execute()
        if data.data:
            return Funcionario.from_dict(data.data[0])
        return None

    # ===== CONFIGURAÇÕES =====
    def get_configuracao(self) -> Optional[Configuracao]:
        data = self.client.table("configuracoes").select("*").limit(1).execute()
        if data.data:
            return Configuracao.from_dict(data.data[0])
        return None

    def salvar_configuracao(self, config: Configuracao) -> Configuracao:
        existing = self.get_configuracao()
        if existing:
            data = self.client.table("configuracoes").update({
                "email_destinatario": config.email_destinatario,
                "email_remetente": config.email_remetente,
                "senha_app": config.senha_app
            }).eq("id", str(existing.id)).execute()
        else:
            data = self.client.table("configuracoes").insert({
                "email_destinatario": config.email_destinatario,
                "email_remetente": config.email_remetente,
                "senha_app": config.senha_app
            }).execute()
        
        if data.data:
            return Configuracao.from_dict(data.data[0])
        raise Exception("Erro ao salvar configuração")

    # ===== OBSERVAÇÕES GERAIS =====
    def salvar_observacao_geral(self, obs: ObservacaoGeral) -> ObservacaoGeral:
        existing = self.get_observacao_geral(obs.dia_trabalho)
        if existing:
            data = self.client.table("observacoes_gerais").update({
                "observacao": obs.observacao
            }).eq("dia_trabalho", obs.dia_trabalho.isoformat()).execute()
        else:
            data = self.client.table("observacoes_gerais").insert(obs.to_dict()).execute()
        
        if data.data:
            return ObservacaoGeral.from_dict(data.data[0])
        raise Exception("Erro ao salvar observação")

    def get_observacao_geral(self, dia_trabalho: date) -> Optional[ObservacaoGeral]:
        if dia_trabalho is None:
            return None
        data = self.client.table("observacoes_gerais").select("*").eq("dia_trabalho", dia_trabalho.isoformat()).execute()
        if data.data:
            return ObservacaoGeral.from_dict(data.data[0])
        return None

    # ===== REGISTROS DE ENVIO =====
    def registrar_envio(self, dia_trabalho: date, dia_semana: str, total_func: int, total_valores: float) -> RegistroTrabalho:
        data = self.client.table("registros_trabalho").insert({
            "dia_trabalho": dia_trabalho.isoformat(),
            "dia_semana": dia_semana,
            "total_funcionarios": total_func,
            "total_valores": total_valores,
            "email_enviado": True,
            "data_envio": "now()"
        }).execute()
        if data.data:
            return RegistroTrabalho.from_dict(data.data[0])
        raise Exception("Erro ao registrar envio")

    def listar_registros(self) -> List[RegistroTrabalho]:
        data = self.client.table("registros_trabalho").select("*").order("dia_trabalho", desc=True).execute()
        return [RegistroTrabalho.from_dict(item) for item in data.data]
