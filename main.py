import random
import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os

class AmigoSecretoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎁 Amigo Secreto")
        self.root.geometry("500x500")
        self.root.configure(bg="#f6f6f8")
        
        # Cores
        self.colors = {
            'primary': '#7c93c4',  # Pastel blue
            'secondary': '#f1959b', # Pastel pink
            'bg': '#f6f6f8',       # Light gray-blue
            'text': '#4a4a4a',     # Dark gray
            'button': '#93b5b3',   # Pastel teal
            'list_bg': '#ffffff'   # Pure white
        }
        
        self.participantes = []
        self.sorteio = {}
        
        self.setup_gui()
        
    def setup_gui(self):
        # Frame principal com padding uniforme
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)
        
        # Container central para melhor alinhamento
        center_container = tk.Frame(main_frame, bg=self.colors['bg'])
        center_container.pack(fill=tk.BOTH, expand=True, padx=10)
        
        # Título com menos espaço
        titulo = tk.Label(
            center_container,
            text="🎄 Amigo Secreto 🎁",
            font=("Helvetica", 24, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['primary']
        )
        titulo.pack(pady=(0, 20))
        
        # Frame para entrada com menos espaçamento
        entry_frame = tk.Frame(center_container, bg=self.colors['bg'])
        entry_frame.pack(fill=tk.X, padx=10, pady=(0, 15))
        
        # Label para o campo de entrada
        entry_label = tk.Label(
            entry_frame,
            text="Nome do Participante:",
            font=("Helvetica", 12),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        entry_label.pack(anchor='w', pady=(0, 5))
        
        # Container para entrada e botão
        input_container = tk.Frame(entry_frame, bg=self.colors['bg'])
        input_container.pack(fill=tk.X)
        
        # Campo de entrada estilizado
        self.nome_entry = ttk.Entry(
            input_container,
            font=("Helvetica", 12)
        )
        self.nome_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        
        # Botão adicionar com hover effect
        add_btn = tk.Button(
            input_container,
            text="Adicionar",
            command=self.adicionar_participante,
            bg=self.colors['button'],
            fg='white',
            font=("Helvetica", 11),
            relief=tk.FLAT,
            padx=25,
            pady=5,
            cursor="hand2"
        )
        add_btn.pack(side=tk.LEFT)
        
        # Frame para lista com menos padding
        self.lista_frame = tk.Frame(
            center_container,
            bg=self.colors['list_bg'],
            highlightbackground=self.colors['button'],
            highlightthickness=1
        )
        self.lista_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Label para a lista com menos padding
        lista_label = tk.Label(
            self.lista_frame,
            text="Participantes:",
            font=("Helvetica", 11, "bold"),
            bg=self.colors['list_bg'],
            fg=self.colors['text']
        )
        lista_label.pack(anchor='w', padx=10, pady=5)
        
        # Container para lista e scrollbar com menos padding
        list_container = tk.Frame(self.lista_frame, bg=self.colors['list_bg'])
        list_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # Scrollbar para a lista
        scrollbar = ttk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox estilizada
        self.listbox = tk.Listbox(
            list_container,
            font=("Helvetica", 12),
            selectmode=tk.SINGLE,
            bg=self.colors['list_bg'],
            fg=self.colors['text'],
            selectbackground=self.colors['button'],
            relief=tk.FLAT,
            highlightthickness=0,
            activestyle='none'
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configurar scrollbar
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)
        
        # Frame para botões de ação com menos espaço
        btn_frame = tk.Frame(center_container, bg=self.colors['bg'])
        btn_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Botão remover
        remove_btn = tk.Button(
            btn_frame,
            text="Remover Selecionado",
            command=self.remover_participante,
            bg=self.colors['secondary'],
            fg='white',
            font=("Helvetica", 11),
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2"
        )
        remove_btn.pack(side=tk.LEFT)
        
        # Botão sortear
        sortear_btn = tk.Button(
            btn_frame,
            text="Realizar Sorteio",
            command=self.realizar_sorteio,
            bg=self.colors['button'],
            fg='white',
            font=("Helvetica", 11, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=5,
            cursor="hand2"
        )
        sortear_btn.pack(side=tk.RIGHT)
        
        # Bind Enter key
        self.nome_entry.bind('<Return>', lambda e: self.adicionar_participante())
        
    def adicionar_participante(self):
        nome = self.nome_entry.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Por favor, digite um nome!")
            return
            
        if nome in self.participantes:
            messagebox.showwarning("Aviso", "Este participante já foi adicionado!")
            return
            
        self.participantes.append(nome)
        self.listbox.insert(tk.END, nome)
        self.nome_entry.delete(0, tk.END)
        
    def remover_participante(self):
        try:
            sel = self.listbox.curselection()[0]
            nome = self.listbox.get(sel)
            self.participantes.remove(nome)
            self.listbox.delete(sel)
        except IndexError:
            messagebox.showwarning("Aviso", "Selecione um participante para remover!")
            
    def realizar_sorteio(self):
        if len(self.participantes) < 2:
            messagebox.showwarning("Aviso", "É necessário pelo menos 2 participantes!")
            return
            
        # Realizar sorteio
        amigos_disponiveis = self.participantes.copy()
        self.sorteio.clear()
        
        for participante in self.participantes:
            while True:
                amigo = random.choice(amigos_disponiveis)
                if amigo != participante:
                    self.sorteio[participante] = amigo
                    amigos_disponiveis.remove(amigo)
                    break
        
        self.mostrar_resultado()
        
    def mostrar_resultado(self):
        # Criar nova janela para resultados
        result_window = tk.Toplevel(self.root)
        result_window.title("🎉 Resultado do Sorteio")
        result_window.geometry("400x350")
        result_window.configure(bg=self.colors['bg'])
        
        # Frame para resultados com menos padding
        result_frame = tk.Frame(result_window, bg=self.colors['bg'])
        result_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # Título do resultado menor
        titulo_resultado = tk.Label(
            result_frame,
            text="Resultado do Sorteio",
            font=("Helvetica", 20, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['primary']
        )
        titulo_resultado.pack(pady=(0, 20))
        
        # Container para seleção
        select_container = tk.Frame(result_frame, bg=self.colors['bg'])
        select_container.pack(fill=tk.X, pady=(0, 20))
        
        # Label para combobox
        label = tk.Label(
            select_container,
            text="Selecione seu nome:",
            font=("Helvetica", 12),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        label.pack(anchor='w', pady=(0, 5))
        
        # Combobox estilizado
        combo = ttk.Combobox(
            select_container,
            values=list(self.sorteio.keys()),
            font=("Helvetica", 12),
            state="readonly"
        )
        combo.pack(fill=tk.X)
        
        # Container para resultado
        result_container = tk.Frame(result_frame, bg=self.colors['bg'])
        result_container.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Label para mostrar resultado
        result_label = tk.Label(
            result_container,
            text="",
            font=("Helvetica", 16, "bold"),
            bg=self.colors['bg'],
            wraplength=350
        )
        result_label.pack(expand=True)
        
        def mostrar_amigo(event):
            participante = combo.get()
            if participante:
                amigo = self.sorteio[participante]
                result_label.config(
                    text=f"🎁 Você tirou:\n\n{amigo}!",
                    fg=self.colors['secondary']
                )
        
        combo.bind('<<ComboboxSelected>>', mostrar_amigo)
        
        # Botão para salvar resultado
        save_btn = tk.Button(
            result_frame,
            text="Salvar Resultado",
            command=lambda: self.salvar_resultado(),
            bg=self.colors['button'],
            fg='white',
            font=("Helvetica", 11),
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        save_btn.pack(pady=(20, 0))
        
    def salvar_resultado(self):
        # Criar diretório se não existir
        if not os.path.exists('resultados'):
            os.makedirs('resultados')
            
        # Nome do arquivo com data e hora
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resultados/sorteio_{timestamp}.json"
        
        # Salvar resultado
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.sorteio, f, ensure_ascii=False, indent=4)
            
        messagebox.showinfo(
            "Sucesso",
            f"Resultado salvo com sucesso em:\n{filename}"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = AmigoSecretoApp(root)
    root.mainloop()