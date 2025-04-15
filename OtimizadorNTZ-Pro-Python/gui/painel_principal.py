import tkinter as tk
from gui import otimizacao_sistema, limpeza_sistema, info_sistema, rede_sistema

# Inicialização da janela principal
def iniciar_interface():
    root = tk.Tk()
    root.title("🛠️ NTZ Pro - Otimizador")
    root.geometry("800x600")
    root.configure(bg="#f0f0f0")

    # Frame superior com título
    header = tk.Frame(root, bg="#4CAF50", height=50)
    header.pack(fill="x", side="top")
    tk.Label(header, text="NTZ Pro - Otimizador", font=("Helvetica", 16, "bold"), bg="#4CAF50", fg="white").pack(pady=10)

    # Frame lateral de navegação
    sidebar = tk.Frame(root, bg="#d9d9d9", width=200)
    sidebar.pack(side="left", fill="y")

    # Frame principal onde as telas aparecem
    main_frame = tk.Frame(root, bg="#f8f8f8", relief="groove", bd=2)
    main_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

    # Botões do menu lateral
    botoes = [
        ("🧰 Otimização de Sistema", lambda: otimizacao_sistema.abrir_otimizacao_sistema(main_frame)),
        ("🧹 Limpeza", lambda: limpeza_sistema.abrir_limpeza(main_frame)),
        ("🌐 Rede", lambda: rede_sistema.abrir_rede(main_frame)),
        ("🖥️ Informações do Sistema", lambda: info_sistema.abrir_info(main_frame)),
        ("⚙️ Configurações", lambda: abrir_configuracoes(main_frame)),
        ("❌ Sair", root.quit)
    ]

    for texto, comando in botoes:
        tk.Button(
            sidebar,
            text=texto,
            command=comando,
            width=22,
            bg="#ececec",
            fg="#333",
            activebackground="#b0c4de",
            activeforeground="#000",
            relief="flat",
            font=("Segoe UI", 10, "bold")
        ).pack(pady=5, padx=10)

    # Mostra a tela inicial
    mostrar_tela_inicial(main_frame)

    root.mainloop()

# Tela inicial
def mostrar_tela_inicial(frame):
    limpar_tela(frame)
    tk.Label(frame, text="Bem-vindo ao NTZ Pro", font=("Helvetica", 18, "bold"), bg="#f8f8f8").pack(pady=40)
    tk.Label(frame, text="Selecione uma opção no menu lateral para começar.", font=("Helvetica", 12), bg="#f8f8f8").pack(pady=10)

# Placeholder simples para outras seções
def limpar_tela(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# Tela de configurações
def abrir_configuracoes(frame):
    limpar_tela(frame)
    tk.Label(frame, text="Configurações", font=("Helvetica", 16, "bold"), bg="#f8f8f8").pack(pady=20)
    tk.Label(frame, text="Ajuste as configurações do NTZ Pro aqui.", font=("Helvetica", 12), bg="#f8f8f8").pack(pady=10)

    # Exemplo de configuração
    tk.Checkbutton(frame, text="Ativar notificações", bg="#f8f8f8", font=("Helvetica", 10)).pack(anchor="w", padx=20, pady=5)
    tk.Checkbutton(frame, text="Modo escuro", bg="#f8f8f8", font=("Helvetica", 10)).pack(anchor="w", padx=20, pady=5)
    tk.Button(frame, text="Salvar Configurações", bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold")).pack(pady=20)