import tkinter as tk
from funcoes import rede

def abrir_rede(master_frame):
    for widget in master_frame.winfo_children():
        widget.destroy()

    class Switch(tk.Frame):
        def __init__(self, master, text, func):
            super().__init__(master, bg="#f8f8f8")
            self.state = False
            self.func = func
            self.btn = tk.Button(self, text=f"{text}: ❌ OFF", bg="red", fg="white", width=35, command=self.toggle)
            self.btn.pack(pady=5)

        def toggle(self):
            self.state = not self.state
            if self.state:
                self.btn.config(text=self.btn.cget("text").replace("❌ OFF", "✅ ON"), bg="green")
            else:
                self.btn.config(text=self.btn.cget("text").replace("✅ ON", "❌ OFF"), bg="red")

        def get(self):
            return self.state

        def execute(self):
            if self.state and self.func:
                return self.func()
            return None, None

    def aplicar_rede():
        log_text.delete("1.0", tk.END)
        for switch in switches:
            ok, msg = switch.execute()
            if msg:
                cor = "✅" if ok else "❌"
                log_text.insert(tk.END, f"> {cor} {msg}\n")

    tk.Label(master_frame, text="🌐 Otimização de Rede", font=("Helvetica", 14, "bold"), bg="#f8f8f8").pack(pady=15)

    switches = []

    s1 = Switch(master_frame, "Alterar DNS para Cloudflare", rede.otimizar_dns)
    s1.pack()
    switches.append(s1)

    s2 = Switch(master_frame, "Ajustar Parâmetros TCP", rede.ajustar_tcp)
    s2.pack()
    switches.append(s2)

    s3 = Switch(master_frame, "Verificar Firewall", rede.verificar_firewall)
    s3.pack()
    switches.append(s3)

    s4 = Switch(master_frame, "Auto Negociação (Ethernet)", lambda: rede.auto_negociacao("Ethernet"))
    s4.pack()
    switches.append(s4)

    s5 = Switch(master_frame, "Otimizar Wi-Fi (MTU, autoconfig)", lambda: rede.otimizar_wifi("Wi-Fi"))
    s5.pack()
    switches.append(s5)

    tk.Button(master_frame, text="Aplicar Otimizações", bg="#4CAF50", fg="white", command=aplicar_rede).pack(pady=15)

    global log_text
    log_text = tk.Text(master_frame, height=10, width=70, bg="black", fg="lime", insertbackground="white")
    log_text.pack(pady=5)