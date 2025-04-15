import tkinter as tk
from PIL import ImageTk, Image
from gui import otimizacao_sistema, limpeza_sistema, info_sistema, rede_sistema


import os

def iniciar_interface():
    root = tk.Tk()
    root.title("🛠️ NTZ Pro - Otimizador")
    root.geometry("800x500")
    root.configure(bg="#f0f0f0")

    sidebar = tk.Frame(root, bg="#d9d9d9", width=180)
    sidebar.pack(side="left", fill="y")

    main_frame = tk.Frame(root, bg="#f8f8f8")
    main_frame.pack(side="right", expand=True, fill="both")

    # Logo NTZ
    logo_path = os.path.join(os.path.dirname(__file__), "../assets/ntz_icon.ico")
    if os.path.exists(logo_path):
        logo_img = ImageTk.PhotoImage(Image.open(logo_path).resize((120, 120)))
        logo_label = tk.Label(sidebar, image=logo_img, bg="#d9d9d9")
        logo_label.image = logo_img
        logo_label.pack(pady=10)

    botoes = [
        ("🧰 Otimização de Sistema", lambda: otimizacao_sistema.abrir_otimizacao_sistema(main_frame)),
        ("🧹 Limpeza", lambda: limpeza_sistema.abrir_limpeza(main_frame)),
        ("🌐 Rede", lambda: rede_sistema.abrir_rede(main_frame)),
        ("🖥️ Info", lambda: info_sistema.abrir_info(main_frame)),
        ("❌ Sair", root.quit)
    ]

    for texto, comando in botoes:
        tk.Button(sidebar, text=texto, command=comando, width=22, bg="#ececec", relief="flat").pack(pady=5, padx=10)

    tk.Label(main_frame, text="Bem-vindo ao NTZ Pro", font=("Helvetica", 16, "bold"), bg="#f8f8f8").pack(pady=60)

    root.mainloop()