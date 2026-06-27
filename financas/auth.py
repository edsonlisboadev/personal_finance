# auth.py - parte de login (autenticacao) do sistema


def authenticate(users, email, senha):
    """Procura um usuario que tenha o email e a senha informados.
    Se achar devolve o usuario, se nao achar devolve None."""
    for user in users:
        if user["user_email"] == email and user["user_password"] == senha:
            return user
    return None
