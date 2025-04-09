import tkinter as tk
from tkinter import messagebox

# Tela de Limpeza com switches e terminal

def abrir_limpeza(master_frame):
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

        def set(self, value):
            self.state = value
            self.btn.config(text=self.format_text(), bg=self.get_color())

        def format_text(self):
            return f"{self.label}: {'✅ ON' if self.state else '❌ OFF'}"

        def get_color(self):
            return "green" if self.state else "red"

    def executar_limpeza():
        log_text.delete("1.0", tk.END)
        logs = []

        if switch_temp.get():
            logs.append("🧹 Limpando arquivos temporários...")
            # aqui vai a função real no futuro
        if switch_cache.get():
            logs.append("🧹 Limpando cache de sistema...")
        if switch_lixeira.get():
            logs.append("🧹 Esvaziando lixeira...")

        for linha in logs:
            log_text.insert(tk.END, f"> {linha}\n")

    tk.Label(master_frame, text="Limpeza de Sistema", font=("Helvetica", 14, "bold"), bg="#f8f8f8").pack(pady=15)

    switch_temp = Switch(master_frame, "Apagar arquivos temporários", initial=True)
    switch_temp.pack()

    switch_cache = Switch(master_frame, "Limpar cache do sistema", initial=False)
    switch_cache.pack()

    switch_lixeira = Switch(master_frame, "Esvaziar lixeira", initial=False)
    switch_lixeira.pack()

    tk.Button(master_frame, text="Executar Limpeza", command=executar_limpeza, bg="#2196F3", fg="white").pack(pady=15)

    global log_text
    log_text = tk.Text(master_frame, height=10, width=70, bg="black", fg="lime", insertbackground="white")
    log_text.pack(pady=5)
