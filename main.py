from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from conexao import conectar

app = FastAPI()

# CORS para permitir chamadas do SvelteKit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    login: str
    senha: str

class Imovel(BaseModel):
    local: str
    cep: str
    descricao: str

@app.get("/")
def root():
    return {"message": "API está rodando!"}

@app.post("/login")
def login(dados: LoginRequest):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        query = "SELECT Usuario_Id, Nome, Login, Senha FROM Usuarios WHERE Login = ? and Senha = ?"
        cursor.execute(query, (dados.login, dados.senha))
        resultado = cursor.fetchone()

        cursor.close()
        conexao.close()
        
        if resultado:
            usuario = {'id': resultado[0], 'name': resultado[1]}
            return {"message": "Autenticado", "usuario": usuario}
        else:
            return {"message": "Usuário não identificado."}
    
    except Exception as e:
        return {"success": False, "erro": str(e)}

@app.get("/imoveis")
def lista_imoveis():
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        query = """
        SELECT Local, Cep, Descricao, CONTRATOS.contrato_id 
        FROM IMOVEIS 
        LEFT JOIN CONTRATOS ON IMOVEIS.Imovel_Id = CONTRATOS.Imovel_Id
        """
        
        cursor.execute(query)
        resultado = cursor.fetchall()

        cursor.close()
        conexao.close()

        if resultado:
            imoveis = [{"local": row[0], "cep": row[1], "descricao": row[2], "contrato_Id": row[3]} for row in resultado]
            return {"imoveis": imoveis}
        else:
            return {"imoveis": []}

    except Exception as e:
        return {"success": False, "erro": str(e)}

# Criar um novo imóvel
@app.post("/imoveis")
def criar_imovel(imovel: Imovel):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        query = """
        INSERT INTO IMOVEIS (Local, Cep, Descricao) 
        VALUES (?, ?, ?)
        """
        
        cursor.execute(query, (imovel.local, imovel.cep, imovel.descricao))
        conexao.commit()
        cursor.close()
        conexao.close()

        return {"message": "Imóvel criado com sucesso!"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar imóvel: {str(e)}")

# Atualizar um imóvel
@app.put("/imoveis/{imovel_id}")
def atualizar_imovel(imovel_id: int, imovel: Imovel):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        query = """
        UPDATE IMOVEIS 
        SET Local = ?, Cep = ?, Descricao = ? 
        WHERE Imovel_Id = ?
        """
        
        cursor.execute(query, (imovel.local, imovel.cep, imovel.descricao, imovel_id))
        conexao.commit()
        cursor.close()
        conexao.close()

        return {"message": "Imóvel atualizado com sucesso!"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar imóvel: {str(e)}")

# Excluir um imóvel
@app.delete("/imoveis/{imovel_id}")
def excluir_imovel(imovel_id: int):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        query = "DELETE FROM IMOVEIS WHERE Imovel_Id = ?"
        
        cursor.execute(query, (imovel_id,))
        conexao.commit()
        cursor.close()
        conexao.close()

        return {"message": "Imóvel excluído com sucesso!"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao excluir imóvel: {str(e)}")
