import platform
import psutil
import shutil
import socket
import subprocess

def get_bios_info():
    try:
        result = subprocess.check_output([
            "powershell",
            "-Command",
            "Get-CimInstance -ClassName Win32_BIOS | Select-Object -ExpandProperty SMBIOSBIOSVersion"
        ], encoding="utf-8")
        return result.strip()
    except:
        return "Não disponível"

def get_battery_status():
    try:
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            charging = "🔌 Carregando" if battery.power_plugged else "🔋 Bateria"
            return f"{charging} - {percent:.0f}%"
        else:
            return "Dispositivo sem bateria"
    except:
        return "Não disponível"

def coletar_info_sistema():
    info = []
    try:
        info.append("🔧 NTZ Pro - Informações do Sistema")
        info.append("-" * 40)
        info.append(f"🖥️ Hostname: {socket.gethostname()}")
        info.append(f"💽 Sistema: {platform.system()} {platform.release()} {platform.version()}")
        info.append(f"📦 Arquitetura: {platform.machine()}")
        info.append(f"🐍 Python: {platform.python_version()}")
        info.append(f"🧠 RAM Total: {round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB")

        disco = shutil.disk_usage("/")
        info.append(f"💾 Disco: Total: {disco.total // (1024**3)} GB | Livre: {disco.free // (1024**3)} GB")

        cpu_freq = psutil.cpu_freq()
        if cpu_freq:
            info.append(f"⚙️ CPU: {platform.processor()} | {psutil.cpu_count(logical=True)} núcleos")
            info.append(f"📈 Frequência atual: {int(cpu_freq.current)} MHz")

        bios = get_bios_info()
        info.append(f"🧬 BIOS: {bios}")

        bateria = get_battery_status()
        info.append(f"🔋 Bateria: {bateria}")

    except Exception as e:
        info.append(f"Erro ao coletar informações: {e}")

    return "\n".join(info)