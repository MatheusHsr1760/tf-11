# Loja refatorada com todas as regras de Object Calisthenics aplicadas.

DESCRICOES_DE_STATUS = {
    "A": "aberto",
    "P": "pago",
    "C": "cancelado",
}


# Representa e valida o numero de CPF de uma pessoa (exatamente 11 caracteres).
class Cpf:
    def __init__(self, numero):
        if len(numero) != 11:
            raise ValueError("cpf invalido")
        self._numero = numero


# Representa e valida o endereco de email de uma pessoa (nao vazio e contendo arroba).
class Email:
    def __init__(self, endereco):
        if len(endereco) == 0:
            raise ValueError("email vazio")
        if "@" not in endereco:
            raise ValueError("email invalido")
        self._endereco = endereco


# Representa e valida o codigo de enderecamento postal (exatamente 8 caracteres).
class Cep:
    def __init__(self, codigo):
        if len(codigo) != 8:
            raise ValueError("cep invalido")
        self._codigo = codigo


# Representa um valor monetario exato em centavos inteiros e realiza operacoes financeiras.
class Dinheiro:
    def __init__(self, centavos):
        self._centavos = int(centavos)

    def somar(self, outro):
        return Dinheiro(self._centavos + outro._centavos)

    def subtrair(self, outro):
        return Dinheiro(self._centavos - outro._centavos)

    def multiplicar(self, quantidade):
        return Dinheiro(self._centavos * quantidade)

    def percentual(self, taxa):
        return Dinheiro(self._centavos * taxa // 100)

    def __str__(self):
        reais = self._centavos // 100
        centavos_restantes = self._centavos % 100
        return f"R$ {reais}.{centavos_restantes:02d}"


# Representa o estado atual de um pedido (aberto, pago ou cancelado).
class Status:
    def __init__(self, codigo):
        self._codigo = codigo

    def esta_aberto(self):
        return self._codigo == "A"

    def esta_pago(self):
        return self._codigo == "P"

    def descrever(self):
        return DESCRICOES_DE_STATUS[self._codigo]

    def __str__(self):
        return self.descrever()


# Define a regra de desconto para clientes do tipo normal (0% de desconto).
class TipoNormal:
    def desconto_sobre(self, valor):
        return valor.percentual(0)


# Define a regra de desconto para clientes do tipo VIP (10% de desconto).
class TipoVip:
    def desconto_sobre(self, valor):
        return valor.percentual(10)


# Define a regra de desconto para clientes que sao funcionarios (20% de desconto).
class TipoFuncionario:
    def desconto_sobre(self, valor):
        return valor.percentual(20)


# Agrupa os dados de identificacao pessoal (nome, CPF e email).
class Pessoa:
    def __init__(self, nome, cpf, email):
        self._nome = nome
        self._cpf = cpf
        self._email = email

    def identificar(self):
        return self._nome


# Agrupa os dados de localizacao de entrega (rua, cidade e CEP).
class Endereco:
    def __init__(self, rua, cidade, cep):
        self._rua = rua
        self._cidade = cidade
        self._cep = cep

    def localizar_cidade(self):
        return self._cidade


# Representa um cliente da loja, associando sua identificacao, endereco e categoria de desconto.
class Cliente:
    def __init__(self, pessoa, endereco, tipo):
        self._pessoa = pessoa
        self._endereco = endereco
        self._tipo = tipo

    def resumo_para_relatorio(self):
        nome = self._pessoa.identificar()
        cidade = self._endereco.localizar_cidade()
        return f"{nome} - {cidade}"

    def calcular_desconto(self, valor):
        return self._tipo.desconto_sobre(valor)


# Representa um item do catalogo de produtos com seu nome e preco unitario.
class Produto:
    def __init__(self, nome, preco):
        self._nome = nome
        self._preco = preco

    def calcular_valor_para(self, quantidade):
        return self._preco.multiplicar(quantidade)

    def descrever_item(self, quantidade):
        subtotal = self.calcular_valor_para(quantidade)
        return f"   {quantidade} x {self._nome} = {subtotal}"


# Associa um produto a uma quantidade comprada dentro de um pedido.
class ItemDoPedido:
    def __init__(self, produto, quantidade):
        self._produto = produto
        self._quantidade = quantidade

    def calcular_subtotal(self):
        return self._produto.calcular_valor_para(self._quantidade)

    def imprimir(self):
        linha = self._produto.descrever_item(self._quantidade)
        print(linha)


# Colecao de primeira classe responsavel por guardar e totalizar os itens de um pedido.
class ItensDoPedido:
    def __init__(self):
        self._itens = []

    def adicionar(self, item):
        self._itens.append(item)

    def esta_vazia(self):
        return len(self._itens) == 0

    def calcular_total(self):
        total = Dinheiro(0)
        for item in self._itens:
            subtotal = item.calcular_subtotal()
            total = total.somar(subtotal)
        return total

    def imprimir(self):
        for item in self._itens:
            item.imprimir()


# Representa um pedido de compra, controlando seus itens, seu ciclo de vida e seus valores.
class Pedido:
    def __init__(self, cliente):
        self._cliente = cliente
        self._itens = ItensDoPedido()
        self._status = Status("A")

    def adicionar_item(self, produto, quantidade):
        item = ItemDoPedido(produto, quantidade)
        self._itens.adicionar(item)

    def pagar(self):
        if not self._status.esta_aberto():
            return False
        if self._itens.esta_vazia():
            return False
        self._status = Status("P")
        return True

    def cancelar(self):
        if not self._status.esta_aberto():
            return False
        self._status = Status("C")
        return True

    def esta_aberto(self):
        return self._status.esta_aberto()

    def calcular_total(self):
        return self._itens.calcular_total()

    def calcular_desconto(self):
        total = self.calcular_total()
        return self._cliente.calcular_desconto(total)

    def calcular_valor_a_pagar(self):
        total = self.calcular_total()
        desconto = self.calcular_desconto()
        return total.subtrair(desconto)

    def valor_arrecadado(self):
        if not self._status.esta_pago():
            return Dinheiro(0)
        return self.calcular_valor_a_pagar()

    def _imprimir_totais(self):
        if self._itens.esta_vazia():
            return
        total = self.calcular_total()
        desconto = self.calcular_desconto()
        valor_a_pagar = self.calcular_valor_a_pagar()
        print(f"  total: {total} | desconto: {desconto} | a pagar: {valor_a_pagar}")

    def imprimir_relatorio(self, numero):
        resumo_do_cliente = self._cliente.resumo_para_relatorio()
        print(f"Pedido {numero} - {resumo_do_cliente}")
        print(f"  status: {self._status}")
        self._itens.imprimir()
        self._imprimir_totais()


# Colecao de primeira classe responsavel por registrar os pedidos da loja e consolidar relatorios.
class Pedidos:
    def __init__(self):
        self._pedidos_por_numero = {}

    def criar_pedido(self, numero, cliente):
        pedido = Pedido(cliente)
        self._pedidos_por_numero[numero] = pedido
        return pedido

    def imprimir_relatorio(self):
        for numero in self._pedidos_por_numero:
            pedido = self._pedidos_por_numero[numero]
            pedido.imprimir_relatorio(numero)

    def calcular_total_arrecadado(self):
        total = Dinheiro(0)
        for numero in self._pedidos_por_numero:
            pedido = self._pedidos_por_numero[numero]
            valor_do_pedido = pedido.valor_arrecadado()
            total = total.somar(valor_do_pedido)
        return total

    def contar_pedidos_abertos(self):
        abertos = [
            numero
            for numero in self._pedidos_por_numero
            if self._pedidos_por_numero[numero].esta_aberto()
        ]
        return len(abertos)


# --- o roteiro da loja (mantem a saida identica ao original) -------------------
pedidos = Pedidos()

caderno = Produto("Caderno", Dinheiro(1550))
caneta = Produto("Caneta", Dinheiro(250))
livro = Produto("Livro", Dinheiro(8950))
fone = Produto("Fone", Dinheiro(6000))

cliente_ana = Cliente(
    Pessoa("Ana Souza", Cpf("12345678901"), Email("ana@mail.com")),
    Endereco("Rua das Flores, 10", "Sorocaba", Cep("18010000")),
    TipoVip(),
)
primeiro_pedido_da_ana = pedidos.criar_pedido(1, cliente_ana)
primeiro_pedido_da_ana.adicionar_item(caderno, 2)
primeiro_pedido_da_ana.adicionar_item(caneta, 5)

try:
    cliente_bruno = Cliente(
        Pessoa("Bruno Lima", Cpf("123"), Email("bruno@mail.com")),
        Endereco("Av. Central, 200", "Votorantim", Cep("18110000")),
        TipoNormal(),
    )
    pedidos.criar_pedido(2, cliente_bruno)
except ValueError as erro:
    print("pedido 2 recusado:", erro)

segundo_pedido_da_ana = pedidos.criar_pedido(3, cliente_ana)
segundo_pedido_da_ana.adicionar_item(livro, 1)

try:
    cliente_carla = Cliente(
        Pessoa("Carla Dias", Cpf("98765432100"), Email("carla.mail.com")),
        Endereco("Rua do Sol, 55", "Sorocaba", Cep("18020000")),
        TipoFuncionario(),
    )
    pedidos.criar_pedido(4, cliente_carla)
except ValueError as erro:
    print("pedido 4 recusado:", erro)

cliente_diego = Cliente(
    Pessoa("Diego Rocha", Cpf("11122233344"), Email("diego@mail.com")),
    Endereco("Rua Nova, 7", "Itu", Cep("13300000")),
    TipoNormal(),
)
pedido_do_diego = pedidos.criar_pedido(5, cliente_diego)

cliente_eva = Cliente(
    Pessoa("Eva Nunes", Cpf("55566677788"), Email("eva@mail.com")),
    Endereco("Alameda Azul, 1", "Itu", Cep("13300001")),
    TipoFuncionario(),
)
pedido_da_eva = pedidos.criar_pedido(6, cliente_eva)
pedido_da_eva.adicionar_item(fone, 1)

try:
    cliente_fabio = Cliente(
        Pessoa("Fabio Costa", Cpf("99988877766"), Email("fabio@mail.com")),
        Endereco("Rua Velha, 3", "Itu", Cep("123")),
        TipoNormal(),
    )
    pedidos.criar_pedido(7, cliente_fabio)
except ValueError as erro:
    print("pedido 7 recusado:", erro)

cliente_gil = Cliente(
    Pessoa("Gil Alves", Cpf("44455566677"), Email("gil@mail.com")),
    Endereco("Rua do Meio, 9", "Sorocaba", Cep("18030000")),
    TipoNormal(),
)
pedido_do_gil = pedidos.criar_pedido(8, cliente_gil)
pedido_do_gil.adicionar_item(fone, 2)

print("pagar 1:", primeiro_pedido_da_ana.pagar())
print("pagar 3:", segundo_pedido_da_ana.pagar())
print("pagar 5:", pedido_do_diego.pagar())
print("pagar 6:", pedido_da_eva.pagar())
print("cancelar 5:", pedido_do_diego.cancelar())
print("cancelar 1:", primeiro_pedido_da_ana.cancelar())

pedidos.imprimir_relatorio()
print("arrecadado:", str(pedidos.calcular_total_arrecadado()))
print("abertos:", pedidos.contar_pedidos_abertos())
