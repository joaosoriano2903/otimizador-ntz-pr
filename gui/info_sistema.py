import tkinter as tk
import platform
import socket
import getpass
import psutil  # Biblioteca para informações de hardware e sistema

try:
    import wmi  # Biblioteca para informações detalhadas no Windows
except ImportError:
    wmi = None  # Caso não esteja no Windows ou a biblioteca não esteja instalada


def abrir_info(master_frame):
    # Limpa os widgets existentes no frame
    for widget in master_frame.winfo_children():
        widget.destroy()

    # Título
    tk.Label(master_frame, text="🖥️ Informações do Sistema", font=("Helvetica", 14, "bold"), bg="#f8f8f8").pack(pady=15)

    # Caixa de texto para exibir as informações
    info_text = tk.Text(master_frame, height=25, width=80, bg="black", fg="lime", insertbackground="white", wrap="word")
    info_text.pack(pady=10)

    # Coleta as informações do sistema
    battery = psutil.sensors_battery()
    battery_status = (
        f"Status da Bateria: {battery.percent}% {'(Carregando)' if battery.power_plugged else '(Descarregando)'}"
        if battery else "Bateria: Não disponível"
    )
    battery_time = (
        f"Tempo Restante: {battery.secsleft // 3600}h {battery.secsleft % 3600 // 60}m"
        if battery and battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Tempo Restante: Indeterminado"
    )

    # Informações detalhadas da bateria no Windows (usando WMI)
    if wmi:
        try:
            c = wmi.WMI(namespace="root\\WMI")
            full_capacity = next(iter(c.BatteryFullChargedCapacity()), None)
            status = next(iter(c.BatteryStatus()), None)
            if full_capacity and status:
                battery_cycles = status.CycleCount if hasattr(status, "CycleCount") else "Não disponível"
                battery_capacity = full_capacity.FullChargedCapacity
                battery_remaining = status.RemainingCapacity
                battery_details = [
                    f"Ciclos de Carga: {battery_cycles}",
                    f"Capacidade Total (mWh): {battery_capacity}",
                    f"Capacidade Restante (mWh): {battery_remaining}",
                ]
            else:
                battery_details = ["Informações detalhadas da bateria não disponíveis."]
        except Exception as e:
            battery_details = [f"Erro ao obter informações detalhadas da bateria: {e}"]
    else:
        battery_details = ["Informações detalhadas da bateria não disponíveis (WMI não instalado ou não no Windows)."]

    # Informações gerais do sistema
    infos = [
        f"Sistema Operacional: {platform.system()} {platform.release()}",
        f"Nome do Computador: {socket.gethostname()}",
        f"Usuário Atual: {getpass.getuser()}",
        f"Versão do Python: {platform.python_version()}",
        f"Arquitetura: {platform.machine()}",
        f"Processador: {platform.processor()}",
        f"Frequência do CPU: {psutil.cpu_freq().current:.2f} MHz",
        f"RAM Total: {round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB",
        f"Disco Total: {round(psutil.disk_usage('/').total / (1024 ** 3), 2)} GB",
        f"Disco Livre: {round(psutil.disk_usage('/').free / (1024 ** 3), 2)} GB",
        battery_status,
        battery_time,
    ] + battery_details

    # Insere as informações na caixa de texto
    for info in infos:
        info_text.insert(tk.END, f"> {info}\n")

    # Desabilita a edição da caixa de texto
    info_text.config(state="disabled")

    # Função para copiar as informações para a área de transferência
    def copiar_para_area_transferencia():
        master_frame.clipboard_clear()
        master_frame.clipboard_append("\n".join(infos))
        master_frame.update()  # Atualiza o clipboard
        tk.messagebox.showinfo("Copiado", "As informações foram copiadas para a área de transferência!")

    # Botão para copiar as informações
    tk.Button(master_frame, text="Copiar Informações", command=copiar_para_area_transferencia, bg="#4CAF50", fg="white", relief="flat", width=20).pack(pady=10)