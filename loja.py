# Passo 2: Todos os nomes abreviados foram trocados por nomes inteiros em portugues.

pedidos = []


class Pedido:
    def __init__(self, numero, nome_do_cliente, cpf_do_cliente, email_do_cliente, rua, cidade, cep, tipo):
        self.numero = numero
        self.nome_do_cliente = nome_do_cliente
        self.cpf_do_cliente = cpf_do_cliente
        self.email_do_cliente = email_do_cliente
        self.rua = rua
        self.cidade = cidade
        self.cep = cep
        self.tipo = tipo
        self.itens = []
        self.status = "A"

    def get_status(self):
        return self.status

    def set_status(self, novo_status):
        self.status = novo_status


def validar_dados(email_do_cliente, cpf_do_cliente, cep):
    if len(email_do_cliente) > 0:
        if "@" in email_do_cliente:
            if len(cpf_do_cliente) == 11:
                if len(cep) == 8:
                    return "ok"
                else:
                    return "cep invalido"
            else:
                return "cpf invalido"
        else:
            return "email invalido"
    else:
        return "email vazio"


def novo_pedido(numero, nome_do_cliente, cpf_do_cliente, email_do_cliente, rua, cidade, cep, tipo):
    resultado_da_validacao = validar_dados(email_do_cliente, cpf_do_cliente, cep)
    if resultado_da_validacao != "ok":
        print("pedido", numero, "recusado:", resultado_da_validacao)
        return None
    else:
        pedido = Pedido(numero, nome_do_cliente, cpf_do_cliente, email_do_cliente, rua, cidade, cep, tipo)
        pedidos.append(pedido)
        return pedido


def adicionar_item(pedido, produto, quantidade, preco):
    pedido.itens.append([produto, quantidade, preco])


def calcular_total(pedido):
    total = 0
    for item in pedido.itens:
        total = total + item[1] * item[2]
    return total


def calcular_desconto(tipo, total):
    if tipo == "V":
        desconto = total * 0.10
    elif tipo == "F":
        desconto = total * 0.20
    else:
        desconto = 0
    return desconto


def calcular_valor_a_pagar(pedido):
    return calcular_total(pedido) - calcular_desconto(pedido.tipo, calcular_total(pedido))


def pagar(pedido):
    if pedido.get_status() == "A":
        if len(pedido.itens) > 0:
            pedido.set_status("P")
            return True
        else:
            return False
    else:
        return False


def cancelar(pedido):
    if pedido.get_status() == "A":
        pedido.set_status("C")
        return True
    else:
        return False


def descrever_status(status):
    if status == "A":
        return "aberto"
    elif status == "P":
        return "pago"
    else:
        return "cancelado"


def imprimir_relatorio():
    for pedido in pedidos:
        print("Pedido", pedido.numero, "-", pedido.nome_do_cliente, "-", pedido.cidade)
        print("  status:", descrever_status(pedido.get_status()))
        for item in pedido.itens:
            print("  ", item[1], "x", item[0], "= R$ %.2f" % (item[1] * item[2]))
        if len(pedido.itens) > 0:
            print(
                "  total: R$ %.2f | desconto: R$ %.2f | a pagar: R$ %.2f"
                % (calcular_total(pedido), calcular_desconto(pedido.tipo, calcular_total(pedido)), calcular_valor_a_pagar(pedido))
            )


def calcular_total_arrecadado():
    total = 0
    for pedido in pedidos:
        if pedido.get_status() == "P":
            total = total + calcular_valor_a_pagar(pedido)
    return total


def contar_pedidos_abertos():
    quantidade_abertos = 0
    for pedido in pedidos:
        if pedido.get_status() == "A":
            quantidade_abertos = quantidade_abertos + 1
    return quantidade_abertos


# --- o roteiro da loja ---
primeiro_pedido_da_ana = novo_pedido(1, "Ana Souza", "12345678901", "ana@mail.com", "Rua das Flores, 10", "Sorocaba", "18010000", "V")
adicionar_item(primeiro_pedido_da_ana, "Caderno", 2, 15.5)
adicionar_item(primeiro_pedido_da_ana, "Caneta", 5, 2.5)

novo_pedido(2, "Bruno Lima", "123", "bruno@mail.com", "Av. Central, 200", "Votorantim", "18110000", "N")

segundo_pedido_da_ana = novo_pedido(3, "Ana Souza", "12345678901", "ana@mail.com", "Rua das Flores, 10", "Sorocaba", "18010000", "V")
adicionar_item(segundo_pedido_da_ana, "Livro", 1, 89.5)

novo_pedido(4, "Carla Dias", "98765432100", "carla.mail.com", "Rua do Sol, 55", "Sorocaba", "18020000", "F")

pedido_do_diego = novo_pedido(5, "Diego Rocha", "11122233344", "diego@mail.com", "Rua Nova, 7", "Itu", "13300000", "N")

pedido_da_eva = novo_pedido(6, "Eva Nunes", "55566677788", "eva@mail.com", "Alameda Azul, 1", "Itu", "13300001", "F")
adicionar_item(pedido_da_eva, "Fone", 1, 60.0)

novo_pedido(7, "Fabio Costa", "99988877766", "fabio@mail.com", "Rua Velha, 3", "Itu", "123", "N")

pedido_do_gil = novo_pedido(8, "Gil Alves", "44455566677", "gil@mail.com", "Rua do Meio, 9", "Sorocaba", "18030000", "N")
adicionar_item(pedido_do_gil, "Fone", 2, 60.0)

print("pagar 1:", pagar(primeiro_pedido_da_ana))
print("pagar 3:", pagar(segundo_pedido_da_ana))
print("pagar 5:", pagar(pedido_do_diego))
print("pagar 6:", pagar(pedido_da_eva))
print("cancelar 5:", cancelar(pedido_do_diego))
print("cancelar 1:", cancelar(primeiro_pedido_da_ana))

imprimir_relatorio()
print("arrecadado: R$ %.2f" % calcular_total_arrecadado())
print("abertos:", contar_pedidos_abertos())
