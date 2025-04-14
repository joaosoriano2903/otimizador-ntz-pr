import tkinter as tk
from funcoes import rede

spinner_label = None
spinner_running = False
spinner_index = 0
spinner_texts = [
    "\U0001F5A7 Otimizando conexão...",
    "\U0001F5A7 Otimizando conexão..",
    "\U0001F5A7 Otimizando conexão...",
    "\U0001F5A7 Otimizando conexão...."
]

frame_resultado = None
relatorio_final = []
log_text = None

def iniciar_spinner(master_frame):
    global spinner_label, spinner_running, spinner_index
    if spinner_label:
        spinner_label.destroy()
    spinner_running = True
    spinner_index = 0

    spinner_label = tk.Label(master_frame, text="", font=("Helvetica", 14, "bold"), fg="orange", bg="#f8f8f8")
    spinner_label.pack(pady=15)

    atualizar_spinner(master_frame)

def atualizar_spinner(master_frame):
    global spinner_label, spinner_running, spinner_index
    if spinner_running and spinner_label:
        spinner_label.config(text=spinner_texts[spinner_index])
        spinner_index = (spinner_index + 1) % len(spinner_texts)
        master_frame.after(400, lambda: atualizar_spinner(master_frame))

def parar_spinner():
    global spinner_running, spinner_label
    spinner_running = False
    if spinner_label:
        spinner_label.destroy()
        spinner_label = None

def mostrar_relatorio(master_frame):
    global log_text
    log_text = tk.Text(master_frame, height=8, width=60, bg="black", fg="lime", insertbackground="white", wrap="word")
    log_text.pack(pady=5)

    for item in relatorio_final:
        log_text.insert(tk.END, f"✅ {item}\n")

    log_text.config(state="disabled")

def abrir_rede(master_frame):
    global log_text
    for widget in master_frame.winfo_children():
        widget.destroy()

    class Switch(tk.Frame):
        def __init__(self, master, text, func):
            super().__init__(master, bg="#f8f8f8")
            self.state = False
            self.text = text
            self.func = func

            self.label = tk.Label(self, text=self.text, font=("Helvetica", 11), bg="#f8f8f8")
            self.label.pack(side="left", padx=10)

            self.canvas = tk.Canvas(self, width=70, height=30, bg="#f8f8f8", highlightthickness=0)
            self.canvas.pack(side="right", padx=10)
            self.canvas.bind("<Button-1>", self.toggle)
            self.draw_switch()

        def toggle(self, event=None):
            self.state = not self.state
            self.draw_switch()

        def get(self):
            return self.state

        def draw_switch(self):
            self.canvas.delete("all")
            if self.state:
                self.canvas.create_rectangle(0, 0, 70, 30, fill="green", outline="")
                self.canvas.create_oval(40, 5, 65, 25, fill="white", outline="")
                self.canvas.create_text(20, 15, text="ON", fill="white", font=("Helvetica", 9, "bold"))
            else:
                self.canvas.create_rectangle(0, 0, 70, 30, fill="red", outline="")
                self.canvas.create_oval(5, 5, 30, 25, fill="white", outline="")
                self.canvas.create_text(50, 15, text="OFF", fill="white", font=("Helvetica", 9, "bold"))

        def execute(self):
            if self.state and self.func:
                return self.func()
            return None, None

    def aplicar_otimizacao_rede():
        global relatorio_final, log_text
        relatorio_final = []

        if log_text:
            log_text.destroy()
            log_text = None

        iniciar_spinner(master_frame)
        master_frame.after(2500, executar_rede)

    def executar_rede():
        parar_spinner()
        for switch in switches:
            ok, msg = switch.execute()
            if msg:
                relatorio_final.append(msg)
        mostrar_relatorio(master_frame)

    tk.Label(master_frame, text="🌐 Otimização de Rede", font=("Helvetica", 14, "bold"), bg="#f8f8f8").pack(pady=15)

    container = tk.Frame(master_frame, bg="#f8f8f8")
    container.pack(pady=10, fill="x", expand=True)

    switches = []

    s1 = Switch(container, "Alterar DNS para Cloudflare", rede.otimizar_dns)
    s1.pack(pady=5, fill="x")
    switches.append(s1)

    s2 = Switch(container, "Ajustar Parâmetros TCP", rede.ajustar_tcp)
    s2.pack(pady=5, fill="x")
    switches.append(s2)

    s3 = Switch(container, "Verificar Firewall", rede.verificar_firewall)
    s3.pack(pady=5, fill="x")
    switches.append(s3)

    s4 = Switch(container, "Auto Negociação (Ethernet)", lambda: rede.auto_negociacao("Ethernet"))
    s4.pack(pady=5, fill="x")
    switches.append(s4)

    s5 = Switch(container, "Otimizar Wi-Fi (MTU, autoconfig)", lambda: rede.otimizar_wifi("Wi-Fi"))
    s5.pack(pady=5, fill="x")
    switches.append(s5)

    tk.Button(
        master_frame,
        text="Aplicar Melhorias de Rede",
        command=aplicar_otimizacao_rede,
        bg="#00994d",
        fg="white",
        font=("Helvetica", 10, "bold"),
        relief="flat",
        width=25,
        height=2,
        bd=0,
        highlightthickness=0
    ).pack(pady=20)
