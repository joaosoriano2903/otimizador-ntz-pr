import tkinter as tk

def abrir_limpeza(master_frame):
    for widget in master_frame.winfo_children():
        widget.destroy()

    class Switch(tk.Frame):
        def __init__(self, master, text, command=None):
            super().__init__(master, bg="#f8f8f8")
            self.state = False
            self.command = command
            self.btn = tk.Button(self, text=f"{text}: ❌ OFF", bg="red", fg="white", width=35, command=self.toggle)
            self.btn.pack(pady=5)

        def toggle(self):
            self.state = not self.state
            if self.state:
                self.btn.config(text=self.btn.cget("text").replace("❌ OFF", "✅ ON"), bg="green")
            else:
                self.btn.config(text=self.btn.cget("text").replace("✅ ON", "❌ OFF"), bg="red")
            if self.command:
                self.command(self.state)

        def get(self):
            return self.state

    def executar_limpeza():
        log_text.delete("1.0", tk.END)
        log_text.insert(tk.END, "> Limpando arquivos temporários...
")
        log_text.insert(tk.END, "> Otimizando armazenamento...
")
        log_text.insert(tk.END, "> Limpando cache do Windows...
")
        log_text.insert(tk.END, "✅ Limpeza concluída com sucesso.
")

    # Layout da tela de limpeza
    tk.Label(master_frame, text="🧹 Otimização de Limpeza", font=("Helvetica", 14, "bold"), bg="#f8f8f8").pack(pady=15)

    switch_temp = Switch(master_frame, "Limpar arquivos temporários")
    switch_temp.pack()

    switch_cache = Switch(master_frame, "Limpar cache do sistema")
    switch_cache.pack()

    switch_storage = Switch(master_frame, "Otimizar armazenamento")
    switch_storage.pack()

    tk.Button(master_frame, text="Executar Limpeza", bg="#2196F3", fg="white", command=executar_limpeza).pack(pady=15)

    global log_text
    log_text = tk.Text(master_frame, height=8, width=60, bg="black", fg="lime", insertbackground="white")
    log_text.pack(pady=5)