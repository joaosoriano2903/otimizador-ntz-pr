import tkinter as tk
import subprocess
import os
import sys
import psutil
import ctypes
from funcoes import sistema
from gui.layout_padrao import criar_layout_padrao  # Importa o layout padrão
from gui.rede_sistema import ModernSwitch 

spinner_label = None
spinner_running = False
spinner_index = 0
spinner_texts = ["👷 Trabalhando...", "👷 Trabalhando..", "👷 Trabalhando...", "👷 Trabalhando...."]

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
    """Exibe o relatório de limpeza na interface."""
    global log_text
    if (log_text):
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
        resultado = subprocess.run(
            comando,
            shell=True,
            check=True,
            text=True,
            capture_output=True,
            encoding="utf-8",  # Força o uso de UTF-8
            errors="ignore",  # Ignora caracteres inválidos
            timeout=60  # Define um timeout de 60 segundos
        )
        # Verifica se stdout é None e retorna uma string vazia se for o caso
        saida = resultado.stdout.strip() if resultado.stdout else ""
        return True, saida
    except subprocess.TimeoutExpired:
        return False, "❌ O comando excedeu o tempo limite de execução."
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
    """Limpa o cache do Windows Update."""
    comandos = [
        r'net start bits',  # Inicia o serviço BITS, se não estiver ativo
        r'net start wuauserv',  # Inicia o serviço Windows Update, se não estiver ativo
        r'net stop wuauserv',  # Para o serviço Windows Update
        r'net stop bits',  # Para o serviço BITS
        r'rd /s /q C:\Windows\SoftwareDistribution',  # Remove o cache do Windows Update
        r'net start wuauserv',  # Reinicia o serviço Windows Update
        r'net start bits'  # Reinicia o serviço BITS
    ]
    mensagens = []
    for comando in comandos:
        sucesso, mensagem = executar_comando(comando)
        if sucesso:
            mensagens.append(f"✅ Comando executado: {comando}")
        else:
            mensagens.append(f"❌ Erro ao executar comando: {mensagem}")
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
    """Verifica se uma chave do registro existe e tenta removê-la."""
    comando_verificar = f'powershell "Test-Path -Path \\"{registro}\\""'
    sucesso, mensagem = executar_comando(comando_verificar)
    if sucesso and mensagem.strip().lower() == "true":
        comando_remover = f'powershell "Remove-Item -Path \\"{registro}\\" -Recurse -ErrorAction SilentlyContinue"'
        sucesso_remover, mensagem_remover = executar_comando(comando_remover)
        if not sucesso_remover:
            if "UnauthorizedAccessException" in mensagem_remover:
                return False, f"❌ Permissão negada ao tentar remover a chave {registro}. Execute o programa como administrador."
            elif "ArgumentException" in mensagem_remover:
                return True, f"🔍 A chave {registro} não existe. Nenhuma ação necessária."
            return False, f"❌ Erro ao remover a chave {registro}: {mensagem_remover}"
        return True, f"✅ Chave {registro} removida com sucesso."
    return True, f"🔍 Chave {registro} não encontrada. Nenhuma ação necessária."

def limpar_chaves_registro():
    """Remove chaves específicas do registro relacionadas a mitigação de segurança."""
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

def abrir_limpeza(master_frame):
    """Interface principal para limpeza do sistema."""
    switches = []

    def criar_switches(container):
        """Cria os switches para limpeza do sistema."""
        lista = [
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
        switches.extend(lista)
        return [switch for switch, _ in lista]

    criar_layout_padrao(
        master_frame,
        titulo="🧹 Limpeza do Sistema",
        switches=criar_switches,
        botao_texto="🚀 Executar Limpeza",
        botao_comando=lambda: executar_limpeza(master_frame, switches)
    )

def verificar_administrador():
    """Verifica se o programa está sendo executado como administrador."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == "__main__":
    if not verificar_administrador():
        print("Este programa precisa ser executado como administrador.")
        input("Pressione Enter para sair...")
        exit(1)

