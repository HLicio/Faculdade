from interface_cli import rodar_jogo
from interface_gui import RPGApp


def main():
    print("=== RPG - Aventura ===")
    print("1 - Jogar na versão CLI")
    print("2 - Jogar na versão GUI")

    while True:
        escolha = input("Escolha uma versão (CLI/GUI): ").strip().lower()

        if escolha in ("1", "cli"):
            rodar_jogo()
            return

        if escolha in ("2", "gui"):
            app = RPGApp()
            app.mainloop()
            return

        print("Opção inválida. Digite CLI ou GUI.")


if __name__ == "__main__":
    main()
