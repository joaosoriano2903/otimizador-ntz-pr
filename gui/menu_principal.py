import tkinter as tk
from PIL import ImageTk, Image
from gui import otimizacao_sistema, limpeza_sistema, info_sistema, rede_sistema

def iniciar_interface():
    root = tk.Tk()
    root.title("NTZ Otimizador v1.1.0")
    root.geometry("800x600")
    root.configure(bg="#e8f0fe")

    # Topo com fundo preto e verde
    topo = tk.Frame(root, bg="#000000", height=120)
    topo.pack(fill="x", side="top")

    try:
        # Carregar e redimensionar a logo
        logo_img = Image.open("assets/ntz_icon.ico")
        logo_img = logo_img.resize((100, 100))  # Aumentar o tamanho da logo
        logo = ImageTk.PhotoImage(logo_img)
        tk.Label(topo, image=logo, bg="#000000").pack(pady=10)
        root.logo = logo  # Previne garbage collection
    except:
        tk.Label(
            topo,
            text="NTZ Otimizador",
            font=("Helvetica", 24, "bold"),
            bg="#000000",
            fg="#00ff00"
        ).pack(pady=10)

    # Container principal
    container = tk.Frame(root, bg="#e8f0fe")
    container.pack(fill="both", expand=True)

    # Menu lateral
    sidebar = tk.Frame(container, bg="#dbe4f0", width=180)
    sidebar.pack(side="left", fill="y", padx=5, pady=5)

    # Área principal
    main_frame = tk.Frame(container, bg="#ffffff", relief="groove", bd=2)
    main_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

    # Botões de navegação
    botoes = [
        ("🧰 Otimização", lambda: otimizacao_sistema.abrir_otimizacao_sistema(main_frame)),
        ("🧹 Limpeza", lambda: limpeza_sistema.abrir_limpeza(main_frame)),
        ("🌐 Rede", lambda: rede_sistema.abrir_rede(main_frame)),
        ("🖥️ Info Sistema", lambda: info_sistema.abrir_info(main_frame)),
        ("❌ Sair", root.destroy)
    ]

    for texto, comando in botoes:
        tk.Button(
            sidebar,
            text=texto,
            width=20,
            command=comando,
            bg="#cbd6e2",
            fg="#333",
            activebackground="#b0c4de",
            activeforeground="#000",
            relief="flat",
            font=("Segoe UI", 10, "bold")
        ).pack(pady=8)

    # Tela inicial
    abrir_menu_principal(main_frame)

    root.mainloop()

def abrir_menu_principal(main_frame):
    """Redefine o conteúdo do main_frame para exibir o menu principal."""
    for widget in main_frame.winfo_children():
        widget.destroy()

    tk.Label(
        main_frame,
        text="🚀 Bem-vindo à versão 1.1.0 do NTZ Otimizador",
        font=("Helvetica", 16),
        bg="#ffffff",
        fg="#333"
    ).pack(pady=60)