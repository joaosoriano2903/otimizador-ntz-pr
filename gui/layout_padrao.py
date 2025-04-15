import tkinter as tk

def criar_layout_padrao(master_frame, titulo, switches, botao_texto, botao_comando):
    """Cria um layout padrão para as interfaces."""
    for widget in master_frame.winfo_children():
        widget.destroy()

    container = tk.Frame(master_frame, bg="#f8f8f8")
    container.place(relx=0.5, rely=0.3, anchor="center")

    tk.Label(container, text=titulo, font=("Helvetica", 14, "bold"), bg="#f8f8f8", fg="black").grid(
        row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew"
    )

    # switches agora é uma função que recebe o container
    switches_widgets = switches(container)

    colunas = 3
    for i, switch in enumerate(switches_widgets):
        switch.grid(row=(i // colunas) + 1, column=i % colunas, padx=10, pady=5, sticky="nsew")

    tk.Button(
        container,
        text=botao_texto,
        command=botao_comando,
        bg="#000000",
        fg="#00ff00",
        font=("Helvetica", 14, "bold"),
        relief="flat",
        width=30,
        height=2,
        bd=0,
        highlightthickness=0,
        activebackground="#00ff00",
        activeforeground="#000000",
        cursor="hand2"
    ).grid(row=(len(switches_widgets) // colunas) + 2, column=0, columnspan=colunas, pady=20, sticky="nsew")
