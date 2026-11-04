# Passo 4: Embrulha os primitivos em Cpf, Email, Cep, Dinheiro e Status.

pedidos = []


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


class Cliente:
    def __init__(self, nome, cpf, email, rua, cidade, cep, tipo):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.rua = rua
        self.cidade = cidade
        self.cep = cep
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


class Pedido:
    def __init__(self, numero, cliente):
        self.numero = numero
        self.cliente = cliente
        self.itens = []
        self.status = Status("A")

    def get_status(self):
        return self.status

    def set_status(self, novo_status):
        self.status = novo_status


def novo_pedido(numero, cliente):
    pedido = Pedido(numero, cliente)
    pedidos.append(pedido)
    return pedido


def adicionar_item(pedido, produto, quantidade):
    pedido.itens.append(ItemDoPedido(produto, quantidade))


def calcular_total(pedido):
    total = Dinheiro(0)
    for item in pedido.itens:
        total = total.somar(item.calcular_subtotal())
    return total


def calcular_desconto(tipo, total):
    if tipo == "V":
        desconto = total.percentual(10)
    elif tipo == "F":
        desconto = total.percentual(20)
    else:
        desconto = Dinheiro(0)
    return desconto


def calcular_valor_a_pagar(pedido):
    total = calcular_total(pedido)
    desconto = calcular_desconto(pedido.cliente.tipo, total)
    return total.subtrair(desconto)


def pagar(pedido):
    if pedido.get_status().esta_aberto():
        if len(pedido.itens) > 0:
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


def imprimir_relatorio():
    for pedido in pedidos:
        print("Pedido", pedido.numero, "-", pedido.cliente.nome, "-", pedido.cliente.cidade)
        print("  status:", str(pedido.get_status()))
        for item in pedido.itens:
            print("  ", item.quantidade, "x", item.produto.nome, "=", str(item.calcular_subtotal()))
        if len(pedido.itens) > 0:
            total = calcular_total(pedido)
            desconto = calcular_desconto(pedido.cliente.tipo, total)
            valor_a_pagar = calcular_valor_a_pagar(pedido)
            print(f"  total: {total} | desconto: {desconto} | a pagar: {valor_a_pagar}")


def calcular_total_arrecadado():
    total = Dinheiro(0)
    for pedido in pedidos:
        if pedido.get_status().esta_pago():
            total = total.somar(calcular_valor_a_pagar(pedido))
    return total


def contar_pedidos_abertos():
    quantidade_abertos = 0
    for pedido in pedidos:
        if pedido.get_status().esta_aberto():
            quantidade_abertos = quantidade_abertos + 1
    return quantidade_abertos


# --- o roteiro da loja ---
caderno = Produto("Caderno", Dinheiro(1550))
caneta = Produto("Caneta", Dinheiro(250))
livro = Produto("Livro", Dinheiro(8950))
fone = Produto("Fone", Dinheiro(6000))

cliente_ana = Cliente(
    "Ana Souza", Cpf("12345678901"), Email("ana@mail.com"), "Rua das Flores, 10", "Sorocaba", Cep("18010000"), "V"
)
primeiro_pedido_da_ana = novo_pedido(1, cliente_ana)
adicionar_item(primeiro_pedido_da_ana, caderno, 2)
adicionar_item(primeiro_pedido_da_ana, caneta, 5)

try:
    cliente_bruno = Cliente(
        "Bruno Lima", Cpf("123"), Email("bruno@mail.com"), "Av. Central, 200", "Votorantim", Cep("18110000"), "N"
    )
    novo_pedido(2, cliente_bruno)
except ValueError as erro:
    print("pedido 2 recusado:", erro)

segundo_pedido_da_ana = novo_pedido(3, cliente_ana)
adicionar_item(segundo_pedido_da_ana, livro, 1)

try:
    cliente_carla = Cliente(
        "Carla Dias", Cpf("98765432100"), Email("carla.mail.com"), "Rua do Sol, 55", "Sorocaba", Cep("18020000"), "F"
    )
    novo_pedido(4, cliente_carla)
except ValueError as erro:
    print("pedido 4 recusado:", erro)

cliente_diego = Cliente(
    "Diego Rocha", Cpf("11122233344"), Email("diego@mail.com"), "Rua Nova, 7", "Itu", Cep("13300000"), "N"
)
pedido_do_diego = novo_pedido(5, cliente_diego)

cliente_eva = Cliente(
    "Eva Nunes", Cpf("55566677788"), Email("eva@mail.com"), "Alameda Azul, 1", "Itu", Cep("13300001"), "F"
)
pedido_da_eva = novo_pedido(6, cliente_eva)
adicionar_item(pedido_da_eva, fone, 1)

try:
    cliente_fabio = Cliente(
        "Fabio Costa", Cpf("99988877766"), Email("fabio@mail.com"), "Rua Velha, 3", "Itu", Cep("123"), "N"
    )
    novo_pedido(7, cliente_fabio)
except ValueError as erro:
    print("pedido 7 recusado:", erro)

cliente_gil = Cliente(
    "Gil Alves", Cpf("44455566677"), Email("gil@mail.com"), "Rua do Meio, 9", "Sorocaba", Cep("18030000"), "N"
)
pedido_do_gil = novo_pedido(8, cliente_gil)
adicionar_item(pedido_do_gil, fone, 2)

print("pagar 1:", pagar(primeiro_pedido_da_ana))
print("pagar 3:", pagar(segundo_pedido_da_ana))
print("pagar 5:", pagar(pedido_do_diego))
print("pagar 6:", pagar(pedido_da_eva))
print("cancelar 5:", cancelar(pedido_do_diego))
print("cancelar 1:", cancelar(primeiro_pedido_da_ana))

imprimir_relatorio()
print("arrecadado:", str(calcular_total_arrecadado()))
print("abertos:", contar_pedidos_abertos())
