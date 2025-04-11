from texte2 import Gestao
import sys

def saida():
    print('Deseja realizar outra ação?')
    operacao = input('s (para sim), n (para não)')
    if operacao == "n":
        print('Fim do programa!')
        sys.exit()
        

gestao = Gestao('banco.db')
while True:
        print('Bem-vindo ao seu gestor de vendas!')
        print('Que ação você deseja realizar?')
        print('Temos as seguintes ações disponíveis no momento:')
        print('1- Adicionar produto')
        print('2- Remover produto')
        print('3- Adicionar cliente')
        print('4- Registrar venda')
        print('5- Listar produtos')
        print('6- Listar clientes')
        print('7- Listar vendas')
        print('8- Gerar relatório')
        print('9- Sair')
    
        escolha = input('Digite o número da ação desejada: ')

        if escolha == '1':
            produto = input('Digite o nome do produto: ')
            marca = input('Digite a marca do produto: ')
            quantidade = int(input('Digite a quantidade: '))
            gestao.adicionar_produto(produto, marca, quantidade)
            print('Produto adicionado com sucesso!')
            saida()

        elif escolha == '2':
            produto = input('Digite o nome do produto: ')
            marca = input('Digite a marca do produto: ')
            quantidade = int(input('Digite a quantidade a remover: '))
            gestao.remover_produto(produto, marca, quantidade)
            print('Produto removido com sucesso!')
            saida()

        elif escolha == '3':
            nome = input('Digite o nome do cliente: ')
            telefone = input('Digite o telefone do cliente: ')
            gestao.adicionar_cliente(nome, telefone)
            print('Cliente adicionado com sucesso!')
            saida()

        elif escolha == '4':
            cliente_id = int(input('Digite o ID do cliente: '))
            produto_id = int(input('Digite o ID do produto: '))
            quantidade = int(input('Digite a quantidade: '))
            gestao.registrar_venda(cliente_id, produto_id, quantidade)
            saida()

        elif escolha == '5':
            produtos = gestao.listar_produtos()
            for produto in produtos:
                print(f'ID: {produto[0]}, Produto: {produto[1]}, Marca: {produto[2]}, Quantidade: {produto[3]}')
            saida()

        elif escolha == '6':
            clientes = gestao.listar_clientes()
            for cliente in clientes:
                print(f'ID: {cliente[0]}, Nome: {cliente[1]}, Telefone: {cliente[2]}')
            saida()

        elif escolha == '7':
            vendas = gestao.listar_vendas()
            for venda in vendas:
                print(f'ID: {venda[0]}, Cliente: {venda[1]}, Produto: {venda[2]}, Quantidade: {venda[3]}, Data/Hora: {venda[4]}')
            saida()
        elif escolha == '8':
            ano = int(input('Digite o ano do relatório: '))
            mes = int(input('Digite o mês do relatório: '))
            gestao.gerar_relatorio_mensal(ano, mes)
            saida()

        elif escolha == '9':
            print('Saindo do sistema...')
            break

        else:
            print('Opção inválida. Tente novamente.')
        
        operacao = input('Deseja realizar outra ação? (s para sim, n para não): ')
        if operacao.lower() == 'n':
            print('Fim do programa!')
            break

    
