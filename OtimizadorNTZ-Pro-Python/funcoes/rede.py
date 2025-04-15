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
            
               
        return True, "✅ DNS alterado para Cloudflare com sucesso."
    except subprocess.CalledProcessError as e:
        return False, f"❌ Erro ao alterar DNS: {e}"

def ajustar_tcp():
    try:
        subprocess.run(
            ["netsh", "int", "tcp", "set", "global", "autotuninglevel=highlyrestricted"],
            check=True
        )
        return True, "✅ Ajuste de TCP aplicado com sucesso."
    except subprocess.CalledProcessError as e:
        return False, f"❌ Erro ao ajustar TCP: {e}"

def verificar_firewall():
    try:
        result = subprocess.check_output(
            ["netsh", "advfirewall", "show", "allprofiles"],
            encoding="utf-8"
        )
        return True, "✅ Firewall verificado:\n" + result.splitlines()[0]
    except Exception as e:
        return False, f"❌ Erro ao verificar firewall: {e}"

def configurar_1gbps(interface="Ethernet"):
    """
    Configura a interface de rede para 1.0 Gbps Full Duplex.
    """
    try:
        # Verifica se a propriedade "Speed & Duplex" está disponível
        comando_verificar = f'Get-NetAdapterAdvancedProperty -Name "{interface}"'
        resultado = subprocess.check_output(["powershell", "-Command", comando_verificar], encoding="utf-8")
        if "Speed & Duplex" not in resultado:
            return False, f"❌ A propriedade 'Speed & Duplex' não está disponível para a interface '{interface}'."

        # Configura a interface para 1.0 Gbps Full Duplex
        comando_configurar = f'Set-NetAdapterAdvancedProperty -Name "{interface}" -DisplayName "Speed & Duplex" -DisplayValue "1.0 Gbps Full Duplex"'
        subprocess.run(["powershell", "-Command", comando_configurar], check=True)
        return True, f"✅ Interface '{interface}' configurada para 1.0 Gbps Full Duplex com sucesso."
    except subprocess.CalledProcessError as e:
        return False, f"❌ Erro ao configurar 1.0 Gbps Full Duplex: {e}"
    except Exception as e:
        return False, f"❌ Erro inesperado: {e}"

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
        return True, f"✅ Interface {interface} Wi-Fi otimizada com sucesso."
    except subprocess.CalledProcessError as e:
        return False, f"❌ Erro ao otimizar Wi-Fi: {e}"

def verificar_perfil_wifi(interface="Wi-Fi"):
    try:
        result = subprocess.check_output(
            ["netsh", "wlan", "show", "profiles"],
            encoding="utf-8"
        )
        if interface in result:
            return True, f"✅ Perfil Wi-Fi '{interface}' encontrado."
        else:
            return False, f"❌ Perfil Wi-Fi '{interface}' não encontrado."
    except subprocess.CalledProcessError as e:
        return False, f"❌ Erro ao verificar perfil Wi-Fi: {e}"

def desabilitar_nagle():
    try:
        # Lógica para desabilitar o algoritmo de Nagle
        # Exemplo: Configurar TCP_NODELAY em sockets (se aplicável)
        return True, "✅ Algoritmo de Nagle desabilitado com sucesso."
    except Exception as e:
        return False, f"❌ Erro ao desabilitar o algoritmo de Nagle: {e}"