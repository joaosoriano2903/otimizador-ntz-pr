import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

PASTA_PROJETO = os.path.abspath(os.path.dirname(__file__))

class GitAutoCommitHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory or not event.src_path.endswith(".py"):
            return

        nome_arquivo = os.path.basename(event.src_path)
        print(f"🔄 Detectada modificação em: {nome_arquivo}")

        try:
            # Adiciona as alterações ao índice
            subprocess.run(["git", "add", "."], cwd=PASTA_PROJETO, check=True)

            # Verifica se há alterações para commit
            result = subprocess.run(["git", "status", "--porcelain"], cwd=PASTA_PROJETO, capture_output=True, text=True)
            if result.stdout.strip() == "":
                print("⏸️ Nenhuma alteração detectada para commit.")
                return

            # Realiza o commit
            subprocess.run(["git", "commit", "-m", f"📌 Auto: Alterado {nome_arquivo}"], cwd=PASTA_PROJETO, check=True)

            # Garante que está na branch 1.1.0
            subprocess.run(["git", "checkout", "1.1.0"], cwd=PASTA_PROJETO, check=True)

            # Atualiza a branch local com o repositório remoto
            subprocess.run(["git", "pull", "--rebase", "origin", "1.1.0"], cwd=PASTA_PROJETO, check=True)

            # Envia as alterações para o repositório remoto
            subprocess.run(["git", "push", "origin", "1.1.0"], cwd=PASTA_PROJETO, check=True)
            print("✅ Alterações enviadas para a branch '1.1.0' no GitHub.")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Falha ao executar Git: {e}")

if __name__ == "__main__":
    print("📡 Monitorando alterações nos arquivos do NTZ Pro com Git sincronizado...")
    event_handler = GitAutoCommitHandler()
    observer = Observer()
    observer.schedule(event_handler, path=PASTA_PROJETO, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()