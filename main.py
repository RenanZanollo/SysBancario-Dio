import datetime as dt
import copy

menu = '''

Bem vindo a ReBank

[D] Deposito
[S] Sacar
[E] Extrato 
[Q] Sair

>> '''

## criar função cadastrar cliente e criar conta, conta tem que ser atralda ao cliente
## cliente deve ter: nome, data de anscimento, cpf, endereço (logadouro, bairro, cidade\sigla estdo)
##criar conta: contas devem ser armazenadas em uma lista, uma conta é comporta por agencia numero
## da conta e usuario, o numero da conta é sequencial, iniciando em 1. o numero da agencia é fixo"0001"
## um usuario pode ter mais de uma conta, mas uma conta só pode ter 1 usuario

saldo = 0
limite = 500
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3

dict_cliente_default = {
                    'nome':'',
                    'data_nascimento':'',
                    'cpf':'',
                    'endereco':{'estado':'', 'cidade':'', 'bairro':'', 'numero':''}
}

dict_clientes = {}

def cadastrar_cliente(dict_cliente_default = dict, dict_clientes = dict):
    dict_cliente = copy.deepcopy(dict_cliente_default)

    dict_cliente['nome'].value() = input('Olá! Para criar sua conta na ReBank, informe seu nome:')
    dict_cliente['data_nascimento'].value() = input('\nInforme sua data de nascimento (DD/MM/AAAA): ')
    dict_cliente['cpf'] = input('\nInforme seu CPF:')

    cpfs = [cliente['cpf'] for cliente in dict_clientes.values()]

    if dict_cliente['cpf'] in cpfs:
        print('codigo se o cpf ja existe')

    dict_cliente['endereco']['estado'].value() = input('\nInforme seu estado/UF: ')
    dict_cliente['endereco']['cidade'].value() = input('\nInforme sua cidade:')
    dict_cliente['endereco']['bairro'].value() = input('\nInforme seu bairro: ')
    dict_cliente['endereco']['numero'].value() = input('\nInforme seu logadouro:')



def criar_conta():


def deposito(saldo: float, extrato: list) -> tuple[float, list]:
    try:
        value = float(input("Informe o valor do Depósito: ").replace(',', '.'))
        
        if value <= 0:
            print("O valor do depósito deve ser positivo.")
            return saldo, extrato
        
        saldo += value
        extrato.append(f"Depósito de R${value:.2f} em {dt.date.today()}")

        print(f"Depósito de R${value:.2f} realizado com sucesso!")
        return saldo, extrato

    except ValueError:
        print("Erro: Valor inválido! Insira um número válido.")
        return saldo, extrato

def saque(saldo: float, extrato: list, limite: float, LIMITE_SAQUES: int, numero_saques: int) -> tuple[float, list, int]:
    try: 
        if numero_saques >= LIMITE_SAQUES:
            print("Limite de 3 saques diários já foi atingido.")
            return saldo, extrato, numero_saques
        
        value = float(input("Informe o valor do Saque: ").replace(',', '.'))

        if value > limite:
            print(f"Saque não pode ser maior que R${limite:.2f}!")
            return saldo, extrato, numero_saques

        if value > saldo:
            print("Saldo insuficiente!")
            return saldo, extrato, numero_saques

        saldo -= value
        extrato.append(f"Saque de R${value:.2f} em {dt.date.today()}")
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
    opcao = input(menu).upper()

    if opcao == "D":
        saldo, extrato = deposito(saldo, extrato)

    elif opcao == "S":
        saldo, extrato, numero_saques = saque(saldo, extrato, limite, LIMITE_SAQUES, numero_saques)

    elif opcao == "E":
        mostra_extrato(saldo, extrato)

    elif opcao == "Q":
        print("Saindo do sistema. Obrigado!")
        break

    else:
        print("Operação inválida, tente novamente.")



