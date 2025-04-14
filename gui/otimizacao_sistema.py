import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from funcoes import sistema

spinner_label = None
spinner_running = False
spinner_index = 0
spinner_texts = ["\U0001F477 Trabalhando...", "\U0001F477 Trabalhando..", "\U0001F477 Trabalhando...", "\U0001F477 Trabalhando...."]

relatorio_final = []
prompt_text = None  # Inicializa a variável global para o prompt
log_text = None  # Inicializa a variável global para o log

class ModernSwitch(tk.Frame):
    """Switch moderno e estilizado para alternar entre ON e OFF."""
    def __init__(self, master, text, key, initial=False):
        super().__init__(master, bg="#f8f8f8")
        self.state = initial
        self.label = text
        self.key = key

        # Rótulo do switch
        self.label_widget = tk.Label(self, text=self.label, font=("Helvetica", 10), bg="#f8f8f8", anchor="w")
        self.label_widget.grid(row=0, column=0, padx=10)

        # Canvas para o switch
        self.canvas = tk.Canvas(self, width=50, height=15, bg="#f8f8f8", highlightthickness=0)
        self.canvas.grid(row=0, column=1, padx=10)
        self.canvas.bind("<Button-1>", self.toggle)
        self.draw_switch()

    def toggle(self, event=None):
        """Alterna o estado do switch."""
        self.state = not self.state
        self.draw_switch()

    def get(self):
        """Retorna o estado atual do switch."""
        return self.state

    def draw_switch(self):
        """Desenha o switch no estado atual."""
        self.canvas.delete("all")

        # Barra de fundo (cinza claro)
        self.canvas.create_rectangle(0, 5, 50, 10, fill="#d3d3d3", outline="")

        if self.state:
            # ON: Bolinha verde à direita
            self.canvas.create_oval(35, 0, 50, 15, fill="green", outline="")
        else:
            # OFF: Bolinha vermelha à esquerda
            self.canvas.create_oval(0, 0, 15, 15, fill="red", outline="")

def iniciar_spinner(master_frame):
    """Inicia o spinner de carregamento abaixo do botão."""
    global spinner_label, spinner_running, spinner_index
    spinner_running = True
    spinner_index = 0

    # Adiciona o spinner abaixo do botão "Executar Otimizações"
    if spinner_label is None:
        spinner_label = tk.Label(master_frame, text="", font=("Helvetica", 14, "bold"), fg="orange", bg="#f8f8f8")
        spinner_label.place(relx=0.5, rely=0.6, anchor="center")  # Centralizado abaixo do botão

    atualizar_spinner(master_frame)

def atualizar_spinner(master_frame):
    """Atualiza o texto do spinner."""
    global spinner_label, spinner_running, spinner_index
    if spinner_running:
        spinner_label.config(text=spinner_texts[spinner_index])
        spinner_index = (spinner_index + 1) % len(spinner_texts)
        master_frame.after(400, lambda: atualizar_spinner(master_frame))

def parar_spinner():
    """Para o spinner de carregamento."""
    global spinner_running, spinner_label
    spinner_running = False
    if spinner_label:
        spinner_label.destroy()
        spinner_label = None

def mostrar_relatorio(master_frame):
    """Exibe o relatório de otimizações na interface."""
    global log_text
    if log_text:
        log_text.destroy()  # Remove o log anterior, se existir
        log_text = None

    # Cria o log responsivo
    log_text = tk.Text(master_frame, bg="black", fg="lime", insertbackground="white", wrap="word")
    log_text.place(relx=0.5, rely=0.75, relwidth=0.9, relheight=0.2, anchor="center")  # Responsivo com relwidth e relheight

    # Insere os resultados no log
    for item in relatorio_final:
        log_text.insert(tk.END, f"✅ {item}\n")

    log_text.config(state="disabled")  # Torna o log somente leitura

