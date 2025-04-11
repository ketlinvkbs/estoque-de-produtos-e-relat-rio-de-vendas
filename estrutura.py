import sqlite3
import csv
from datetime import datetime


class Gestao:
    def __init__(self, banco):
        self.conn = sqlite3.connect(banco)
        self.criar_tabela_estoque()
        self.criar_tabela_clientes()
        self.criar_tabela_vendas()
        self.criar_tabela_log()

    def criar_tabela_estoque(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS estoque (
                id INTEGER PRIMARY KEY,
                produto TEXT,
                marca TEXT,
                quantidade INTEGER
            )
        ''')
        self.conn.commit()

    def criar_tabela_clientes(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY,
                nome TEXT,
                telefone INTEGER
            )
        ''')
        self.conn.commit()

    def criar_tabela_vendas(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY,
                cliente_id INTEGER,
                produto_id INTEGER,
                quantidade INTEGER,
                data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id),
                FOREIGN KEY (produto_id) REFERENCES estoque(id)
            )
        ''')
        self.conn.commit()

    def criar_tabela_log(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS log_operacoes (
                id INTEGER PRIMARY KEY,
                operacao TEXT,
                produto TEXT,
                marca TEXT,
                quantidade INTEGER,
                data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    def registrar_operacao(self, operacao, produto, marca, quantidade):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO log_operacoes (operacao, produto, marca, quantidade) VALUES (?, ?, ?, ?)",
                       (operacao, produto, marca, quantidade))
        self.conn.commit()

    def adicionar_produto(self, produto, marca, quantidade):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT quantidade FROM estoque WHERE produto=? AND marca=?", (produto, marca))
            resultado = cursor.fetchone()
            if resultado:
                quantidade_existente = resultado[0]
                nova_quantidade = quantidade_existente + quantidade
                cursor.execute("UPDATE estoque SET quantidade=? WHERE produto=? AND marca=?", (nova_quantidade, produto, marca))
            else:
                cursor.execute("INSERT INTO estoque (produto, marca, quantidade) VALUES (?, ?, ?)", (produto, marca, quantidade))
            self.conn.commit()
            self.registrar_operacao('Adição', produto, marca, quantidade)
        except sqlite3.Error as e:
            print(f"Erro ao adicionar produto: {e}")

    def remover_produto(self, produto, marca, quantidade):
        cursor = self.conn.cursor()
        cursor.execute("SELECT quantidade FROM estoque WHERE produto=? AND marca=?", (produto, marca))
        resultado = cursor.fetchone()
        if resultado:
            estoque_atual = resultado[0]
            if estoque_atual >= quantidade:
                nova_quantidade = estoque_atual - quantidade
                if nova_quantidade > 0:
                    cursor.execute("UPDATE estoque SET quantidade=? WHERE produto=? AND marca=?", (nova_quantidade, produto, marca))
                else:
                    cursor.execute("DELETE FROM estoque WHERE produto=? AND marca=?", (produto, marca))
                self.conn.commit()
                self.registrar_operacao('Remoção', produto, marca, quantidade)
            else:
                print(f"Quantidade insuficiente de {produto} da marca {marca} no estoque.")
        else:
            print(f"{produto} da marca {marca} não encontrado no estoque.")

    def adicionar_cliente(self, nome, telefone):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO clientes (nome, telefone) VALUES (?, ?)", (nome, telefone))
        self.conn.commit()

    def registrar_venda(self, cliente_id, produto_id, quantidade):
        cursor = self.conn.cursor()
        cursor.execute("SELECT quantidade FROM estoque WHERE id=?", (produto_id,))
        resultado = cursor.fetchone()
        if resultado:
            estoque_atual = resultado[0]
            if estoque_atual >= quantidade:
                nova_quantidade = estoque_atual - quantidade
                cursor.execute("UPDATE estoque SET quantidade=? WHERE id=?", (nova_quantidade, produto_id))
                cursor.execute("INSERT INTO vendas (cliente_id, produto_id, quantidade) VALUES (?, ?, ?)",
                               (cliente_id, produto_id, quantidade))
                self.conn.commit()
                print("Venda registrada com sucesso!")
            else:
                print("Quantidade insuficiente no estoque.")
        else:
            print("Produto não encontrado no estoque.")

    def listar_produtos(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, produto, marca, quantidade FROM estoque")
        produtos = cursor.fetchall()
        return produtos

    def listar_clientes(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, nome, telefone FROM clientes")
        clientes = cursor.fetchall()
        return clientes

    def listar_vendas(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT vendas.id, clientes.nome, estoque.produto, vendas.quantidade, vendas.data_hora
            FROM vendas
            JOIN clientes ON vendas.cliente_id = clientes.id
            JOIN estoque ON vendas.produto_id = estoque.id
        ''')
        vendas = cursor.fetchall()
        return vendas

    def gerar_relatorio_mensal(self, ano, mes):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT operacao, produto, marca, quantidade, data_hora
            FROM log_operacoes
            WHERE strftime('%Y', data_hora) = ? AND strftime('%m', data_hora) = ?
        ''', (str(ano), f'{mes:02d}'))
        operacoes = cursor.fetchall()

        relatorio = f'relatorio_{ano}_{mes:02d}.csv'
        with open(relatorio, mode='w', newline='') as arquivo:
            escritor_csv = csv.writer(arquivo)
            escritor_csv.writerow(['Operação', 'Produto', 'Marca', 'Quantidade', 'Data/Hora'])
            escritor_csv.writerows(operacoes)

        print(f'Relatório gerado: {relatorio}')

    def __del__(self):
        self.conn.close()
