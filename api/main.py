from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import urllib

# Carregar variáveis do .env
load_dotenv()

# Configurar string de conexão
params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={os.getenv('DB_SERVER')},{os.getenv('DB_PORT')};"
    f"DATABASE={os.getenv('DB_NAME')};"
    f"UID={os.getenv('DB_USER')};"
    f"PWD={os.getenv('DB_PASS')};"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# Iniciar FastAPI
app = FastAPI()

# Modelo de entrada
class DadoEntrada(BaseModel):
    nome: str
    idade: int
    salario: float

# ✅ Rota GET / (status)
@app.get("/")
def read_root():
    return {"mensagem": "API rodando com sucesso!"}

# ✅ Rota POST /coletar
@app.post("/coletar")
def coletar_dado(dado: DadoEntrada):
    with engine.begin() as conn:  # engine.begin() faz commit automaticamente
        query = text("""
            INSERT INTO Dados (Nome, Idade, Salario)
            VALUES (:nome, :idade, :salario)
        """)
        conn.execute(query, {
            "nome": dado.nome,
            "idade": dado.idade,
            "salario": dado.salario
        })
    return {"mensagem": "Dado inserido com sucesso"}

# ✅ Rota GET /dados
@app.get("/dados")
def listar_dados():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT Id, Nome, Idade, Salario, CriadoEm FROM Dados"))
        dados = [dict(row) for row in result]
    return {"dados": dados}
