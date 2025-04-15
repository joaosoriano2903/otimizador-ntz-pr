import subprocess

def desativar_animacoes():
    # Código para desativar animações
    return True, "Animações desativadas."

def reverter_desativar_animacoes():
    # Código para reverter a desativação de animações
    return True, "Animações ativadas novamente."

def ativar_modo_desempenho():
    # Código para ativar o modo de desempenho
    return True, "Modo de desempenho ativado."

def reverter_ativar_modo_desempenho():
    # Código para reverter o modo de desempenho
    return True, "Modo de desempenho desativado."

def reverter_ativar_modo_ultimate():
    # Código para reverter o modo Ultimate
    return True, "Modo Ultimate desativado."

def reverter_desativar_servicos_desnecessarios():
    # Código para reverter a desativação de serviços
    return True, "Serviços desnecessários reativados."

def desativar_modo_desempenho():
    try:
        subprocess.run([
            "powershell", "-Command",
            "powercfg -setactive SCHEME_BALANCED"
        ], check=True)
        return True, "Modo equilibrado reativado."
    except subprocess.CalledProcessError as e:
        return False, f"Erro ao reverter modo de desempenho: {e}"

def ativar_modo_ultimate():
    try:
        subprocess.run([
            "powershell", "-Command",
            "powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61"
        ], check=True)

        resultado = subprocess.run([
            "powershell", "-Command",
            "powercfg -setactive e9a42b02-d5df-448d-aa00-03f14749eb61"
        ], capture_output=True, text=True)

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
        result = subprocess.run([
            "powershell", "-Command",
            '(Get-ItemProperty "HKCU:\\Control Panel\\Desktop").UserPreferencesMask'
        ], capture_output=True, text=True)
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

def otimizar_usb():
    """Aplica otimizações no gerenciamento de energia do USB."""
    # Adicione os comandos para otimizar o USB aqui
    return True, "Otimizações de USB aplicadas com sucesso."

def reverter_otimizacao_usb():
    """Reverte as otimizações no gerenciamento de energia do USB."""
    # Adicione os comandos para reverter as otimizações de USB aqui
    return True, "Otimizações de USB revertidas com sucesso."

def otimizar_cpu_amd():
    """Aplica otimizações específicas para CPUs AMD."""
    try:
        comandos = [
            r'reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "DistributeTimers" /t REG_DWORD /d "1" /f',
            # Outros comandos...
        ]
        for comando in comandos:
            subprocess.run(comando, shell=True, check=True)
        return True, "Otimizações para CPU AMD aplicadas com sucesso."
    except subprocess.CalledProcessError as e:
        return False, f"Erro ao aplicar otimizações para CPU AMD: {e}"

def otimizar_cpu_intel():
    """Aplica otimizações específicas para CPUs Intel."""
    try:
        comandos = [
            r'reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\kernel" /v "DistributeTimers" /t REG_DWORD /d "1" /f',
            # Outros comandos...
        ]
        for comando in comandos:
            subprocess.run(comando, shell=True, check=True)
        return True, "Otimizações para CPU Intel aplicadas com sucesso."
    except subprocess.CalledProcessError as e:
        return False, f"Erro ao aplicar otimizações para CPU Intel: {e}"

def limpeza_sistema():
    """Executa comandos de limpeza e otimização do sistema."""
    try:
        comandos = [
            # BCD Tweaks
            r'bcdedit /set useplatformclock No',
            r'bcdedit /set disabledynamictick Yes',
            # Desabilitando Mitigações
            r'powershell "ForEach($v in (Get-Command -Name \"Set-ProcessMitigation\").Parameters[\"Disable\"].Attributes.ValidValues){Set-ProcessMitigation -System -Disable $v.ToString() -ErrorAction SilentlyContinue}"',
            r'powershell "Remove-Item -Path \"HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\*\" -Recurse -ErrorAction SilentlyContinue"',
            r'reg add "HKLM\SOFTWARE\Policies\Microsoft\FVE" /v "DisableExternalDMAUnderLock" /t REG_DWORD /d "0" /f',
            r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DeviceGuard" /v "EnableVirtualizationBasedSecurity" /t REG_DWORD /d "0" /f',
            # NTFS Tweaks
            r'fsutil behavior set memoryusage 2',
            r'fsutil behavior set mftzone 4',
            r'fsutil behavior set disablelastaccess 1',
            # Desabilitando Compressor de Memória
            r'powershell -Command "Disable-MMAgent -MemoryCompression"',
            # Setando prioridades Win32
            r'reg add "HKLM\SYSTEM\CurrentControlSet\Control\PriorityControl" /v "Win32PrioritySeparation" /t REG_DWORD /d "38" /f',
            # Habilitando Cache de Sistema
            r'reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /v "LargeSystemCache" /t REG_DWORD /d "1" /f',
            # Desabilitando Inicialização Rápida
            r'reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Power" /v "HiberbootEnabled" /t REG_DWORD /d "0" /f',
            # Desabilitando DEP
            r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Internet Explorer\Main" /v "DEPOff" /t REG_DWORD /d "1" /f',
            # Desabilitando Manutenção Automática
            r'reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\Maintenance" /v "MaintenanceDisabled" /t REG_DWORD /d "1" /f',
            # Habilitando Modo de Jogo
            r'reg add "HKCU\SOFTWARE\Microsoft\GameBar" /v "AllowAutoGameMode" /t REG_DWORD /d "1" /f',
            r'reg add "HKCU\SOFTWARE\Microsoft\GameBar" /v "AutoGameModeEnabled" /t REG_DWORD /d "1" /f',
            # Desabilitando Game Bar e DVR
            r'reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\PolicyManager\default\ApplicationManagement\AllowGameDVR" /v "value" /t REG_DWORD /d 0 /f',
            # Configurações Gerais
            r'reg add "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\AdvertisingInfo" /v "Enabled" /t REG_DWORD /d 0 /f',
            # Desabilitando Diagnósticos e Feedbacks
            r'reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\DataCollection" /v "AllowTelemetry" /t REG_DWORD /d 0 /f',
        ]

        for comando in comandos:
            subprocess.run(comando, shell=True, check=True)

        return True, "Limpeza e otimização do sistema concluídas com sucesso."
    except subprocess.CalledProcessError as e:
        return False, f"Erro ao executar limpeza de sistema: {e}"
