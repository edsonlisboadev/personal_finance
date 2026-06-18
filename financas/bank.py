users = [
    {"type": "admin",
    "user_email": "admin@admin",
    "user_password": 1234,
    "balance": 10000,
    "limit": 10000},

    {"type": "user",
    "user_email": "chorenafeature@user",
    "user_password": 6767,
    "balance": 6767,
    "limit": 86400},

    {"type": "user",
    "user_email": "lucasguloso@user",
    "user_password": 6969,
    "balance": 2440,
    "limit": 30},

    {"type": "user",
    "user_email": "aninhafazcompleto@user",
    "user_password": 8888,
    "balance": 250,
    "limit": 3600}
]

for user in users:
    user['max_limit'] = user['limit']


def get_balance(user):
    return user['balance']


def get_limit(user):
    return user['limit']


def withdraw(user, amount):
    balance = user['balance']
    limit = user['limit']

    if amount > balance + limit:
        print("não tem saldo suficiente")
    else:
        if amount > balance:
            difference = amount - balance
            limit -= difference
            balance = 0
        else:
            balance -= amount

        user['balance'] = balance
        user['limit'] = limit

        print(f"Saque realizado! Saldo atual: R${balance:.2f}")


def deposit(user, amount):
    balance = user['balance']
    limit = user['limit']
    max_limit = user['max_limit']

    if limit < max_limit:
        difference = max_limit - limit
        if amount >= difference:
            limit = max_limit
            balance += amount - difference
            print(f"Limite restaurado! Saldo: R${balance:.2f}")
        else:
            limit += amount
            print(f"Limite atualizado: R${limit:.2f}")
    else:
        balance += amount
        print(f"Saldo atual: R${balance:.2f}")

    user['balance'] = balance
    user['limit'] = limit
    print("Depósito realizado com sucesso")

test_user = users[2]
print("Antes:", test_user)

withdraw(test_user, 2450)
print("Depois do saque:", test_user)

deposit(test_user, 5)
print("Depois do depósito 1:", test_user)

deposit(test_user, 10)
print("Depois do depósito 2:", test_user)