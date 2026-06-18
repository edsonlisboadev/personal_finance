user_selection = input("\n Digite 1 para acessar e 2 para encerrar: \n ")
retry = 0
diferenca = 0
logged_user = None

users = [
    {"type": "admin", "user_email": "admin@admin", "user_password": 1234, "saldo": 10000, "limite": 10000},
    {"type": "user", "user_email": "chorenafeature@user", "user_password": 6767, "saldo": 6767, "limite": 86400},
    {"type": "user", "user_email": "lucasguloso@user", "user_password": 6969, "saldo": 2440, "limite": 30},
    {"type": "user", "user_email": "aninhafazcompleto@user", "user_password": 8888, "saldo": 250, "limite": 3600},
]


def print_menu():
    print("\n- UNIVILLE Internet Banking -")
    if logged_user["type"] == "admin":
        print("0. Gerenciar Usuários")
    print("1. Consultar Saldo")
    print("2. Realizar Saque")
    print("3. Realizar Depósito")
    print("4. Consultar Limite")
    print("5. Encerrar")

def invalid_code():
    print("Valor inválido, tente novamente.")

if user_selection == '2':
    print("Encerrado")
    exit()
elif user_selection != '1':
    invalid_code()
    exit()
else:
    while retry < 3:
        user_email = input("Digite o seu e-mail: ")
        try:
            user_password = int(input("Digite a sua senha: "))
        except ValueError:
            invalid_code()
            continue

        logged_user = None
        for user in users:
            if user["user_email"] == user_email and user["user_password"] == user_password:
                logged_user = user
                break

        if logged_user:
            match logged_user["type"]:
                case "admin":
                    print("Bem vindo adm!", user_email)
                case "user":
                    print("Bem vindo usuário!", user_email)
                case _:
                    invalid_code()
                    exit()
            break

        retry += 1
        print(f"Tudo errado, tenta denovo parceiro, você tem mais {3 - retry} tentativas.")

    if retry >= 3:
        print("Deu a tua cota")
        exit()

    type = logged_user['type']
    current_user = logged_user
    saldo = current_user['saldo']
    limite = current_user['limite']

    while True:
        try:
            print_menu()
            user_selection_menu = input("Escolha uma opção: \n")
        except ValueError:
            invalid_code()
            continue

        # ── Gerenciar usuários (admin) ──
        if user_selection_menu == "0":
            if type != "admin":
                invalid_code()
            else:
                for i, user in enumerate(users):
                    if user["type"] == "user":  # ← CORRIGIDO
                        print(f"{i}. {user['user_email']}")
                try:
                    select = int(input("Escolhe um: "))
                    current_user = users[select]
                    saldo = current_user['saldo']   # ← CORRIGIDO
                    limite = current_user['limite']  # ← CORRIGIDO
                    print(f"Gerenciando: {current_user['user_email']}")
                except (ValueError, IndexError):
                    invalid_code()

        # ── Consultar saldo ──
        elif user_selection_menu == '1':
            print(f"Saldo: R${saldo:.2f}")

        # ── Saque ──
        elif user_selection_menu == '2':
            while True:
                try:
                    saque = float(input("Digite o valor do saque: "))
                    break
                except ValueError:
                    invalid_code()

            if saque > saldo + limite:
                print(f"Saldo e limite insuficientes. Falta R${saque - (saldo + limite):.2f}")
            else:
                if saque > saldo:
                    diferenca = saque - saldo
                    limite -= diferenca
                    saldo = 0
                else:
                    saldo -= saque
                current_user['saldo'] = saldo
                current_user['limite'] = limite
                print(f"Saque realizado! Saldo atual: R${saldo:.2f}")

        # ── Depósito ──
        elif user_selection_menu == '3':
            while True:
                try:
                    deposito = float(input("Digite o valor do depósito: "))
                    break
                except ValueError:
                    invalid_code()

            if limite < 100:
                diferenca = 100 - limite
                if deposito >= diferenca:
                    limite = 100
                    saldo += deposito - diferenca
                    print(f"Limite restaurado! Saldo: R${saldo:.2f}")
                else:
                    limite += deposito
                    print(f"Limite atualizado: R${limite:.2f}")
            else:
                saldo += deposito
                print(f"Saldo atual: R${saldo:.2f}")

            current_user['saldo'] = saldo
            current_user['limite'] = limite
            print("Depósito realizado com sucesso")

        # ── Limite ──
        elif user_selection_menu == '4':
            print(f"Limite: R${limite:.2f}")

        # ── Encerrar ──
        elif user_selection_menu == '5':
            print("Encerrado")
            exit()

        else:
            invalid_code()