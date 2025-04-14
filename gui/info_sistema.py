import tkinter as tk
import platform
import socket
import getpass
import psutil

try:
    import wmi
except ImportError:
    wmi = None

monitorando = False


def abrir_info(master_frame):
    global monitorando
    monitorando = False

    for widget in master_frame.winfo_children():
        widget.destroy()

    tk.Label(master_frame, text="🖥️ Informações do Sistema", font=("Helvetica", 16, "bold"), bg="#f8f8f8").pack(pady=15)

    info_text = tk.Text(master_frame, height=20, width=80, bg="black", fg="lime", insertbackground="white", wrap="word")
    info_text.pack(pady=10)

    infos = coletar_informacoes_sistema()
    for info in infos:
        info_text.insert(tk.END, f"> {info}\n")

    info_text.config(state="disabled")

    botoes_frame = tk.Frame(master_frame, bg="#f8f8f8")
    botoes_frame.pack(pady=10)

    tk.Button(
        botoes_frame,
        text="Copiar Informações",
        command=lambda: copiar_para_area_transferencia(master_frame, infos),
        bg="#4CAF50",
        fg="white",
        relief="flat",
        font=("Helvetica", 10, "bold"),
        width=20
    ).grid(row=0, column=0, padx=5, pady=5)

    tk.Button(
        botoes_frame,
        text="Atualizar Informações",
        command=lambda: abrir_info(master_frame),
        bg="#2196F3",
        fg="white",
        relief="flat",
        font=("Helvetica", 10, "bold"),
        width=20
    ).grid(row=0, column=1, padx=5, pady=5)

    monitorar_sistema(master_frame)


def coletar_informacoes_sistema():
    battery = psutil.sensors_battery()
    battery_status = (
        f"Status da Bateria: {battery.percent}% {'(Carregando)' if battery.power_plugged else '(Descarregando)'}"
        if battery else "Bateria: Não disponível"
    )
    battery_time = (
        f"Tempo Restante: {battery.secsleft // 3600}h {battery.secsleft % 3600 // 60}m"
        if battery and battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Tempo Restante: Indeterminado"
    )
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
    ]
    return infos


def copiar_para_area_transferencia(master_frame, infos):
    master_frame.clipboard_clear()
    master_frame.clipboard_append("\n".join(infos))
    master_frame.update()
    tk.messagebox.showinfo("Copiado", "As informações foram copiadas para a área de transferência!")


def monitorar_sistema(master_frame):
    global monitorando
    monitorando = True

    cpu_label = tk.Label(master_frame, text="CPU: 0%", font=("Helvetica", 12), bg="#f8f8f8")
    cpu_label.pack(pady=5)
    ram_label = tk.Label(master_frame, text="RAM: 0%", font=("Helvetica", 12), bg="#f8f8f8")
    ram_label.pack(pady=5)

    def atualizar_monitoramento():
        while monitorando:
            try:
                cpu_label.config(text=f"CPU: {psutil.cpu_percent()}%")
                ram_label.config(text=f"RAM: {psutil.virtual_memory().percent}%")
                master_frame.update_idletasks()
            except tk.TclError:
                break

    import threading
    threading.Thread(target=atualizar_monitoramento, daemon=True).start()
