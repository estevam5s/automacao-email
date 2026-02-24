import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List
import io
from datetime import date
from data.models.funcionario import Funcionario
from services.report_generator import ReportGenerator

class EmailService:
    def __init__(self, remetente: str, senha: str, host: str = "smtp.gmail.com", porta: int = 587):
        self.remetente = remetente
        self.senha = senha
        self.host = host
        self.porta = porta

    def _criar_template_html(self, funcionarios: List[Funcionario], dia_trabalho: date, dia_semana: str, total: float, obs_geral: str = "") -> str:
        total_func = len(funcionarios)
        total_vales = sum(f.vale for f in funcionarios if f.vale)
        func_pagos = sum(1 for f in funcionarios if f.pago)
        func_pendentes = total_func - func_pagos
        
        def calcular_horas(entrada, saida):
            try:
                h1, m1 = map(int, entrada.split(':'))
                h2, m2 = map(int, saida.split(':'))
                horas = (h2 * 60 + m2) - (h1 * 60 + m1)
                if horas < 0:
                    horas += 24 * 60
                return f"{horas // 60}h{horas % 60:02d}"
            except:
                return "-"
        
        rows = ""
        for f in funcionarios:
            horas_trabalhadas = calcular_horas(f.hora_entrada, f.hora_saida)
            pago_texto = "✅ SIM" if f.pago else "❌ NÃO"
            pago_style = "color: #27ae60; font-weight: bold;" if f.pago else "color: #e74c3c; font-weight: bold;"
            vale_texto = f"R$ {f.vale:.2f}" if f.vale else "-"
            tipo_vale_texto = f.tipo_vale.upper() if f.tipo_vale else "-"
            
            rows += f"""
            <tr style="border-bottom: 1px solid #ddd; background-color: {'#f9f9f9' if func_pagos % 2 == 0 else '#ffffff'};">
                <td style="padding: 12px; color: #333; font-weight: 600;">{f.nome}</td>
                <td style="padding: 12px; color: #2E7D32; font-weight: bold; font-size: 14px;">R$ {f.valor_10_percent:.2f}</td>
                <td style="padding: 12px; color: #666;">{f.hora_entrada}</td>
                <td style="padding: 12px; color: #666;">{f.hora_saida}</td>
                <td style="padding: 12px; color: #666; text-align: center;">{horas_trabalhadas}</td>
                <td style="padding: 12px; color: #e67e22;">{vale_texto}</td>
                <td style="padding: 12px; color: #9b59b6; font-size: 11px;">{tipo_vale_texto}</td>
                <td style="padding: 12px; {pago_style}">{pago_texto}</td>
                <td style="padding: 12px; color: #666; font-size: 12px;">{f.observacao or '-'}</td>
            </tr>"""
        
        return f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Salários - {dia_trabalho.strftime('%d/%m/%Y')}</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 0; background-color: #f0f2f5; }}
        .container {{ max-width: 900px; margin: 0 auto; background: #ffffff; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 35px; text-align: center; }}
        .header h1 {{ color: #ffffff; margin: 0; font-size: 28px; font-weight: bold; }}
        .header .subtitle {{ color: #a8c0ff; margin: 10px 0 0 0; font-size: 16px; }}
        .content {{ padding: 30px; }}
        
        .info-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-bottom: 25px; }}
        .info-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; padding: 20px; color: white; }}
        .info-card.green {{ background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }}
        .info-card.orange {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }}
        .info-card.blue {{ background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }}
        .info-card.purple {{ background: linear-gradient(135deg, #c471ed 0%, #12c2e9 100%); }}
        
        .info-card .label {{ font-size: 12px; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px; }}
        .info-card .value {{ font-size: 28px; font-weight: bold; margin-top: 5px; }}
        
        .summary-box {{ background: #e8f5e9; border-radius: 10px; padding: 20px; margin-bottom: 25px; border-left: 5px solid #4caf50; }}
        .summary-row {{ display: flex; justify-content: space-between; margin: 8px 0; }}
        .summary-label {{ color: #666; font-size: 14px; }}
        .summary-value {{ color: #333; font-weight: bold; font-size: 14px; }}
        .summary-total {{ font-size: 20px; color: #2e7d32; }}
        
        .obs-box {{ background: #fff3e0; border-radius: 10px; padding: 20px; margin-bottom: 25px; border-left: 5px solid #ff9800; }}
        .obs-title {{ color: #e65100; font-weight: bold; margin-bottom: 10px; }}
        .obs-text {{ color: #666; font-size: 14px; line-height: 1.6; }}
        
        h3 {{ color: #1e3c72; margin-bottom: 15px; border-bottom: 2px solid #1e3c72; padding-bottom: 10px; }}
        
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; background: #ffffff; }}
        th {{ background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 15px 10px; text-align: left; font-weight: 600; font-size: 12px; text-transform: uppercase; }}
        td {{ padding: 12px 10px; font-size: 13px; }}
        
        .footer {{ background: #1e1e2f; color: #a0a0a0; padding: 25px; text-align: center; font-size: 12px; }}
        .footer .logo {{ color: #ffffff; font-size: 18px; font-weight: bold; margin-bottom: 10px; }}
        
        @media (max-width: 600px) {{
            .info-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💼 Relatório de Salários dos Garçons</h1>
            <p class="subtitle">{dia_semana}, {dia_trabalho.strftime('%d de %B de %Y')}</p>
        </div>
        
        <div class="content">
            <div class="info-grid">
                <div class="info-card blue">
                    <div class="label">👥 Total Funcionários</div>
                    <div class="value">{total_func}</div>
                </div>
                <div class="info-card green">
                    <div class="label">💰 Total 10% a Pagar</div>
                    <div class="value">R$ {total:.2f}</div>
                </div>
                <div class="info-card purple">
                    <div class="label">✅ Funcionários Pagos</div>
                    <div class="value">{func_pagos}</div>
                </div>
                <div class="info-card orange">
                    <div class="label">💳 Total em Vales</div>
                    <div class="value">R$ {total_vales:.2f}</div>
                </div>
            </div>
            
            <div class="summary-box">
                <div class="summary-row">
                    <span class="summary-label">📅 Data de Trabalho:</span>
                    <span class="summary-value">{dia_trabalho.strftime('%d/%m/%Y')}</span>
                </div>
                <div class="summary-row">
                    <span class="summary-label">📆 Dia da Semana:</span>
                    <span class="summary-value">{dia_semana}</span>
                </div>
                <div class="summary-row">
                    <span class="summary-label">👥 Total de Registros:</span>
                    <span class="summary-value">{total_func}</span>
                </div>
                <div class="summary-row">
                    <span class="summary-label">✅ Já Pagos:</span>
                    <span class="summary-value">{func_pagos}</span>
                </div>
                <div class="summary-row">
                    <span class="summary-label">⏳ Pendentes:</span>
                    <span class="summary-value">{func_pendentes}</span>
                </div>
                <div class="summary-row" style="margin-top: 15px; padding-top: 15px; border-top: 2px solid #a5d6a7;">
                    <span class="summary-label summary-total">💵 TOTAL A PAGAR (10%):</span>
                    <span class="summary-value summary-total">R$ {total:.2f}</span>
                </div>
            </div>
            
            {f'''
            <div class="obs-box">
                <div class="obs-title">📝 Observação Geral do Dia:</div>
                <div class="obs-text">{obs_geral}</div>
            </div>
            ''' if obs_geral else ''}
            
            <h3>📋 Detalhamento dos Funcionários</h3>
            <table>
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>10% (R$)</th>
                        <th>Entrada</th>
                        <th>Saída</th>
                        <th>Horas</th>
                        <th>Vale (R$)</th>
                        <th>Tipo Vale</th>
                        <th>Pago?</th>
                        <th>Observação</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <div class="logo">🏪 Sistema de Relatório de Salários</div>
            <p>Este é um e-mail automático. Por favor, não responda.</p>
            <p>Gerado em {date.today().strftime('%d/%m/%Y às %H:%M')}</p>
            <p style="margin-top: 15px; font-size: 10px; opacity: 0.7;">
                © 2026 - Sistema de Automação de Salários de Garçons
            </p>
        </div>
    </div>
</body>
</html>"""

    def enviar_relatorio(
        self, 
        destinatario: str, 
        funcionarios: List[Funcionario], 
        dia_trabalho: date,
        dia_semana: str,
        arquivos: dict = None,
        obs_geral: str = ""
    ) -> bool:
        
        total = sum(f.valor_10_percent for f in funcionarios)
        
        msg = MIMEMultipart('related')
        msg['From'] = self.remetente
        msg['To'] = destinatario
        msg['Subject'] = f"💼 Relatório Salários Garçons - {dia_semana}, {dia_trabalho.strftime('%d/%m/%Y')} - {len(funcionarios)} funcionários"
        
        html_content = self._criar_template_html(funcionarios, dia_trabalho, dia_semana, total, obs_geral)
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))
        
        if arquivos:
            formatos = {
                'docx': ('relatorio.docx', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'),
                'excel': ('relatorio.xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                'csv': ('relatorio.csv', 'text/csv'),
                'json': ('relatorio.json', 'application/json'),
                'xml': ('relatorio.xml', 'application/xml'),
                'html': ('relatorio.html', 'text/html')
            }
            
            for formato, (nome_arquivo, content_type) in formatos.items():
                if formato in arquivos and arquivos[formato]:
                    parte = MIMEBase('application', 'octet-stream')
                    parte.set_payload(arquivos[formato])
                    encoders.encode_base64(parte)
                    parte.add_header('Content-Disposition', f'attachment; filename=relatorio_{dia_trabalho}.{formato}')
                    msg.attach(parte)
        
        try:
            with smtplib.SMTP(self.host, self.porta) as server:
                server.starttls()
                server.login(self.remetente, self.senha)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")
            return False

    def enviar_relatorio_com_anexos(
        self,
        destinatario: str,
        funcionarios: List[Funcionario],
        dia_trabalho: date,
        dia_semana: str,
        report_generator: ReportGenerator,
        obs_geral: str = ""
    ) -> bool:
        
        arquivos = report_generator.generate_all()
        return self.enviar_relatorio(destinatario, funcionarios, dia_trabalho, dia_semana, arquivos, obs_geral)
