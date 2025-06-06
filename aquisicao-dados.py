# importando bibliotecas

import pandas as pd
import requests
import sqlite3 as sql
import os
from google.colab import files

# arquivo CSV

df = pd.read_csv('base_vendas.csv', encoding='utf-8', nrows=10)
df

# arquivo CSV, delimitador ';'

df = pd.read_csv('base_vendas_ponto_virgula.csv', sep=';')
df.head()

# arquivo TSV, delimitador 'tab'

df = pd.read_csv('base_vendas_tab.tsv', sep='\t')
df.head()

# arquivo Excel

df = pd.read_excel('Vendas.xlsx')
df.head()

# consultar planilhas
pd.ExcelFile('Vendas.xlsx').sheet_names

# arquivo Excel com parâmetros

df_vendas = pd.read_excel('Vendas.xlsx', sheet_name='base_vendas')
df_funcionarios = pd.read_excel('Vendas.xlsx', sheet_name='funcionarios')

df_vendas.head()
df_funcionarios.head()

# arquivo JSON

df = pd.read_json('base_vendas.json')
df.head()

# dados de API (ViaCEP) em arquivo JSON

resposta = requests.get('https://viacep.com.br/ws/01001000/json/')

if resposta.status_code == 200:
    dados = resposta.json()
    df = pd.DataFrame([dados])
else:
    print(f'Erro na requisição: {resposta.status_code}')

df.head()

# arquivo de um banco de dados

conn = sql.connect('vendas.db')
df = pd.read_sql_query('SELECT * FROM pedidos', conn)

df.head()

# consultar tabelas
pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", conn)

# consultar colunas
pd.read_sql_query("PRAGMA table_info(pedidos)", conn)

# arquivo HTML

tabelas = pd.read_html('base_vendas.html')

df = tabelas[0]
df.head()

# arquivo HTML extraído de site + filtro

tabelas = pd.read_html('https://pt.wikipedia.org/wiki/Lista_de_estados_do_Brasil_por_popula%C3%A7%C3%A3o')

for tabela in tabelas:
    if 'Estado' in tabela.columns or 'Unidade federativa' in tabela.columns:
        df = tabela
        break

df.head()

# automatização de leitura de arquivos CSV

pasta = 'dados/'
arquivos = os.listdir(pasta)

df_total = []

for arquivo in arquivos:
    if arquivo.endswith('.csv'):
        caminho = os.path.join(pasta, arquivo)
        df = pd.read_csv(caminho)
        df_total.append(df)

df_final = pd.concat(df_total, ignore_index=True)
df_final.head()

# salvando e exportando arquivo CSV

df_final.to_csv('resultado.csv', index=False)
files.download('resultado.csv')

# automatização de leitura de arquivos Excel

pasta = 'dados/'
arquivos = os.listdir(pasta)

df_total = []

for arquivo in arquivos:
    if arquivo.endswith('.xlsx'):
        caminho = os.path.join(pasta, arquivo)
        planilhas = pd.ExcelFile(caminho).sheet_names

        for planilha in planilhas:
            df = pd.read_excel(caminho, sheet_name=planilha)
            df_total.append(df)

df_final = pd.concat(df_total, ignore_index=True)
df_final.head()

# salvando e exportando arquivo Excel

df_final.to_excel('resultado.xlsx', index=False)
files.download('resultado.xlsx')
