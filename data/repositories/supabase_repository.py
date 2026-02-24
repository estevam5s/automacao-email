from supabase import create_client, Client
from typing import List, Optional
from datetime import date, timedelta
import uuid
from config.settings import settings
from data.models.funcionario import Funcionario, FuncionarioBase, RegistroDiario, ObservacaoGeral, Configuracao, RegistroTrabalho, Log, HistoricoPresenca, HistoricoPagamento, TotalFuncionarios, DataCadastramento, RankingPagamento

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
    
    def buscar_funcionario_por_nome_e_data(self, nome: str, dia_trabalho: date) -> Optional[Funcionario]:
        data = self.client.table("funcionarios").select("*").eq("nome", nome).eq("dia_trabalho", dia_trabalho.isoformat()).execute()
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

    # ===== LOGS DO SISTEMA =====
    def salvar_log(self, acao: str, tabela: str, registro_id: str = None, 
                   dados_anteriores: dict = None, dados_novos: dict = None, 
                   usuario: str = "sistema", ip_origem: str = None) -> Log:
        try:
            data = self.client.table("logs").insert({
                "acao": acao,
                "tabela": tabela,
                "registro_id": registro_id,
                "dados_anteriores": str(dados_anteriores) if dados_anteriores else None,
                "dados_novos": str(dados_novos) if dados_novos else None,
                "usuario": usuario,
                "ip_origem": ip_origem
            }).execute()
            if data.data:
                return Log.from_dict(data.data[0])
        except Exception as e:
            print(f"Erro ao salvar log: {e}")
        return None

    def listar_logs(self, limite: int = 100) -> List[Log]:
        try:
            data = self.client.table("logs").select("*").order("created_at", desc=True).limit(limite).execute()
            return [Log.from_dict(item) for item in data.data]
        except:
            return []

    def listar_logs_por_tabela(self, tabela: str, limite: int = 100) -> List[Log]:
        try:
            data = self.client.table("logs").select("*").eq("tabela", tabela).order("created_at", desc=True).limit(limite).execute()
            return [Log.from_dict(item) for item in data.data]
        except:
            return []

    def listar_logs_por_acao(self, acao: str, limite: int = 100) -> List[Log]:
        try:
            data = self.client.table("logs").select("*").eq("acao", acao).order("created_at", desc=True).limit(limite).execute()
            return [Log.from_dict(item) for item in data.data]
        except:
            return []

    def limpar_logs(self) -> bool:
        try:
            self.client.table("logs").delete().execute()
            return True
        except:
            return False

    # ===== HISTÓRICO DE PRESENÇA =====
    def listar_historico_presenca(self, limite: int = 100) -> List[HistoricoPresenca]:
        try:
            data = self.client.table("funcionarios").select("*").order("dia_trabalho", desc=True).limit(limite).execute()
            resultados = []
            for item in data.data:
                hp = HistoricoPresenca(
                    id=uuid.UUID(item["id"]) if item.get("id") else None,
                    nome=item.get("nome", ""),
                    dia_trabalho=date.fromisoformat(item["dia_trabalho"]) if item.get("dia_trabalho") else None,
                    hora_entrada=item.get("hora_entrada", "08:00"),
                    hora_saida=item.get("hora_saida", "16:00"),
                    valor_10_percent=float(item.get("valor_10_percent", 0)),
                    observacao=item.get("observacao", ""),
                    created_at=item.get("created_at"),
                    dia_formatado=""
                )
                if hp.dia_trabalho == date.today():
                    hp.dia_formatado = "Hoje"
                elif hp.dia_trabalho == date.today() - timedelta(days=1):
                    hp.dia_formatado = "Ontem"
                else:
                    hp.dia_formatado = hp.dia_trabalho.strftime("%d/%m/%Y") if hp.dia_trabalho else ""
                resultados.append(hp)
            return resultados
        except Exception as e:
            print(f"Erro ao listar histórico de presença: {e}")
            return []

    # ===== HISTÓRICO DE PAGAMENTOS =====
    def listar_historico_pagamentos(self, limite: int = 100) -> List[HistoricoPagamento]:
        try:
            data = self.client.table("funcionarios").select("*").order("dia_trabalho", desc=True).limit(limite).execute()
            resultados = []
            for item in data.data:
                hp = HistoricoPagamento(
                    id=uuid.UUID(item["id"]) if item.get("id") else None,
                    nome=item.get("nome", ""),
                    dia_trabalho=date.fromisoformat(item["dia_trabalho"]) if item.get("dia_trabalho") else None,
                    valor_10_percent=float(item.get("valor_10_percent", 0)),
                    vale=float(item["vale"]) if item.get("vale") is not None else None,
                    tipo_pagamento=item.get("tipo_pagamento", "pix"),
                    pago=bool(item.get("pago", False)),
                    data_pagamento=item.get("updated_at"),
                    status_pagamento="Pago" if item.get("pago") else "Pendente",
                    numero_parcela=0
                )
                resultados.append(hp)
            return resultados
        except Exception as e:
            print(f"Erro ao listar histórico de pagamentos: {e}")
            return []

    # ===== TOTAL DE FUNCIONÁRIOS =====
    def get_total_funcionarios(self) -> TotalFuncionarios:
        try:
            data = self.client.table("funcionarios").select("nome", "dia_trabalho", "valor_10_percent", "pago", "created_at").execute()
            if not data.data:
                return TotalFuncionarios()
            
            nomes_unicos = set()
            total_valores = 0.0
            total_pago = 0.0
            total_pendente = 0.0
            primeiro_registro = None
            ultimo_registro = None
            
            for item in data.data:
                nomes_unicos.add(item.get("nome"))
                valor = float(item.get("valor_10_percent", 0))
                total_valores += valor
                if item.get("pago"):
                    total_pago += valor
                else:
                    total_pendente += valor
                
                dia = item.get("dia_trabalho")
                if dia:
                    dia_date = date.fromisoformat(dia)
                    if primeiro_registro is None or dia_date < primeiro_registro:
                        primeiro_registro = dia_date
                    if ultimo_registro is None or dia_date > ultimo_registro:
                        ultimo_registro = dia_date
            
            return TotalFuncionarios(
                total_cadastrados=len(nomes_unicos),
                total_registros=len(data.data),
                total_dias_trabalhados=len(set(date.fromisoformat(item["dia_trabalho"]) for item in data.data if item.get("dia_trabalho"))),
                total_geral_pago=total_valores,
                total_pago=total_pago,
                total_pendente=total_pendente,
                primeiro_registro=primeiro_registro,
                ultimo_registro=ultimo_registro
            )
        except Exception as e:
            print(f"Erro ao get total funcionários: {e}")
            return TotalFuncionarios()

    # ===== DATA DE CADASTRAMENTO =====
    def listar_data_cadastramento(self) -> List[DataCadastramento]:
        try:
            data = self.client.table("funcionarios").select("nome", "dia_trabalho", "valor_10_percent", "created_at").execute()
            if not data.data:
                return []
            
            funcionarios_dict = {}
            for item in data.data:
                nome = item.get("nome", "")
                if nome not in funcionarios_dict:
                    funcionarios_dict[nome] = {
                        "nome": nome,
                        "primeiro_dia_trabalho": item.get("dia_trabalho"),
                        "ultimo_dia_trabalho": item.get("dia_trabalho"),
                        "total_dias_trabalhados": 0,
                        "total_recebido": 0.0,
                        "data_cadastro_banco": item.get("created_at"),
                        "dias_trabalhados": set()
                    }
                
                func = funcionarios_dict[nome]
                func["total_dias_trabalhados"] += 1
                func["total_recebido"] += float(item.get("valor_10_percent", 0))
                func["dias_trabalhados"].add(item.get("dia_trabalho"))
                
                if item.get("dia_trabalho"):
                    if func["primeiro_dia_trabalho"] is None or item["dia_trabalho"] < func["primeiro_dia_trabalho"]:
                        func["primeiro_dia_trabalho"] = item["dia_trabalho"]
                    if func["ultimo_dia_trabalho"] is None or item["dia_trabalho"] > func["ultimo_dia_trabalho"]:
                        func["ultimo_dia_trabalho"] = item["dia_trabalho"]
            
            resultados = []
            for func in funcionarios_dict.values():
                dc = DataCadastramento(
                    nome=func["nome"],
                    primeiro_dia_trabalho=date.fromisoformat(func["primeiro_dia_trabalho"]) if func["primeiro_dia_trabalho"] else None,
                    ultimo_dia_trabalho=date.fromisoformat(func["ultimo_dia_trabalho"]) if func["ultimo_dia_trabalho"] else None,
                    total_dias_trabalhados=func["total_dias_trabalhados"],
                    total_recebido=func["total_recebido"],
                    data_cadastro_banco=func["data_cadastro_banco"],
                    dias_trabalhados=list(func["dias_trabalhados"])
                )
                resultados.append(dc)
            
            resultados.sort(key=lambda x: x.primeiro_dia_trabalho or date.min, reverse=True)
            return resultados
        except Exception as e:
            print(f"Erro ao listar data cadastramento: {e}")
            return []

    # ===== RANKING DE PAGAMENTOS =====
    def listar_ranking_pagamentos(self) -> List[RankingPagamento]:
        try:
            data = self.client.table("funcionarios").select("nome", "dia_trabalho", "valor_10_percent", "pago").execute()
            if not data.data:
                return []
            
            funcionarios_dict = {}
            for item in data.data:
                nome = item.get("nome", "")
                if nome not in funcionarios_dict:
                    funcionarios_dict[nome] = {
                        "nome": nome,
                        "dias_trabalhados": 0,
                        "total_recebido": 0.0,
                        "maior_diaria": 0.0,
                        "menor_diaria": float("inf"),
                        "total_pago": 0.0,
                        "total_pendente": 0.0
                    }
                
                func = funcionarios_dict[nome]
                valor = float(item.get("valor_10_percent", 0))
                func["dias_trabalhados"] += 1
                func["total_recebido"] += valor
                if valor > func["maior_diaria"]:
                    func["maior_diaria"] = valor
                if valor < func["menor_diaria"]:
                    func["menor_diaria"] = valor
                if item.get("pago"):
                    func["total_pago"] += valor
                else:
                    func["total_pendente"] += valor
            
            resultados = []
            for func in funcionarios_dict.values():
                if func["menor_diaria"] == float("inf"):
                    func["menor_diaria"] = 0.0
                rp = RankingPagamento(
                    nome=func["nome"],
                    dias_trabalhados=func["dias_trabalhados"],
                    total_recebido=func["total_recebido"],
                    media_diaria=func["total_recebido"] / func["dias_trabalhados"] if func["dias_trabalhados"] > 0 else 0,
                    maior_diaria=func["maior_diaria"],
                    menor_diaria=func["menor_diaria"],
                    total_pago=func["total_pago"],
                    total_pendente=func["total_pendente"]
                )
                resultados.append(rp)
            
            resultados.sort(key=lambda x: x.total_recebido, reverse=True)
            for i, rp in enumerate(resultados, 1):
                rp.posicao = i
            
            return resultados
        except Exception as e:
            print(f"Erro ao listar ranking: {e}")
            return []

    # ===== BUSCAR HISTÓRICO POR FUNCIONÁRIO =====
    def buscar_historico_funcionario(self, nome: str) -> List[HistoricoPagamento]:
        try:
            data = self.client.table("funcionarios").select("*").ilike("nome", f"%{nome}%").order("dia_trabalho", desc=True).execute()
            resultados = []
            for item in data.data:
                hp = HistoricoPagamento(
                    id=uuid.UUID(item["id"]) if item.get("id") else None,
                    nome=item.get("nome", ""),
                    dia_trabalho=date.fromisoformat(item["dia_trabalho"]) if item.get("dia_trabalho") else None,
                    valor_10_percent=float(item.get("valor_10_percent", 0)),
                    vale=float(item["vale"]) if item.get("vale") is not None else None,
                    tipo_pagamento=item.get("tipo_pagamento", "pix"),
                    pago=bool(item.get("pago", False)),
                    data_pagamento=item.get("updated_at"),
                    status_pagamento="Pago" if item.get("pago") else "Pendente",
                    numero_parcela=0
                )
                resultados.append(hp)
            return resultados
        except Exception as e:
            print(f"Erro ao buscar histórico: {e}")
            return []
