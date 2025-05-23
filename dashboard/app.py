import streamlit as st
import joblib

st.title("Previsão de Salário")

st.write("🔍 Carregando modelo...")

try:
    modelo = joblib.load("ml/modelo.pkl")
    st.write("✅ Modelo carregado com sucesso!")
except Exception as e:
    st.error(f"❌ Erro ao carregar modelo: {e}")

idade = st.slider("Informe sua idade:", 18, 80, 30)

try:
    salario = modelo.predict([[idade]])
    st.success(f"Salário estimado: R$ {salario[0]:.2f}")
except Exception as e:
    st.error(f"❌ Erro na previsão: {e}")
