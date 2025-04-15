import tkinter as tk
import os
import sys

# Adiciona o diretório pai ao sys.path para localizar o módulo 'funcoes'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from funcoes import rede
from gui.layout_padrao import criar_layout_padrao

relatorio_final = []
log_text = None

spinner_label = None
spinner_running = False
spinner_index = 0
spinner_texts = [
    "\U0001F5A7 Otimizando conexão...",
    "\U0001F5A7 Otimizando conexão..",
    "\U0001F5A7 Otimizando conexão...",
    "\U0001F5A7 Otimizando conexão...."
]

class ModernSwitch(tk.Frame):
    def __init__(self, master, text, key, initial=False):
        super().__init__(master, bg="#f8f8f8")
        self.state = initial
        self.label = text
        self.key = key

        self.label_widget = tk.Label(self, text=self.label, font=("Helvetica", 10), bg="#f8f8f8", anchor="w")
        self.label_widget.grid(row=0, column=0, padx=10)

        self.canvas = tk.Canvas(self, width=50, height=15, bg="#f8f8f8", highlightthickness=0)
        self.canvas.grid(row=0, column=1, padx=10)
        self.canvas.bind("<Button-1>", self.toggle)
        self.draw_switch()

    def toggle(self, event=None):
        self.state = not self.state
        self.draw_switch()

    def get(self):
        return self.state

    def draw_switch(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 5, 50, 10, fill="#d3d3d3", outline="")
        if self.state:
            self.canvas.create_oval(35, 0, 50, 15, fill="green", outline="")
        else:
            self.canvas.create_oval(0, 0, 15, 15, fill="red", outline="")

def iniciar_spinner(master_frame):
    global spinner_label, spinner_running, spinner_index
    spinner_running = True
    spinner_index = 0
    if spinner_label is None:
        spinner_label = tk.Label(master_frame, text="", font=("Helvetica", 14, "bold"), fg="orange", bg="#f8f8f8")
        spinner_label.place(relx=0.5, rely=0.6, anchor="center")
    atualizar_spinner(master_frame)

def atualizar_spinner(master_frame):
    global spinner_label, spinner_running, spinner_index
    if spinner_running:
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
    if log_text:
        log_text.destroy()
        log_text = None

    log_text = tk.Text(master_frame, bg="black", fg="lime", insertbackground="white", wrap="word")
    log_text.place(relx=0.5, rely=0.75, relwidth=0.9, relheight=0.2, anchor="center")

    for item in relatorio_final:
        log_text.insert(tk.END, f"{item}\n")

    log_text.config(state="disabled")

def aplicar_otimizacao_rede(master_frame, switches):
    global relatorio_final, log_text
    relatorio_final = []

    if log_text:
        log_text.destroy()
        log_text = None

    iniciar_spinner(master_frame)

    def executar():
        for switch, funcao in switches:
            if switch.get():
                try:
                    ok, msg = funcao()
                    if msg:
                        relatorio_final.append(msg)
                except Exception as e:
                    relatorio_final.append(f"❌ Erro ao executar {funcao.__name__}: {e}")

        parar_spinner()
        mostrar_relatorio(master_frame)

    master_frame.after(3000, executar)

def abrir_rede(master_frame):
    """Interface principal para otimização de rede."""

    switches = []

    def criar_switches(container):
        # Cria os switches dentro do container correto
        s1 = ModernSwitch(container, "Alterar DNS para Cloudflare", "alterar_dns")
        s2 = ModernSwitch(container, "Ajustar Parâmetros TCP", "ajustar_tcp")
        s3 = ModernSwitch(container, "Verificar Firewall", "verificar_firewall")
        s4 = ModernSwitch(container, "Configurar 1 Gbps Full Duplex", "configurar_1gbps")
        s5 = ModernSwitch(container, "Otimizar Wi-Fi (MTU, autoconfig)", "otimizar_wifi")

        # Adiciona os pares (switch, função) à lista global
        switches.extend([
            (s1, getattr(rede, "otimizar_dns", lambda: (False, "Função não encontrada"))),
            (s2, getattr(rede, "ajustar_tcp", lambda: (False, "Função não encontrada"))),
            (s3, getattr(rede, "verificar_firewall", lambda: (False, "Função não encontrada"))),
            (s4, getattr(rede, "configurar_1gbps", lambda: (False, "Função não encontrada"))),
            (s5, getattr(rede, "otimizar_wifi", lambda: (False, "Função não encontrada"))),
        ])

        return [s1, s2, s3, s4, s5]  # Retorna os widgets criados

    # Chamada do layout padrão com switches criados no container
    criar_layout_padrao(
        master_frame,
        titulo="🌐 Otimização de Rede",
        switches=criar_switches,  # Agora é função que recebe o container
        botao_texto="🚀 Aplicar Melhorias de Rede",
        botao_comando=lambda: aplicar_otimizacao_rede(master_frame, switches)
    )
