import pyodbc

def conectar():
    dados_conexao = (
        "Driver={SQL SERVER};"
        "Server=akio;"
        "Database=site_imoveis;"
        "Trusted_Connection=yes;"
    )
    conexao = pyodbc.connect(dados_conexao)
    return conexao
