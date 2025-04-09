import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

PASTA_PROJETO = os.path.abspath(os.path.dirname(__file__))

class GitAutoCommitHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".py"):
            nome_arquivo = os.path.basename(event.src_path)
            print(f"🔄 Detectada modificação em: {nome_arquivo}")
            try:
                subprocess.run(["git", "add", "."], cwd=PASTA_PROJETO, check=True)
                subprocess.run(["git", "commit", "-m", f"📌 Auto: Alterado {nome_arquivo}"], cwd=PASTA_PROJETO, check=True)
                subprocess.run(["git", "push"], cwd=PASTA_PROJETO, check=True)
                print("✅ Alterações enviadas para o GitHub.")
            except subprocess.CalledProcessError as e:
                print(f"⚠️ Falha ao executar Git: {e}")

if __name__ == "__main__":
    print("📡 Monitorando alterações nos arquivos do NTZ Pro...")
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