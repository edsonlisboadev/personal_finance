# main.py - inicio do programa (junta todas as partes)
import bank
import ui


def main():
    # carrega os usuarios salvos (ou cria os iniciais na primeira vez)
    users = bank.carregar_usuarios()

    print("Bem-vindo ao Internet Banking!")
    print("Digite 1 para acessar ou 2 para encerrar.")
    escolha = input("Opcao: ")

    if escolha == "2":
        print("Programa encerrado.")
        return
    if escolha != "1":
        print("Opcao invalida.")
        return

    # tela de login
    usuario = ui.tela_login(users)
    if usuario is None:
        return

    # decide qual menu mostrar dependendo do tipo do usuario
    if usuario["type"] == "admin":
        ui.menu_admin(users, usuario)
    else:
        ui.menu_usuario(users, usuario)

    print("Ate logo!")


if __name__ == "__main__":
    main()
