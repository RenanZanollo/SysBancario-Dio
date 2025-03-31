import datetime as dt

menu = '''

[D] Deposito
[S] Sacar
[E] Extrato 
[Q] Sair

>> '''

saldo = 0
limite = 500
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3

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





