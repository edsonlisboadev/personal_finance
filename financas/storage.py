# storage.py - cuida de salvar e carregar as informacoes nos arquivos
import json
import os

# caminho da pasta "dados" (fica do lado deste arquivo)
PASTA_DADOS = os.path.join(os.path.dirname(__file__), "dados")
ARQUIVO_USERS = os.path.join(PASTA_DADOS, "users.json")
ARQUIVO_TRANSACOES = os.path.join(PASTA_DADOS, "transacoes.json")

# usuarios padrao - so sao usados na primeira vez, quando o arquivo
# ainda nao existe ou esta vazio (funciona como uma copia de seguranca)
USERS_INICIAIS = [
    {"type": "admin", "user_email": "admin@admin", "user_password": 1234,
     "balance": 10000, "limit": 10000, "max_limit": 10000},
    {"type": "user", "user_email": "chorenafeature@user", "user_password": 6767,
     "balance": 6767, "limit": 86400, "max_limit": 86400},
    {"type": "user", "user_email": "lucasguloso@user", "user_password": 6969,
     "balance": 2440, "limit": 30, "max_limit": 30},
    {"type": "user", "user_email": "aninhafazcompleto@user", "user_password": 8888,
     "balance": 250, "limit": 3600, "max_limit": 3600},
]


def carregar_users():
    """Le os usuarios do arquivo. Se nao existir ou estiver vazio,
    cria o arquivo com os usuarios padrao (USERS_INICIAIS)."""
    try:
        with open(ARQUIVO_USERS, "r", encoding="utf-8") as arquivo:
            users = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        users = []

    if not users:
        users = USERS_INICIAIS
        salvar_users(users)

    return users


def salvar_users(users):
    """Grava a lista de usuarios no arquivo."""
    with open(ARQUIVO_USERS, "w", encoding="utf-8") as arquivo:
        json.dump(users, arquivo, ensure_ascii=False, indent=4)


def carregar_transacoes():
    """Le as transacoes (entradas e saidas) do arquivo."""
    try:
        with open(ARQUIVO_TRANSACOES, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def salvar_transacoes(transacoes):
    """Grava a lista de transacoes no arquivo."""
    with open(ARQUIVO_TRANSACOES, "w", encoding="utf-8") as arquivo:
        json.dump(transacoes, arquivo, ensure_ascii=False, indent=4)
