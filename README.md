# TF 11 - Refatoração com Object Calisthenics

## 1. Normalização
Normalizar consiste em registrar cada entidade uma única vez na memória e fazer os demais objetos referenciarem essa mesma instância. Na loja original, os dados da cliente Ana Souza estavam duplicados nos pedidos 1 e 3; com a classe `Cliente`, criamos `cliente_ana` apenas uma vez e ambos os pedidos apontam para o mesmo objeto (assim como o produto `fone`, compartilhado entre os pedidos 6 e 8).

## 2. Obsessão por tipos primitivos
Transformar o `Cpf` em classe impede que um texto inválido como `"123"` circule pelo sistema, pois a validação ocorre imediatamente no construtor e garante que todo objeto `Cpf` existente seja válido. Já a classe `Dinheiro` armazena os valores internamente como centavos inteiros (`int`) porque números de ponto flutuante (`float`) sofrem imprecisões de representação binária (como `0.1 + 0.2 != 0.3`), o que causaria erros de arredondamento em somas e descontos financeiros.

## 3. Diga, não pergunte
Antes, uma função externa consultava `pedido.get_st()` para decidir se podia mudar o status com `pedido.set_st("P")`, espalhando a regra de negócio para fora da classe. Agora chamamos diretamente `pedido.pagar()` e `pedido.cancelar()`, encapsulando a regra (só pagar pedido aberto com itens; só cancelar pedido aberto) dentro do próprio `Pedido`, sem expor atributos nem getters/setters.

## 4. Fail first
O *hadouken* estava principalmente na função `valida` (quatro `if`s aninhados com `else` para checar email, CPF e CEP) e na função `pagar`. Ele foi eliminado levando cada validação para o construtor da sua respectiva classe (`Email`, `Cpf`, `Cep`) com cláusulas de guarda, e usando retorno antecipado em `pagar()` e `cancelar()`, enquanto a cadeia de `if/elif/else` do cálculo de desconto foi substituída por polimorfismo nas classes de tipo de cliente.

## 5. Modularização — Responsabilidade das classes
- `Cpf`: Validar e representar um número de CPF com exatamente 11 caracteres.
- `Email`: Validar e representar um endereço de e-mail não vazio que contenha `@`.
- `Cep`: Validar e representar um código de CEP com exatamente 8 caracteres.
- `Dinheiro`: Representar valores monetários em centavos inteiros e executar operações de soma, subtração, multiplicação e percentual.
- `Status`: Representar o código de estado de um pedido (`A`, `P` ou `C`), informar se está aberto/pago e fornecer sua descrição textual.
- `TipoNormal`: Aplicar a política de desconto de 0% para clientes comuns.
- `TipoVip`: Aplicar a política de desconto de 10% para clientes VIP.
- `TipoFuncionario`: Aplicar a política de desconto de 20% para clientes funcionários.
- `Pessoa`: Agrupar os dados de identificação pessoal do cliente (nome, CPF e e-mail).
- `Endereco`: Agrupar os dados de localização física do cliente (rua, cidade e CEP).
- `Cliente`: Unir os dados pessoais, o endereço e a categoria de desconto do comprador.
- `Produto`: Representar um item comercializado pela loja com seu nome e preço unitário.
- `ItemDoPedido`: Associar um produto a uma quantidade comprada e calcular o subtotal daquela linha.
- `ItensDoPedido`: Encapsular a coleção de itens de um pedido, calculando o total bruto e imprimindo suas linhas.
- `Pedido`: Controlar o ciclo de vida de uma compra (adicionar itens, pagar, cancelar, calcular valores e imprimir seu resumo).
- `Pedidos`: Encapsular o dicionário de pedidos da loja, emitindo o relatório geral e consolidando o total arrecadado e o número de pedidos abertos.

## 6. Dívida técnica
Todas as regras propostas foram aplicadas sem atalhos. A regra mais desafiadora foi manter apenas um nível de indentação por método combinado com um único ponto por linha na coleção `Pedidos`: para somar o total arrecadado e contar os pedidos abertos sem colocar um `if` dentro do `for`, foi necessário delegar a decisão de valor arrecadado para `Pedido.valor_arrecadado()` e extrair o predicado `_pedido_esta_aberto()`.
