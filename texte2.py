import sqlite3
import tkinter as tk
from tkinter import messagebox
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
                email TEXT
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

    def adicionar_cliente(self, nome, email):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO clientes (nome, email) VALUES (?, ?)", (nome, email))
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
        cursor.execute("SELECT id, nome, email FROM clientes")
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

        nome_arquivo = f'relatorio_{ano}_{mes:02d}.csv'
        with open(nome_arquivo, mode='w', newline='') as arquivo:
            escritor_csv = csv.writer(arquivo)
            escritor_csv.writerow(['Operação', 'Produto', 'Marca', 'Quantidade', 'Data/Hora'])
            escritor_csv.writerows(operacoes)

        print(f'Relatório gerado: {nome_arquivo}')

    def __del__(self):
        self.conn.close()

def adicionar_produto():
    produto = entry_produto.get()
    marca = entry_marca.get()
    try:
        quantidade = int(entry_quantidade.get())
        if produto and marca and quantidade > 0:
            sistema.adicionar_produto(produto, marca, quantidade)
            messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
        else:
            messagebox.showerror("Erro", "Preencha todos os campos corretamente.")
    except ValueError:
        messagebox.showerror("Erro", "Quantidade deve ser um número inteiro.")

def remover_produto():
    produto = entry_produto.get()
    marca = entry_marca.get()
    try:
        quantidade = int(entry_quantidade.get())
        if produto and marca and quantidade > 0:
            sistema.remover_produto(produto, marca, quantidade)
            messagebox.showinfo("Sucesso", "Produto removido com sucesso!")
            listar_produtos()
        else:
            messagebox.showerror("Erro", "Preencha todos os campos corretamente.")
    except ValueError:
        messagebox.showerror("Erro", "Quantidade deve ser um número inteiro.")

def listar_produtos():
    produtos = sistema.listar_produtos()
    lista_produtos.delete(0, tk.END)
    for produto in produtos:
        lista_produtos.insert(tk.END, f"{produto[0]} - {produto[1]} - {produto[2]}: {produto[3]} unidades")

def adicionar_cliente():
    nome = entry_nome.get()
    email = entry_email.get()
    if nome and email:
        sistema.adicionar_cliente(nome, email)
        messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso!")
    else:
        messagebox.showerror("Erro", "Preencha todos os campos corretamente.")

def listar_clientes():
    clientes = sistema.listar_clientes()
    lista_clientes.delete(0, tk.END)
    for cliente in clientes:
        lista_clientes.insert(tk.END, f"{cliente[0]} - {cliente[1]} - {cliente[2]}")

def registrar_venda():
    try:
        cliente_id = int(entry_cliente_id.get())
        produto_id = int(entry_produto_id.get())
        quantidade = int(entry_quantidade_venda.get())
        sistema.registrar_venda(cliente_id, produto_id, quantidade)
        messagebox.showinfo("Sucesso", "Venda registrada com sucesso!")
        listar_produtos()
    except ValueError:
        messagebox.showerror("Erro", "IDs e quantidade devem ser números inteiros.")

def listar_vendas():
    vendas = sistema.listar_vendas()
    lista_vendas.delete(0, tk.END)
    for venda in vendas:
        lista_vendas.insert(tk.END, f"{venda[0]} - {venda[1]} - {venda[2]}: {venda[3]} unidades em {venda[4]}")

def gerar_relatorio():
    try:
        ano = int(entry_ano.get())
        mes = int(entry_mes.get())
        sistema.gerar_relatorio_mensal(ano, mes)
        messagebox.showinfo("Sucesso", f"Relatório gerado para {mes}/{ano}!")
    except ValueError: