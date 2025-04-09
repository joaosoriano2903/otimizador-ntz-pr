import tkinter as tk
from tkinter import messagebox
from gui import otimizacao_sistema  # importa a GUI real

def limpar_temporarios():
    """Função para limpeza de arquivos temporários (placeholder)."""
    messagebox.showinfo("Limpeza", "Função real em breve: limpeza de arquivos temporários.")

def otimizar_rede():
    """Função para otimização de rede (placeholder)."""
    messagebox.showinfo("Rede", "Função real em breve: otimização de rede.")

def gerenciar_servicos():
    """Abre a interface de otimização de sistema."""
    otimizacao_sistema.abrir_otimizacao_sistema()

def info_sistema():
    """Exibe informações do sistema (placeholder)."""
    messagebox.showinfo("Sistema", "Função real em breve: coleta de informações do sistema.")

def sair():
    """Fecha a aplicação."""
    root.destroy()

def iniciar_interface():
    """Inicializa a interface principal do NTZ Pro."""
    global root
    root = tk.Tk()
    root.title("🛠️ NTZ Pro - Otimizador")
    root.geometry("400x420")
    root.configure(bg="#f0f0f0")

    # Título
    titulo = tk.Label(root, text="🛠️ NTZ PRO - Otimizador", font=("Helvetica", 16, "bold"), bg="#f0f0f0", fg="#333")
    titulo.pack(pady=20)

    # Botões com ações reais e futuras
    botoes = [
        ("🧹 Limpeza Temporária", limpar_temporarios),
        ("🌐 Otimizar Rede", otimizar_rede),
        ("🧰 Otimização de Sistema", gerenciar_servicos),
        ("🖥️ Info do Sistema", info_sistema),
        ("❌ Sair", sair)
    ]

    for texto, comando in botoes:
        tk.Button(root, text=texto, width=30, command=comando).pack(pady=5)

    # Inicia o loop principal da interface
    root.mainloop()

# Apenas executa a interface se o arquivo for executado diretamente
if __name__ == "__main__":
    iniciar_interface()
class Switch(tk.Frame):
    def __init__(self, master, text, command=None):
        super().__init__(master, bg="#f8f8f8")
        self.state = False
        self.command = command
        self.btn = tk.Button(self, text=f"{text}: ❌ OFF", bg="red", fg="white", width=25, command=self.toggle)
        self.btn.pack(pady=5)

    def toggle(self):
        self.state = not self.state
        if self.state:
            self.btn.config(text=self.btn.cget("text").replace("❌ OFF", "✅ ON"), bg="green")
        else:
            self.btn.config(text=self.btn.cget("text").replace("✅ ON", "❌ OFF"), bg="red")
        if self.command:
            self.command(self.state)

    def get(self):
        return self.state
