import tkinter as tk
from gui import otimizacao_sistema, limpeza_sistema

def iniciar_interface():
    root = tk.Tk()
    root.title("🛠️ NTZ Pro - Otimizador")
    root.geometry("700x480")
    root.configure(bg="#f0f0f0")

    sidebar = tk.Frame(root, bg="#d9d9d9", width=200)
    sidebar.pack(side="left", fill="y")

    main_frame = tk.Frame(root, bg="#f8f8f8")
    main_frame.pack(side="right", expand=True, fill="both")

    # Botões do menu lateral
    botoes = [
        ("🧰 Otimização de Sistema", lambda: otimizacao_sistema.abrir_otimizacao_sistema(main_frame)),
        ("🧹 Limpeza", lambda: limpeza_sistema.abrir_limpeza(main_frame)),
        ("🌐 Rede", lambda: limpar_tela(main_frame, "Otimização de Rede")),
        ("🖥️ Info", lambda: limpar_tela(main_frame, "Informações do Sistema")),
        ("❌ Sair", root.quit)
    ]

    for texto, comando in botoes:
        tk.Button(sidebar, text=texto, command=comando, width=22, bg="#ececec", relief="flat").pack(pady=5, padx=10)

    # Tela inicial
    limpar_tela(main_frame, "Bem-vindo ao NTZ Pro")

    root.mainloop()

def limpar_tela(frame, titulo):
    for widget in frame.winfo_children():
        widget.destroy()
    tk.Label(frame, text=titulo, font=("Helvetica", 14, "bold"), bg="#f8f8f8").pack(pady=40)
    tk.Label(frame, text="Conteúdo em desenvolvimento...", bg="#f8f8f8").pack(pady=10)