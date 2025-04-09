import os
import shutil
import glob

def limpar_temp():
    try:
        temp_dir = os.environ.get('TEMP', '')
        if not temp_dir or not os.path.exists(temp_dir):
            return False, "Pasta TEMP não encontrada."

        arquivos = glob.glob(os.path.join(temp_dir, "*"))
        for arquivo in arquivos:
            try:
                if os.path.isfile(arquivo) or os.path.islink(arquivo):
                    os.unlink(arquivo)
                elif os.path.isdir(arquivo):
                    shutil.rmtree(arquivo)
            except Exception:
                pass
        return True, "Arquivos temporários excluídos com sucesso."
    except Exception as e:
        return False, f"Erro ao limpar TEMP: {e}"

def limpar_logs_tmp(diretorio='C:/'):
    encontrados = 0
    try:
        for raiz, _, arquivos in os.walk(diretorio):
            for nome in arquivos:
                if nome.endswith(".log") or nome.endswith(".tmp"):
                    caminho = os.path.join(raiz, nome)
                    try:
                        os.remove(caminho)
                        encontrados += 1
                    except Exception:
                        pass
        return True, f"{encontrados} arquivos .log/.tmp removidos."
    except Exception as e:
        return False, f"Erro ao limpar logs/tmp: {e}"