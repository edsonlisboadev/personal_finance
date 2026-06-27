# finance.py - parte de financas pessoais: categorias, entradas, saidas e relatorio
import storage
from datetime import datetime

# categorias disponiveis para classificar as transacoes
CATEGORIAS = ["Alimentacao", "Transporte", "Lazer", "Moradia", "Saude", "Salario", "Outros"]


def registrar_transacao(email, tipo, categoria, valor):
    """Guarda uma transacao no arquivo. O tipo pode ser 'entrada' ou 'saida'."""
    transacoes = storage.carregar_transacoes()
    nova_transacao = {
        "user_email": email,
        "tipo": tipo,
        "categoria": categoria,
        "valor": valor,
        "data": datetime.now().strftime("%d/%m/%Y"),
    }
    transacoes.append(nova_transacao)
    storage.salvar_transacoes(transacoes)


def transacoes_do_usuario(email):
    """Devolve so as transacoes do usuario informado."""
    todas = storage.carregar_transacoes()
    return [t for t in todas if t["user_email"] == email]


def relatorio_mes(email):
    """Monta um resumo das entradas e saidas do mes atual."""
    mes_atual = datetime.now().strftime("%m/%Y")
    minhas = transacoes_do_usuario(email)

    total_entradas = 0
    total_saidas = 0
    gastos_por_categoria = {}

    for t in minhas:
        # a data esta no formato dd/mm/aaaa, entao pego so o "mm/aaaa"
        mes_da_transacao = t["data"][3:]
        if mes_da_transacao != mes_atual:
            continue

        if t["tipo"] == "entrada":
            total_entradas += t["valor"]
        else:
            total_saidas += t["valor"]
            categoria = t["categoria"]
            gastos_por_categoria[categoria] = gastos_por_categoria.get(categoria, 0) + t["valor"]

    saldo_do_mes = total_entradas - total_saidas

    return {
        "mes": mes_atual,
        "entradas": total_entradas,
        "saidas": total_saidas,
        "saldo": saldo_do_mes,
        "por_categoria": gastos_por_categoria,
    }
