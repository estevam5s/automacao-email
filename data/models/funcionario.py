from dataclasses import dataclass
from datetime import date
from typing import Optional
import uuid

@dataclass
class Funcionario:
    id: Optional[uuid.UUID] = None
    nome: str = ""
    valor_10_percent: float = 0.0
    hora_entrada: str = "08:00"
    hora_saida: str = "16:00"
    dia_trabalho: Optional[date] = None
    observacao: str = ""
    vale: Optional[float] = None
    tipo_vale: Optional[str] = None
    pago: bool = False
    tipo_pagamento: str = "pix"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_dict(self) -> dict:
        data = {
            "nome": self.nome,
            "valor_10_percent": self.valor_10_percent,
            "hora_entrada": self.hora_entrada,
            "hora_saida": self.hora_saida,
            "dia_trabalho": self.dia_trabalho.isoformat() if self.dia_trabalho else None,
            "observacao": self.observacao,
            "vale": self.vale,
            "tipo_vale": self.tipo_vale if self.tipo_vale else None,
            "pago": self.pago,
            "tipo_pagamento": self.tipo_pagamento if self.tipo_pagamento else "pix"
        }
        if self.id:
            data["id"] = str(self.id)
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Funcionario":
        return cls(
            id=uuid.UUID(data["id"]) if data.get("id") else None,
            nome=data.get("nome", ""),
            valor_10_percent=float(data.get("valor_10_percent", 0)),
            hora_entrada=data.get("hora_entrada", "08:00"),
            hora_saida=data.get("hora_saida", "16:00"),
            dia_trabalho=date.fromisoformat(data["dia_trabalho"]) if data.get("dia_trabalho") else None,
            observacao=data.get("observacao", ""),
            vale=float(data["vale"]) if data.get("vale") is not None else None,
            tipo_vale=data.get("tipo_vale"),
            pago=bool(data.get("pago", False)),
            tipo_pagamento=data.get("tipo_pagamento", "pix"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )


@dataclass
class FuncionarioBase:
    id: Optional[uuid.UUID] = None
    nome: str = ""
    pix: str = ""
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_dict(self) -> dict:
        data = {"nome": self.nome, "pix": self.pix}
        if self.id:
            data["id"] = str(self.id)
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "FuncionarioBase":
        return cls(
            id=uuid.UUID(data["id"]) if data.get("id") else None,
            nome=data.get("nome", ""),
            pix=data.get("pix", ""),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )


@dataclass
class RegistroDiario:
    id: Optional[uuid.UUID] = None
    nome_funcionario: str = ""
    dia_trabalho: Optional[date] = None
    valor_10_percent: float = 0.0
    hora_entrada: str = "08:00"
    hora_saida: str = "16:00"
    vale: Optional[float] = None
    tipo_vale: str = "pix"
    pago: bool = False
    observacao: str = ""
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_dict(self) -> dict:
        data = {
            "nome_funcionario": self.nome_funcionario,
            "dia_trabalho": self.dia_trabalho.isoformat() if self.dia_trabalho else None,
            "valor_10_percent": self.valor_10_percent,
            "hora_entrada": self.hora_entrada,
            "hora_saida": self.hora_saida,
            "vale": self.vale,
            "tipo_vale": self.tipo_vale,
            "pago": self.pago,
            "observacao": self.observacao
        }
        if self.id:
            data["id"] = str(self.id)
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "RegistroDiario":
        return cls(
            id=uuid.UUID(data["id"]) if data.get("id") else None,
            nome_funcionario=data.get("nome_funcionario", ""),
            dia_trabalho=date.fromisoformat(data["dia_trabalho"]) if data.get("dia_trabalho") else None,
            valor_10_percent=float(data.get("valor_10_percent", 0)),
            hora_entrada=data.get("hora_entrada", "08:00"),
            hora_saida=data.get("hora_saida", "16:00"),
            vale=float(data["vale"]) if data.get("vale") is not None else None,
            tipo_vale=data.get("tipo_vale", "pix"),
            pago=bool(data.get("pago", False)),
            observacao=data.get("observacao", ""),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )


@dataclass
class ObservacaoGeral:
    id: Optional[uuid.UUID] = None
    dia_trabalho: Optional[date] = None
    observacao: str = ""
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_dict(self) -> dict:
        data = {
            "dia_trabalho": self.dia_trabalho.isoformat() if self.dia_trabalho else None,
            "observacao": self.observacao
        }
        if self.id:
            data["id"] = str(self.id)
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "ObservacaoGeral":
        return cls(
            id=uuid.UUID(data["id"]) if data.get("id") else None,
            dia_trabalho=date.fromisoformat(data["dia_trabalho"]) if data.get("dia_trabalho") else None,
            observacao=data.get("observacao", ""),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )


@dataclass
class Configuracao:
    id: Optional[uuid.UUID] = None
    email_destinatario: str = ""
    email_remetente: str = ""
    senha_app: str = ""
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587

    @classmethod
    def from_dict(cls, data: dict) -> "Configuracao":
        return cls(
            id=uuid.UUID(data["id"]) if data.get("id") else None,
            email_destinatario=data.get("email_destinatario", ""),
            email_remetente=data.get("email_remetente", ""),
            senha_app=data.get("senha_app", ""),
            smtp_host=data.get("smtp_host", "smtp.gmail.com"),
            smtp_port=int(data.get("smtp_port", 587))
        )


@dataclass
class RegistroTrabalho:
    id: Optional[uuid.UUID] = None
    dia_trabalho: Optional[date] = None
    dia_semana: str = ""
    total_funcionarios: int = 0
    total_valores: float = 0.0
    email_enviado: bool = False
    data_envio: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "RegistroTrabalho":
        return cls(
            id=uuid.UUID(data["id"]) if data.get("id") else None,
            dia_trabalho=date.fromisoformat(data["dia_trabalho"]) if data.get("dia_trabalho") else None,
            dia_semana=data.get("dia_semana", ""),
            total_funcionarios=int(data.get("total_funcionarios", 0)),
            total_valores=float(data.get("total_valores", 0)),
            email_enviado=bool(data.get("email_enviado", False)),
            data_envio=data.get("data_envio")
        )


@dataclass
class Log:
    id: Optional[uuid.UUID] = None
    acao: str = ""
    tabela: str = ""
    registro_id: Optional[str] = None
    dados_anteriores: Optional[dict] = None
    dados_novos: Optional[dict] = None
    usuario: str = "sistema"
    ip_origem: Optional[str] = None
    created_at: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "acao": self.acao,
            "tabela": self.tabela,
            "registro_id": self.registro_id,
            "dados_anteriores": str(self.dados_anteriores) if self.dados_anteriores else None,
            "dados_novos": str(self.dados_novos) if self.dados_novos else None,
            "usuario": self.usuario,
            "ip_origem": self.ip_origem
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Log":
        return cls(
            id=uuid.UUID(data["id"]) if data.get("id") else None,
            acao=data.get("acao", ""),
            tabela=data.get("tabela", ""),
            registro_id=data.get("registro_id"),
            dados_anteriores=data.get("dados_anteriores"),
            dados_novos=data.get("dados_novos"),
            usuario=data.get("usuario", "sistema"),
            ip_origem=data.get("ip_origem"),
            created_at=data.get("created_at")
        )


@dataclass
class HistoricoPresenca:
    id: Optional[uuid.UUID] = None
    nome: str = ""
    dia_trabalho: Optional[date] = None
    hora_entrada: str = "08:00"
    hora_saida: str = "16:00"
    valor_10_percent: float = 0.0
    observacao: str = ""
    created_at: Optional[str] = None
    dia_formatado: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "HistoricoPresenca":
        return cls(
            id=uuid.UUID(data["id"]) if data.get("id") else None,
            nome=data.get("nome", ""),
            dia_trabalho=date.fromisoformat(data["dia_trabalho"]) if data.get("dia_trabalho") else None,
            hora_entrada=data.get("hora_entrada", "08:00"),
            hora_saida=data.get("hora_saida", "16:00"),
            valor_10_percent=float(data.get("valor_10_percent", 0)),
            observacao=data.get("observacao", ""),
            created_at=data.get("created_at"),
            dia_formatado=data.get("dia_formatado", "")
        )


@dataclass
class HistoricoPagamento:
    id: Optional[uuid.UUID] = None
    nome: str = ""
    dia_trabalho: Optional[date] = None
    valor_10_percent: float = 0.0
    vale: Optional[float] = None
    tipo_pagamento: str = "pix"
    pago: bool = False
    data_pagamento: Optional[str] = None
    status_pagamento: str = ""
    numero_parcela: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> "HistoricoPagamento":
        return cls(
            id=uuid.UUID(data["id"]) if data.get("id") else None,
            nome=data.get("nome", ""),
            dia_trabalho=date.fromisoformat(data["dia_trabalho"]) if data.get("dia_trabalho") else None,
            valor_10_percent=float(data.get("valor_10_percent", 0)),
            vale=float(data["vale"]) if data.get("vale") is not None else None,
            tipo_pagamento=data.get("tipo_pagamento", "pix"),
            pago=bool(data.get("pago", False)),
            data_pagamento=data.get("data_pagamento"),
            status_pagamento=data.get("status_pagamento", ""),
            numero_parcela=int(data.get("numero_parcela", 0))
        )


@dataclass
class TotalFuncionarios:
    total_cadastrados: int = 0
    total_registros: int = 0
    total_dias_trabalhados: int = 0
    total_geral_pago: float = 0.0
    total_pago: float = 0.0
    total_pendente: float = 0.0
    primeiro_registro: Optional[date] = None
    ultimo_registro: Optional[date] = None

    @classmethod
    def from_dict(cls, data: dict) -> "TotalFuncionarios":
        return cls(
            total_cadastrados=int(data.get("total_cadastrados", 0)),
            total_registros=int(data.get("total_registros", 0)),
            total_dias_trabalhados=int(data.get("total_dias_trabalhados", 0)),
            total_geral_pago=float(data.get("total_geral_pago", 0)),
            total_pago=float(data.get("total_pago", 0)),
            total_pendente=float(data.get("total_pendente", 0)),
            primeiro_registro=date.fromisoformat(data["primeiro_registro"]) if data.get("primeiro_registro") else None,
            ultimo_registro=date.fromisoformat(data["ultimo_registro"]) if data.get("ultimo_registro") else None
        )


@dataclass
class DataCadastramento:
    nome: str = ""
    primeiro_dia_trabalho: Optional[date] = None
    ultimo_dia_trabalho: Optional[date] = None
    total_dias_trabalhados: int = 0
    total_recebido: float = 0.0
    data_cadastro_banco: Optional[str] = None
    dias_trabalhados: list = None

    def __post_init__(self):
        if self.dias_trabalhados is None:
            self.dias_trabalhados = []

    @classmethod
    def from_dict(cls, data: dict) -> "DataCadastramento":
        return cls(
            nome=data.get("nome", ""),
            primeiro_dia_trabalho=date.fromisoformat(data["primeiro_dia_trabalho"]) if data.get("primeiro_dia_trabalho") else None,
            ultimo_dia_trabalho=date.fromisoformat(data["ultimo_dia_trabalho"]) if data.get("ultimo_dia_trabalho") else None,
            total_dias_trabalhados=int(data.get("total_dias_trabalhados", 0)),
            total_recebido=float(data.get("total_recebido", 0)),
            data_cadastro_banco=data.get("data_cadastro_banco"),
            dias_trabalhados=data.get("dias_trabalhados", [])
        )


@dataclass
class RankingPagamento:
    posicao: int = 0
    nome: str = ""
    dias_trabalhados: int = 0
    total_recebido: float = 0.0
    media_diaria: float = 0.0
    maior_diaria: float = 0.0
    menor_diaria: float = 0.0
    total_pago: float = 0.0
    total_pendente: float = 0.0

    @classmethod
    def from_dict(cls, data: dict) -> "RankingPagamento":
        return cls(
            posicao=int(data.get("posicao", 0)),
            nome=data.get("nome", ""),
            dias_trabalhados=int(data.get("dias_trabalhados", 0)),
            total_recebido=float(data.get("total_recebido", 0)),
            media_diaria=float(data.get("media_diaria", 0)),
            maior_diaria=float(data.get("maior_diaria", 0)),
            menor_diaria=float(data.get("menor_diaria", 0)),
            total_pago=float(data.get("total_pago", 0)),
            total_pendente=float(data.get("total_pendente", 0))
        )
