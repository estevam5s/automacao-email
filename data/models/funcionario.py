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
    tipo_vale: str = "pix"
    pago: bool = False
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
            "tipo_vale": self.tipo_vale,
            "pago": self.pago
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
            tipo_vale=data.get("tipo_vale", "pix"),
            pago=bool(data.get("pago", False)),
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
