import random
from datetime import datetime, timedelta
import re

menu = '''

Bem vindo a ReBank

[D] Deposito
[S] Sacar
[E] Extrato 
[Q] Sair

>> '''

saldo = 0
limite = 500
extrato = []
numero_depositos = 0
numero_saques = 0
LIMITE_TRANSACOES = 10
contador_contas = 1

ufs_validas = {
        "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", 
        "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", 
        "TO"
    }

dict_clientes = {}
dict_contas = {}

def verificar_data(data_str, formato="%d/%m/%Y"):
    try:
        # Tenta converter a string para o formato de data especificado
        datetime.strptime(data_str, formato)
        return True  # A data é válida
    except ValueError:
        return False  # A data não é válida

def verifica_idade(data_str, formato="%d/%m/%Y"):
    try:
        data_nascimento = datetime.strptime(data_str, formato)

        d = datetime.now()

        limite_idade = d - timedelta(days=18*365) 

        if data_nascimento <= limite_idade:
            return True
        else:
            return False
    except ValueError:
        return False
    
def verificar_nome(nome):
    if any(char.isdigit() for char in nome):
        return False  # Nome não pode ter números
    return True

def verificar_cpf(cpf):
    if any(char.isalpha() for char in cpf):
        return False  # CPF não pode ter letras
    return True

def verificar_uf(uf):
    return uf.upper() in ufs_validas

def verificar_endereco(endereco):
    if any(char.isdigit() for char in endereco):
        return False  # Endereço não pode ter números
    return True

def cadastrar_cliente(dict_clientes):
    dict_cliente = {
        'nome': '',
        'data_nascimento': '',
        'cpf': '',
        'endereco': {'estado': '', 'cidade': '', 'bairro': '', 'numero': '', 'complemento': ''}
    }
    
    try:
        # Nome do cliente
        dict_cliente['nome'] = input('Olá! Para criar sua conta na ReBank, informe seu nome:')
        if not verificar_nome(dict_cliente['nome']):
            print('Nome não pode ter número.')
            return

        # Data de nascimento
        dict_cliente['data_nascimento'] = input('\nInforme sua data de nascimento (DD/MM/AAAA): ')
        if not verificar_data(dict_cliente['data_nascimento']):
            print('Data de nascimento inválida.')
            return
        if not verifica_idade(dict_cliente['data_nascimento']):
            print('Data de nascimento inválida.')
            return

        # CPF
        dict_cliente['cpf'] = input('\nInforme seu CPF:')
        if not verificar_cpf(dict_cliente['cpf']):
            print('CPF não pode conter letras.')
            return

        # Verifica se o CPF já existe
        if dict_cliente['cpf'] in [cliente['cpf'] for cliente in dict_clientes.values()]:
            print('CPF já cadastrado.')
            return

        # Estado/UF
        dict_cliente['endereco']['estado'] = input('\nInforme seu estado/UF: ').upper()
        if not verificar_uf(dict_cliente['endereco']['estado']):
            print('UF não é válida.')
            return

        # Cidade
        dict_cliente['endereco']['cidade'] = input('\nInforme sua cidade:')
        if not verificar_endereco(dict_cliente['endereco']['cidade']):
            print('Cidade não pode ter número.')
            return

        # Bairro
        dict_cliente['endereco']['bairro'] = input('\nInforme seu bairro: ')
        if not verificar_endereco(dict_cliente['endereco']['bairro']):
            print('Bairro não pode ter número.')
            return

        # Número do endereço
        dict_cliente['endereco']['numero'] = input('\nInforme o número do seu endereço:')
        if any(char.isalpha() for char in dict_cliente['endereco']['numero']):
            print('Número do endereço não pode conter letras.')
            return

        # Complemento (opcional)
        dict_cliente['endereco']['complemento'] = input('\nInforme um complemento (opcional):')

        # Adiciona o cliente ao dicionário
        dict_clientes[dict_cliente['cpf']] = dict_cliente
        print(f'Cliente {dict_cliente["nome"]} cadastrado com sucesso!')
    
    except Exception as e:
        print(f"Algo deu errado: {e}. Tente novamente mais tarde.")

        


def criar_conta():
    global contador_contas  # Utilizamos um contador global para garantir o incremento das contas

    try:
        cpf_cliente = input('Informe o CPF do cliente para vincular a conta: ')
        
        # Verifica se o CPF existe no dicionário de clientes
        if cpf_cliente not in dict_clientes:
            print('Cliente não encontrado!')
            return
        
        # Gera um número de conta aumentativo (1, 2, 3, ...)
        numero_conta = contador_contas
        contador_contas += 1  # Aumenta o contador para a próxima conta

        # Associa o número da conta ao CPF do cliente
        dict_clientes[numero_conta] = cpf_cliente

        print(f'Conta criada com sucesso! Número da conta: {numero_conta}')
        print(f'Conta vinculada ao cliente: {dict_clientes[cpf_cliente]["nome"]}')
        
    except Exception as e:
        print(f"Erro ao criar conta: {e}")




def deposito(saldo: float, extrato: list) -> tuple[float, list]:
    try:
        value = float(input("Informe o valor do Depósito: ").replace(',', '.'))
        
        if value <= 0:
            print("O valor do depósito deve ser positivo.")
            return saldo, extrato
        
        saldo += value
        extrato.append(f"Depósito de R${value:.2f} em {datetime.date.today()}")

        print(f"Depósito de R${value:.2f} realizado com sucesso!")
        return saldo, extrato

    except ValueError:
        print("Erro: Valor inválido! Insira um número válido.")
        return saldo, extrato

def saque(saldo: float, extrato: list, limite: float, LIMITE_TRANSACOES: int, numero_saques: int, numero_depositos: int) -> tuple[float, list, int, int]:
    try: 
        if numero_saques >= LIMITE_TRANSACOES:
            print("Limite de transações diárias já foi atingida.")
            return saldo, extrato, numero_saques
        
        value = float(input("Informe o valor do Saque: ").replace(',', '.'))

        if value > limite:
            print(f"Saque não pode ser maior que R${limite:.2f}!")
            return saldo, extrato, numero_saques

        if value > saldo:
            print("Saldo insuficiente!")
            return saldo, extrato, numero_saques

        saldo -= value
        extrato.append(f"Saque de R${value:.2f} em {datetime.date.today()}")
        numero_saques += 1

        print(f"Saque de R${value:.2f} realizado com sucesso!")
        return saldo, extrato, numero_saques
    
    except ValueError:
        print("Erro: Valor inválido! Insira um número válido.")
        return saldo, extrato, numero_saques

def mostra_extrato(saldo: float, extrato: list):
    print("\n===== EXTRATO =====")
    if not extrato:
        print("Nenhuma transação realizada.")
    else:
        for item in extrato:
            print(item)
            print("*" * 60)
    print(f"Saldo atual: R${saldo:.2f}\n")

while True:

    cadastrar_cliente(dict_clientes)

    opcao = input(menu).upper()

    if opcao == "D":
        saldo, extrato = deposito(saldo, extrato)

    elif opcao == "S":
        saldo, extrato, numero_saques = saque(saldo, extrato, limite, LIMITE_TRANSACOES, numero_saques)

    elif opcao == "E":
        mostra_extrato(saldo, extrato)

    elif opcao == "Q":
        print("Saindo do sistema. Obrigado!")
        break

    else:
        print("Operação inválida, tente novamente.")



