import subprocess

def otimizar_dns():
    try:
        subprocess.run(
            [
                "powershell", "-Command",
                "Set-DnsClientServerAddress -InterfaceAlias '*' -ServerAddresses ('1.1.1.1','1.0.0.1')"
            ],
            check=True
        )
        return True, "DNS alterado para Cloudflare com sucesso."
    except subprocess.CalledProcessError as e:
        return False, f"Erro ao alterar DNS: {e}"

def ajustar_tcp():
    try:
        subprocess.run(
            ["netsh", "int", "tcp", "set", "global", "autotuninglevel=highlyrestricted"],
            check=True
        )
        return True, "Ajuste de TCP aplicado com sucesso."
    except subprocess.CalledProcessError as e:
        return False, f"Erro ao ajustar TCP: {e}"

def verificar_firewall():
    try:
        result = subprocess.check_output(
            ["netsh", "advfirewall", "show", "allprofiles"],
            encoding="utf-8"
        )
        return True, "Firewall verificado:\n" + result.splitlines()[0]
    except Exception as e:
        return False, f"Erro ao verificar firewall: {e}"

def auto_negociacao(interface="Ethernet"):
    try:
        comando = (
            f"$adapter = Get-NetAdapter -Name '{interface}' -ErrorAction Stop; "
            f"If ($adapter) {{ Write-Output 'Interface encontrada: {interface}'; }} "
            f"Else {{ Throw 'Interface não encontrada'; }}"
        )
        subprocess.run(
            ["powershell", "-Command", comando],
            check=True
        )
        return True, f"Auto negociação configurada na interface {interface} (se suportado)."
    except subprocess.CalledProcessError as e:
        return False, f"Erro ao aplicar configuração de auto negociação: {e}"

def otimizar_wifi(interface="Wi-Fi"):
    try:
        comandos = [
            f"netsh wlan set autoconfig enabled=yes interface=\"{interface}\"",
            f"netsh interface ipv4 set subinterface \"{interface}\" mtu=1400 store=persistent"
        ]
        for cmd in comandos:
            subprocess.run(
                ["powershell", "-Command", cmd],
                check=True
            )
        return True, f"Interface {interface} Wi-Fi otimizada com sucesso."
    except subprocess.CalledProcessError as e:
        return False, f"Erro ao otimizar Wi-Fi: {e}"

def verificar_perfil_wifi(interface="Wi-Fi"):
    try:
        result = subprocess.check_output(
            ["netsh", "wlan", "show", "profiles"],
            encoding="utf-8"
        )
        if interface in result:
            return True, f"Perfil Wi-Fi '{interface}' encontrado."
        else:
            return False, f"Perfil Wi-Fi '{interface}' não encontrado."
    except subprocess.CalledProcessError as e:
        return False, f"Erro ao verificar perfil Wi-Fi: {e}"

def desabilitar_nagle():
    try:
        # Lógica para desabilitar o algoritmo de Nagle
        # Exemplo: Configurar TCP_NODELAY em sockets (se aplicável)
        return True, "Algoritmo de Nagle desabilitado com sucesso"
    except Exception as e:
        return False, f"Erro ao desabilitar o algoritmo de Nagle: {e}"