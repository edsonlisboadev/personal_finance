# bank.py - operacoes do banco (saldo, saque, deposito...)
import storage


def carregar_usuarios():
    """Pega os usuarios. O storage ja cuida de criar os padrao na primeira vez."""
    return storage.carregar_users()


def consultar_saldo(user):
    return user["balance"]


def consultar_limite(user):
    return user["limit"]


def sacar(users, user, valor):
    """Tenta sacar um valor. Pode usar o saldo e depois o limite.
    Devolve (deu_certo, mensagem)."""
    saldo = user["balance"]
    limite = user["limit"]

    if valor > saldo + limite:
        falta = valor - (saldo + limite)
        return False, f"Saldo e limite insuficientes. Falta R${falta:.2f}"

    if valor > saldo:
        diferenca = valor - saldo
        limite -= diferenca
        saldo = 0
    else:
        saldo -= valor

    user["balance"] = saldo
    user["limit"] = limite
    storage.salvar_users(users)
    return True, f"Saque realizado! Saldo atual: R${saldo:.2f}"


def depositar(users, user, valor):
    """Deposita um valor. Se o limite estiver gasto, ele recupera o limite primeiro.
    Devolve (deu_certo, mensagem)."""
    saldo = user["balance"]
    limite = user["limit"]
    limite_max = user["max_limit"]

    if limite < limite_max:
        diferenca = limite_max - limite
        if valor >= diferenca:
            limite = limite_max
            saldo += valor - diferenca
        else:
            limite += valor
    else:
        saldo += valor

    user["balance"] = saldo
    user["limit"] = limite
    storage.salvar_users(users)
    return True, f"Deposito realizado! Saldo atual: R${saldo:.2f}"


def adicionar_ao_saldo(users, user, valor):
    """Soma um valor quando entra dinheiro. Repoe o limite primeiro:
    se o valor for maior que o limite gasto, o restante vai pro saldo;
    caso contrario, soma so no limite."""
    saldo = user["balance"]
    limite = user["limit"]
    limite_max = user["max_limit"]

    if limite < limite_max:
        diferenca = limite_max - limite
        if valor >= diferenca:
            limite = limite_max
            saldo += valor - diferenca
        else:
            limite += valor
    else:
        saldo += valor

    user["balance"] = saldo
    user["limit"] = limite
    storage.salvar_users(users)


def tirar_do_saldo(users, user, valor):
    """Tira um valor do saldo (usado quando tem um gasto).
    Se o saldo nao for suficiente, usa o limite. So devolve False quando
    saldo + limite nao cobrem o valor."""
    saldo = user["balance"]
    limite = user["limit"]

    if valor > saldo + limite:
        return False

    if valor > saldo:
        diferenca = valor - saldo
        limite -= diferenca
        saldo = 0
    else:
        saldo -= valor

    user["balance"] = saldo
    user["limit"] = limite
    storage.salvar_users(users)
    return True


def atualizar_usuario(users):
    """Salva qualquer alteracao feita nos usuarios (usado pelo gerente)."""
    storage.salvar_users(users)
