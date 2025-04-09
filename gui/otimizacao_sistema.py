import tkinter as tk
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from funcoes import sistema

def abrir_otimizacao_sistema(master_frame):
    for widget in master_frame.winfo_children():
        widget.destroy()

    class Switch(tk.Frame):
        def __init__(self, master, text, initial=False):
            super().__init__(master, bg="#f8f8f8")
            self.state = initial
            self.label = text
            self.btn = tk.Button(self, text=self.format_text(), bg=self.get_color(), fg="white", width=35, command=self.toggle)
            self.btn.pack(pady=3)

        def toggle(self):
            self.state = not self.state
            self.btn.config(text=self.format_text(), bg=self.get_color())

        def get(self):
            return self.state

        def format_text(self):
            return f"{self.label}: {'✅ ON' if self.state else '❌ OFF'}"

        def get_color(self):
            return "green" if self.state else "red"

    def aplicar_otimizacoes():
        resultados = []

        log_text.delete("1.0", tk.END)

        if switch_anims.get():
            if hasattr(sistema, 'desativar_animacoes'):
                ok, msg = sistema.desativar_animacoes()
            else:
                ok, msg = False, "Função desativar_animacoes() não encontrada."
        else:
            if hasattr(sistema, 'ativar_animacoes'):
                ok, msg = sistema.ativar_animacoes()
            else:
                ok, msg = False, "Função ativar_animacoes() não encontrada."
        resultados.append(msg)

        if switch_desempenho.get():
            if hasattr(sistema, 'ativar_modo_desempenho'):
                ok, msg = sistema.ativar_modo_desempenho()
            else:
                ok, msg = False, "Função ativar_modo_desempenho() não encontrada."
        else:
            if hasattr(sistema, 'desativar_modo_desempenho'):
                ok, msg = sistema.desativar_modo_desempenho()
            else:
                ok, msg = False, "Função desativar_modo_desempenho() não encontrada."
        resultados.append(msg)

        if switch_ultimate.get():
            ok, msg = sistema.ativar_modo_ultimate()
            resultados.append(msg)

        if switch_servicos.get():
            ok, msg = sistema.desativar_servicos_desnecessarios()
        else:
            msg = "Serviços mantidos ativados"
        resultados.append(msg)

        for linha in resultados:
            log_text.insert(tk.END, f"> {linha}\n")

    tk.Label(master_frame, text="Configurações de Otimização", font=("Helvetica", 14, "bold"), bg="#f8f8f8").pack(pady=15)

    switch_anims = Switch(master_frame, "Desativar animações do Windows", initial=True)
    switch_anims.pack()

    switch_desempenho = Switch(master_frame, "Habilitar modo de desempenho", initial=False)
    switch_desempenho.pack()

    switch_ultimate = Switch(master_frame, "⚡ Desempenho Máximo (Ultimate)", initial=False)
    switch_ultimate.pack()

    switch_servicos = Switch(master_frame, "Desativar serviços desnecessários", initial=True)
    switch_servicos.pack()

    tk.Button(master_frame, text="Aplicar Selecionadas", command=aplicar_otimizacoes, bg="#4CAF50", fg="white").pack(pady=15)

    global log_text
    log_text = tk.Text(master_frame, height=10, width=70, bg="black", fg="lime", insertbackground="white")
    log_text.pack(pady=5)