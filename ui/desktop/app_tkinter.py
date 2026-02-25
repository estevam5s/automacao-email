import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date, datetime
from typing import List
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.models.funcionario import Funcionario, ObservacaoGeral
from data.repositories.supabase_repository import SupabaseRepository
from services.report_generator import ReportGenerator
from services.email_service import EmailService
from config.settings import settings


class AppTkinter:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Relatório de Salários - Garçons")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        self.root.configure(bg="#1e1e2f")
        
        self.repository = SupabaseRepository()
        self.funcionarios: List[Funcionario] = []
        
        self.setup_styles()
        self.create_widgets()
        self.carregar_dados()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Main.TFrame', background='#1e1e2f')
        style.configure('Content.TFrame', background='#27293d')
        style.configure('Sidebar.TFrame', background='#1e1e2f')
        
        style.configure('TLabel', background='#27293d', foreground='#ffffff', font=('Segoe UI', 11))
        style.configure('Header.TLabel', font=('Segoe UI', 18, 'bold'), foreground='#00d4ff', background='#27293d')
        style.configure('Subheader.TLabel', font=('Segoe UI', 14, 'bold'), foreground='#00d4ff', background='#27293d')
        style.configure('Title.TLabel', font=('Segoe UI', 24, 'bold'), foreground='#ffffff', background='#1e1e2f')
        style.configure('Info.TLabel', font=('Segoe UI', 10), foreground='#a0a0a0', background='#27293d')
        
        style.configure('Card.TLabelframe', background='#323244', relief='flat', borderwidth=0)
        style.configure('Card.TLabelframe.Label', background='#323244', foreground='#00d4ff', font=('Segoe UI', 12, 'bold'))
        
        style.configure('Primary.TButton', font=('Segoe UI', 11, 'bold'), padding=12)
        style.configure('Primary.TButton', background='#00d4ff', foreground='#1e1e2f')
        style.configure('Secondary.TButton', font=('Segoe UI', 10), padding=8)
        
        style.configure('Treeview', background='#323244', foreground='#ffffff', fieldbackground='#323244', 
                       font=('Segoe UI', 10), rowheight=35)
        style.configure('Treeview.Heading', background='#00d4ff', foreground='#1e1e2f', 
                       font=('Segoe UI', 11, 'bold'), padding=10)
        style.configure('Treeview.selection', background='#00d4ff', foreground='#1e1e2f')
        
        style.configure('TEntry', fieldbackground='#323244', foreground='#ffffff', borderwidth=0, padding=8)
        
        style.configure('TCombobox', 
                       fieldbackground='#323244',
                       foreground='#ffffff', 
                       background='#323244',
                       borderwidth=0,
                       arrowcolor='#00d4ff')
        style.map('TCombobox', 
                  fieldbackground=[('readonly', '#323244')],
                  background=[('readonly', '#323244')],
                  foreground=[('readonly', '#ffffff')])
        
        style.configure('Notebook', background='#1e1e2f', borderwidth=0)
        style.configure('Notebook.Tab', background='#323244', foreground='#a0a0a0', padding=(15, 8), font=('Segoe UI', 11))
        style.map('Notebook.Tab', background=[('selected', '#00d4ff')], foreground=[('selected', '#1e1e2f')])

    def create_widgets(self):
        main_container = tk.Frame(self.root, bg='#1e1e2f')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(main_container, bg='#1e1e2f', height=80)
        header_frame.pack(fill=tk.X, padx=30, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        title = tk.Label(header_frame, text="💼 Sistema de Relatório de Salários", 
                        font=('Segoe UI', 24, 'bold'), foreground='#ffffff', bg='#1e1e2f')
        title.pack(side=tk.LEFT)
        
        subtitle = tk.Label(header_frame, text="Gerenciamento de Comissões de Garçons", 
                           font=('Segoe UI', 12), foreground='#00d4ff', bg='#1e1e2f')
        subtitle.pack(side=tk.LEFT, padx=20, anchor=tk.CENTER)
        
        date_label = tk.Label(header_frame, text=f"Data: {date.today().strftime('%d/%m/%Y')}", 
                             font=('Segoe UI', 11), foreground='#a0a0a0', bg='#1e1e2f')
        date_label.pack(side=tk.RIGHT)
        
        content_container = tk.Frame(main_container, bg='#1e1e2f')
        content_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.notebook = ttk.Notebook(content_container)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.tab_frames = {}
        self.tab_cadastro, self.tab_frames['cadastro'] = self._create_scrollable_tab()
        self.tab_registrar, self.tab_frames['registrar'] = self._create_scrollable_tab()
        self.tab_envio, self.tab_frames['envio'] = self._create_scrollable_tab()
        self.tab_supabase, self.tab_frames['supabase'] = self._create_scrollable_tab()
        self.tab_logs, self.tab_frames['logs'] = self._create_scrollable_tab()
        self.tab_historico, self.tab_frames['historico'] = self._create_scrollable_tab()
        self.tab_codigo, self.tab_frames['codigo'] = self._create_scrollable_tab()
        self.tab_docs, self.tab_frames['docs'] = self._create_scrollable_tab()
        self.tab_config, self.tab_frames['config'] = self._create_scrollable_tab()
        
        self.notebook.add(self.tab_cadastro, text="  👥  Cadastrar Funcionários  ")
        self.notebook.add(self.tab_registrar, text="  📝  Registrar Dia de Trabalho  ")
        self.notebook.add(self.tab_envio, text="  📧  Enviar E-mail com Relatório  ")
        self.notebook.add(self.tab_supabase, text="  🗄️  Supabase (BD)  ")
        self.notebook.add(self.tab_logs, text="  📋  Logs do Sistema  ")
        self.notebook.add(self.tab_historico, text="  📊  Histórico  ")
        self.notebook.add(self.tab_codigo, text="  💻  Código Fonte  ")
        self.notebook.add(self.tab_docs, text="  📚  Documentação  ")
        self.notebook.add(self.tab_config, text="  ⚙️  Configurações  ")
        
        self.create_tab_cadastro()
        self.create_tab_registrar()
        self.create_tab_envio()
        self.create_tab_supabase()
        self.create_tab_logs()
        self.create_tab_historico()
        self.create_tab_codigo()
        self.create_tab_docs()
        self.create_tab_config()

    def _create_scrollable_tab(self):
        container = ttk.Frame(self.notebook, style='Content.TFrame')
        
        canvas = tk.Canvas(container, bg='#27293d', highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#27293d')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind('<Configure>', on_canvas_configure)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        return container, scrollable_frame

    def _create_label(self, parent, text, font=('Segoe UI', 11), fg='#ffffff', bg='#27293d'):
        return tk.Label(parent, text=text, font=font, foreground=fg, background=bg)

    def _create_entry(self, parent, width=30):
        entry = tk.Entry(parent, width=width, bg='#323244', fg='#ffffff', 
                        font=('Segoe UI', 11), relief='flat', bd=0)
        entry.config(highlightbackground='#00d4ff', highlightthickness=1)
        return entry

    def _create_button(self, parent, text, command, bg='#00d4ff', fg='#1e1e2f', 
                      font=('Segoe UI', 11, 'bold'), padx=20, pady=8):
        btn = tk.Button(parent, text=text, command=command, bg=bg, fg=fg, 
                       font=font, relief='flat', padx=padx, pady=pady, cursor='hand2')
        btn.bind('<Enter>', lambda e: btn.config(bg='#00b8e6' if bg == '#00d4ff' else bg))
        btn.bind('<Leave>', lambda e: btn.config(bg=bg))
        return btn

    def create_tab_cadastro(self):
        frame = self.tab_frames['cadastro']
        
        title_frame = tk.Frame(frame, bg='#27293d')
        title_frame.pack(fill=tk.X, padx=30, pady=(30, 20))
        
        self._create_label(title_frame, "Cadastro de Funcionários", 
                         font=('Segoe UI', 20, 'bold'), fg='#00d4ff').pack(side=tk.LEFT)
        self._create_label(title_frame, "Gerencie a lista de funcionários do restaurante",
                         font=('Segoe UI', 11), fg='#a0a0a0').pack(side=tk.LEFT, padx=20, anchor=tk.CENTER)
        
        form_card = ttk.LabelFrame(frame, text="Novo Funcionário", style='Card.TLabelframe', padding=30)
        form_card.pack(fill=tk.X, padx=30, pady=10)
        
        input_frame = tk.Frame(form_card, bg='#323244')
        input_frame.pack(fill=tk.X)
        
        self._create_label(input_frame, "Nome do Funcionário:", fg='#a0a0a0').grid(row=0, column=0, sticky=tk.W, pady=10)
        self.entry_nome = self._create_entry(input_frame, width=40)
        self.entry_nome.grid(row=0, column=1, padx=15, pady=10, sticky=tk.EW)
        
        btn_frame = tk.Frame(input_frame, bg='#323244')
        btn_frame.grid(row=0, column=2, padx=15, pady=10)
        
        self._create_button(btn_frame, "✅ Cadastrar", self.cadastrar_funcionario, 
                           padx=25).pack(side=tk.LEFT)
        
        table_card = tk.Frame(frame, bg='#323244', padx=20, pady=20)
        table_card.pack(fill=tk.BOTH, expand=True, padx=30, pady=(10, 30))
        
        table_title = self._create_label(table_card, "Funcionários Cadastrados", 
                                        font=('Segoe UI', 12, 'bold'), fg='#00d4ff', bg='#323244')
        table_title.pack(anchor=tk.W, pady=(0, 10))
        
        cols = ('Nome', 'Data Cadastro', 'Status')
        self.tree_cadastro = ttk.Treeview(table_card, columns=cols, show='headings', height=8)
        
        self.tree_cadastro.heading('Nome', text='Nome do Funcionário')
        self.tree_cadastro.heading('Data Cadastro', text='Data de Cadastro')
        self.tree_cadastro.heading('Status', text='Status')
        
        self.tree_cadastro.column('Nome', width=300)
        self.tree_cadastro.column('Data Cadastro', width=150)
        self.tree_cadastro.column('Status', width=100)
        
        scrollbar = ttk.Scrollbar(table_frame := tk.Frame(table_card, bg='#323244'), 
                                  orient=tk.VERTICAL, command=self.tree_cadastro.yview)
        self.tree_cadastro.configure(yscrollcommand=scrollbar.set)
        
        self.tree_cadastro.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 0), pady=0)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=10)
        
        btn_delete_frame = tk.Frame(table_card, bg='#323244')
        btn_delete_frame.pack(fill=tk.X, pady=15)
        
        self._create_button(btn_delete_frame, "🗑️ Deletar Funcionário Selecionado", 
                           self.deletar_funcionario, bg='#e74c3c', fg='#ffffff', padx=20).pack(side=tk.LEFT, padx=5)
        
        self._create_button(btn_delete_frame, "🗑️ Deletar Todos os Funcionários", 
                           self.deletar_todos_funcionarios, bg='#c0392b', fg='#ffffff', padx=20).pack(side=tk.LEFT, padx=5)

    def create_tab_registrar(self):
        frame = self.tab_frames['registrar']
        
        title_frame = tk.Frame(frame, bg='#27293d')
        title_frame.pack(fill=tk.X, padx=30, pady=(30, 20))
        
        self._create_label(title_frame, "📝 Registro de Dia de Trabalho", 
                         font=('Segoe UI', 20, 'bold'), fg='#00d4ff').pack(side=tk.LEFT)
        
        section1 = tk.Frame(frame, bg='#323244', padx=20, pady=15)
        section1.pack(fill=tk.X, padx=30, pady=(0, 10))
        
        self._create_label(section1, "📅 1. SELECIONE A DATA", 
                         font=('Segoe UI', 12, 'bold'), fg='#00d4ff', bg='#323244').pack(anchor=tk.W, pady=(0, 10))
        
        date_row = tk.Frame(section1, bg='#323244')
        date_row.pack(fill=tk.X)
        
        self._create_label(date_row, "Data:", fg='#ffffff', bg='#323244').pack(side=tk.LEFT, padx=10)
        self.entry_dia = self._create_entry(date_row, width=20)
        self.entry_dia.insert(0, date.today().strftime("%Y-%m-%d"))
        self.entry_dia.pack(side=tk.LEFT, padx=10)
        
        section2 = tk.Frame(frame, bg='#323244', padx=20, pady=15)
        section2.pack(fill=tk.X, padx=30, pady=10)
        
        self._create_label(section2, "👤 2. DADOS DO FUNCIONÁRIO", 
                         font=('Segoe UI', 12, 'bold'), fg='#00d4ff', bg='#323244').pack(anchor=tk.W, pady=(0, 10))
        
        row1 = tk.Frame(section2, bg='#323244')
        row1.pack(fill=tk.X, pady=5)
        
        lbl_func = self._create_label(row1, "Funcionário:", fg='#a0a0a0', bg='#323244')
        lbl_func.pack(side=tk.LEFT, padx=10)
        
        self.combo_funcionarios = ttk.Combobox(row1, width=25, state='readonly', font=('Segoe UI', 11))
        self.combo_funcionarios.pack(side=tk.LEFT, padx=10)
        
        lbl_10 = self._create_label(row1, "10% das Vendas (R$):", fg='#a0a0a0', bg='#323244')
        lbl_10.pack(side=tk.LEFT, padx=10)
        
        self.entry_10 = self._create_entry(row1, width=15)
        self.entry_10.pack(side=tk.LEFT, padx=10)
        
        section3 = tk.Frame(frame, bg='#323244', padx=20, pady=15)
        section3.pack(fill=tk.X, padx=30, pady=10)
        
        self._create_label(section3, "⏰ 3. HORÁRIOS", 
                         font=('Segoe UI', 12, 'bold'), fg='#00d4ff', bg='#323244').pack(anchor=tk.W, pady=(0, 10))
        
        row2 = tk.Frame(section3, bg='#323244')
        row2.pack(fill=tk.X, pady=5)
        
        self._create_label(row2, "Entrada:", fg='#a0a0a0', bg='#323244').pack(side=tk.LEFT, padx=10)
        self.entry_entrada = self._create_entry(row2, width=12)
        self.entry_entrada.insert(0, "08:00")
        self.entry_entrada.pack(side=tk.LEFT, padx=10)
        
        self._create_label(row2, "Saída:", fg='#a0a0a0', bg='#323244').pack(side=tk.LEFT, padx=10)
        self.entry_saida = self._create_entry(row2, width=12)
        self.entry_saida.insert(0, "16:00")
        self.entry_saida.pack(side=tk.LEFT, padx=10)
        
        section4 = tk.Frame(frame, bg='#323244', padx=20, pady=15)
        section4.pack(fill=tk.X, padx=30, pady=10)
        
        self._create_label(section4, "💳 4. VALE (Opcional)", 
                         font=('Segoe UI', 12, 'bold'), fg='#00d4ff', bg='#323244').pack(anchor=tk.W, pady=(0, 10))
        
        row3 = tk.Frame(section4, bg='#323244')
        row3.pack(fill=tk.X, pady=5)
        
        self._create_label(row3, "Valor do Vale (R$):", fg='#a0a0a0', bg='#323244').pack(side=tk.LEFT, padx=10)
        self.entry_vale = self._create_entry(row3, width=12)
        self.entry_vale.pack(side=tk.LEFT, padx=10)
        
        self._create_label(row3, "Tipo do Vale:", fg='#a0a0a0', bg='#323244').pack(side=tk.LEFT, padx=10)
        self.combo_tipo = ttk.Combobox(row3, values=['', 'pix', 'dinheiro'], width=12, state='readonly')
        self.combo_tipo.pack(side=tk.LEFT, padx=10)
        
        self._create_label(row3, "(Preencha apenas se o funcionário recebeu vale)", 
                         fg='#666666', bg='#323244', font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=10)
        
        section5 = tk.Frame(frame, bg='#323244', padx=20, pady=15)
        section5.pack(fill=tk.X, padx=30, pady=10)
        
        self._create_label(section5, "✅ 5. PAGAMENTO DO SALÁRIO", 
                         font=('Segoe UI', 12, 'bold'), fg='#00d4ff', bg='#323244').pack(anchor=tk.W, pady=(0, 10))
        
        row5 = tk.Frame(section5, bg='#323244')
        row5.pack(fill=tk.X, pady=5)
        
        self._create_label(row5, "Status do Pagamento:", fg='#a0a0a0', bg='#323244').pack(side=tk.LEFT, padx=10)
        
        self.pago_var = tk.BooleanVar()
        checkbox = tk.Checkbutton(row5, text="Salário Pago", variable=self.pago_var, bg='#323244', 
                                fg='#ffffff', selectcolor='#27ae60', font=('Segoe UI', 11, 'bold'))
        checkbox.pack(side=tk.LEFT, padx=10)
        
        self._create_label(row5, "Tipo de Pagamento:", fg='#a0a0a0', bg='#323244').pack(side=tk.LEFT, padx=20)
        self.combo_pagamento = ttk.Combobox(row5, values=['pix', 'dinheiro'], width=12, state='readonly')
        self.combo_pagamento.current(0)
        self.combo_pagamento.pack(side=tk.LEFT, padx=10)
        
        section6 = tk.Frame(frame, bg='#323244', padx=20, pady=15)
        section6.pack(fill=tk.X, padx=30, pady=10)
        
        self._create_label(section6, "📝 6. OBSERVAÇÃO", 
                         font=('Segoe UI', 12, 'bold'), fg='#00d4ff', bg='#323244').pack(anchor=tk.W, pady=(0, 10))
        
        row4 = tk.Frame(section6, bg='#323244')
        row4.pack(fill=tk.X, pady=5)
        
        self.entry_obs = self._create_entry(row4, width=50)
        self.entry_obs.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        section7 = tk.Frame(frame, bg='#323244', padx=20, pady=15)
        section7.pack(fill=tk.X, padx=30, pady=10)
        
        btn_row = tk.Frame(section7, bg='#323244')
        btn_row.pack()
        
        self._create_button(btn_row, "🧹 Limpar Campos", self.limpar_campos_registro, 
                          bg='#e74c3c', fg='#ffffff', padx=25).pack(side=tk.LEFT, padx=10)
        
        self._create_button(btn_row, "➕ Adicionar Registro", self.adicionar_registro, 
                          bg='#27ae60', fg='#ffffff', padx=25).pack(side=tk.LEFT, padx=10)
        
        self._create_button(btn_row, "👁️ Ver Registros do Dia", self.carregar_dia, 
                          bg='#3498db', fg='#ffffff', padx=25).pack(side=tk.LEFT, padx=10)
        
        table_card = tk.Frame(frame, bg='#323244', padx=20, pady=20)
        table_card.pack(fill=tk.BOTH, expand=True, padx=30, pady=(10, 30))
        
        table_title = self._create_label(table_card, "Registros do Dia", 
                                        font=('Segoe UI', 12, 'bold'), fg='#00d4ff', bg='#323244')
        table_title.pack(anchor=tk.W, pady=(0, 10))
        
        cols = ('Nome', '10%', 'Entrada', 'Saída', 'Vale', 'Tipo', 'Pago', 'Observação')
        self.tree_registrar = ttk.Treeview(table_card, columns=cols, show='headings', height=10)
        
        widths = [180, 80, 80, 80, 80, 70, 60, 150]
        headings = ['Nome', '10% (R$)', 'Entrada', 'Saída', 'Vale (R$)', 'Tipo', 'Pago', 'Observação']
        
        for col, width, heading in zip(cols, widths, headings):
            self.tree_registrar.heading(col, text=heading)
            self.tree_registrar.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(table_frame := tk.Frame(table_card, bg='#323244'), 
                                  orient=tk.VERTICAL, command=self.tree_registrar.yview)
        self.tree_registrar.configure(yscrollcommand=scrollbar.set)
        
        self.tree_registrar.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 0), pady=0)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=10)
        
        btn_delete_frame = tk.Frame(table_card, bg='#323244')
        btn_delete_frame.pack(fill=tk.X, pady=10)
        
        self._create_button(btn_delete_frame, "🗑️ Deletar Registro Selecionado", self.deletar_registro_selecionado, 
                           bg='#e74c3c', fg='#ffffff', padx=20).pack(side=tk.LEFT, padx=5)
        
        self._create_button(btn_delete_frame, "🔄 Recarregar Registros", self.carregar_dia, 
                           bg='#3498db', fg='#ffffff', padx=20).pack(side=tk.LEFT, padx=5)

    def create_tab_envio(self):
        frame = self.tab_frames['envio']
        
        title_frame = tk.Frame(frame, bg='#27293d')
        title_frame.pack(fill=tk.X, padx=30, pady=(30, 20))
        
        self._create_label(title_frame, "Enviar E-mail com Relatório", 
                         font=('Segoe UI', 20, 'bold'), fg='#00d4ff').pack(side=tk.LEFT)
        self._create_label(title_frame, "Envie o relatório diário por e-mail",
                         font=('Segoe UI', 11), fg='#a0a0a0').pack(side=tk.LEFT, padx=20, anchor=tk.CENTER)
        
        date_card = ttk.LabelFrame(frame, text="Selecionar Data", style='Card.TLabelframe', padding=25)
        date_card.pack(fill=tk.X, padx=30, pady=10)
        
        date_frame = tk.Frame(date_card, bg='#323244')
        date_frame.pack(fill=tk.X)
        
        self._create_label(date_frame, "Data (AAAA-MM-DD):", fg='#a0a0a0').grid(row=0, column=0, sticky=tk.W, pady=10)
        self.entry_dia_envio = self._create_entry(date_frame, width=20)
        self.entry_dia_envio.insert(0, date.today().strftime("%Y-%m-%d"))
        self.entry_dia_envio.grid(row=0, column=1, padx=15, pady=10, sticky=tk.W)
        
        self._create_button(date_frame, "📥 Carregar Dados do Dia", self.carregar_dia_envio, 
                           padx=20).grid(row=0, column=2, padx=15, pady=10)
        
        self._create_button(date_frame, "🗑️ Limpar Dados", self.limpar_dados_envio, 
                           bg='#e74c3c', fg='#ffffff', padx=20).grid(row=0, column=3, padx=15, pady=10)
        
        obs_card = ttk.LabelFrame(frame, text="Observação Geral do Dia", style='Card.TLabelframe', padding=20)
        obs_card.pack(fill=tk.X, padx=30, pady=10)
        
        obs_frame = tk.Frame(obs_card, bg='#323244')
        obs_frame.pack(fill=tk.X)
        
        self.txt_obs = tk.Text(obs_frame, width=80, height=4, bg='#323244', fg='#ffffff', 
                               font=('Segoe UI', 11), relief='flat', bd=0)
        self.txt_obs.pack(fill=tk.X, pady=5)
        
        self._create_button(obs_frame, "💾 Salvar Observação", self.salvar_obs_geral, 
                           bg='#27ae60', padx=15).pack(side=tk.RIGHT, pady=5)
        
        table_card = tk.Frame(frame, bg='#323244', padx=20, pady=20)
        table_card.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        table_title = self._create_label(table_card, "Funcionários do Dia", 
                                        font=('Segoe UI', 12, 'bold'), fg='#00d4ff', bg='#323244')
        table_title.pack(anchor=tk.W, pady=(0, 10))
        
        cols = ('Nome', '10%', 'Entrada', 'Saída', 'Vale', 'Tipo', 'Pago', 'Obs')
        self.tree_envio = ttk.Treeview(table_card, columns=cols, show='headings', height=8)
        
        widths = [180, 80, 80, 80, 80, 70, 60, 150]
        headings = ['Nome', '10% (R$)', 'Entrada', 'Saída', 'Vale (R$)', 'Tipo', 'Pago', 'Observação']
        
        for col, width, heading in zip(cols, widths, headings):
            self.tree_envio.heading(col, text=heading)
            self.tree_envio.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(table_frame := tk.Frame(table_card, bg='#323244'), 
                                  orient=tk.VERTICAL, command=self.tree_envio.yview)
        self.tree_envio.configure(yscrollcommand=scrollbar.set)
        
        self.tree_envio.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 0), pady=0)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=10)
        
        self.lbl_total = self._create_label(frame, "Total: R$ 0.00", 
                                           font=('Segoe UI', 16, 'bold'), fg='#00d4ff', bg='#27293d')
        self.lbl_total.pack(pady=10)
        
        action_card = ttk.LabelFrame(frame, text="Ações", style='Card.TLabelframe', padding=25)
        action_card.pack(fill=tk.X, padx=30, pady=(10, 30))
        
        email_frame = tk.Frame(action_card, bg='#323244')
        email_frame.pack(fill=tk.X, pady=10)
        
        self._create_label(email_frame, "E-mail do Destinatário:", fg='#a0a0a0').grid(row=0, column=0, sticky=tk.W, pady=10)
        self.entry_email = self._create_entry(email_frame, width=40)
        self.entry_email.insert(0, "estevams186@gmail.com")
        self.entry_email.grid(row=0, column=1, padx=15, pady=10, sticky=tk.EW)
        
        self._create_button(email_frame, "📧 Enviar E-mail", self.enviar_email, 
                           bg='#3498db', padx=25).grid(row=0, column=2, padx=15, pady=10)
        
        format_frame = tk.Frame(action_card, bg='#323244')
        format_frame.pack(fill=tk.X, pady=10)
        
        self._create_label(format_frame, "Gerar Relatório em:", fg='#a0a0a0').grid(row=0, column=0, sticky=tk.W, pady=10)
        self.formato_var = tk.StringVar(value="Excel")
        formatos = ["Excel", "DOCX", "CSV", "JSON", "XML", "HTML"]
        
        for i, fmt in enumerate(formatos):
            rb = tk.Radiobutton(format_frame, text=fmt, variable=self.formato_var, value=fmt,
                               bg='#323244', fg='#ffffff', selectcolor='#00d4ff', font=('Segoe UI', 10))
            rb.grid(row=0, column=i+1, padx=15, pady=10)
        
        self._create_button(format_frame, "📄 Gerar Relatório", self.gerar_relatorio, 
                           bg='#9b59b6', padx=25).grid(row=0, column=len(formatos)+1, padx=15, pady=10)

    def create_tab_config(self):
        frame = self.tab_frames['config']
        
        title_frame = tk.Frame(frame, bg='#27293d')
        title_frame.pack(fill=tk.X, padx=30, pady=(30, 20))
        
        self._create_label(title_frame, "Configurações do Sistema", 
                         font=('Segoe UI', 20, 'bold'), fg='#00d4ff').pack(side=tk.LEFT)
        self._create_label(title_frame, "Configure as opções de e-mail",
                         font=('Segoe UI', 11), fg='#a0a0a0').pack(side=tk.LEFT, padx=20, anchor=tk.CENTER)
        
        config_card = ttk.LabelFrame(frame, text="Configurações de E-mail", style='Card.TLabelframe', padding=30)
        config_card.pack(fill=tk.X, padx=30, pady=20)
        
        row1 = tk.Frame(config_card, bg='#323244')
        row1.pack(fill=tk.X, pady=10)
        
        self._create_label(row1, "E-mail Remetente:", fg='#a0a0a0').grid(row=0, column=0, sticky=tk.W, pady=10)
        self.entry_remetente = self._create_entry(row1, width=45)
        self.entry_remetente.grid(row=0, column=1, padx=15, pady=10, sticky=tk.EW)
        
        row2 = tk.Frame(config_card, bg='#323244')
        row2.pack(fill=tk.X, pady=10)
        
        self._create_label(row2, "E-mail Destinatário:", fg='#a0a0a0').grid(row=0, column=0, sticky=tk.W, pady=10)
        self.entry_dest = self._create_entry(row2, width=45)
        self.entry_dest.grid(row=0, column=1, padx=15, pady=10, sticky=tk.EW)
        
        row3 = tk.Frame(config_card, bg='#323244')
        row3.pack(fill=tk.X, pady=10)
        
        self._create_label(row3, "Senha de App Gmail:", fg='#a0a0a0').grid(row=0, column=0, sticky=tk.W, pady=10)
        self.entry_senha = self._create_entry(row3, width=45)
        self.entry_senha.config(show="*")
        self.entry_senha.grid(row=0, column=1, padx=15, pady=10, sticky=tk.EW)
        
        info_card = tk.Frame(config_card, bg='#2c2c3e', padx=20, pady=15)
        info_card.pack(fill=tk.X, pady=20)
        
        self._create_label(info_card, "ℹ️ Para obter a senha de app do Gmail:", 
                         font=('Segoe UI', 10, 'bold'), fg='#00d4ff').pack(anchor=tk.W, pady=(0, 5))
        self._create_label(info_card, "1. Acesse myaccount.google.com/apppasswords", 
                         font=('Segoe UI', 9), fg='#a0a0a0').pack(anchor=tk.W)
        self._create_label(info_card, "2. Selecione 'E-mail' como app", 
                         font=('Segoe UI', 9), fg='#a0a0a0').pack(anchor=tk.W)
        self._create_label(info_card, "3. Gere e copie a senha de 16 caracteres", 
                         font=('Segoe UI', 9), fg='#a0a0a0').pack(anchor=tk.W)
        
        self._create_button(config_card, "💾 Salvar Configurações", self.salvar_config, 
                           bg='#27ae60', padx=30).pack(pady=20)
        
        self.carregar_config()

    def create_tab_supabase(self):
        frame = self.tab_frames['supabase']
        
        title_frame = tk.Frame(frame, bg='#27293d')
        title_frame.pack(fill=tk.X, padx=30, pady=(30, 20))
        
        self._create_label(title_frame, "Gerenciamento do Banco de Dados Supabase", 
                         font=('Segoe UI', 20, 'bold'), fg='#00d4ff').pack(side=tk.LEFT)
        
        info_card = tk.Frame(frame, bg='#323244', padx=20, pady=15)
        info_card.pack(fill=tk.X, padx=30, pady=10)
        
        self._create_label(info_card, "📊 Tabelas do Banco de Dados", 
                         font=('Segoe UI', 14, 'bold'), fg='#00d4ff', bg='#323244').pack(anchor=tk.W, pady=(0, 10))
        
        tables = [
            ("funcionarios", "Funcionários - Registros de salários e dados dos garçons"),
            ("configuracoes", "Configurações - Configurações de e-mail do sistema"),
            ("observacoes_gerais", "Observações Gerais - Observações diárias do trabalho"),
            ("registros_trabalho", "Registros de Trabalho - Controle de dias trabalhados"),
            ("logs", "Logs - Histórico de ações do sistema")
        ]
        
        for table_name, description in tables:
            table_frame = tk.Frame(info_card, bg='#2c2c3e', padx=15, pady=10)
            table_frame.pack(fill=tk.X, pady=5)
            
            self._create_label(table_frame, f"📋 {table_name}", 
                             font=('Segoe UI', 12, 'bold'), fg='#ffffff', bg='#2c2c3e').pack(anchor=tk.W)
            self._create_label(table_frame, description, 
                             font=('Segoe UI', 9), fg='#a0a0a0', bg='#2c2c3e').pack(anchor=tk.W)
            
            btn_frame = tk.Frame(table_frame, bg='#2c2c3e')
            btn_frame.pack(anchor=tk.W, pady=8)
            
            self._create_button(btn_frame, "👁️ Visualizar", 
                              lambda t=table_name: self.visualizar_tabela(t), 
                              bg='#3498db', fg='#ffffff', padx=15).pack(side=tk.LEFT, padx=5)
            
            self._create_button(btn_frame, "➕ Inserir", 
                              lambda t=table_name: self.inserir_registro(t), 
                              bg='#27ae60', fg='#ffffff', padx=15).pack(side=tk.LEFT, padx=5)
            
            self._create_button(btn_frame, "🔄 Atualizar", 
                              lambda t=table_name: self.atualizar_registro(t), 
                              bg='#f39c12', fg='#ffffff', padx=15).pack(side=tk.LEFT, padx=5)
            
            self._create_button(btn_frame, "🗑️ Deletar", 
                              lambda t=table_name: self.deletar_registro(t), 
                              bg='#e74c3c', fg='#ffffff', padx=15).pack(side=tk.LEFT, padx=5)
        
        db_info_card = tk.Frame(frame, bg='#323244', padx=20, pady=15)
        db_info_card.pack(fill=tk.X, padx=30, pady=10)
        
        self._create_label(db_info_card, "ℹ️ Informações do Banco", 
                         font=('Segoe UI', 14, 'bold'), fg='#00d4ff', bg='#323244').pack(anchor=tk.W, pady=(0, 10))
        
        self._create_label(db_info_card, f"URL: {settings.SUPABASE_URL}", 
                         font=('Segoe UI', 10), fg='#a0a0a0', bg='#323244').pack(anchor=tk.W)
        
        self._create_label(db_info_card, "Status: 🟢 Conectado", 
                         font=('Segoe UI', 10), fg='#27ae60', bg='#323244').pack(anchor=tk.W)

    def create_tab_logs(self):
        frame = self.tab_frames['logs']
        
        title_frame = tk.Frame(frame, bg='#27293d')
        title_frame.pack(fill=tk.X, padx=30, pady=(30, 20))
        
        self._create_label(title_frame, "📋 Logs do Sistema em Tempo Real", 
                         font=('Segoe UI', 20, 'bold'), fg='#00d4ff').pack(side=tk.LEFT)
        
        btn_atualizar = self._create_button(title_frame, "🔄 Atualizar Logs", self.atualizar_logs_tempo_real, 
                           bg='#3498db', fg='#ffffff', padx=20)
        btn_atualizar.pack(side=tk.RIGHT, padx=10)
        
        filtros_card = tk.Frame(frame, bg='#323244', padx=20, pady=15)
        filtros_card.pack(fill=tk.X, padx=30, pady=10)
        
        self._create_label(filtros_card, "🎯 Filtros:", 
                         font=('Segoe UI', 12, 'bold'), fg='#00d4ff', bg='#323244').pack(side=tk.LEFT, padx=10)
        
        self.combo_filtro_acao = ttk.Combobox(filtros_card, values=['Todos', 'CRIAR', 'ATUALIZAR', 'DELETAR', 'VISUALIZAR', 'ENVIAR_EMAIL'], 
                                              width=15, state='readonly')
        self.combo_filtro_acao.current(0)
        self.combo_filtro_acao.pack(side=tk.LEFT, padx=10)
        
        self.combo_filtro_tabela = ttk.Combobox(filtros_card, values=['Todas', 'funcionarios', 'configuracoes', 'observacoes_gerais', 'logs', 'registros_trabalho'], 
                                                width=18, state='readonly')
        self.combo_filtro_tabela.current(0)
        self.combo_filtro_tabela.pack(side=tk.LEFT, padx=10)
        
        self._create_button(filtros_card, "🔍 Aplicar Filtro", self.aplicar_filtro_logs, 
                          bg='#9b59b6', fg='#ffffff', padx=20).pack(side=tk.LEFT, padx=10)
        
        self._create_button(filtros_card, "🗑️ Limpar Logs", self.limpar_logs, 
                          bg='#e74c3c', fg='#ffffff', padx=20).pack(side=tk.LEFT, padx=10)
        
        table_card = tk.Frame(frame, bg='#323244', padx=20, pady=15)
        table_card.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        cols = ('ID', 'Data/Hora', 'Ação', 'Tabela', 'Registro ID', 'Usuário')
        self.tree_logs = ttk.Treeview(table_card, columns=cols, show='headings', height=15)
        
        widths = [200, 160, 100, 120, 180, 100]
        headings = ['ID', 'Data/Hora', 'Ação', 'Tabela', 'Registro ID', 'Usuário']
        
        for col, width, heading in zip(cols, widths, headings):
            self.tree_logs.heading(col, text=heading)
            self.tree_logs.column(col, width=width)
        
        scrollbar_y = ttk.Scrollbar(table_card, orient=tk.VERTICAL, command=self.tree_logs.yview)
        scrollbar_x = ttk.Scrollbar(table_card, orient=tk.HORIZONTAL, command=self.tree_logs.xview)
        self.tree_logs.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.tree_logs.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, sticky='ew')
        
        table_card.grid_rowconfigure(0, weight=1)
        table_card.grid_columnconfigure(0, weight=1)
        
        info_card = tk.Frame(frame, bg='#323244', padx=20, pady=15)
        info_card.pack(fill=tk.X, padx=30, pady=10)
        
        self.lbl_total_logs = self._create_label(info_card, "Total de logs: 0", 
                                              font=('Segoe UI', 11), fg='#00d4ff', bg='#323244')
        self.lbl_total_logs.pack(side=tk.LEFT, padx=10)
        
        self.lbl_status_logs = self._create_label(info_card, "Status: Carregando...", 
                                                 font=('Segoe UI', 10), fg='#f39c12', bg='#323244')
        self.lbl_status_logs.pack(side=tk.RIGHT, padx=10)

    def atualizar_logs_tempo_real(self):
        try:
            self.lbl_status_logs.config(text="Status: Carregando...", fg='#f39c12')
            self.root.update()
            
            logs = self.repository.listar_logs(limite=200)
            self.atualizar_tree_logs(logs)
            
            self.lbl_status_logs.config(text=f"Status: {len(logs)} logs carregados", fg='#27ae60')
            messagebox.showinfo("Sucesso", f"Carregados {len(logs)} logs")
        except Exception as e:
            self.lbl_status_logs.config(text=f"Status: Erro - {str(e)[:50]}", fg='#e74c3c')
            messagebox.showerror("Erro", f"Erro ao carregar logs: {str(e)}")
    
    def atualizar_tree_logs(self, logs):
        for item in self.tree_logs.get_children():
            self.tree_logs.delete(item)
        
        acao_icone = {
            'CRIAR': '✅',
            'ATUALIZAR': '✏️',
            'DELETAR': '🗑️',
            'VISUALIZAR': '👁️',
            'ENVIAR_EMAIL': '📧'
        }
        
        for log in logs:
            icone = acao_icone.get(log.acao, '📋')
            data_formatada = log.created_at[:19] if log.created_at else '-'
            
            log_id = str(log.id)[:8] if log.id else '-'
            
            self.tree_logs.insert('', tk.END, values=(
                log_id,
                data_formatada,
                f"{icone} {log.acao}",
                log.tabela,
                log.registro_id or '-',
                log.usuario
            ))
        
        self.lbl_total_logs.config(text=f"Total de logs: {len(logs)}")
    
    def aplicar_filtro_logs(self):
        try:
            acao = self.combo_filtro_acao.get()
            tabela = self.combo_filtro_tabela.get()
            
            self.lbl_status_logs.config(text="Status: Filtrando...", fg='#f39c12')
            self.root.update()
            
            if acao == 'Todos' and tabela == 'Todas':
                logs = self.repository.listar_logs(limite=200)
            elif acao != 'Todos' and tabela == 'Todas':
                logs = self.repository.listar_logs_por_acao(acao, limite=200)
            elif acao == 'Todos' and tabela != 'Todas':
                logs = self.repository.listar_logs_por_tabela(tabela, limite=200)
            else:
                logs = self.repository.listar_logs(limite=200)
                logs = [l for l in logs if l.acao == acao and l.tabela == tabela]
            
            self.atualizar_tree_logs(logs)
            self.lbl_status_logs.config(text=f"Status: {len(logs)} logs encontrados", fg='#27ae60')
            messagebox.showinfo("Sucesso", f"Encontrados {len(logs)} logs")
        except Exception as e:
            self.lbl_status_logs.config(text=f"Status: Erro", fg='#e74c3c')
            messagebox.showerror("Erro", f"Erro ao filtrar: {str(e)}")
    
    def limpar_logs(self):
        if messagebox.askyesno("Confirmar", "Deseja limpar TODOS os logs? Esta ação não pode ser desfeita!"):
            try:
                self.lbl_status_logs.config(text="Status: Limpando...", fg='#f39c12')
                self.root.update()
                
                self.repository.limpar_logs()
                self.atualizar_tree_logs([])
                
                self.lbl_status_logs.config(text="Status: Logs limpos", fg='#27ae60')
                messagebox.showinfo("Sucesso", "Logs limpos com sucesso!")
            except Exception as e:
                self.lbl_status_logs.config(text=f"Status: Erro", fg='#e74c3c')
                messagebox.showerror("Erro", f"Erro ao limpar: {str(e)}")

    def create_tab_historico(self):
        frame = self.tab_frames['historico']
        
        title_frame = tk.Frame(frame, bg='#27293d')
        title_frame.pack(fill=tk.X, padx=30, pady=(30, 20))
        
        self._create_label(title_frame, "📊 Histórico e Estatísticas", 
                         font=('Segoe UI', 20, 'bold'), fg='#00d4ff').pack(side=tk.LEFT)
        
        btn_atualizar = self._create_button(title_frame, "🔄 Atualizar Dados", self.atualizar_historico,
                           bg='#3498db', fg='#ffffff', padx=20)
        btn_atualizar.pack(side=tk.RIGHT, padx=10)
        
        stats_card = tk.Frame(frame, bg='#323244', padx=20, pady=15)
        stats_card.pack(fill=tk.X, padx=30, pady=10)
        
        self._create_label(stats_card, "📈 RESUMO GERAL DO SISTEMA", 
                         font=('Segoe UI', 14, 'bold'), fg='#00d4ff', bg='#323244').pack(pady=(0, 15))
        
        self.stats_labels = {}
        stats_items = [
            ('total_cadastrados', '👥 Total de Funcionários:', '0'),
            ('total_registros', '📝 Total de Registros:', '0'),
            ('total_dias', '📅 Dias Trabalhados:', '0'),
            ('total_geral', '💰 Total Geral (10%):', 'R$ 0,00'),
            ('total_pago', '✅ Total Pago:', 'R$ 0,00'),
            ('total_pendente', '⏳ Total Pendente:', 'R$ 0,00'),
        ]
        
        stats_grid = tk.Frame(stats_card, bg='#323244')
        stats_grid.pack(fill=tk.X, pady=10)
        
        for i, (key, label, default) in enumerate(stats_items):
            row, col = i // 3, i % 3
            cell = tk.Frame(stats_grid, bg='#2a2a3e', padx=15, pady=15)
            cell.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            cell.grid_rowconfigure(0, weight=1)
            cell.grid_columnconfigure(0, weight=1)
            
            tk.Label(cell, text=label, font=('Segoe UI', 11), fg='#a0a0a0', bg='#2a2a3e').pack()
            self.stats_labels[key] = tk.Label(cell, text=default, font=('Segoe UI', 16, 'bold'), fg='#00d4ff', bg='#2a2a3e')
            self.stats_labels[key].pack()
        
        stats_grid.grid_columnconfigure((0, 1, 2), weight=1)
        
        notebook_historico = ttk.Notebook(frame)
        notebook_historico.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        tab_ranking = tk.Frame(notebook_historico, bg='#27293d')
        tab_presenca = tk.Frame(notebook_historico, bg='#27293d')
        tab_pagamentos = tk.Frame(notebook_historico, bg='#27293d')
        tab_cadastramento = tk.Frame(notebook_historico, bg='#27293d')
        
        notebook_historico.add(tab_ranking, text=" 🏆 Ranking de Pagamentos ")
        notebook_historico.add(tab_presenca, text=" 📅 Histórico de Presença ")
        notebook_historico.add(tab_pagamentos, text=" 💵 Histórico de Pagamentos ")
        notebook_historico.add(tab_cadastramento, text=" 📋 Data de Cadastramento ")
        
        self._create_ranking_tab(tab_ranking)
        self._create_presenca_tab(tab_presenca)
        self._create_pagamentos_tab(tab_pagamentos)
        self._create_cadastramento_tab(tab_cadastramento)
        
        self.atualizar_historico()

    def _create_ranking_tab(self, parent):
        table_card = tk.Frame(parent, bg='#323244', padx=20, pady=15)
        table_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        cols = ('Posição', 'Funcionário', 'Dias Trab.', 'Total Recebido', 'Média Diária', 'Maior', 'Menor', 'Pago', 'Pendente')
        self.tree_ranking = ttk.Treeview(table_card, columns=cols, show='headings', height=18)
        
        widths = [60, 150, 80, 100, 90, 80, 80, 90, 90]
        headings = ['Posição', 'Funcionário', 'Dias', 'Total', 'Média', 'Maior', 'Menor', 'Pago', 'Pendente']
        
        for col, width, heading in zip(cols, widths, headings):
            self.tree_ranking.heading(col, text=heading)
            self.tree_ranking.column(col, width=width, anchor='center')
        
        scrollbar = ttk.Scrollbar(table_card, orient=tk.VERTICAL, command=self.tree_ranking.yview)
        self.tree_ranking.configure(yscrollcommand=scrollbar.set)
        
        self.tree_ranking.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _create_presenca_tab(self, parent):
        search_frame = tk.Frame(parent, bg='#323244', padx=20, pady=10)
        search_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self._create_label(search_frame, "🔍 Buscar funcionário:", fg='#a0a0a0', bg='#323244').pack(side=tk.LEFT, padx=10)
        self.entry_busca_presenca = self._create_entry(search_frame, width=30)
        self.entry_busca_presenca.pack(side=tk.LEFT, padx=10)
        self._create_button(search_frame, "Buscar", self.buscar_presenca, bg='#3498db', fg='#ffffff', padx=15).pack(side=tk.LEFT, padx=10)
        self._create_button(search_frame, "Limpar", self.limpar_busca_presenca, bg='#95a5a6', fg='#ffffff', padx=15).pack(side=tk.LEFT, padx=10)
        
        table_card = tk.Frame(parent, bg='#323244', padx=20, pady=15)
        table_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        cols = ('Data', 'Funcionário', 'Entrada', 'Saída', 'Valor 10%', 'Observação')
        self.tree_presenca = ttk.Treeview(table_card, columns=cols, show='headings', height=18)
        
        widths = [100, 150, 80, 80, 100, 200]
        headings = ['Data', 'Funcionário', 'Entrada', 'Saída', 'Valor', 'Observação']
        
        for col, width, heading in zip(cols, widths, headings):
            self.tree_presenca.heading(col, text=heading)
            self.tree_presenca.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(table_card, orient=tk.VERTICAL, command=self.tree_presenca.yview)
        self.tree_presenca.configure(yscrollcommand=scrollbar.set)
        
        self.tree_presenca.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _create_pagamentos_tab(self, parent):
        search_frame = tk.Frame(parent, bg='#323244', padx=20, pady=10)
        search_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self._create_label(search_frame, "🔍 Buscar funcionário:", fg='#a0a0a0', bg='#323244').pack(side=tk.LEFT, padx=10)
        self.entry_busca_pagamento = self._create_entry(search_frame, width=30)
        self.entry_busca_pagamento.pack(side=tk.LEFT, padx=10)
        self._create_button(search_frame, "Buscar", self.buscar_pagamentos, bg='#3498db', fg='#ffffff', padx=15).pack(side=tk.LEFT, padx=10)
        
        table_card = tk.Frame(parent, bg='#323244', padx=20, pady=15)
        table_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        cols = ('Funcionário', 'Data', 'Valor', 'Vale', 'Tipo Pagto', 'Status')
        self.tree_pagamentos = ttk.Treeview(table_card, columns=cols, show='headings', height=18)
        
        widths = [150, 100, 100, 80, 100, 80]
        headings = ['Funcionário', 'Data', 'Valor', 'Vale', 'Tipo', 'Status']
        
        for col, width, heading in zip(cols, widths, headings):
            self.tree_pagamentos.heading(col, text=heading)
            self.tree_pagamentos.column(col, width=width, anchor='center')
        
        scrollbar = ttk.Scrollbar(table_card, orient=tk.VERTICAL, command=self.tree_pagamentos.yview)
        self.tree_pagamentos.configure(yscrollcommand=scrollbar.set)
        
        self.tree_pagamentos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _create_cadastramento_tab(self, parent):
        table_card = tk.Frame(parent, bg='#323244', padx=20, pady=15)
        table_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        cols = ('Funcionário', 'Primeiro Dia', 'Último Dia', 'Dias Trab.', 'Total Recebido')
        self.tree_cadastramento = ttk.Treeview(table_card, columns=cols, show='headings', height=18)
        
        widths = [150, 110, 110, 100, 120]
        headings = ['Funcionário', 'Primeiro Dia', 'Último Dia', 'Dias Trab.', 'Total Recebido']
        
        for col, width, heading in zip(cols, widths, headings):
            self.tree_cadastramento.heading(col, text=heading)
            self.tree_cadastramento.column(col, width=width, anchor='center')
        
        scrollbar = ttk.Scrollbar(table_card, orient=tk.VERTICAL, command=self.tree_cadastramento.yview)
        self.tree_cadastramento.configure(yscrollcommand=scrollbar.set)
        
        self.tree_cadastramento.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def atualizar_historico(self):
        try:
            total = self.repository.get_total_funcionarios()
            
            self.stats_labels['total_cadastrados'].config(text=str(total.total_cadastrados))
            self.stats_labels['total_registros'].config(text=str(total.total_registros))
            self.stats_labels['total_dias'].config(text=str(total.total_dias_trabalhados))
            self.stats_labels['total_geral'].config(text=f"R$ {total.total_geral_pago:,.2f}")
            self.stats_labels['total_pago'].config(text=f"R$ {total.total_pago:,.2f}")
            self.stats_labels['total_pendente'].config(text=f"R$ {total.total_pendente:,.2f}")
            
            ranking = self.repository.listar_ranking_pagamentos()
            self.atualizar_tree_ranking(ranking)
            
            presenca = self.repository.listar_historico_presenca(limite=200)
            self.atualizar_tree_presenca(presenca)
            
            pagamentos = self.repository.listar_historico_pagamentos(limite=200)
            self.atualizar_tree_pagamentos(pagamentos)
            
            cadastramento = self.repository.listar_data_cadastramento()
            self.atualizar_tree_cadastramento(cadastramento)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar histórico: {str(e)}")

    def atualizar_tree_ranking(self, ranking):
        for item in self.tree_ranking.get_children():
            self.tree_ranking.delete(item)
        
        for r in ranking:
            self.tree_ranking.insert('', tk.END, values=(
                f"#{r.posicao}",
                r.nome,
                r.dias_trabalhados,
                f"R$ {r.total_recebido:,.2f}",
                f"R$ {r.media_diaria:,.2f}",
                f"R$ {r.maior_diaria:,.2f}",
                f"R$ {r.menor_diaria:,.2f}",
                f"R$ {r.total_pago:,.2f}",
                f"R$ {r.total_pendente:,.2f}"
            ))

    def atualizar_tree_presenca(self, presenca):
        for item in self.tree_presenca.get_children():
            self.tree_presenca.delete(item)
        
        for p in presenca:
            dia = p.dia_trabalho.strftime("%d/%m/%Y") if p.dia_trabalho else "-"
            self.tree_presenca.insert('', tk.END, values=(
                p.dia_formatado or dia,
                p.nome,
                p.hora_entrada,
                p.hora_saida,
                f"R$ {p.valor_10_percent:,.2f}",
                p.observacao or "-"
            ))

    def atualizar_tree_pagamentos(self, pagamentos):
        for item in self.tree_pagamentos.get_children():
            self.tree_pagamentos.delete(item)
        
        for p in pagamentos:
            dia = p.dia_trabalho.strftime("%d/%m/%Y") if p.dia_trabalho else "-"
            status = "✅ Pago" if p.pago else "⏳ Pendente"
            self.tree_pagamentos.insert('', tk.END, values=(
                p.nome,
                dia,
                f"R$ {p.valor_10_percent:,.2f}",
                f"R$ {p.vale:,.2f}" if p.vale else "-",
                p.tipo_pagamento,
                status
            ))

    def atualizar_tree_cadastramento(self, cadastramento):
        for item in self.tree_cadastramento.get_children():
            self.tree_cadastramento.delete(item)
        
        for c in cadastramento:
            primeiro = c.primeiro_dia_trabalho.strftime("%d/%m/%Y") if c.primeiro_dia_trabalho else "-"
            ultimo = c.ultimo_dia_trabalho.strftime("%d/%m/%Y") if c.ultimo_dia_trabalho else "-"
            self.tree_cadastramento.insert('', tk.END, values=(
                c.nome,
                primeiro,
                ultimo,
                c.total_dias_trabalhados,
                f"R$ {c.total_recebido:,.2f}"
            ))

    def buscar_presenca(self):
        nome = self.entry_busca_presenca.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Digite um nome para buscar")
            return
        
        try:
            todos = self.repository.listar_historico_presenca(limite=500)
            filtrado = [p for p in todos if nome.lower() in p.nome.lower()]
            self.atualizar_tree_presenca(filtrado)
            messagebox.showinfo("Sucesso", f"Encontrados {len(filtrado)} registros")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def limpar_busca_presenca(self):
        self.entry_busca_presenca.delete(0, tk.END)
        self.atualizar_historico()

    def buscar_pagamentos(self):
        nome = self.entry_busca_pagamento.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Digite um nome para buscar")
            return
        
        try:
            resultados = self.repository.buscar_historico_funcionario(nome)
            self.atualizar_tree_pagamentos(resultados)
            messagebox.showinfo("Sucesso", f"Encontrados {len(resultados)} registros")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def create_tab_codigo(self):
        frame = self.tab_frames['codigo']
        
        title_frame = tk.Frame(frame, bg='#27293d')
        title_frame.pack(fill=tk.X, padx=30, pady=(30, 20))
        
        self._create_label(title_frame, "💻 Download do Código Fonte", 
                         font=('Segoe UI', 20, 'bold'), fg='#00d4ff').pack(side=tk.LEFT)
        
        intro_card = tk.Frame(frame, bg='#323244', padx=30, pady=20)
        intro_card.pack(fill=tk.X, padx=30, pady=10)
        
        intro_text = """📦 Esta seção permite fazer o download de todo o código fonte da aplicação.

O arquivo compactado (.zip) conterá:
• Todos os arquivos Python do projeto
• Arquivos de configuração
• Scripts SQL para banco de dados
• Arquivos de documentação (README.md)
• Estrutura completa de diretórios

Clique no botão abaixo para gerar e baixar o código fonte.
"""
        self._create_label(intro_card, intro_text, 
                         font=('Segoe UI', 11), fg='#a0a0a0', bg='#323244').pack(anchor=tk.W, pady=(0, 20))
        
        btn_gerar = self._create_button(intro_card, "📥 Gerar e Baixar Código Fonte", 
                                       self.baixar_codigo_fonte, bg='#27ae60', fg='#ffffff', 
                                       font=('Segoe UI', 12, 'bold'), padx=30, pady=15)
        btn_gerar.pack(pady=10)
        
        info_card = tk.Frame(frame, bg='#323244', padx=30, pady=20)
        info_card.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        self._create_label(info_card, "📁 Estrutura do Projeto", 
                         font=('Segoe UI', 14, 'bold'), fg='#00d4ff', bg='#323244').pack(anchor=tk.W, pady=(0, 15))
        
        estrutura = [
            ("📂 automacao/", "Pasta principal do projeto"),
            ("├── 📂 config/", "Arquivos de configuração"),
            ("│   └── settings.py", "Configurações do sistema"),
            ("├── 📂 data/", "Camada de dados"),
            ("│   ├── models/", "Modelos de dados"),
            ("│   └── repositories/", "Repositórios"),
            ("├── 📂 services/", "Serviços de negócio"),
            ("│   ├── email_service.py", "Serviço de e-mail"),
            ("│   └── report_generator.py", "Gerador de relatórios"),
            ("├── 📂 sql/", "Scripts SQL"),
            ("├── 📂 ui/", "Interfaces de usuário"),
            ("│   ├── desktop/", "Aplicação Desktop (Tkinter)"),
            ("│   └── web/", "Aplicação Web (Streamlit)"),
            ("└── README.md", "Documentação do projeto"),
        ]
        
        for item, desc in estrutura:
            row = tk.Frame(info_card, bg='#323244')
            row.pack(fill=tk.X, pady=3)
            self._create_label(row, item, font=('Consolas', 10), fg='#00d4ff', bg='#323244').pack(side=tk.LEFT, padx=(20, 10))
            self._create_label(row, desc, font=('Segoe UI', 10), fg='#a0a0a0', bg='#323244').pack(side=tk.LEFT)
        
        tech_card = tk.Frame(frame, bg='#323244', padx=30, pady=20)
        tech_card.pack(fill=tk.X, padx=30, pady=10)
        
        self._create_label(tech_card, "🛠️ Tecnologias Utilizadas", 
                         font=('Segoe UI', 14, 'bold'), fg='#00d4ff', bg='#323244').pack(anchor=tk.W, pady=(0, 15))
        
        tecnologias = [
            "🐍 Python - Linguagem de programação",
            "🎨 Tkinter - Interface Desktop",
            "🌐 Streamlit - Interface Web",
            "🗄️ Supabase - Banco de dados",
            "📧 SMTP - Envio de e-mails",
            "📊 Pandas/OpenPyXL - Relatórios Excel",
            "📄 Python-Docx - Relatórios Word",
        ]
        
        for tech in tecnologias:
            self._create_label(tech_card, f"  {tech}", font=('Segoe UI', 11), fg='#ffffff', bg='#323244').pack(anchor=tk.W, pady=3)
        
        self.lbl_status_download = self._create_label(frame, "", font=('Segoe UI', 11), fg='#27ae60', bg='#27293d')
        self.lbl_status_download.pack(pady=10)

    def baixar_codigo_fonte(self):
        import zipfile
        import io
        import os
        from datetime import datetime
        
        try:
            self.lbl_status_download.config(text="🔄 Gerando código fonte...", fg='#f39c12')
            self.root.update()
            
            projeto_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
            default_filename = f"sistema_salarios_garcons_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".zip",
                filetypes=[("Arquivos ZIP", "*.zip")],
                initialfile=default_filename,
                title="Salvar Código Fonte"
            )
            
            if not file_path:
                self.lbl_status_download.config(text="⚠️ Download cancelado pelo usuário", fg='#f39c12')
                return
            
            with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(projeto_dir):
                    dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.venv', 'venv', 'node_modules', '.idea']]
                    
                    for file in files:
                        if file.endswith(('.py', '.md', '.txt', '.json', '.sql', '.yml', '.yaml', '.toml', '.cfg', '.ini')):
                            file_path_arc = os.path.join(root, file)
                            arcname = os.path.relpath(file_path_arc, projeto_dir)
                            zipf.write(file_path_arc, arcname)
            
            tamanho = os.path.getsize(file_path)
            tamanho_str = f"{tamanho / 1024:.1f} KB" if tamanho > 1024 else f"{tamanho} bytes"
            
            self.lbl_status_download.config(text=f"✅ Download concluído! Arquivo: {os.path.basename(file_path)} ({tamanho_str})", fg='#27ae60')
            messagebox.showinfo("Sucesso", f"Código fonte baixado com sucesso!\n\nArquivo: {os.path.basename(file_path)}\nTamanho: {tamanho_str}")
            
        except Exception as e:
            self.lbl_status_download.config(text=f"❌ Erro ao gerar código: {str(e)}", fg='#e74c3c')
            messagebox.showerror("Erro", f"Erro ao gerar código fonte:\n{str(e)}")

    def create_tab_docs(self):
        frame = self.tab_frames['docs']
        
        title_frame = tk.Frame(frame, bg='#27293d')
        title_frame.pack(fill=tk.X, padx=30, pady=(30, 20))
        
        self._create_label(title_frame, "📚 Documentação do Projeto", 
                         font=('Segoe UI', 20, 'bold'), fg='#00d4ff').pack(side=tk.LEFT)
        
        docs_card = tk.Frame(frame, bg='#323244', padx=20, pady=15)
        docs_card.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        intro_text = """📖 Esta seção exibe a documentação do projeto.

O arquivo README.md contém todas as informações sobre:
• Visão geral do sistema
• Arquitetura do projeto
• Instalação e configuração
• Como usar a aplicação
• Estrutura do banco de dados
• Solução de problemas

Clique nos botões abaixo para visualizar a documentação.
"""
        
        self._create_label(docs_card, intro_text, 
                         font=('Segoe UI', 11), fg='#a0a0a0', bg='#323244').pack(anchor=tk.W, pady=(0, 20))
        
        btn_frame = tk.Frame(docs_card, bg='#323244')
        btn_frame.pack(fill=tk.X, pady=10)
        
        self._create_button(btn_frame, "🌐 Visualizar Documentação (Navegador)", self.visualizar_docs_navegador, 
                           bg='#3498db', fg='#ffffff', padx=25).pack(side=tk.LEFT, padx=10, pady=10)
        
        self._create_button(btn_frame, "📄 Abrir Arquivo Markdown", self.abrir_readme, 
                           bg='#27ae60', fg='#ffffff', padx=25).pack(side=tk.LEFT, padx=10, pady=10)
        
        self._create_button(btn_frame, "📁 Abrir Pasta do Projeto", self.abrir_pasta, 
                           bg='#9b59b6', fg='#ffffff', padx=25).pack(side=tk.LEFT, padx=10, pady=10)
        
        info_card = tk.Frame(docs_card, bg='#2c2c3e', padx=20, pady=15)
        info_card.pack(fill=tk.X, pady=20)
        
        self._create_label(info_card, "📁 Localização dos Arquivos", 
                         font=('Segoe UI', 12, 'bold'), fg='#00d4ff', bg='#2c2c3e').pack(anchor=tk.W, pady=(0, 10))
        
        self._create_label(info_card, "• README.md - Documentação principal", 
                         font=('Segoe UI', 10), fg='#a0a0a0', bg='#2c2c3e').pack(anchor=tk.W)
        self._create_label(info_card, "• ui/desktop/app_tkinter.py - Aplicação Desktop", 
                         font=('Segoe UI', 10), fg='#a0a0a0', bg='#2c2c3e').pack(anchor=tk.W)
        self._create_label(info_card, "• ui/web/app_streamlit.py - Aplicação Web", 
                         font=('Segoe UI', 10), fg='#a0a0a0', bg='#2c2c3e').pack(anchor=tk.W)
        self._create_label(info_card, "• services/ - Serviços de negócio", 
                         font=('Segoe UI', 10), fg='#a0a0a0', bg='#2c2c3e').pack(anchor=tk.W)
        self._create_label(info_card, "• data/ - Modelos e repositórios", 
                         font=('Segoe UI', 10), fg='#a0a0a0', bg='#2c2c3e').pack(anchor=tk.W)

    def visualizar_docs_navegador(self):
        import webbrowser
        import os
        import tempfile
        
        try:
            with open('README.md', 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            html_content = self._converter_markdown_html(md_content)
            
            temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8')
            temp_file.write(html_content)
            temp_file.close()
            
            webbrowser.open(f'file://{temp_file.name}')
            
            messagebox.showinfo("Sucesso", "Documentação aberta no navegador!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir documentação: {str(e)}")
    
    def _converter_markdown_html(self, md_content):
        import re
        
        html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Documentação do Projeto</title>
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            background: #1e1e2f;
            color: #ffffff;
            line-height: 1.6;
        }
        h1 { color: #00d4ff; border-bottom: 2px solid #00d4ff; padding-bottom: 10px; }
        h2 { color: #00d4ff; margin-top: 30px; }
        h3 { color: #9b59b6; }
        code { background: #323244; padding: 2px 6px; border-radius: 4px; font-family: Consolas, monospace; }
        pre { background: #323244; padding: 15px; border-radius: 8px; overflow-x: auto; }
        pre code { background: none; padding: 0; }
        a { color: #3498db; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        th, td { border: 1px solid #4a4a5a; padding: 12px; text-align: left; }
        th { background: #323244; color: #00d4ff; }
        blockquote { border-left: 4px solid #00d4ff; margin: 20px 0; padding: 10px 20px; background: #27293d; }
        ul, ol { padding-left: 25px; }
        li { margin: 5px 0; }
        hr { border: none; border-top: 1px solid #4a4a5a; margin: 30px 0; }
    </style>
</head>
<body>
"""
        
        lines = md_content.split('\n')
        in_code_block = False
        in_list = False
        
        for line in lines:
            if line.startswith('```'):
                if in_code_block:
                    html += '</code></pre>\n'
                    in_code_block = False
                else:
                    html += f'<pre><code>'
                    in_code_block = True
                continue
            
            if in_code_block:
                html += line + '\n'
                continue
            
            line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            
            if line.startswith('# '):
                html += f'<h1>{line[2:]}</h1>\n'
            elif line.startswith('## '):
                html += f'<h2>{line[3:]}</h2>\n'
            elif line.startswith('### '):
                html += f'<h3>{line[4:]}</h3>\n'
            elif line.startswith('- '):
                if not in_list:
                    html += '<ul>\n'
                    in_list = True
                html += f'<li>{line[2:]}</li>\n'
            elif line.startswith('|'):
                if '|' in line and '-' not in line:
                    cols = [c.strip() for c in line.split('|') if c.strip()]
                    html += '<tr>' + ''.join(f'<td>{c}</td>' for c in cols) + '</tr>\n'
            else:
                if in_list:
                    html += '</ul>\n'
                    in_list = False
                
                line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
                line = re.sub(r'\*(.+?)\*', r'<em>\1</em>', line)
                line = re.sub(r'`(.+?)`', r'<code>\1</code>', line)
                line = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', line)
                
                if line.strip():
                    html += f'<p>{line}</p>\n'
        
        if in_list:
            html += '</ul>\n'
        
        html += """</body></html>"""
        
        return html

    def abrir_pasta(self):
        import os
        import webbrowser
        
        pasta_atual = os.path.dirname(os.path.abspath('README.md'))
        webbrowser.open(f'file://{pasta_atual}')

    def visualizar_tabela(self, table_name):
        janela = tk.Toplevel(self.root)
        janela.title(f"Visualizar: {table_name}")
        janela.geometry("1000x600")
        janela.configure(bg="#1e1e2f")
        
        tk.Label(janela, text=f"📊 Tabela: {table_name}", font=('Segoe UI', 14, 'bold'), 
                fg='#00d4ff', bg="#1e1e2f").pack(pady=10)
        
        frame_tabela = tk.Frame(janela, bg="#323244")
        frame_tabela.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        colunas = self.get_colunas_tabela(table_name)
        
        tree = ttk.Treeview(frame_tabela, columns=colunas, show='headings')
        
        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        scrollbar_y = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL, command=tree.yview)
        scrollbar_x = ttk.Scrollbar(frame_tabela, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        tree.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, sticky='ew')
        
        frame_tabela.grid_rowconfigure(0, weight=1)
        frame_tabela.grid_columnconfigure(0, weight=1)
        
        try:
            dados = self.repository.client.table(table_name).select("*").execute()
            
            for registro in dados.data:
                valores = []
                for col in colunas:
                    val = registro.get(col, '')
                    if isinstance(val, dict):
                        val = str(val)
                    elif val is None:
                        val = ''
                    valores.append(val)
                tree.insert('', tk.END, values=valores)
            
            tk.Label(janela, text=f"Total de registros: {len(dados.data)}", 
                    fg='#27ae60', bg="#1e1e2f").pack(pady=5)
            
        except Exception as e:
            tk.Label(janela, text=f"Erro ao carregar dados: {str(e)}", 
                    fg='#e74c3c', bg="#1e1e2f").pack(pady=10)
        
        btn_frame = tk.Frame(janela, bg="#1e1e2f")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="🔄 Atualizar", command=lambda: self.atualizar_tree_view(tree, table_name, colunas),
                 bg='#3498db', fg='#ffffff', padx=20).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="❌ Fechar", command=janela.destroy,
                 bg='#e74c3c', fg='#ffffff', padx=20).pack(side=tk.LEFT, padx=5)

    def atualizar_tree_view(self, tree, table_name, colunas):
        for item in tree.get_children():
            tree.delete(item)
        
        try:
            dados = self.repository.client.table(table_name).select("*").execute()
            
            for registro in dados.data:
                valores = []
                for col in colunas:
                    val = registro.get(col, '')
                    if isinstance(val, dict):
                        val = str(val)
                    elif val is None:
                        val = ''
                    valores.append(val)
                tree.insert('', tk.END, values=valores)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def get_colunas_tabela(self, table_name):
        colunas = {
            'funcionarios': ['id', 'nome', 'valor_10_percent', 'hora_entrada', 'hora_saida', 
                           'dia_trabalho', 'observacao', 'vale', 'tipo_vale', 'pago', 'tipo_pagamento', 'created_at'],
            'configuracoes': ['id', 'email_destinatario', 'email_remetente', 'senha_app', 'smtp_host', 'smtp_port', 'created_at'],
            'observacoes_gerais': ['id', 'dia_trabalho', 'observacao', 'created_at'],
            'registros_trabalho': ['id', 'dia_trabalho', 'dia_semana', 'total_funcionarios', 'total_valores', 'email_enviado', 'data_envio'],
            'logs': ['id', 'acao', 'tabela', 'registro_id', 'dados_anteriores', 'dados_novos', 'usuario', 'created_at']
        }
        return colunas.get(table_name, ['id', 'created_at'])

    def inserir_registro(self, table_name):
        janela = tk.Toplevel(self.root)
        janela.title(f"Inserir: {table_name}")
        janela.geometry("600x500")
        janela.configure(bg="#1e1e2f")
        
        tk.Label(janela, text=f"➕ Inserir Registro - {table_name}", 
                font=('Segoe UI', 14, 'bold'), fg='#00d4ff', bg="#1e1e2f").pack(pady=10)
        
        frame_campos = tk.Frame(janela, bg="#323244", padx=20, pady=20)
        frame_campos.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        campos = self.get_colunas_tabela(table_name)
        entries = {}
        
        for i, campo in enumerate(campos):
            if campo in ['id', 'created_at']:
                continue
            
            tk.Label(frame_campos, text=f"{campo}:", fg='#ffffff', bg="#323244").grid(
                row=i, column=0, sticky=tk.W, pady=5, padx=5)
            
            entry = tk.Entry(frame_campos, width=40, bg='#27293d', fg='#ffffff')
            entry.grid(row=i, column=1, pady=5, padx=5)
            entries[campo] = entry
        
        def salvar():
            dados = {}
            for campo, entry in entries.items():
                valor = entry.get().strip()
                if valor:
                    if campo in ['valor_10_percent', 'vale', 'smtp_port']:
                        try:
                            dados[campo] = float(valor)
                        except:
                            dados[campo] = valor
                    else:
                        dados[campo] = valor
            
            try:
                self.repository.client.table(table_name).insert(dados).execute()
                messagebox.showinfo("Sucesso", "Registro inserido com sucesso!")
                janela.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao inserir: {str(e)}")
        
        btn_frame = tk.Frame(janela, bg="#1e1e2f")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="💾 Salvar", command=salvar,
                 bg='#27ae60', fg='#ffffff', padx=20).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="❌ Cancelar", command=janela.destroy,
                 bg='#e74c3c', fg='#ffffff', padx=20).pack(side=tk.LEFT, padx=5)

    def atualizar_registro(self, table_name):
        janela = tk.Toplevel(self.root)
        janela.title(f"Atualizar: {table_name}")
        janela.geometry("800x600")
        janela.configure(bg="#1e1e2f")
        
        tk.Label(janela, text=f"🔄 Atualizar Registro - {table_name}", 
                font=('Segoe UI', 14, 'bold'), fg='#00d4ff', bg="#1e1e2f").pack(pady=10)
        
        frame_busca = tk.Frame(janela, bg="#323244", padx=20, pady=10)
        frame_busca.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(frame_busca, text="ID do Registro:", fg='#ffffff', bg="#323244").pack(side=tk.LEFT)
        
        entry_id = tk.Entry(frame_busca, width=40, bg='#27293d', fg='#ffffff')
        entry_id.pack(side=tk.LEFT, padx=10)
        
        frame_campos = tk.Frame(janela, bg="#323244", padx=20, pady=20)
        frame_campos.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        campos = self.get_colunas_tabela(table_name)
        entries = {}
        
        for i, campo in enumerate(campos):
            if campo in ['id', 'created_at']:
                continue
            
            tk.Label(frame_campos, text=f"{campo}:", fg='#ffffff', bg="#323244").grid(
                row=i, column=0, sticky=tk.W, pady=5, padx=5)
            
            entry = tk.Entry(frame_campos, width=40, bg='#27293d', fg='#ffffff')
            entry.grid(row=i, column=1, pady=5, padx=5)
            entries[campo] = entry
        
        def buscar():
            record_id = entry_id.get().strip()
            if not record_id:
                messagebox.showwarning("Aviso", "Digite o ID do registro")
                return
            
            try:
                dados = self.repository.client.table(table_name).select("*").eq("id", record_id).execute()
                
                if dados.data:
                    registro = dados.data[0]
                    for campo, entry in entries.items():
                        val = registro.get(campo, '')
                        if val is not None:
                            entry.insert(0, str(val))
                else:
                    messagebox.showwarning("Aviso", "Registro não encontrado")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao buscar: {str(e)}")
        
        def salvar():
            record_id = entry_id.get().strip()
            if not record_id:
                messagebox.showwarning("Aviso", "Digite o ID do registro")
                return
            
            dados = {}
            for campo, entry in entries.items():
                valor = entry.get().strip()
                if valor:
                    if campo in ['valor_10_percent', 'vale', 'smtp_port']:
                        try:
                            dados[campo] = float(valor)
                        except:
                            dados[campo] = valor
                    else:
                        dados[campo] = valor
            
            if not dados:
                messagebox.showwarning("Aviso", "Nenhum dado para atualizar")
                return
            
            try:
                self.repository.client.table(table_name).update(dados).eq("id", record_id).execute()
                messagebox.showinfo("Sucesso", "Registro atualizado com sucesso!")
                janela.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar: {str(e)}")
        
        btn_frame = tk.Frame(janela, bg="#1e1e2f")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="🔍 Buscar", command=buscar,
                 bg='#3498db', fg='#ffffff', padx=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="💾 Salvar", command=salvar,
                 bg='#27ae60', fg='#ffffff', padx=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="❌ Cancelar", command=janela.destroy,
                 bg='#e74c3c', fg='#ffffff', padx=15).pack(side=tk.LEFT, padx=5)

    def deletar_registro(self, table_name):
        janela = tk.Toplevel(self.root)
        janela.title(f"Deletar: {table_name}")
        janela.geometry("500x300")
        janela.configure(bg="#1e1e2f")
        
        tk.Label(janela, text=f"🗑️ Deletar Registro - {table_name}", 
                font=('Segoe UI', 14, 'bold'), fg='#e74c3c', bg="#1e1e2f").pack(pady=20)
        
        frame = tk.Frame(janela, bg="#323244", padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(frame, text="⚠️ Esta ação não pode ser desfeita!", 
                fg='#f39c12', bg="#323244", font=('Segoe UI', 11)).pack(pady=10)
        
        tk.Label(frame, text="ID do Registro:", fg='#ffffff', bg="#323244").pack(pady=5)
        
        entry_id = tk.Entry(frame, width=40, bg='#27293d', fg='#ffffff')
        entry_id.pack(pady=10)
        
        def deletar():
            record_id = entry_id.get().strip()
            if not record_id:
                messagebox.showwarning("Aviso", "Digite o ID do registro")
                return
            
            if not messagebox.askyesno("Confirmar", f"Tem certeza que deseja deletar o registro {record_id}?"):
                return
            
            try:
                self.repository.client.table(table_name).delete().eq("id", record_id).execute()
                messagebox.showinfo("Sucesso", "Registro deletado com sucesso!")
                janela.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao deletar: {str(e)}")
        
        btn_frame = tk.Frame(janela, bg="#1e1e2f")
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="🗑️ Deletar", command=deletar,
                 bg='#e74c3c', fg='#ffffff', padx=20).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="❌ Cancelar", command=janela.destroy,
                 bg='#95a5a6', fg='#ffffff', padx=20).pack(side=tk.LEFT, padx=10)
        
    def abrir_readme(self):
        import webbrowser
        try:
            webbrowser.open('README.md')
        except:
            messagebox.showerror("Erro", "Não foi possível abrir o arquivo")
            
    def atualizar_docs(self):
        try:
            with open('README.md', 'r', encoding='utf-8') as f:
                doc_content = f.read()
            messagebox.showinfo("Sucesso", "Documentação atualizada!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar: {str(e)}")

    def carregar_dados(self):
        try:
            todos = self.repository.listar_todos_funcionarios()
            nomes = list(set(f.nome for f in todos if f.nome))
            self.combo_funcionarios['values'] = nomes
            self.atualizar_tree_cadastro()
            
            try:
                logs = self.repository.listar_logs(limite=200)
                self.atualizar_tree_logs(logs)
                self.lbl_status_logs.config(text=f"Status: {len(logs)} logs carregados", fg='#27ae60')
            except Exception as log_e:
                print(f"Erro ao carregar logs: {log_e}")
                self.lbl_status_logs.config(text="Status: Erro ao carregar logs", fg='#e74c3c')
        except Exception as e:
            print(f"Erro: {e}")

    def carregar_config(self):
        try:
            config = self.repository.get_configuracao()
            if config:
                self.entry_remetente.insert(0, config.email_remetente or settings.EMAIL_DEFAULT)
                self.entry_dest.insert(0, config.email_destinatario or settings.EMAIL_DEFAULT)
                self.entry_senha.insert(0, config.senha_app or settings.SENHA_APP)
            else:
                self.entry_remetente.insert(0, settings.EMAIL_DEFAULT)
                self.entry_dest.insert(0, settings.EMAIL_DEFAULT)
                self.entry_senha.insert(0, settings.SENHA_APP)
        except:
            pass

    def atualizar_tree_cadastro(self):
        for item in self.tree_cadastro.get_children():
            self.tree_cadastro.delete(item)
        for func in self.repository.listar_todos_funcionarios():
            self.tree_cadastro.insert('', tk.END, values=(
                func.nome,
                func.dia_trabalho.strftime('%d/%m/%Y') if func.dia_trabalho else '-',
                'Ativo' if func.nome else '-'
            ))

    def carregar_dia(self):
        try:
            dia = datetime.strptime(self.entry_dia.get(), "%Y-%m-%d").date()
            self.funcionarios = []
            print(f"DEBUG: Carregando registros para a data: {dia}")
            
            todos_funcs = self.repository.listar_todos_funcionarios()
            print(f"DEBUG: Total de funcionários no banco: {len(todos_funcs)}")
            
            self.funcionarios = self.repository.listar_funcionarios(dia)
            print(f"DEBUG: Registros encontrados para {dia}: {len(self.funcionarios)}")
            for f in self.funcionarios:
                print(f"  - {f.nome}: {f.valor_10_percent}, dia: {f.dia_trabalho}")
            
            self.atualizar_tree_registrar()
            messagebox.showinfo("Sucesso", f"Carregados {len(self.funcionarios)} registros")
        except Exception as e:
            print(f"DEBUG ERRO carregar_dia: {e}")
            messagebox.showerror("Erro", str(e))

    def limpar_campos_registro(self):
        self.combo_funcionarios.set('')
        self.entry_10.delete(0, tk.END)
        self.entry_10.insert(0, "0.00")
        self.entry_entrada.delete(0, tk.END)
        self.entry_entrada.insert(0, "08:00")
        self.entry_saida.delete(0, tk.END)
        self.entry_saida.insert(0, "16:00")
        self.entry_vale.delete(0, tk.END)
        self.combo_tipo.set('')
        self.combo_pagamento.set('pix')
        self.pago_var.set(False)
        self.entry_obs.delete(0, tk.END)
        messagebox.showinfo("Sucesso", "Campos limpos!")

    def deletar_registro_selecionado(self):
        sel = self.tree_registrar.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um registro para deletar")
            return
        
        valores = self.tree_registrar.item(sel[0])['values']
        nome = valores[0]
        
        if messagebox.askyesno("Confirmar", f"Deseja deletar o registro de {nome}?"):
            try:
                for f in self.funcionarios:
                    if f.nome == nome:
                        self.repository.deletar_funcionario(str(f.id))
                        break
                self.carregar_dia()
                messagebox.showinfo("Sucesso", "Registro deletado!")
            except Exception as e:
                messagebox.showerror("Erro", str(e))

    def mostrar_dados_salvos(self):
        if not self.funcionarios:
            messagebox.showwarning("Aviso", "Carregue os dados primeiro usando 'Carregar Registros do Dia'")
            return
        
        if not self.funcionarios:
            messagebox.showinfo("Info", "Nenhum dado salvo para este dia")
            return
        
        func = self.funcionarios[0]
        
        self.combo_funcionarios.set(func.nome)
        self.entry_10.delete(0, tk.END)
        self.entry_10.insert(0, f"{func.valor_10_percent:.2f}")
        self.entry_entrada.delete(0, tk.END)
        self.entry_entrada.insert(0, func.hora_entrada)
        self.entry_saida.delete(0, tk.END)
        self.entry_saida.insert(0, func.hora_saida)
        self.entry_vale.delete(0, tk.END)
        if func.vale:
            self.entry_vale.insert(0, f"{func.vale:.2f}")
        self.combo_tipo.set(func.tipo_vale or "pix")
        self.pago_var.set(func.pago)
        self.entry_obs.delete(0, tk.END)
        self.entry_obs.insert(0, func.observacao or "")
        
        messagebox.showinfo("Sucesso", f"Dados de {func.nome} carregados nos campos!")

    def atualizar_tree_registrar(self):
        for item in self.tree_registrar.get_children():
            self.tree_registrar.delete(item)
        for f in self.funcionarios:
            self.tree_registrar.insert('', tk.END, values=(
                f.nome, f"{f.valor_10_percent:.2f}", f.hora_entrada, f.hora_saida,
                f"{f.vale:.2f}" if f.vale else "-", f.tipo_vale or "pix",
                "✅" if f.pago else "❌", f.observacao or "-"
            ))

    def adicionar_registro(self):
        nome = self.combo_funcionarios.get()
        if not nome:
            messagebox.showwarning("Aviso", "Selecione um funcionário")
            return
        try:
            dia = datetime.strptime(self.entry_dia.get(), "%Y-%m-%d").date()
            print(f"DEBUG: Adicionando registro para {nome}, data: {dia}")
            
            hora_entrada = self.entry_entrada.get().strip() or "08:00"
            hora_saida = self.entry_saida.get().strip() or "16:00"
            
            if ":" not in hora_entrada:
                hora_entrada = hora_entrada + ":00"
            if ":" not in hora_saida:
                hora_saida = hora_saida + ":00"
            
            valor_10 = 0.0
            try:
                valor_10 = float(self.entry_10.get().replace(',', '.')) if self.entry_10.get() else 0.0
            except ValueError:
                messagebox.showerror("Erro", "Valor de 10% deve ser um número")
                return
            
            vale = None
            if self.entry_vale.get().strip():
                try:
                    vale = float(self.entry_vale.get().replace(',', '.'))
                except ValueError:
                    pass
            
            print(f"DEBUG: Verificando se {nome} já existe no banco para {dia}")
            
            existente = self.repository.buscar_funcionario_por_nome_e_data(nome, dia)
            
            if existente:
                print(f"DEBUG: Encontrou registro existente no banco: ID={existente.id}")
            
            tipo_vale = self.combo_tipo.get() if self.combo_tipo.get() else None
            tipo_pagamento = self.combo_pagamento.get() if self.combo_pagamento.get() else "pix"
            
            func = Funcionario(
                nome=nome,
                dia_trabalho=dia,
                valor_10_percent=valor_10,
                hora_entrada=hora_entrada,
                hora_saida=hora_saida,
                vale=vale,
                tipo_vale=tipo_vale,
                pago=self.pago_var.get(),
                tipo_pagamento=tipo_pagamento,
                observacao=self.entry_obs.get().strip()
            )
            
            if existente:
                func.id = existente.id
                self.repository.atualizar_funcionario(func)
                msg = f"Registro de {nome} atualizado com sucesso!"
            else:
                self.repository.cadastrar_funcionario(func)
                msg = f"Registro de {nome} adicionado com sucesso!"
            
            print(f"DEBUG: Registro salvo com sucesso")
            
            self.combo_funcionarios.set('')
            self.entry_10.delete(0, tk.END)
            self.entry_10.insert(0, "0.00")
            self.entry_entrada.delete(0, tk.END)
            self.entry_entrada.insert(0, "08:00")
            self.entry_saida.delete(0, tk.END)
            self.entry_saida.insert(0, "16:00")
            self.entry_vale.delete(0, tk.END)
            self.combo_tipo.set('pix')
            self.pago_var.set(False)
            self.entry_obs.delete(0, tk.END)
            
            self.carregar_dia()
            messagebox.showinfo("Sucesso", msg)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

    def salvar_registros(self):
        self.carregar_dia()
        messagebox.showinfo("Sucesso", "Dados salvos!")

    def carregar_dia_envio(self):
        try:
            dia = datetime.strptime(self.entry_dia_envio.get(), "%Y-%m-%d").date()
            self.funcionarios = self.repository.listar_funcionarios(dia)
            self.atualizar_tree_envio()
            
            obs = self.repository.get_observacao_geral(dia)
            self.txt_obs.delete('1.0', tk.END)
            if obs:
                self.txt_obs.insert('1.0', obs.observacao or "")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def limpar_dados_envio(self):
        self.funcionarios = []
        for item in self.tree_envio.get_children():
            self.tree_envio.delete(item)
        self.txt_obs.delete('1.0', tk.END)
        self.lbl_total.config(text="Total: 0 funcionários | Total 10%: R$ 0.00")
        messagebox.showinfo("Sucesso", "Dados limpos!")

    def atualizar_tree_envio(self):
        for item in self.tree_envio.get_children():
            self.tree_envio.delete(item)
        
        total = 0
        for f in self.funcionarios:
            self.tree_envio.insert('', tk.END, values=(
                f.nome, f"{f.valor_10_percent:.2f}", f.hora_entrada, f.hora_saida,
                f"{f.vale:.2f}" if f.vale else "-", f.tipo_vale or "pix",
                "✅" if f.pago else "❌", f.observacao or "-"
            ))
            total += f.valor_10_percent
        
        self.lbl_total.config(text=f"Total: {len(self.funcionarios)} funcionários | Total 10%: R$ {total:.2f}")

    def salvar_obs_geral(self):
        try:
            dia = datetime.strptime(self.entry_dia_envio.get(), "%Y-%m-%d").date()
            obs = ObservacaoGeral(dia_trabalho=dia, observacao=self.txt_obs.get('1.0', tk.END).strip())
            self.repository.salvar_observacao_geral(obs)
            messagebox.showinfo("Sucesso", "Observação salva!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def cadastrar_funcionario(self):
        nome = self.entry_nome.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Digite o nome do funcionário")
            return
        try:
            func = Funcionario(nome=nome, dia_trabalho=date.today())
            self.repository.cadastrar_funcionario(func)
            self.entry_nome.delete(0, tk.END)
            self.carregar_dados()
            messagebox.showinfo("Sucesso", "Funcionário cadastrado!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def deletar_funcionario(self):
        sel = self.tree_cadastro.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um funcionário para deletar")
            return
        nome = self.tree_cadastro.item(sel[0])['values'][0]
        if messagebox.askyesno("Confirmar", f"Deseja deletar {nome}?"):
            for f in self.repository.listar_todos_funcionarios():
                if f.nome == nome:
                    self.repository.deletar_funcionario(str(f.id))
                    break
            self.carregar_dados()
            messagebox.showinfo("Sucesso", "Funcionário deletado!")

    def deletar_todos_funcionarios(self):
        if not messagebox.askyesno("Confirmar", "Deseja deletar TODOS os funcionários? Esta ação não pode ser desfeita!"):
            return
        
        try:
            todos = self.repository.listar_todos_funcionarios()
            for f in todos:
                self.repository.deletar_funcionario(str(f.id))
            self.carregar_dados()
            messagebox.showinfo("Sucesso", "Todos os funcionários foram deletados!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def salvar_config(self):
        try:
            from data.models.funcionario import Configuracao
            config = Configuracao(
                email_remetente=self.entry_remetente.get(),
                email_destinatario=self.entry_dest.get(),
                senha_app=self.entry_senha.get()
            )
            self.repository.salvar_configuracao(config)
            messagebox.showinfo("Sucesso", "Configurações salvas!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def gerar_relatorio(self):
        if not self.funcionarios:
            messagebox.showwarning("Aviso", "Carregue os dados primeiro")
            return
        try:
            dia = datetime.strptime(self.entry_dia_envio.get(), "%Y-%m-%d").date()
            report = ReportGenerator(self.funcionarios, dia)
            ext = {"HTML": "html", "Excel": "xlsx", "DOCX": "docx", "CSV": "csv", "JSON": "json", "XML": "xml"}[self.formato_var.get()]
            filename = filedialog.asksaveasfilename(defaultextension=f".{ext}")
            if filename:
                if self.formato_var.get() == "HTML":
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(report.generate_html())
                elif self.formato_var.get() == "Excel":
                    with open(filename, 'wb') as f:
                        f.write(report.generate_excel())
                elif self.formato_var.get() == "DOCX":
                    with open(filename, 'wb') as f:
                        f.write(report.generate_docx())
                elif self.formato_var.get() == "CSV":
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(report.generate_csv())
                elif self.formato_var.get() == "JSON":
                    with open(filename, 'wb') as f:
                        f.write(report.generate_json())
                elif self.formato_var.get() == "XML":
                    with open(filename, 'wb') as f:
                        f.write(report.generate_xml())
                messagebox.showinfo("Sucesso", "Relatório gerado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def enviar_email(self):
        if not self.funcionarios:
            messagebox.showwarning("Aviso", "Carregue os dados primeiro")
            return
        try:
            dia = datetime.strptime(self.entry_dia_envio.get(), "%Y-%m-%d").date()
            email_svc = EmailService(
                remetente=self.entry_remetente.get() or settings.EMAIL_DEFAULT,
                senha=settings.SENHA_APP
            )
            report = ReportGenerator(self.funcionarios, dia)
            dia_semana = settings.DIAS_SEMANA.get(dia.weekday(), "")
            obs_geral = self.txt_obs.get('1.0', tk.END).strip()
            sucesso = email_svc.enviar_relatorio_com_anexos(
                self.entry_email.get(), self.funcionarios, dia, dia_semana, report, obs_geral
            )
            if sucesso:
                messagebox.showinfo("Sucesso", "E-mail enviado com sucesso!")
            else:
                messagebox.showerror("Erro", "Falha ao enviar e-mail")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao enviar e-mail: {str(e)}")


def main():
    root = tk.Tk()
    
    login_frame = tk.Frame(root, bg="#1e1e2f")
    login_frame.pack(fill=tk.BOTH, expand=True)
    
    center_frame = tk.Frame(login_frame, bg="#1e1e2f")
    center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    title = tk.Label(center_frame, text="Sistema de Salários", 
                     font=('Segoe UI', 28, 'bold'), foreground='#00d4ff', bg="#1e1e2f")
    title.pack(pady=(0, 10))
    
    subtitle = tk.Label(center_frame, text="Faça login para continuar", 
                      font=('Segoe UI', 14), foreground='#a0a0a0', bg="#1e1e2f")
    subtitle.pack(pady=(0, 30))
    
    tk.Label(center_frame, text="E-mail:", font=('Segoe UI', 12), 
            foreground='#ffffff', bg="#1e1e2f").pack(anchor=tk.W)
    entry_email = tk.Entry(center_frame, font=('Segoe UI', 14), width=35,
                           bg='#323244', fg='#ffffff', insertbackground='#ffffff',
                           relief=tk.FLAT)
    entry_email.pack(pady=(0, 15))
    entry_email.focus()
    
    tk.Label(center_frame, text="Senha:", font=('Segoe UI', 12), 
            foreground='#ffffff', bg="#1e1e2f").pack(anchor=tk.W)
    entry_senha = tk.Entry(center_frame, font=('Segoe UI', 14), width=35,
                           bg='#323244', fg='#ffffff', insertbackground='#ffffff',
                           relief=tk.FLAT, show="*")
    entry_senha.pack(pady=(0, 20))
    
    msg_label = tk.Label(center_frame, text="", font=('Segoe UI', 11), 
                        fg='#e74c3c', bg="#1e1e2f")
    msg_label.pack(pady=(0, 10))
    
    from services.auth_service import auth_service
    
    def attempt_login():
        email = entry_email.get().strip()
        password = entry_senha.get()
        
        if not email or not password:
            msg_label.config(text="Preencha todos os campos")
            return
        
        msg_label.config(text="Autenticando...", fg='#00d4ff')
        root.update()
        
        result = auth_service.sign_in(email, password)
        
        if result.get("success"):
            login_frame.destroy()
            app = AppTkinter(root)
            root.state('zoomed')
            root.mainloop()
        else:
            msg_label.config(text=result.get("error", "Erro ao fazer login"), fg='#e74c3c')
            entry_senha.delete(0, tk.END)
    
    btn_login = tk.Button(center_frame, text="Entrar", command=attempt_login,
                         font=('Segoe UI', 14, 'bold'), bg='#00d4ff', fg='#1e1e2f',
                         relief=tk.FLAT, padx=40, pady=12, cursor="hand2")
    btn_login.pack(pady=(10, 0))
    
    root.geometry("600x500")
    root.mainloop()


if __name__ == "__main__":
    main()
