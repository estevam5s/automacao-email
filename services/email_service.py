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

    def _criar_template_html(self, funcionarios: List[Funcionario], dia_trabalho: date, dia_semana: str, total: float) -> str:
        total_func = len(funcionarios)
        
        rows = ""
        for f in funcionarios:
            rows += f"""
            <tr style="border-bottom: 1px solid #ddd;">
                <td style="padding: 12px; color: #333;">{f.nome}</td>
                <td style="padding: 12px; color: #2E7D32; font-weight: bold;">R$ {f.valor_10_percent:.2f}</td>
                <td style="padding: 12px; color: #666;">{f.hora_entrada}</td>
                <td style="padding: 12px; color: #666;">{f.hora_saida}</td>
                <td style="padding: 12px; color: #666;">{f.observacao or '-'}</td>
            </tr>"""
        
        base_url = "https://seusite.com/downloads"
        
        return f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Salários</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background: #ffffff; }}
        .header {{ background: linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%); padding: 30px; text-align: center; }}
        .header h1 {{ color: #ffffff; margin: 0; font-size: 28px; }}
        .header p {{ color: #C8E6C9; margin: 10px 0 0 0; font-size: 16px; }}
        .content {{ padding: 30px; }}
        .info-box {{ background: #E8F5E9; border-radius: 10px; padding: 20px; margin-bottom: 25px; }}
        .info-row {{ display: flex; justify-content: space-between; margin: 10px 0; }}
        .info-label {{ color: #666; font-size: 14px; }}
        .info-value {{ color: #333; font-weight: bold; font-size: 16px; }}
        .total-value {{ color: #2E7D32; font-size: 24px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th {{ background: #1565C0; color: white; padding: 15px; text-align: left; font-weight: 600; }}
        .buttons-section {{ margin-top: 30px; padding: 25px; background: #f9f9f9; border-radius: 10px; }}
        .buttons-section h3 {{ color: #333; margin-top: 0; margin-bottom: 15px; }}
        .btn-container {{ display: flex; flex-wrap: wrap; gap: 10px; }}
        .btn {{ 
            display: inline-block; padding: 12px 24px; border-radius: 6px; text-decoration: none; 
            font-weight: bold; font-size: 14px; transition: all 0.3s ease;
        }}
        .btn-docx {{ background: #2B579A; color: white; }}
        .btn-docx:hover {{ background: #1e3f7a; }}
        .btn-excel {{ background: #217346; color: white; }}
        .btn-excel:hover {{ background: #1a5c38; }}
        .btn-csv {{ background: #6c757d; color: white; }}
        .btn-csv:hover {{ background: #5a6268; }}
        .btn-json {{ background: #FF9800; color: white; }}
        .btn-json:hover {{ background: #e68900; }}
        .btn-xml {{ background: #9C27B0; color: white; }}
        .btn-xml:hover {{ background: #7b1fa2; }}
        .btn-html {{ background: #E91E63; color: white; }}
        .btn-html:hover {{ background: #c2185b; }}
        .footer {{ background: #333; color: #fff; padding: 20px; text-align: center; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💼 Relatório de Salários dos Garçons</h1>
            <p> {dia_semana}, {dia_trabalho.strftime('%d de %B de %Y')}</p>
        </div>
        
        <div class="content">
            <div class="info-box">
                <div class="info-row">
                    <span class="info-label">📅 Data de Trabalho:</span>
                    <span class="info-value">{dia_trabalho.strftime('%d/%m/%Y')}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">📆 Dia da Semana:</span>
                    <span class="info-value">{dia_semana}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">👥 Total de Funcionários:</span>
                    <span class="info-value">{total_func}</span>
                </div>
                <div class="info-row" style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #A5D6A7;">
                    <span class="info-label" style="font-size: 16px;">💰 Total a Pagar:</span>
                    <span class="info-value total-value">R$ {total:.2f}</span>
                </div>
            </div>
            
            <h3 style="color: #333; margin-bottom: 15px;">📋 Detalhamento dos Funcionários</h3>
            <table>
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>10% (R$)</th>
                        <th>Entrada</th>
                        <th>Saída</th>
                        <th>Observação</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
            
            <div class="buttons-section">
                <h3>📥 Baixar Relatório Completo</h3>
                <p style="color: #666; margin-bottom: 15px;">Clique no formato desejado para baixar:</p>
                <div class="btn-container">
                    <a href="{base_url}/relatorio_{dia_trabalho}.docx" class="btn btn-docx">📄 DOCX</a>
                    <a href="{base_url}/relatorio_{dia_trabalho}.xlsx" class="btn btn-excel">📊 Excel</a>
                    <a href="{base_url}/relatorio_{dia_trabalho}.csv" class="btn btn-csv">📋 CSV</a>
                    <a href="{base_url}/relatorio_{dia_trabalho}.json" class="btn btn-json">📋 JSON</a>
                    <a href="{base_url}/relatorio_{dia_trabalho}.xml" class="btn btn-xml">📋 XML</a>
                    <a href="{base_url}/relatorio_{dia_trabalho}.html" class="btn btn-html">🌐 HTML</a>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>Este é um e-mail automático. Por favor, não responda.</p>
            <p>Gerado em {date.today().strftime('%d/%m/%Y às %H:%M')}</p>
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
        arquivos: dict = None
    ) -> bool:
        
        total = sum(f.valor_10_percent for f in funcionarios)
        
        msg = MIMEMultipart('related')
        msg['From'] = self.remetente
        msg['To'] = destinatario
        msg['Subject'] = f"💼 Relatório Salários Garçons - {dia_semana}, {dia_trabalho.strftime('%d/%m/%Y')}"
        
        html_content = self._criar_template_html(funcionarios, dia_trabalho, dia_semana, total)
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
        report_generator: ReportGenerator
    ) -> bool:
        
        arquivos = report_generator.generate_all()
        return self.enviar_relatorio(destinatario, funcionarios, dia_trabalho, dia_semana, arquivos)
