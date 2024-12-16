"""
Interface gráfica principal do aplicativo
"""
import tkinter as tk
from tkinter import ttk, messagebox

from ..core.sorteio import realizar_sorteio
from ..utils.file_handler import salvar_resultado
from . import styles
from .effects import GradientFrame

class AmigoSecretoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎁 Amigo Secreto")
        self.root.geometry("600x800")
        self.root.configure(bg=styles.COLORS['bg'])
        
        # Configurar estilo para widgets ttk
        self.style = ttk.Style()
        self.style.configure(
            "TScrollbar",
            background=styles.COLORS['bg'],
            troughcolor=styles.COLORS['bg'],
            fieldbackground=styles.COLORS['bg'],
            arrowcolor=styles.COLORS['primary']
        )
        
        self.style.configure(
            "TNotebook",
            background=styles.COLORS['bg'],
            tabmargins=[2, 5, 2, 0]
        )
        
        self.style.configure(
            "TNotebook.Tab",
            background=styles.COLORS['button'],
            foreground='black',
            padding=[10, 5],
            font=styles.FONTS['button']
        )
        
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", styles.COLORS['header_bg'])],
            foreground=[("selected", "black")]  # Mantém o texto preto quando selecionado
        )
        
        self.participantes = []
        self.sorteio = {}
        self.contatos = {}
        
        # Criar notebook para as abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Aba principal
        self.main_tab = tk.Frame(self.notebook, bg=styles.COLORS['bg'])
        self.notebook.add(self.main_tab, text="🎲 Sorteio")
        
        # Aba de contatos
        self.contact_tab = tk.Frame(self.notebook, bg=styles.COLORS['bg'])
        self.notebook.add(self.contact_tab, text="📱 Contatos")
        
        self._setup_main_tab()
        self._setup_contact_tab()
        
    def _setup_main_tab(self):
        # Gradiente do cabeçalho para o fundo
        gradient_height = 150  # Altura do gradiente
        header_gradient = GradientFrame(
            self.main_tab,
            styles.COLORS['header_bg'],
            styles.COLORS['bg'],
            height=gradient_height,
            title="🎄 Amigo Secreto 🎁",
            title_font=styles.FONTS['header'],
            title_color=styles.COLORS['text_light'],
            bg=styles.COLORS['bg'],
            highlightthickness=0
        )
        header_gradient.pack(fill=tk.X, pady=(0, 20))
        
        # Container principal
        main_frame = tk.Frame(self.main_tab, bg=styles.COLORS['bg'])
        main_frame.pack(padx=styles.FRAME_STYLE['padx'], 
                       pady=styles.FRAME_STYLE['pady'], 
                       fill=tk.BOTH, 
                       expand=True)
        
        self._setup_entry(main_frame)
        self._setup_list(main_frame)
        self._setup_buttons(main_frame)
        
    def _setup_contact_tab(self):
        # Header
        header_frame = tk.Frame(self.contact_tab, bg=styles.COLORS['header_bg'])
        header_frame.pack(fill=tk.X)
        
        header_label = tk.Label(
            header_frame,
            text="📱 Gerenciar Contatos",
            font=styles.FONTS['header'],
            bg=styles.COLORS['header_bg'],
            fg='white',
            pady=15
        )
        header_label.pack()
        
        # Frame para seleção de participante
        select_frame = tk.Frame(self.contact_tab, bg=styles.COLORS['bg'])
        select_frame.pack(fill=tk.X, padx=20, pady=20)
        
        select_label = tk.Label(
            select_frame,
            text="Selecione seu nome:",
            font=styles.FONTS['normal'],
            bg=styles.COLORS['bg'],
            fg='black'
        )
        select_label.pack(anchor='w')
        
        # Lista de participantes sem telefone
        self.participants_listbox = tk.Listbox(
            select_frame,
            font=styles.FONTS['normal'],  # Usando a fonte Roboto
            selectmode=tk.SINGLE,
            bg=styles.COLORS['bg'],
            fg='black',
            selectbackground=styles.COLORS['button'],
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=styles.COLORS['border'],
            height=4
        )
        self.participants_listbox.pack(fill=tk.X, pady=(5, 10))
        
        # Bind para seleção de participante
        self.participants_listbox.bind('<<ListboxSelect>>', self._on_participant_select)
        
        # Frame para entrada do telefone
        phone_frame = tk.Frame(self.contact_tab, bg=styles.COLORS['bg'])
        phone_frame.pack(fill=tk.X, padx=20)
        
        phone_label = tk.Label(
            phone_frame,
            text="Seu telefone:",
            font=styles.FONTS['normal'],
            bg=styles.COLORS['bg'],
            fg='black'
        )
        phone_label.pack(anchor='w')
        
        self.contact_phone_entry = tk.Entry(
            phone_frame,
            font=styles.FONTS['normal'],
            width=40
        )
        self.contact_phone_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Botão salvar
        save_contact_btn = tk.Button(
            phone_frame,
            text="💾 Salvar Telefone",
            command=self._salvar_telefone,
            bg=styles.COLORS['button'],
            fg='black',
            font=styles.FONTS['button'],
            **styles.BUTTON_STYLE
        )
        save_contact_btn.pack(pady=10)
        
        # Lista de contatos
        list_frame = tk.Frame(
            self.contact_tab,
            bg=styles.COLORS['bg'],
            highlightbackground=styles.COLORS['border'],
            highlightthickness=1
        )
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(20, 20))
        
        contacts_label = tk.Label(
            list_frame,
            text="📋 Lista de Contatos",
            font=styles.FONTS['title'],
            bg=styles.COLORS['bg'],
            fg='black',
            pady=10
        )
        contacts_label.pack()
        
        # Scrollbar e Listbox para contatos
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.contacts_listbox = tk.Listbox(
            list_frame,
            font=styles.FONTS['normal'],  # Usando a fonte Roboto
            selectmode=tk.SINGLE,
            bg=styles.COLORS['bg'],
            fg='black',
            selectbackground=styles.COLORS['button'],
            relief=tk.FLAT,
            highlightthickness=0,
            activestyle='none'
        )
        self.contacts_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        # Configurar scrollbar
        scrollbar.config(command=self.contacts_listbox.yview)
        self.contacts_listbox.config(yscrollcommand=scrollbar.set)
        
        # Botão remover
        remove_contact_btn = tk.Button(
            self.contact_tab,
            text="🗑 Remover Contato",
            command=self._remover_contato,
            bg=styles.COLORS['secondary'],
            fg='black',
            font=styles.FONTS['button'],
            **styles.BUTTON_STYLE
        )
        remove_contact_btn.pack(pady=(0, 20))
        
    def _setup_entry(self, parent):
        entry_frame = tk.Frame(parent, bg=styles.COLORS['bg'])
        entry_frame.pack(fill=tk.X, pady=(0, 20))
        
        entry_label = tk.Label(
            entry_frame,
            text="Nome do Participante:",
            font=styles.FONTS['title'],
            bg=styles.COLORS['bg'],
            fg='black'
        )
        entry_label.pack(anchor='w', pady=(0, 8))
        
        input_container = tk.Frame(entry_frame, bg=styles.COLORS['bg'])
        input_container.pack(fill=tk.X)
        
        # Entry com borda arredondada
        entry_border = tk.Frame(
            input_container,
            bg=styles.COLORS['border'],
            padx=1,
            pady=1
        )
        entry_border.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        
        self.nome_entry = ttk.Entry(
            entry_border,
            font=styles.FONTS['normal'],
            style='TEntry'
        )
        self.nome_entry.pack(fill=tk.X, padx=2, pady=2)
        
        add_btn = tk.Button(
            input_container,
            text="Adicionar",
            command=self.adicionar_participante,
            bg=styles.COLORS['button'],
            fg='black',
            font=styles.FONTS['button'],
            **styles.BUTTON_STYLE
        )
        add_btn.pack(side=tk.LEFT)
        
        # Hover effect para o botão
        add_btn.bind('<Enter>', lambda e: add_btn.configure(bg=styles.COLORS['button_hover']))
        add_btn.bind('<Leave>', lambda e: add_btn.configure(bg=styles.COLORS['button']))
        
        # Bind Enter key
        self.nome_entry.bind('<Return>', lambda e: self.adicionar_participante())
        
    def _setup_list(self, parent):
        list_frame = tk.Frame(
            parent,
            bg=styles.COLORS['bg'],
            highlightbackground=styles.COLORS['border'],
            highlightthickness=1
        )
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        list_header = tk.Frame(list_frame, bg=styles.COLORS['button'])
        list_header.pack(fill=tk.X)
        
        lista_label = tk.Label(
            list_header,
            text="Lista de Participantes",
            font=styles.FONTS['title'],
            bg=styles.COLORS['button'],
            fg='black',
            pady=8
        )
        lista_label.pack(anchor='w', padx=15)
        
        list_container = tk.Frame(list_frame, bg=styles.COLORS['bg'])
        list_container.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        scrollbar = ttk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(
            list_container,
            font=styles.FONTS['normal'],
            selectmode=tk.SINGLE,
            bg=styles.COLORS['bg'],
            fg='black',
            selectbackground=styles.COLORS['button'],
            relief=tk.FLAT,
            highlightthickness=0,
            activestyle='none'
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)
        
    def _setup_buttons(self, parent):
        btn_frame = tk.Frame(parent, bg=styles.COLORS['bg'])
        btn_frame.pack(fill=tk.X)
        
        remove_btn = tk.Button(
            btn_frame,
            text="🗑 Remover Selecionado",
            command=self.remover_participante,
            bg=styles.COLORS['secondary'],
            fg='black',
            font=styles.FONTS['button'],
            **styles.BUTTON_STYLE
        )
        remove_btn.pack(side=tk.LEFT)
        
        # Hover effect
        remove_btn.bind('<Enter>', lambda e: remove_btn.configure(bg='#ff5252'))
        remove_btn.bind('<Leave>', lambda e: remove_btn.configure(bg=styles.COLORS['secondary']))
        
        sortear_btn = tk.Button(
            btn_frame,
            text="🎲 Realizar Sorteio",
            command=self._realizar_sorteio,
            bg=styles.COLORS['button'],
            fg='black',
            font=styles.FONTS['button'],
            **styles.BUTTON_STYLE
        )
        sortear_btn.pack(side=tk.RIGHT)
        
        # Hover effect
        sortear_btn.bind('<Enter>', lambda e: sortear_btn.configure(bg=styles.COLORS['button_hover']))
        sortear_btn.bind('<Leave>', lambda e: sortear_btn.configure(bg=styles.COLORS['button']))
        
        # Bind Enter key
        self.nome_entry.bind('<Return>', lambda e: self.adicionar_participante())
        
    def adicionar_participante(self):
        nome = self.nome_entry.get().strip()
        if not nome:
            messagebox.showwarning(
                "Aviso",
                "Por favor, digite um nome!"
            )
            return
            
        if nome in self.participantes:
            messagebox.showwarning(
                "Aviso",
                "Este participante já está na lista!"
            )
            return
            
        self.participantes.append(nome)
        self.listbox.insert(tk.END, nome)
        self.nome_entry.delete(0, tk.END)
        
        # Adiciona o nome à lista de contatos se ainda não existir
        if nome not in self.contatos:
            self.contatos[nome] = ""
            self._atualizar_lista_contatos()
            self._atualizar_lista_participantes()  # Atualiza a lista de participantes sem telefone
            
    def remover_participante(self):
        try:
            sel = self.listbox.curselection()[0]
            nome = self.listbox.get(sel)
            self.participantes.remove(nome)
            self.listbox.delete(sel)
            
            # Remove o nome dos contatos também
            if nome in self.contatos:
                del self.contatos[nome]
                self._atualizar_lista_contatos()
                self._atualizar_lista_participantes()
        except IndexError:
            messagebox.showwarning(
                "Aviso",
                "Por favor, selecione um participante para remover!"
            )
            
    def _realizar_sorteio(self):
        try:
            self.sorteio = realizar_sorteio(self.participantes)
            self._mostrar_resultado()
        except ValueError as e:
            messagebox.showwarning("⚠️ Aviso", str(e))
            
    def _mostrar_resultado(self):
        result_window = tk.Toplevel(self.root)
        result_window.title("🎉 Resultado do Sorteio")
        result_window.geometry(styles.RESULT_WINDOW_SIZE)
        result_window.configure(bg=styles.COLORS['bg'])
        
        # Header com gradiente
        gradient_height = 100
        header_gradient = GradientFrame(
            result_window,
            styles.COLORS['header_bg'],
            styles.COLORS['bg'],
            height=gradient_height,
            title="🎁 Resultado do Sorteio",
            title_font=styles.FONTS['header'],
            title_color=styles.COLORS['text_light'],
            bg=styles.COLORS['bg'],
            highlightthickness=0
        )
        header_gradient.pack(fill=tk.X)
        
        # Conteúdo
        content_frame = tk.Frame(result_window, bg=styles.COLORS['bg'])
        content_frame.pack(padx=30, pady=30, fill=tk.BOTH, expand=True)
        
        select_container = tk.Frame(content_frame, bg=styles.COLORS['bg'])
        select_container.pack(fill=tk.X)
        
        label = tk.Label(
            select_container,
            text="Selecione seu nome:",
            font=styles.FONTS['title'],
            bg=styles.COLORS['bg'],
            fg='black'
        )
        label.pack(anchor='w', pady=(0, 10))
        
        combo_frame = tk.Frame(
            select_container,
            bg=styles.COLORS['border'],
            padx=1,
            pady=1
        )
        combo_frame.pack(fill=tk.X)
        
        combo = ttk.Combobox(
            combo_frame,
            values=list(self.sorteio.keys()),
            font=styles.FONTS['normal'],
            state="readonly"
        )
        combo.pack(fill=tk.X, padx=2, pady=2)
        
        result_container = tk.Frame(content_frame, bg=styles.COLORS['bg'])
        result_container.pack(fill=tk.BOTH, expand=True, pady=30)
        
        result_label = tk.Label(
            result_container,
            text="",
            font=("Helvetica", 18, "bold"),
            bg=styles.COLORS['bg'],
            wraplength=400
        )
        result_label.pack(expand=True)
        
        def mostrar_amigo(event):
            participante = combo.get()
            if participante:
                amigo = self.sorteio[participante]
                result_label.config(
                    text=f"🎁 Você tirou:\n\n{amigo}!",
                    fg='black'
                )
        
        combo.bind('<<ComboboxSelected>>', mostrar_amigo)
        
        save_btn = tk.Button(
            content_frame,
            text="💾 Salvar Resultado",
            command=self._salvar_resultado,
            bg=styles.COLORS['button'],
            fg='black',
            font=styles.FONTS['button'],
            **styles.BUTTON_STYLE
        )
        save_btn.pack()
        
        # Hover effect
        save_btn.bind('<Enter>', lambda e: save_btn.configure(bg=styles.COLORS['button_hover']))
        save_btn.bind('<Leave>', lambda e: save_btn.configure(bg=styles.COLORS['button']))
        
    def _salvar_resultado(self):
        try:
            filename = salvar_resultado(self.sorteio)
            messagebox.showinfo(
                "✅ Sucesso",
                f"Resultado salvo com sucesso em:\n{filename}"
            )
        except Exception as e:
            messagebox.showerror(
                "❌ Erro",
                f"Erro ao salvar o resultado:\n{str(e)}"
            )

    def _on_participant_select(self, event):
        selection = self.participants_listbox.curselection()
        if selection:
            nome = self.participants_listbox.get(selection[0])
            # Se já tiver telefone cadastrado, mostra no campo
            if self.contatos[nome]:
                self.contact_phone_entry.delete(0, tk.END)
                self.contact_phone_entry.insert(0, self.contatos[nome])
                
    def _salvar_telefone(self):
        selection = self.participants_listbox.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Por favor, selecione um participante!")
            return
            
        nome = self.participants_listbox.get(selection[0])
        telefone = self.contact_phone_entry.get().strip()
        
        if not self._validar_telefone(telefone):
            messagebox.showwarning("Aviso", "Telefone inválido! O telefone deve seguir o formato: DDD (2 dígitos) + 9 dígitos, começando com 9.")
            return
            
        self.contatos[nome] = telefone
        self._atualizar_lista_contatos()
        self._atualizar_lista_participantes()
        
        messagebox.showinfo("Sucesso", "Telefone salvo com sucesso!")
        
    def _validar_telefone(self, telefone):
        # Verifica se o telefone tem o formato correto
        if len(telefone) < 11:
            return False
        if not telefone[:2].isdigit() or not telefone[2] == '9':
            return False
        if not telefone[2:].isdigit():
            return False
        return True
        
    def _atualizar_lista_participantes(self):
        self.participants_listbox.delete(0, tk.END)
        for nome in sorted(self.participantes):
            if not self.contatos[nome]:  # Mostra apenas participantes sem telefone
                self.participants_listbox.insert(tk.END, nome)
                
    def _atualizar_lista_contatos(self):
        self.contacts_listbox.delete(0, tk.END)
        for nome, telefone in sorted(self.contatos.items()):
            if telefone:  # Mostra apenas contatos com telefone
                self.contacts_listbox.insert(tk.END, f"{nome} - {telefone}")
                
    def _remover_contato(self):
        selection = self.contacts_listbox.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Por favor, selecione um contato para remover!")
            return
            
        nome = self.contacts_listbox.get(selection[0]).split(" - ")[0]
        self.contatos[nome] = ""  # Apenas remove o telefone, mantém o nome
        self._atualizar_lista_contatos()
        self._atualizar_lista_participantes()
