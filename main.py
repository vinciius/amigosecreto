"""
Arquivo principal do aplicativo Amigo Secreto
"""
import tkinter as tk
from src.gui.app import AmigoSecretoApp

if __name__ == "__main__":
    root = tk.Tk()
    app = AmigoSecretoApp(root)
    root.mainloop()