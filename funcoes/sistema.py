import subprocess

def desativar_animacoes():
    try:
        subprocess.run(["powershell", "-Command", 'reg add "HKCU\\Control Panel\\Desktop" /v UserPreferencesMask /t REG_BINARY /d 9012038010000000 /f'], check=True)
        return True, "Animações visuais desativadas com sucesso."
    except subprocess.CalledProcessError as e:
        return False, f"Erro ao desativar animações: {e}"

def ativar_animacoes():
    try:
        subprocess.run(["powershell", "-Command", 'reg add "HKCU\\Control Panel\\Desktop" /v UserPreferencesMask /t REG_BINARY /d 9e1e038012000000 /f'], check=True)
        return True, "Animações visuais ativadas novamente."
    except subprocess.CalledProcessError as e:
        return False, f"Erro ao ativar animações: {e}"

def ativar_modo_desempenho():
    try:
        subprocess.run(["powershell", "-Command", "powercfg -setactive SCHEME_MIN"], check=True)
        return True, "Modo de alto desempenho ativado."
    except subprocess.CalledProcessError as e:
        return False, f"Erro ao ativar modo de desempenho: {e}"

def desativar_modo_desempenho():
    try:
        subprocess.run(["powershell", "-Command", "powercfg -setactive SCHEME_BALANCED"], check=True)
        return True, "Modo equilibrado reativado."
    except subprocess.CalledProcessError as e:
        return False, f"Erro ao reverter modo de desempenho: {e}"

def ativar_modo_ultimate():
    try:
        subprocess.run(["powershell", "-Command", "powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61"], check=True)
        resultado = subprocess.run(["powershell", "-Command", "powercfg -setactive e9a42b02-d5df-448d-aa00-03f14749eb61"], capture_output=True, text=True)
        if resultado.returncode != 0:
            return False, "⚠️ Ultimate Performance criado, mas não pôde ser ativado automaticamente."
        return True, "Modo de desempenho máximo (Ultimate) ativado."
    except subprocess.CalledProcessError as e:
        return False, f"Erro ao ativar Ultimate Performance: {e}"

def desativar_servicos_desnecessarios():
    comandos = [
        'Stop-Service -Name "DiagTrack" -Force',
        'Set-Service -Name "DiagTrack" -StartupType Disabled',
        'Stop-Service -Name "WSearch" -Force',
        'Set-Service -Name "WSearch" -StartupType Disabled'
    ]
    erros = []
    for cmd in comandos:
        try:
            subprocess.run(["powershell", "-Command", cmd], check=True)
        except subprocess.CalledProcessError as e:
            erros.append(f"Erro ao executar: {cmd} → {e}")
    if not erros:
        return True, "Serviços desnecessários desativados com sucesso."
    else:
        return False, "Alguns serviços não puderam ser desativados:\n" + "\n".join(erros)

def estado_animacoes():
    try:
        result = subprocess.run(["powershell", "-Command", '(Get-ItemProperty \"HKCU:\\Control Panel\\Desktop\").UserPreferencesMask'], capture_output=True, text=True)
        return "9e1e038012000000" in result.stdout.lower()
    except:
        return False

def modo_ultimate_ativo():
    try:
        result = subprocess.run(["powercfg", "/getactivescheme"], capture_output=True, text=True)
        return "e9a42b02-d5df-448d-aa00-03f14749eb61" in result.stdout.lower()
    except:
        return False

def modo_desempenho_ativo():
    try:
        result = subprocess.run(["powercfg", "/getactivescheme"], capture_output=True, text=True)
        return "SCHEME_MIN" in result.stdout or "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c" in result.stdout
    except:
        return False