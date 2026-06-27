# ui.py - parte visual (telas e menus) do programa
import auth
import bank
import finance


def tela_login(users):
    """Pede email e senha (3 tentativas). Retorna o usuario ou None."""
    print("\n===== UNIVILLE Internet Banking =====")
    tentativas = 0
    while tentativas < 3:
        email = input("Digite o seu e-mail: ")
        try:
            senha = int(input("Digite a sua senha: "))
        except ValueError:
            print("Senha invalida, tente de novo.")
            continue

        usuario = auth.authenticate(users, email, senha)
        if usuario:
            print(f"\nBem-vindo(a), {email}!")
            return usuario

        tentativas += 1
        restantes = 3 - tentativas
        print(f"E-mail ou senha incorretos. Voce ainda tem {restantes} tentativa(s).")

    print("Numero de tentativas esgotado.")
    return None


def pedir_valor(mensagem, minimo=0.01):
    """Pede um numero para o usuario, repetindo ate ele digitar algo valido."""
    while True:
        try:
            valor = float(input(mensagem))
            if valor < minimo:
                print(f"Digite um valor maior ou igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("Valor invalido, tente de novo.")


def escolher_categoria():
    """Mostra as categorias e devolve a que o usuario escolher."""
    print("\nCategorias:")
    for i, categoria in enumerate(finance.CATEGORIAS):
        print(f"{i + 1}. {categoria}")
    while True:
        try:
            escolha = int(input("Escolha a categoria: "))
            return finance.CATEGORIAS[escolha - 1]
        except (ValueError, IndexError):
            print("Categoria invalida, tente de novo.")


def mostrar_historico(email):
    """Lista todas as transacoes (entradas e saidas) de um usuario."""
    transacoes = finance.transacoes_do_usuario(email)
    if not transacoes:
        print("Nenhuma transacao encontrada.")
        return
    print("\n----- Historico de Transacoes -----")
    for t in transacoes:
        sinal = "+" if t["tipo"] == "entrada" else "-"
        print(f"{t['data']} | {t['tipo'].upper():7} | {t['categoria']:12} | {sinal}R${t['valor']:.2f}")
    print("-----------------------------------")


def mostrar_relatorio(email):
    """Imprime o relatorio do mes de um usuario."""
    rel = finance.relatorio_mes(email)
    print(f"\n----- Relatorio de {rel['mes']} -----")
    print(f"Total de entradas: R${rel['entradas']:.2f}")
    print(f"Total de saidas:   R${rel['saidas']:.2f}")
    print(f"Saldo do mes:      R${rel['saldo']:.2f}")
    if rel["por_categoria"]:
        print("\nGastos por categoria:")
        for categoria, valor in rel["por_categoria"].items():
            print(f"   - {categoria}: R${valor:.2f}")
    print("--------------------------------")


def menu_usuario(users, usuario):
    """Menu de um cliente comum. Ele pode mexer na propria conta
    (saque e deposito) e consultar as suas informacoes."""
    email = usuario["user_email"]
    while True:
        print("\n--------- MENU ---------")
        print("1. Consultar Saldo")
        print("2. Consultar Limite")
        print("3. Realizar Saque")
        print("4. Realizar Deposito")
        print("5. Ver Historico de Transacoes")
        print("6. Relatorio do Mes")
        print("7. Sair")
        opcao = input("Escolha uma opcao: ")

        if opcao == "1":
            print(f"Saldo: R${bank.consultar_saldo(usuario):.2f}")

        elif opcao == "2":
            print(f"Limite: R${bank.consultar_limite(usuario):.2f}")

        elif opcao == "3":
            valor = pedir_valor("Valor do saque: ")
            # todo saque e um tipo de gasto, entao pedimos a categoria
            categoria = escolher_categoria()
            deu_certo, mensagem = bank.sacar(users, usuario, valor)
            print(mensagem)
            if deu_certo:
                finance.registrar_transacao(email, "saida", categoria, valor)

        elif opcao == "4":
            valor = pedir_valor("Valor do deposito: ")
            deu_certo, mensagem = bank.depositar(users, usuario, valor)
            print(mensagem)
            if deu_certo:
                finance.registrar_transacao(email, "entrada", "Outros", valor)

        elif opcao == "5":
            mostrar_historico(email)

        elif opcao == "6":
            mostrar_relatorio(email)

        elif opcao == "7":
            print("Saindo da sua conta...")
            break

        else:
            print("Opcao invalida, tente novamente.")


def escolher_cliente(clientes):
    """Mostra a lista de clientes e devolve o que o gerente escolher."""
    print("\nClientes:")
    for i, cliente in enumerate(clientes):
        print(f"{i + 1}. {cliente['user_email']}")
    try:
        escolha = int(input("Escolha o cliente: "))
        return clientes[escolha - 1]
    except (ValueError, IndexError):
        print("Cliente invalido.")
        return None


def menu_admin(users, admin):
    """Menu do gerente do banco (modo administrador).
    Apenas o gerente pode fazer alteracoes nas transacoes dos clientes."""
    while True:
        print("\n----- MENU GERENTE DO BANCO -----")
        print("1. Listar todos os clientes")
        print("2. Consultar dados de um cliente")
        print("3. Atualizar dados de um cliente")
        print("4. Registrar Entrada para um cliente")
        print("5. Registrar Saida (gasto) para um cliente")
        print("6. Ver Historico e Relatorio de um cliente")
        print("7. Sair")
        opcao = input("Escolha uma opcao: ")

        # o gerente so mexe com os clientes comuns
        clientes = [u for u in users if u["type"] == "user"]

        if opcao == "1":
            print("\nClientes do banco:")
            for i, cliente in enumerate(clientes):
                print(f"{i + 1}. {cliente['user_email']} - Saldo: R${cliente['balance']:.2f}")

        elif opcao == "2":
            cliente = escolher_cliente(clientes)
            if cliente:
                print(f"\nE-mail: {cliente['user_email']}")
                print(f"Saldo:  R${cliente['balance']:.2f}")
                print(f"Limite: R${cliente['limit']:.2f}")

        elif opcao == "3":
            cliente = escolher_cliente(clientes)
            if cliente:
                novo_saldo = pedir_valor("Novo saldo: ", minimo=0)
                novo_limite = pedir_valor("Novo limite: ", minimo=0)
                cliente["balance"] = novo_saldo
                cliente["limit"] = novo_limite
                bank.atualizar_usuario(users)
                print("Dados atualizados com sucesso!")

        elif opcao == "4":
            cliente = escolher_cliente(clientes)
            if cliente:
                valor = pedir_valor("Valor da entrada: ")
                categoria = escolher_categoria()
                bank.adicionar_ao_saldo(users, cliente, valor)
                finance.registrar_transacao(cliente["user_email"], "entrada", categoria, valor)
                print(f"Entrada registrada! Saldo do cliente: R${cliente['balance']:.2f}")

        elif opcao == "5":
            cliente = escolher_cliente(clientes)
            if cliente:
                valor = pedir_valor("Valor do gasto: ")
                categoria = escolher_categoria()
                conseguiu = bank.tirar_do_saldo(users, cliente, valor)
                if conseguiu:
                    finance.registrar_transacao(cliente["user_email"], "saida", categoria, valor)
                    print(f"Gasto registrado! Saldo do cliente: R${cliente['balance']:.2f}")
                else:
                    print("Saldo insuficiente do cliente para esse gasto.")

        elif opcao == "6":
            cliente = escolher_cliente(clientes)
            if cliente:
                mostrar_historico(cliente["user_email"])
                mostrar_relatorio(cliente["user_email"])

        elif opcao == "7":
            print("Saindo do modo gerente...")
            break

        else:
            print("Opcao invalida, tente novamente.")
