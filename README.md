# Sistema de Gestão de Vendas e Estoque

## Introdução

Este projeto tem como objetivo desenvolver um sistema de gestão de vendas e estoque simples, utilizando **Python** e **SQLite**. A aplicação é executada via terminal, permitindo ao usuário:

- Cadastrar produtos e clientes  
- Registrar vendas  
- Gerar relatórios mensais  
- Acompanhar histórico de alterações no estoque  
- Consultar dados cadastrados em tempo real  

---

## Descrição das Tabelas e Campos

### `estoque`

- `id`: Identificador único do produto (chave primária)  
- `produto`: Nome do produto  
- `marca`: Marca do produto  
- `quantidade`: Quantidade disponível no estoque  

### `clientes`

- `id`: Identificador único do cliente (chave primária)  
- `nome`: Nome do cliente  
- `telefone`: Telefone do cliente  

### `vendas`

- `id`: Identificador da venda (chave primária)  
- `cliente_id`: ID do cliente (chave estrangeira)  
- `produto_id`: ID do produto (chave estrangeira)  
- `quantidade`: Quantidade vendida  
- `data_hora`: Data e hora da venda  

### `log_operacoes`

- `id`: Identificador do log  
- `operacao`: Tipo de operação realizada (Adição ou Remoção)  
- `produto`: Nome do produto  
- `marca`: Marca do produto  
- `quantidade`: Quantidade afetada  
- `data_hora`: Data e hora da operação  

---

## Execução do Código

Exemplo de uso via terminal:

```bash
$ python main.py
Bem-vindo ao seu gestor de vendas!
Que ação você deseja realizar?
1- Adicionar produto
2- Remover produto
...

