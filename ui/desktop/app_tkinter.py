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
        self.root.geometry("1200x850")
        self.root.configure(bg="#f5f5f5")
        
        self.repository = SupabaseRepository()
        self.funcionarios: List[Funcionario] = []
        
        self.setup_styles()
        self.create_widgets()
        self.carregar_dados()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#f5f5f5')
        style.configure('Card.TFrame', background='#ffffff', relief='flat')
        style.configure('TLabel', background='#f5f5f5', font=('Segoe UI', 10))
        style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'), foreground='#2E7D32')
        style.configure('Title.TLabel', font=('Segoe UI', 20, 'bold'), foreground='#1B5E20')
        style.configure('TButton', font=('Segoe UI', 10, 'bold'), padding=10)
        style.configure('Treeview', font=('Segoe UI', 10), rowheight=30)
        style.configure('Treeview.Heading', font=('Segoe UI', 11, 'bold'))

    def create_widgets(self):
        main_container = ttk.Frame(self.root, style='TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        header_frame = ttk.Frame(main_container, style='Card.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title = ttk.Label(header_frame, text="💼 Sistema de Relatório de Salários dos Garçons", style='Title.TLabel')
        title.pack(pady=20)
        
        content_frame = ttk.Frame(main_container, style='TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.tab_frames = {}
        self.tab_cadastro, self.tab_frames['cadastro'] = self._create_scrollable_tab()
        self.tab_registrar, self.tab_frames['registrar'] = self._create_scrollable_tab()
        self.tab_envio, self.tab_frames['envio'] = self._create_scrollable_tab()
        self.tab_config, self.tab_frames['config'] = self._create_scrollable_tab()
        
        self.notebook.add(self.tab_cadastro, text="👥 Cadastrar")
        self.notebook.add(self.tab_registrar, text="📝 Registrar Dia")
        self.notebook.add(self.tab_envio, text="📧 Enviar E-mail")
        self.notebook.add(self.tab_config, text="⚙️ Configurações")
        
        self.create_tab_cadastro()
        self.create_tab_registrar()
        self.create_tab_envio()
        self.create_tab_config()

    def _create_scrollable_tab(self):
        container = ttk.Frame(self.notebook)
        
        canvas = tk.Canvas(container, bg='#f5f5f5')
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        return container, scrollable_frame

    def create_tab_cadastro(self):
        frame = self.tab_frames['cadastro']
        form_frame = ttk.LabelFrame(frame, text="Novo Funcionário", padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(form_frame, text="Nome:").grid(row=0, column=0, sticky=tk.W, pady=8)
        self.entry_nome = ttk.Entry(form_frame, width=35)
        self.entry_nome.grid(row=0, column=1, sticky=tk.EW, pady=8, padx=5)
        
        btn_cadastrar = ttk.Button(form_frame, text="✅ Cadastrar", command=self.cadastrar_funcionario)
        btn_cadastrar.grid(row=1, column=0, columnspan=2, pady=20, sticky=tk.EW)
        
        table_frame = ttk.LabelFrame(frame, text="Funcionários", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        ttk.Label(form_frame, text="Nome:").grid(row=0, column=0, sticky=tk.W, pady=8)
        self.entry_nome = ttk.Entry(form_frame, width=35)
        self.entry_nome.grid(row=0, column=1, sticky=tk.EW, pady=8, padx=5)
        
        btn_cadastrar = ttk.Button(form_frame, text="✅ Cadastrar", command=self.cadastrar_funcionario)
        btn_cadastrar.grid(row=1, column=0, columnspan=2, pady=20, sticky=tk.EW)
        
        table_frame = ttk.LabelFrame(self.tab_cadastro, text="Funcionários", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        cols = ('Nome',)
        self.tree_cadastro = ttk.Treeview(table_frame, columns=cols, show='headings')
        self.tree_cadastro.heading('Nome', text='Nome')
        self.tree_cadastro.column('Nome', width=250)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree_cadastro.yview)
        self.tree_cadastro.configure(yscrollcommand=scrollbar.set)
        
        self.tree_cadastro.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        btn_deletar = ttk.Button(table_frame, text="🗑️ Deletar", command=self.deletar_funcionario)
        btn_deletar.pack(pady=10)

    def create_tab_registrar(self):
        dia_frame = ttk.LabelFrame(self.tab_frames['registrar'], text="Data do Trabalho", padding=15)
        dia_frame.pack(fill=tk.X, padx=20, pady=20)
        
        ttk.Label(dia_frame, text="Dia:").grid(row=0, column=0, padx=5)
        self.entry_dia = ttk.Entry(dia_frame, width=15)
        self.entry_dia.insert(0, date.today().strftime("%Y-%m-%d"))
        self.entry_dia.grid(row=0, column=1, padx=5)
        
        btn_carregar = ttk.Button(dia_frame, text="📥 Carregar", command=self.carregar_dia)
        btn_carregar.grid(row=0, column=2, padx=5)
        
        func_frame = ttk.LabelFrame(self.tab_frames['registrar'], text="Registrar", padding=15)
        func_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        ttk.Label(func_frame, text="Funcionário:").grid(row=0, column=0, padx=5, pady=5)
        self.combo_funcionarios = ttk.Combobox(func_frame, width=20, state='readonly')
        self.combo_funcionarios.grid(row=0, column=1, padx=5)
        
        ttk.Label(func_frame, text="10% (R$):").grid(row=0, column=2, padx=5)
        self.entry_10 = ttk.Entry(func_frame, width=10)
        self.entry_10.grid(row=0, column=3, padx=5)
        
        ttk.Label(func_frame, text="Entrada:").grid(row=0, column=4, padx=5)
        self.entry_entrada = ttk.Entry(func_frame, width=8)
        self.entry_entrada.grid(row=0, column=5, padx=5)
        
        ttk.Label(func_frame, text="Saída:").grid(row=0, column=6, padx=5)
        self.entry_saida = ttk.Entry(func_frame, width=8)
        self.entry_saida.grid(row=0, column=7, padx=5)
        
        btn_add = ttk.Button(func_frame, text="➕ Adicionar", command=self.adicionar_registro)
        btn_add.grid(row=0, column=8, padx=5)
        
        ttk.Label(func_frame, text="Vale (R$):").grid(row=1, column=0, padx=5, pady=5)
        self.entry_vale = ttk.Entry(func_frame, width=10)
        self.entry_vale.grid(row=1, column=1, padx=5)
        
        ttk.Label(func_frame, text="Tipo:").grid(row=1, column=2, padx=5)
        self.combo_tipo = ttk.Combobox(func_frame, values=['pix', 'dinheiro'], width=8, state='readonly')
        self.combo_tipo.current(0)
        self.combo_tipo.grid(row=1, column=3, padx=5)
        
        self.pago_var = tk.BooleanVar()
        ttk.Checkbutton(func_frame, text="Pago", variable=self.pago_var).grid(row=1, column=4, padx=5)
        
        ttk.Label(func_frame, text="Obs:").grid(row=1, column=5, padx=5)
        self.entry_obs = ttk.Entry(func_frame, width=20)
        self.entry_obs.grid(row=1, column=6, padx=5, columnspan=2)
        
        btn_salvar = ttk.Button(func_frame, text="💾 Salvar", command=self.salvar_registros)
        btn_salvar.grid(row=2, column=0, columnspan=9, pady=10, sticky=tk.EW)
        
        table_frame = ttk.Frame(func_frame)
        table_frame.grid(row=3, column=0, columnspan=9, sticky='nsew')
        func_frame.rowconfigure(3, weight=1)
        
        cols = ('Nome', '10%', 'Entrada', 'Saída', 'Vale', 'Tipo', 'Pago', 'Obs')
        self.tree_registrar = ttk.Treeview(table_frame, columns=cols, show='headings', height=10)
        
        for col in cols:
            self.tree_registrar.heading(col, text=col)
            self.tree_registrar.column(col, width=90)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree_registrar.yview)
        self.tree_registrar.configure(yscrollcommand=scrollbar.set)
        
        self.tree_registrar.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_tab_envio(self):
        dia_frame = ttk.LabelFrame(self.tab_frames['envio'], text="Data", padding=15)
        dia_frame.pack(fill=tk.X, padx=20, pady=20)
        
        ttk.Label(dia_frame, text="Dia:").grid(row=0, column=0, padx=5)
        self.entry_dia_envio = ttk.Entry(dia_frame, width=15)
        self.entry_dia_envio.insert(0, date.today().strftime("%Y-%m-%d"))
        self.entry_dia_envio.grid(row=0, column=1, padx=5)
        
        btn_carregar = ttk.Button(dia_frame, text="📥 Carregar", command=self.carregar_dia_envio)
        btn_carregar.grid(row=0, column=2, padx=5)
        
        obs_frame = ttk.LabelFrame(self.tab_frames['envio'], text="Observação Geral", padding=15)
        obs_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.txt_obs = tk.Text(obs_frame, width=60, height=3)
        self.txt_obs.pack(fill=tk.X)
        
        btn_salvar_obs = ttk.Button(obs_frame, text="💾 Salvar Obs", command=self.salvar_obs_geral)
        btn_salvar_obs.pack(pady=5)
        
        table_frame = ttk.LabelFrame(self.tab_frames['envio'], text="Funcionários", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        cols = ('Nome', '10%', 'Entrada', 'Saída', 'Vale', 'Tipo', 'Pago', 'Obs')
        self.tree_envio = ttk.Treeview(table_frame, columns=cols, show='headings')
        
        for col in cols:
            self.tree_envio.heading(col, text=col)
            self.tree_envio.column(col, width=90)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree_envio.yview)
        self.tree_envio.configure(yscrollcommand=scrollbar.set)
        
        self.tree_envio.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.lbl_total = ttk.Label(table_frame, text="Total: 0", font=('Segoe UI', 11, 'bold'))
        self.lbl_total.pack(pady=10)
        
        email_frame = ttk.LabelFrame(self.tab_frames['envio'], text="Enviar E-mail", padding=15)
        email_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        ttk.Label(email_frame, text="Destinatário:").grid(row=0, column=0)
        self.entry_email = ttk.Entry(email_frame, width=40)
        self.entry_email.grid(row=0, column=1, padx=5)
        self.entry_email.insert(0, settings.EMAIL_DEFAULT)
        
        btn_enviar = ttk.Button(email_frame, text="📧 Enviar", command=self.enviar_email)
        btn_enviar.grid(row=1, column=0, columnspan=2, pady=10, sticky=tk.EW)
        
        gerar_frame = ttk.LabelFrame(self.tab_frames['envio'], text="Gerar", padding=15)
        gerar_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.formato_var = tk.StringVar(value="HTML")
        ttk.Combobox(gerar_frame, textvariable=self.formato_var, values=["HTML", "Excel", "DOCX", "CSV", "JSON", "XML"], state='readonly').grid(row=0, column=0)
        btn_gerar = ttk.Button(gerar_frame, text="📊 Gerar", command=self.gerar_relatorio)
        btn_gerar.grid(row=0, column=1, padx=5)

    def create_tab_config(self):
        frame = ttk.LabelFrame(self.tab_frames['config'], text="E-mail", padding=20)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(frame, text="Remetente:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_remetente = ttk.Entry(frame, width=40)
        self.entry_remetente.grid(row=0, column=1, pady=5)
        
        ttk.Label(frame, text="Destinatário:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_dest = ttk.Entry(frame, width=40)
        self.entry_dest.grid(row=1, column=1, pady=5)
        
        ttk.Label(frame, text="Senha:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_senha = ttk.Entry(frame, width=40, show="*")
        self.entry_senha.grid(row=2, column=1, pady=5)
        
        ttk.Button(frame, text="💾 Salvar", command=self.salvar_config).grid(row=3, column=0, columnspan=2, pady=20, sticky=tk.EW)
        
        ttk.Label(frame, text=f"Data: {date.today().strftime('%d/%m/%Y')}").grid(row=4, column=0, columnspan=2, sticky=tk.W)
        
        self.carregar_config()

    def carregar_dados(self):
        try:
            todos = self.repository.listar_todos_funcionarios()
            nomes = list(set(f.nome for f in todos if f.nome))
            self.combo_funcionarios['values'] = nomes
            self.atualizar_tree_cadastro()
        except Exception as e:
            print(f"Erro: {e}")

    def carregar_config(self):
        try:
            config = self.repository.get_configuracao()
            if config:
                self.entry_remetente.insert(0, config.email_remetente or "")
                self.entry_dest.insert(0, config.email_destinatario or "")
                self.entry_senha.insert(0, config.senha_app or "")
        except:
            pass

    def atualizar_tree_cadastro(self):
        for item in self.tree_cadastro.get_children():
            self.tree_cadastro.delete(item)
        for func in self.repository.listar_todos_funcionarios():
            self.tree_cadastro.insert('', tk.END, values=(func.nome,))

    def carregar_dia(self):
        try:
            dia = datetime.strptime(self.entry_dia.get(), "%Y-%m-%d").date()
            self.funcionarios = self.repository.listar_funcionarios(dia)
            self.atualizar_tree_registrar()
            messagebox.showinfo("Sucesso", f"Carregados {len(self.funcionarios)} registros")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

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
            
            hora_entrada = self.entry_entrada.get() or "08:00"
            hora_saida = self.entry_saida.get() or "16:00"
            
            if ":" not in hora_entrada:
                hora_entrada = hora_entrada + ":00"
            if ":" not in hora_saida:
                hora_saida = hora_saida + ":00"
            
            func = Funcionario(
                nome=nome,
                dia_trabalho=dia,
                valor_10_percent=float(self.entry_10.get() or 0),
                hora_entrada=hora_entrada,
                hora_saida=hora_saida,
                vale=float(self.entry_vale.get()) if self.entry_vale.get() else None,
                tipo_vale=self.combo_tipo.get(),
                pago=self.pago_var.get(),
                observacao=self.entry_obs.get()
            )
            
            existente = None
            for f in self.funcionarios:
                if f.nome == nome:
                    existente = f
                    break
            
            if existente:
                func.id = existente.id
                self.repository.atualizar_funcionario(func)
            else:
                self.repository.cadastrar_funcionario(func)
            
            self.carregar_dia()
            messagebox.showinfo("Sucesso", "Registrado!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

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
        
        self.lbl_total.config(text=f"Total: {len(self.funcionarios)} | R$ {total:.2f}")

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
            messagebox.showwarning("Aviso", "Digite o nome")
            return
        try:
            func = Funcionario(nome=nome, dia_trabalho=date.today())
            self.repository.cadastrar_funcionario(func)
            self.entry_nome.delete(0, tk.END)
            self.carregar_dados()
            messagebox.showinfo("Sucesso", "Cadastrado!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def deletar_funcionario(self):
        sel = self.tree_cadastro.selection()
        if not sel:
            return
        nome = self.tree_cadastro.item(sel[0])['values'][0]
        if messagebox.askyesno("Confirmar", f"Deletar {nome}?"):
            for f in self.repository.listar_todos_funcionarios():
                if f.nome == nome:
                    self.repository.deletar_funcionario(str(f.id))
                    break
            self.carregar_dados()

    def salvar_config(self):
        try:
            from data.models.funcionario import Configuracao
            config = Configuracao(
                email_remetente=self.entry_remetente.get(),
                email_destinatario=self.entry_dest.get(),
                senha_app=self.entry_senha.get()
            )
            self.repository.salvar_configuracao(config)
            messagebox.showinfo("Sucesso", "Salvo!")
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
                messagebox.showinfo("Sucesso", "Gerado!")
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
            sucesso = email_svc.enviar_relatorio_com_anexos(
                self.entry_email.get(), self.funcionarios, dia, dia_semana, report
            )
            if sucesso:
                messagebox.showinfo("Sucesso", "E-mail enviado!")
            else:
                messagebox.showerror("Erro", "Falha ao enviar")
        except Exception as e:
            messagebox.showerror("Erro", str(e))


def main():
    root = tk.Tk()
    app = AppTkinter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
