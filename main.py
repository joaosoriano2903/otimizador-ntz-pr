from gui import menu_principal

if __name__ == "__main__":
    try:
        print("Iniciando a interface do Otimizador NTZ...")
        menu_principal.iniciar_interface()
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
    finally:
        print("Encerrando o programa. Até logo!")