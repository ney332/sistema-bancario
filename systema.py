from datetime import date

class Usuario:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf

class ContaBancaria:
    LIMITE_SAQUE_DIARIO = 500.00
    LIMITE_SAQUES = 3

    def __init__(self, usuario: Usuario):
        self.usuario = usuario
        self.saldo = 0.0
        self.extrato = []
        self.saques_hoje = 0
        self.total_sacado_hoje = 0.0
        self.data_saque = date.today()

    def resetar_limite_diario(self):
        """Reseta o limite de saques se o dia mudou."""
        if self.data_saque != date.today():
            self.saques_hoje = 0
            self.total_sacado_hoje = 0.0
            self.data_saque = date.today()

    def deposito(self, valor: float) -> str:
        if valor <= 0:
            return "Erro: O valor do depósito deve ser positivo."
        self.saldo += valor
        self.extrato.append(f"Depósito: +R$ {valor:.2f}")
        return f"Depósito de R$ {valor:.2f} realizado com sucesso!"

    def saque(self, valor: float) -> str:
        self.resetar_limite_diario()

        if valor <= 0:
            return "Erro: O valor do saque deve ser positivo."
        if self.saldo < valor:
            return "Erro: Saldo insuficiente para realizar o saque."
        if self.saques_hoje >= self.LIMITE_SAQUES:
            return "Erro: Limite de 3 saques diários atingido."
        if (self.total_sacado_hoje + valor) > self.LIMITE_SAQUE_DIARIO:
            return f"Erro: Limite diário de R$ {self.LIMITE_SAQUE_DIARIO:.2f} em saques atingido."

        self.saldo -= valor
        self.saques_hoje += 1
        self.total_sacado_hoje += valor
        self.extrato.append(f"Saque: -R$ {valor:.2f}")
        return f"Saque de R$ {valor:.2f} realizado com sucesso!"

    def investimento(self, valor: float, meses: int, taxa_juros: float = 0.01) -> str:
        if valor <= 0:
            return "Erro: O valor do investimento deve ser positivo."
        if self.saldo < valor:
            return "Erro: Saldo insuficiente para investir."

        self.saldo -= valor
        montante = valor * ((1 + taxa_juros) ** meses)
        lucro = montante - valor
        self.saldo += montante
        self.extrato.append(f"Investimento: +R$ {lucro:.2f} (após {meses} meses)")
        return (
            f"Investimento de R$ {valor:.2f} realizado por {meses} meses.\n"
            f"Lucro obtido: R$ {lucro:.2f} (Taxa: {taxa_juros*100:.2f}% ao mês)"
        )

    def ver_extrato(self) -> str:
        self.resetar_limite_diario()

        linhas = [
            f"=== Extrato Bancário ===",
            f"Cliente: {self.usuario.nome} (CPF: {self.usuario.cpf})",
            "-" * 30,
        ]

        if not self.extrato:
            linhas.append("Nenhuma operação realizada.")
        else:
            linhas.extend(self.extrato)

        linhas.append("-" * 30)
        linhas.append(f"Saldo atual: R$ {self.saldo:.2f}")
        linhas.append(
            f"Saques hoje: {self.saques_hoje}/{self.LIMITE_SAQUES} "
            f"(R$ {self.total_sacado_hoje:.2f} de R$ {self.LIMITE_SAQUE_DIARIO:.2f})"
        )
        linhas.append("=" * 30)

        return "\n".join(linhas)


class BancoApp:
    def __init__(self):
        self.conta = None

    def iniciar(self):
        print("=== Bem-vindo ao Banco Python ===")
        nome = input("Digite seu nome: ")
        cpf = input("Digite seu CPF (somente números): ")

        usuario = Usuario(nome, cpf)
        self.conta = ContaBancaria(usuario)

        self.menu()

    def menu(self):
        while True:
            print("\nMenu Principal:")
            print("1. Depósito")
            print("2. Saque")
            print("3. Extrato")
            print("4. Investimento")
            print("5. Sair")

            opcao = input("\nEscolha uma opção: ")

            if opcao == "1":
                try:
                    valor = float(input("Valor do depósito: R$ "))
                    print(self.conta.deposito(valor))
                except ValueError:
                    print("Erro: Valor inválido. Use números (ex: 100.50)")

            elif opcao == "2":
                try:
                    valor = float(input("Valor do saque: R$ "))
                    print(self.conta.saque(valor))
                except ValueError:
                    print("Erro: Valor inválido. Use números (ex: 100.50)")

            elif opcao == "3":
                print(self.conta.ver_extrato())

            elif opcao == "4":
                try:
                    valor = float(input("Valor a investir: R$ "))
                    meses = int(input("Quantidade de meses: "))
                    print(self.conta.investimento(valor, meses))
                except ValueError:
                    print("Erro: Digite números válidos para valor e meses.")

            elif opcao == "5":
                print("\nObrigado por usar nossos serviços. Até logo!")
                break
            else:
                print("\nOpção inválida. Tente novamente.")


if __name__ == "__main__":
    app = BancoApp()
    app.iniciar()
