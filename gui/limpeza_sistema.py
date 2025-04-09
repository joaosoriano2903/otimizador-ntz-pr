def abrir_limpeza(master_frame):
    for widget in master_frame.winfo_children():
        widget.destroy()
    ...