def executar_comando(comando):
    """Executa um comando no shell e captura erros."""
    try:
        subprocess.run(comando, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar comando: {comando}\n{e}")
        return False

def aplicar_otimizacoes(master_frame, switches_sistema, switches_windows_fix):
    """Aplica ou reverte todas as otimizações e comandos ativados/desativados."""
    global relatorio_final, log_text
    relatorio_final = []

    if log_text:
        log_text.destroy()  # Remove o log anterior, se existir
        log_text = None

    iniciar_spinner(master_frame)

    def executar():
        # Aplicar ou reverter otimizações do sistema
        for switch, funcao in switches_sistema:
            if switch.get():
                if hasattr(sistema, funcao):
                    ok, msg = getattr(sistema, funcao)()
                    relatorio_final.append(msg)
                else:
                    relatorio_final.append(f"Função {funcao} não encontrada.")
            else:
                # Reverter alterações se o switch estiver OFF
                reversao_funcao = f"reverter_{funcao}"
                if hasattr(sistema, reversao_funcao):
                    ok, msg = getattr(sistema, reversao_funcao)()
                    relatorio_final.append(msg)
                else:
                    relatorio_final.append(f"Função de reversão {reversao_funcao} não encontrada.")

        # Aplicar ou ignorar comandos do Windows Fix
        for switch, comando, descricao in switches_windows_fix:
            if switch.get():
                sucesso = executar_comando(comando)
                if sucesso:
                    relatorio_final.append(f"{descricao} executado com sucesso.")
                else:
                    relatorio_final.append(f"Erro ao executar: {descricao}")
            else:
                relatorio_final.append(f"{descricao} ignorado (desativado).")

        parar_spinner()
        mostrar_relatorio(master_frame)  # Exibe o relatório após finalizar

    master_frame.after(3000, executar)

def exibir_prompt(master_frame):
    """Exibe o prompt estilo preto e verde abaixo do botão."""
    global prompt_text
    if prompt_text is None:  # Cria o prompt apenas se ele ainda não existir
        prompt_text = tk.Text(master_frame, height=10, width=80, bg="black", fg="lime", wrap="word", state="disabled")
        prompt_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    else:
        prompt_text.grid()  # Torna o prompt visível, caso esteja oculto

def atualizar_prompt():
    """Atualiza o prompt com o que foi feito."""
    global relatorio_final, prompt_text
    if prompt_text:
        prompt_text.config(state="normal")  # Permite edição temporária
        prompt_text.delete("1.0", tk.END)  # Limpa o conteúdo anterior
        prompt_text.insert(tk.END, "\n".join(relatorio_final))  # Adiciona o novo conteúdo
        prompt_text.config(state="disabled")  # Bloqueia edição novamente

def mostrar_prompt(master_frame):
    """Exibe o prompt estilo preto e verde no canto inferior da tela."""
    global prompt_text
    if prompt_text is None:  # Cria o prompt apenas se ele ainda não existir
        prompt_text = tk.Text(master_frame, height=10, width=80, bg="black", fg="lime", wrap="word", state="disabled")
        prompt_text.place(relx=0.5, rely=0.9, anchor="center")  # Posicionado no canto inferior da tela

def atualizar_prompt():
    """Atualiza o prompt com o que foi feito."""
    global relatorio_final, prompt_text
    if prompt_text and prompt_text.winfo_exists():  # Verifica se o widget ainda existe
        prompt_text.config(state="normal")  # Permite edição temporária
        prompt_text.delete("1.0", tk.END)  # Limpa o conteúdo anterior
        prompt_text.insert(tk.END, "\n".join(relatorio_final))  # Adiciona o novo conteúdo
        prompt_text.config(state="disabled")  # Bloqueia edição novamente

def abrir_otimizacao_sistema(master_frame):
    """Interface principal para otimizações do sistema."""
    for widget in master_frame.winfo_children():
        widget.destroy()

    # Centralizar o layout
    container = tk.Frame(master_frame, bg="#f8f8f8")
    container.place(relx=0.5, rely=0.3, anchor="center")  # Posiciona mais para cima

    # Seção de Otimizações Disponíveis
    tk.Label(container, text="⚙️ Otimizações Disponíveis", font=("Helvetica", 14, "bold"), bg="#f8f8f8", fg="black").grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # Seção de Windows Fix
    tk.Label(container, text="🛠️ Windows Fix", font=("Helvetica", 14, "bold"), bg="#f8f8f8", fg="black").grid(row=0, column=1, padx=10, pady=10, sticky="w")

    # Seção de USB
    tk.Label(container, text="🔌 Otimização de USB", font=("Helvetica", 14, "bold"), bg="#f8f8f8", fg="black").grid(row=0, column=2, padx=10, pady=10, sticky="w")

    # Seção de CPU
    tk.Label(container, text="🖥️ Otimização de CPU", font=("Helvetica", 14, "bold"), bg="#f8f8f8", fg="black").grid(row=0, column=3, padx=10, pady=10, sticky="w")

    # Containers para switches
    sistema_container = tk.Frame(container, bg="#f8f8f8")
    sistema_container.grid(row=1, column=0, padx=10, pady=10, sticky="n")

    windows_fix_container = tk.Frame(container, bg="#f8f8f8")
    windows_fix_container.grid(row=1, column=1, padx=10, pady=10, sticky="n")

    usb_container = tk.Frame(container, bg="#f8f8f8")
    usb_container.grid(row=1, column=2, padx=10, pady=10, sticky="n")

    cpu_container = tk.Frame(container, bg="#f8f8f8")
    cpu_container.grid(row=1, column=3, padx=10, pady=10, sticky="n")

    # Switches para otimizações do sistema
    switches_sistema = [
        (ModernSwitch(sistema_container, "Desativar Animações do Windows", "desativar_animacoes", initial=True), "desativar_animacoes"),
        (ModernSwitch(sistema_container, "Habilitar Modo de Desempenho", "ativar_modo_desempenho", initial=True), "ativar_modo_desempenho"),
        (ModernSwitch(sistema_container, "⚡ Modo Ultimate (Desempenho Máximo)", "ativar_modo_ultimate", initial=False), "ativar_modo_ultimate"),
        (ModernSwitch(sistema_container, "Desativar Serviços Desnecessários", "desativar_servicos_desnecessarios", initial=True), "desativar_servicos_desnecessarios")
    ]

    for i, (switch, _) in enumerate(switches_sistema):
        switch.grid(row=i, column=0, padx=10, pady=5, sticky="w")

    # Switches para comandos do Windows Fix
    comandos = [
        ("Start Component Cleanup", "DISM /Online /Cleanup-Image /StartComponentCleanup", "Remove componentes desnecessários."),
        ("Check Health", "DISM /Online /Cleanup-Image /CheckHealth", "Verifica problemas de integridade."),
        ("Scan Health", "DISM /Online /Cleanup-Image /ScanHealth", "Realiza uma varredura profunda."),
        ("Restore Health", "DISM /Online /Cleanup-Image /RestoreHealth", "Corrige problemas encontrados."),
        ("System File Checker (SFC)", "sfc /scannow", "Verifica e repara arquivos do sistema.")
    ]

    switches_windows_fix = []
    for i, (label, comando, descricao) in enumerate(comandos):
        switch = ModernSwitch(windows_fix_container, label, comando, initial=True)
        switch.grid(row=i, column=0, padx=10, pady=5, sticky="w")
        switches_windows_fix.append((switch, comando, descricao))

    # Switch único para otimização e reversão de USB
    switch_usb = ModernSwitch(usb_container, "Gerenciar Otimização de USB", "otimizar_usb", initial=True)
    switch_usb.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    switches_usb = [(switch_usb, "otimizar_usb")]

    # Switches para otimização de CPU
    switch_cpu_amd = ModernSwitch(cpu_container, "Otimizar CPU AMD", "otimizar_cpu_amd", initial=False)
    switch_cpu_amd.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    switch_cpu_intel = ModernSwitch(cpu_container, "Otimizar CPU Intel", "otimizar_cpu_intel", initial=False)
    switch_cpu_intel.grid(row=1, column=0, padx=10, pady=5, sticky="w")

    switches_cpu = [
        (switch_cpu_amd, "otimizar_cpu_amd"),
        (switch_cpu_intel, "otimizar_cpu_intel")
    ]

    # Botão para executar todas as otimizações
    botao_executar = tk.Button(
        container,
        text="🚀 Executar Otimizações",
        command=lambda: aplicar_otimizacoes(master_frame, switches_sistema + switches_usb + switches_cpu, switches_windows_fix),
        bg="#000000",  # Fundo preto
        fg="#00ff00",  # Texto verde
        font=("Helvetica", 14, "bold"),
        relief="flat",
        width=30,
        height=2,
        bd=0,
        highlightthickness=0,
        activebackground="#00ff00",  # Fundo verde ao clicar
        activeforeground="#000000",  # Texto preto ao clicar
        cursor="hand2"
    )
    botao_executar.grid(row=2, column=0, columnspan=4, pady=20)