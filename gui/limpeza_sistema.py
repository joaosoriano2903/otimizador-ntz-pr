import tkinter as tk
import subprocess
import os
import sys
import locale
import psutil
import ctypes

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from funcoes import sistema

spinner_label = None
spinner_running = False
spinner_index = 0
spinner_texts = ["👷 Trabalhando...", "👷 Trabalhando..", "👷 Trabalhando...", "👷 Trabalhando...."]

relatorio_final = []
log_text = None

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
    """Exibe o relatório de limpeza na interface."""
    global log_text
    if log_text:
        log_text.destroy()  # Remove o log anterior, se existir
        log_text = None

    # Cria o log responsivo
    log_text = tk.Text(master_frame, bg="black", fg="lime", insertbackground="white", wrap="word")
    log_text.place(relx=0.5, rely=0.75, relwidth=0.9, relheight=0.2, anchor="center")  # Responsivo com relwidth e relheight

    # Insere os resultados no log
    for item in relatorio_final:
        log_text.insert(tk.END, f"{item}\n")

    log_text.config(state="disabled")  # Torna o log somente leitura

def executar_comando(comando):
    """Executa um comando no shell e captura a saída."""
    try:
        encoding_padrao = locale.getpreferredencoding()
        resultado = subprocess.run(
            comando,
            shell=True,
            check=True,
            text=True,
            capture_output=True,
            encoding=encoding_padrao
        )
        # Verifica se stdout é None e retorna uma string vazia se for o caso
        saida = resultado.stdout.strip() if resultado.stdout else ""
        # Filtra mensagens de aviso específicas
        saida_filtrada = "\n".join(
            linha for linha in saida.split("\n")
            if "not supported in system mode" not in linha
        )
        return True, saida_filtrada
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip() if e.stderr else "Erro desconhecido."

def aplicar_tweaks_bcd():
    comandos = [
        r'bcdedit /set useplatformclock No',
        r'bcdedit /set disabledynamictick Yes'
    ]
    mensagens = []
    for comando in comandos:
        sucesso, mensagem = executar_comando(comando)
        if mensagem:
            mensagens.append(mensagem)
        else:
            mensagens.append(f"✅ Comando executado: {comando}")
    return True, "\n".join(mensagens)

def desabilitar_mitigacoes():
    comandos = [
        r'powershell "ForEach($v in (Get-Command -Name \"Set-ProcessMitigation\").Parameters[\"Disable\"].Attributes.ValidValues){Set-ProcessMitigation -System -Disable $v.ToString()}"',
        r'powershell "Remove-Item -Path \"HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\*\" -Recurse"'
    ]
    mensagens = []
    for comando in comandos:
        sucesso, mensagem = executar_comando(comando)
        if mensagem:
            mensagens.append(mensagem)
        else:
            mensagens.append(f"✅ Comando executado: {comando}")
    return True, "\n".join(mensagens)

def aplicar_ntfs_tweaks():
    comandos = [
        r'fsutil behavior set memoryusage 2',
        r'fsutil behavior set mftzone 4',
        r'fsutil behavior set disablelastaccess 1'
    ]
    mensagens = []
    for comando in comandos:
        sucesso, mensagem = executar_comando(comando)
        if mensagem:
            mensagens.append(mensagem)
        else:
            mensagens.append(f"✅ Comando executado: {comando}")
    return True, "\n".join(mensagens)

def desabilitar_compressor_memoria():
    comandos = [
        r'powershell -Command "Disable-MMAgent -MemoryCompression"'
    ]
    mensagens = []
    for comando in comandos:
        sucesso, mensagem = executar_comando(comando)
        if sucesso:
            mensagens.append("✅ Compressor de memória desabilitado com sucesso.")
            mensagens.append(
                "🔍 O compressor de memória foi desativado. Isso pode melhorar o desempenho em sistemas com memória suficiente, "
                "reduzindo a sobrecarga de CPU causada pela compressão e descompressão de memória."
            )
        else:
            mensagens.append(f"❌ Erro ao desabilitar o compressor de memória: {mensagem}")
    return True, "\n".join(mensagens)

def limpar_arquivos_temporarios():
    comandos = [
        r'del /q /f /s %TEMP%\*',
        r'del /q /f /s C:\Windows\Temp\*'
    ]
    mensagens = []
    for comando in comandos:
        sucesso, mensagem = executar_comando(comando)
        if sucesso:
            mensagens.append("✅ Arquivos temporários removidos com sucesso.")
        else:
            mensagens.append(f"❌ Erro ao remover arquivos temporários: {mensagem}")
    return True, "\n".join(mensagens)

def limpar_cache_windows_update():
    comandos = [
        r'net stop wuauserv',
        r'net stop bits',
        r'rd /s /q C:\Windows\SoftwareDistribution',
        r'net start wuauserv',
        r'net start bits'
    ]
    mensagens = []
    for comando in comandos:
        sucesso, mensagem = executar_comando(comando)
        if sucesso:
            mensagens.append("✅ Cache do Windows Update limpo com sucesso.")
        else:
            mensagens.append(f"❌ Erro ao limpar o cache do Windows Update: {mensagem}")
    return True, "\n".join(mensagens)

def limpar_logs_sistema():
    comandos = [
        r'del /q /f /s C:\Windows\System32\LogFiles\*',
        r'del /q /f /s C:\Windows\Logs\*'
    ]
    mensagens = []
    for comando in comandos:
        sucesso, mensagem = executar_comando(comando)
        if sucesso:
            mensagens.append("✅ Logs do sistema removidos com sucesso.")
        else:
            mensagens.append(f"❌ Erro ao remover logs do sistema: {mensagem}")
    return True, "\n".join(mensagens)

