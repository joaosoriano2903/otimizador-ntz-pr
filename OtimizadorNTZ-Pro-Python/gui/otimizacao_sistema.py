import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys
from gui.rede_sistema import ModernSwitch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from funcoes import sistema
from gui.layout_padrao import criar_layout_padrao

spinner_label = None
spinner_running = False
spinner_index = 0
spinner_texts = ["\U0001F477 Trabalhando...", "\U0001F477 Trabalhando..", "\U0001F477 Trabalhando...", "\U0001F477 Trabalhando...."]

relatorio_final = []
log_text = None

def iniciar_spinner(master_frame):
    """Inicia o spinner de carregamento."""
    global spinner_label, spinner_running, spinner_index
    spinner_running = True
    spinner_index = 0
    if spinner_label is None:
        spinner_label = tk.Label(master_frame, text="", font=("Helvetica", 14, "bold"), fg="orange", bg="#f8f8f8")
        spinner_label.place(relx=0.5, rely=0.6, anchor="center")
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
        log_text.destroy()
        log_text = None

    log_text = tk.Text(master_frame, bg="black", fg="lime", insertbackground="white", wrap="word")
    log_text.place(relx=0.5, rely=0.75, relwidth=0.9, relheight=0.2, anchor="center")

    for item in relatorio_final:
        log_text.insert(tk.END, f"✅ {item}\n")

    log_text.config(state="disabled")

def executar_comando(comando):
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
        log_text.destroy()
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
        mostrar_relatorio(master_frame)

    master_frame.after(3000, executar)

def abrir_otimizacao_sistema(master_frame):
    """Interface principal para otimizações do sistema."""
    switches_sistema = []
    switches_windows_fix = []

    def criar_switches(container):
        """Cria os switches para otimizações do sistema."""
        s1 = ModernSwitch(container, "Desativar Animações do Windows", "desativar_animacoes", initial=True)
        s2 = ModernSwitch(container, "Habilitar Modo de Desempenho", "ativar_modo_desempenho", initial=True)
        s3 = ModernSwitch(container, "⚡ Modo Ultimate (Desempenho Máximo)", "ativar_modo_ultimate", initial=False)
        s4 = ModernSwitch(container, "Desativar Serviços Desnecessários", "desativar_servicos_desnecessarios", initial=True)
        switches_sistema.extend([
            (s1, "desativar_animacoes"),
            (s2, "ativar_modo_desempenho"),
            (s3, "ativar_modo_ultimate"),
            (s4, "desativar_servicos_desnecessarios")
        ])
        return [s1, s2, s3, s4]

    def criar_fix(container):
        """Cria os switches para comandos do Windows Fix."""
        comandos = [
            ("Start Component Cleanup", "DISM /Online /Cleanup-Image /StartComponentCleanup", "Remove componentes desnecessários."),
            ("Check Health", "DISM /Online /Cleanup-Image /CheckHealth", "Verifica problemas de integridade."),
            ("Scan Health", "DISM /Online /Cleanup-Image /ScanHealth", "Realiza uma varredura profunda."),
            ("Restore Health", "DISM /Online /Cleanup-Image /RestoreHealth", "Corrige problemas encontrados."),
            ("System File Checker (SFC)", "sfc /scannow", "Verifica e repara arquivos do sistema.")
        ]
        lista = []
        for label, comando, descricao in comandos:
            s = ModernSwitch(container, label, comando, initial=True)
            lista.append(s)
            switches_windows_fix.append((s, comando, descricao))
        return lista

    criar_layout_padrao(
        master_frame,
        titulo="⚙️ Otimização de Sistema e Windows Fix",
        switches=criar_switches,
        botao_texto="🚀 Executar Otimizações",
        botao_comando=lambda: aplicar_otimizacoes(master_frame, switches_sistema, switches_windows_fix)
    )
