# Passo 6: Quebra o Cliente em Pessoa e Endereco (entidades pequenas).


class Cpf:
    def __init__(self, numero):
        if len(numero) != 11:
            raise ValueError("cpf invalido")
        self.numero = numero


class Email:
    def __init__(self, endereco):
        if len(endereco) == 0:
            raise ValueError("email vazio")
        if "@" not in endereco:
            raise ValueError("email invalido")
        self.endereco = endereco


class Cep:
    def __init__(self, codigo):
        if len(codigo) != 8:
            raise ValueError("cep invalido")
        self.codigo = codigo


class Dinheiro:
    def __init__(self, centavos):
        self.centavos = int(centavos)

    def somar(self, outro):
        return Dinheiro(self.centavos + outro.centavos)

    def subtrair(self, outro):
        return Dinheiro(self.centavos - outro.centavos)

    def multiplicar(self, quantidade):
        return Dinheiro(self.centavos * quantidade)

    def percentual(self, taxa):
        return Dinheiro(self.centavos * taxa // 100)

    def __str__(self):
        reais = self.centavos // 100
        centavos_restantes = self.centavos % 100
        return f"R$ {reais}.{centavos_restantes:02d}"


class Status:
    def __init__(self, codigo):
        self.codigo = codigo

    def esta_aberto(self):
        return self.codigo == "A"

    def esta_pago(self):
        return self.codigo == "P"

    def descrever(self):
        if self.codigo == "A":
            return "aberto"
        elif self.codigo == "P":
            return "pago"
        else:
            return "cancelado"

    def __str__(self):
        return self.descrever()


class Pessoa:
    def __init__(self, nome, cpf, email):
        self.nome = nome
        self.cpf = cpf
        self.email = email


class Endereco:
    def __init__(self, rua, cidade, cep):
        self.rua = rua
        self.cidade = cidade
        self.cep = cep


class Cliente:
    def __init__(self, pessoa, endereco, tipo):
        self.pessoa = pessoa
        self.endereco = endereco
        self.tipo = tipo


class Produto:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco


class ItemDoPedido:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade

    def calcular_subtotal(self):
        return self.produto.preco.multiplicar(self.quantidade)

    def imprimir(self):
        print("  ", self.quantidade, "x", self.produto.nome, "=", str(self.calcular_subtotal()))


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
            total = total.somar(item.calcular_subtotal())
        return total

    def imprimir(self):
        for item in self._itens:
            item.imprimir()


class Pedido:
    def __init__(self, cliente):
        self.cliente = cliente
        self.itens = ItensDoPedido()
        self.status = Status("A")

    def get_status(self):
        return self.status

    def set_status(self, novo_status):
        self.status = novo_status

    def adicionar_item(self, produto, quantidade):
        self.itens.adicionar(ItemDoPedido(produto, quantidade))


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
            print("Pedido", numero, "-", pedido.cliente.pessoa.nome, "-", pedido.cliente.endereco.cidade)
            print("  status:", str(pedido.get_status()))
            pedido.itens.imprimir()
            if not pedido.itens.esta_vazia():
                total = pedido.itens.calcular_total()
                desconto = calcular_desconto(pedido.cliente.tipo, total)
                valor_a_pagar = total.subtrair(desconto)
                print(f"  total: {total} | desconto: {desconto} | a pagar: {valor_a_pagar}")

    def calcular_total_arrecadado(self):
        total = Dinheiro(0)
        for numero in self._pedidos_por_numero:
            pedido = self._pedidos_por_numero[numero]
            if pedido.get_status().esta_pago():
                total_pedido = pedido.itens.calcular_total()
                desconto = calcular_desconto(pedido.cliente.tipo, total_pedido)
                total = total.somar(total_pedido.subtrair(desconto))
        return total

    def contar_pedidos_abertos(self):
        quantidade_abertos = 0
        for numero in self._pedidos_por_numero:
            pedido = self._pedidos_por_numero[numero]
            if pedido.get_status().esta_aberto():
                quantidade_abertos = quantidade_abertos + 1
        return quantidade_abertos


def calcular_desconto(tipo, total):
    if tipo == "V":
        desconto = total.percentual(10)
    elif tipo == "F":
        desconto = total.percentual(20)
    else:
        desconto = Dinheiro(0)
    return desconto


def pagar(pedido):
    if pedido.get_status().esta_aberto():
        if not pedido.itens.esta_vazia():
            pedido.set_status(Status("P"))
            return True
        else:
            return False
    else:
        return False


def cancelar(pedido):
    if pedido.get_status().esta_aberto():
        pedido.set_status(Status("C"))
        return True
    else:
        return False


# --- o roteiro da loja ---
pedidos = Pedidos()

caderno = Produto("Caderno", Dinheiro(1550))
caneta = Produto("Caneta", Dinheiro(250))
livro = Produto("Livro", Dinheiro(8950))
fone = Produto("Fone", Dinheiro(6000))

cliente_ana = Cliente(
    Pessoa("Ana Souza", Cpf("12345678901"), Email("ana@mail.com")),
    Endereco("Rua das Flores, 10", "Sorocaba", Cep("18010000")),
    "V",
)
primeiro_pedido_da_ana = pedidos.criar_pedido(1, cliente_ana)
primeiro_pedido_da_ana.adicionar_item(caderno, 2)
primeiro_pedido_da_ana.adicionar_item(caneta, 5)

try:
    cliente_bruno = Cliente(
        Pessoa("Bruno Lima", Cpf("123"), Email("bruno@mail.com")),
        Endereco("Av. Central, 200", "Votorantim", Cep("18110000")),
        "N",
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
        "F",
    )
    pedidos.criar_pedido(4, cliente_carla)
except ValueError as erro:
    print("pedido 4 recusado:", erro)

cliente_diego = Cliente(
    Pessoa("Diego Rocha", Cpf("11122233344"), Email("diego@mail.com")),
    Endereco("Rua Nova, 7", "Itu", Cep("13300000")),
    "N",
)
pedido_do_diego = pedidos.criar_pedido(5, cliente_diego)

cliente_eva = Cliente(
    Pessoa("Eva Nunes", Cpf("55566677788"), Email("eva@mail.com")),
    Endereco("Alameda Azul, 1", "Itu", Cep("13300001")),
    "F",
)
pedido_da_eva = pedidos.criar_pedido(6, cliente_eva)
pedido_da_eva.adicionar_item(fone, 1)

try:
    cliente_fabio = Cliente(
        Pessoa("Fabio Costa", Cpf("99988877766"), Email("fabio@mail.com")),
        Endereco("Rua Velha, 3", "Itu", Cep("123")),
        "N",
    )
    pedidos.criar_pedido(7, cliente_fabio)
except ValueError as erro:
    print("pedido 7 recusado:", erro)

cliente_gil = Cliente(
    Pessoa("Gil Alves", Cpf("44455566677"), Email("gil@mail.com")),
    Endereco("Rua do Meio, 9", "Sorocaba", Cep("18030000")),
    "N",
)
pedido_do_gil = pedidos.criar_pedido(8, cliente_gil)
pedido_do_gil.adicionar_item(fone, 2)

print("pagar 1:", pagar(primeiro_pedido_da_ana))
print("pagar 3:", pagar(segundo_pedido_da_ana))
print("pagar 5:", pagar(pedido_do_diego))
print("pagar 6:", pagar(pedido_da_eva))
print("cancelar 5:", cancelar(pedido_do_diego))
print("cancelar 1:", cancelar(primeiro_pedido_da_ana))

pedidos.imprimir_relatorio()
print("arrecadado:", str(pedidos.calcular_total_arrecadado()))
print("abertos:", pedidos.contar_pedidos_abertos())