def desabilitar_hibernacao():
    comandos = [
        r'powercfg -h off'
    ]
    mensagens = []
    for comando in comandos:
        sucesso, mensagem = executar_comando(comando)
        if sucesso:
            mensagens.append("✅ Hibernação desabilitada com sucesso.")
        else:
            mensagens.append(f"❌ Erro ao desabilitar hibernação: {mensagem}")
    return True, "\n".join(mensagens)

def verificar_e_remover_chave(registro):
    comando_verificar = f'powershell "Test-Path -Path \\"{registro}\\""'
    sucesso, mensagem = executar_comando(comando_verificar)
    if sucesso and mensagem.strip().lower() == "true":
        comando_remover = f'powershell "Remove-Item -Path \\"{registro}\\" -Recurse -ErrorAction SilentlyContinue"'
        sucesso_remover, mensagem_remover = executar_comando(comando_remover)
        if not sucesso_remover:
            if "UnauthorizedAccessException" in mensagem_remover:
                return False, f"❌ Permissão negada ao tentar remover a chave {registro}. Execute o programa como administrador."
            return False, f"❌ Erro ao remover a chave {registro}: {mensagem_remover}"
        return True, f"✅ Chave {registro} removida com sucesso."
    return True, f"🔍 Chave {registro} não encontrada. Nenhuma ação necessária."

def limpar_chaves_registro():
    chaves = [
        r"HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\MRT.exe",
        r"HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\MsMpEng.exe",
        r"HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\MsSense.exe"
    ]
    mensagens = []
    for chave in chaves:
        sucesso, mensagem = verificar_e_remover_chave(chave)
        mensagens.append(mensagem)
    return True, "\n".join(mensagens)

def desfragmentar_memoria():
    """Desfragmenta a memória do sistema e retorna a quantidade de memória liberada."""
    try:
        # Obtém a memória disponível antes da desfragmentação
        memoria_antes = psutil.virtual_memory().available

        # Chama o EmptyWorkingSet para liberar memória não utilizada
        ctypes.windll.psapi.EmptyWorkingSet(ctypes.windll.kernel32.GetCurrentProcess())

        # Obtém a memória disponível após a desfragmentação
        memoria_depois = psutil.virtual_memory().available

        # Calcula a quantidade de memória liberada
        memoria_liberada = (memoria_depois - memoria_antes) / (1024 * 1024)  # Converte para MB

        if memoria_liberada > 0:
            return True, f"✅ Memória desfragmentada com sucesso. Memória liberada: {memoria_liberada:.2f} MB."
        else:
            return True, "🔍 Nenhuma memória adicional foi liberada durante a desfragmentação."
    except Exception as e:
        return False, f"❌ Erro ao desfragmentar a memória: {e}"

def abrir_limpeza(master_frame):
    """Interface principal para limpeza do sistema."""
    global log_text
    for widget in master_frame.winfo_children():
        widget.destroy()

    # Centralizar o layout
    container = tk.Frame(master_frame, bg="#f8f8f8")
    container.place(relx=0.5, rely=0.3, anchor="center")  # Posiciona mais para cima

    # Título da seção
    tk.Label(container, text="🧹 Limpeza do Sistema", font=("Helvetica", 14, "bold"), bg="#f8f8f8", fg="black").grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # Lista de switches
    switches = [
        (ModernSwitch(container, "Aplicar Tweaks de BCD", "aplicar_tweaks_bcd", initial=True), aplicar_tweaks_bcd),
        (ModernSwitch(container, "Desabilitar Mitigações", "desabilitar_mitigacoes", initial=True), desabilitar_mitigacoes),
        (ModernSwitch(container, "Aplicar Tweaks de NTFS", "aplicar_ntfs_tweaks", initial=True), aplicar_ntfs_tweaks),
        (ModernSwitch(container, "Desabilitar Compressor de Memória", "desabilitar_compressor_memoria", initial=True), desabilitar_compressor_memoria),
        (ModernSwitch(container, "Limpar Arquivos Temporários", "limpar_arquivos_temporarios", initial=True), limpar_arquivos_temporarios),
        (ModernSwitch(container, "Limpar Cache do Windows Update", "limpar_cache_windows_update", initial=True), limpar_cache_windows_update),
        (ModernSwitch(container, "Limpar Logs do Sistema", "limpar_logs_sistema", initial=True), limpar_logs_sistema),
        (ModernSwitch(container, "Desabilitar Hibernação", "desabilitar_hibernacao", initial=False), desabilitar_hibernacao),
        (ModernSwitch(container, "Desfragmentar Memória", "desfragmentar_memoria", initial=True), desfragmentar_memoria),
    ]

    for i, (switch, _) in enumerate(switches):
        switch.grid(row=i + 1, column=0, padx=10, pady=5, sticky="w")

    # Botão para executar a limpeza
    tk.Button(
        container,
        text="🚀 Executar Limpeza",
        command=lambda: executar_limpeza(master_frame, switches),
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
    ).grid(row=len(switches) + 1, column=0, pady=20)

def executar_limpeza(master_frame, switches):
    """Executa as funções associadas aos switches ativados."""
    global relatorio_final, log_text
    relatorio_final = []

    if log_text:
        log_text.destroy()  # Remove o log anterior, se existir
        log_text = None

    for switch, funcao in switches:
        if switch.get():
            ok, msg = funcao()
            relatorio_final.append(msg)

    mostrar_relatorio(master_frame)
