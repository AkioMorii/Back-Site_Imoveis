import pyodbc

def conectar():
    dados_conexao = (
        "Driver={SQL SERVER};"
        "Server=SeuServer;"
        "Database=SuaDatabase;"
        "Trusted_Connection=yes;"
    )
    conexao = pyodbc.connect(dados_conexao)
    return conexao
