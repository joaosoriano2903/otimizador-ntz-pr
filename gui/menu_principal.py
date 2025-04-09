import tkinter as tk
from tkinter import messagebox
from gui import otimizacao_sistema, limpeza_sistema

def otimizar_rede():
    messagebox.showinfo("Rede", "Função real em breve: otimização de rede.")

def info_sistema():
    messagebox.showinfo("Sistema", "Função real em breve: coleta de informações do sistema.")

def sair():
    root.destroy()

def iniciar_interface():
    global root
    root = tk.Tk()
    root.title("🛠️ NTZ Pro - Otimizador")
    root.geometry("400x420")
    root.configure(bg="#f0f0f0")

    # Título
    titulo = tk.Label(root, text="🛠️ NTZ PRO - Otimizador", font=("Helvetica", 16, "bold"), bg="#f0f0f0", fg="#333")
    titulo.pack(pady=20)

    # Botões do menu principal
    botoes = [
        ("🧰 Otimização de Sistema", lambda: otimizacao_sistema.abrir_otimizacao_sistema(root)),
        ("🧹 Limpeza", lambda: limpeza_sistema.abrir_limpeza(main_frame)),
        ("🌐 Otimizar Rede", otimizar_rede),
        ("🖥️ Info do Sistema", info_sistema),
        ("❌ Sair", sair)
    ] 

    for texto, comando in botoes:
        tk.Button(root, text=texto, width=30, command=comando).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    iniciar_interface()