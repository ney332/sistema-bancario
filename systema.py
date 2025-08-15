class Usuario:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf

class ContaBancaria:
    LIMITE_SAQUE_DIARIO = 500.00
    
    def __init__(self, usuario):
        self.usuario = usuario
        self.saldo = 0.0
        self.extrato = []
        self.saques_hoje = 0
        self.total_sacado_hoje = 0.0

    def deposito(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato.append(f'Depósito: +R$ {valor:.2f}')
            print(f'\nDepósito de R$ {valor:.2f} realizado com sucesso!')
        else:
            print('\nErro: O valor do depósito deve ser positivo.')

    def saque(self, valor):
        if valor <= 0:
            print('\nErro: O valor do saque deve ser positivo.')
            return
        
        if self.saldo < valor:
            print('\nErro: Saldo insuficiente para realizar o saque.')
            return
            
        if self.saques_hoje >= 3:
            print('\nErro: Limite de 3 saques diários atingido.')
            return
            
        if (self.total_sacado_hoje + valor) > self.LIMITE_SAQUE_DIARIO:
            print(f'\nErro: Limite diário de R$ {self.LIMITE_SAQUE_DIARIO:.2f} em saques atingido.')
            return
            
        self.saldo -= valor
        self.saques_hoje += 1
        self.total_sacado_hoje += valor
        self.extrato.append(f'Saque: -R$ {valor:.2f}')
        print(f'\nSaque de R$ {valor:.2f} realizado com sucesso!')

    def investimento(self, valor, meses, taxa_juros=0.01):
        """Investe um valor com juros compostos mensais."""
        if valor <= 0:
            print("\nErro: O valor do investimento deve ser positivo.")
            return
        if self.saldo < valor:
            print("\nErro: Saldo insuficiente para investir.")
            return
        
        self.saldo -= valor
        montante = valor * ((1 + taxa_juros) ** meses)
        lucro = montante - valor
        self.saldo += montante
        self.extrato.append(f'Investimento: +R$ {lucro:.2f} (após {meses} meses)')
        print(f"\nInvestimento de R$ {valor:.2f} realizado por {meses} meses.")
        print(f"Lucro obtido: R$ {lucro:.2f} (Taxa: {taxa_juros*100:.2f}% ao mês)")

    def ver_extrato(self):
        print(f'\n=== Extrato Bancário ===')
        print(f'Cliente: {self.usuario.nome} (CPF: {self.usuario.cpf})')
        print('-' * 30)
        
        if not self.extrato:
            print('Nenhuma operação realizada.')
        else:
            for operacao in self.extrato:
                print(operacao)
        
        print('-' * 30)
        print(f'Saldo atual: R$ {self.saldo:.2f}')
        print(f'Saques hoje: {self.saques_hoje}/3 (R$ {self.total_sacado_hoje:.2f} de R$ {self.LIMITE_SAQUE_DIARIO:.2f})')
        print('=' * 30)

def main():
    print('=== Bem-vindo ao Banco Python ===')
    nome = input('Digite seu nome: ')
    cpf = input('Digite seu CPF (somente números): ')
    
    usuario = Usuario(nome, cpf)
    conta = ContaBancaria(usuario)
    
    while True:
        print('\nMenu Principal:')
        print('1. Depósito')
        print('2. Saque')
        print('3. Extrato')
        print('4. Investimento')
        print('5. Sair')
        
        opcao = input('\nEscolha uma opção: ')
        
        if opcao == '1':
            try:
                valor = float(input('Valor do depósito: R$ '))
                conta.deposito(valor)
            except ValueError:
                print('Erro: Valor inválido. Use números (ex: 100.50)')
                
        elif opcao == '2':
            try:
                valor = float(input('Valor do saque: R$ '))
                conta.saque(valor)
            except ValueError:
                print('Erro: Valor inválido. Use números (ex: 100.50)')
                
        elif opcao == '3':
            conta.ver_extrato()
        
        elif opcao == '4':
            try:
                valor = float(input('Valor a investir: R$ '))
                meses = int(input('Quantidade de meses: '))
                conta.investimento(valor, meses)
            except ValueError:
                print('Erro: Digite números válidos para valor e meses.')
            
        elif opcao == '5':
            print('\nObrigado por usar nossos serviços. Até logo!')
            break
            
        else:
            print('\nOpção inválida. Tente novamente.')

if __name__ == "__main__":
    main()
