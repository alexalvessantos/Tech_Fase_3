import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import urllib
from sklearn.linear_model import LinearRegression
import joblib

# Carregar variáveis do .env
load_dotenv()

# String de conexão
params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={os.getenv('DB_SERVER')},{os.getenv('DB_PORT')};"
    f"DATABASE={os.getenv('DB_NAME')};"
    f"UID={os.getenv('DB_USER')};"
    f"PWD={os.getenv('DB_PASS')};"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# Ler dados da tabela
df = pd.read_sql("SELECT Idade, Salario FROM Dados", engine)

# Separar variáveis
X = df[["Idade"]]
y = df["Salario"]

# Treinar modelo
modelo = LinearRegression()
modelo.fit(X, y)

# Salvar modelo treinado
joblib.dump(modelo, "ml/modelo.pkl")

print("✅ Modelo treinado e salvo com sucesso!")
