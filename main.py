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

@app.get("/")
def root():
    return {"message": "API está rodando!"}

@app.post("/login")
def login(dados: LoginRequest):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        query = "SELECT Login, Senha FROM Usuarios WHERE Login = ?"
        cursor.execute(query, (dados.login))
        resultado = cursor.fetchone()

        cursor.close()
        conexao.close()
        
        if resultado:
            return {"message": f"Teste {resultado[0]}"}
        else:
            return {"message": "Usuário não identificado."}
    
    except Exception as e:
        return {"success": False, "erro": str(e)}