import streamlit as st
import os
import random
from deep_translator import GoogleTranslator

# TESTE DE SOBREVIVÊNCIA DA MACHINA
st.set_page_config(page_title="Diagnóstico Machina", layout="wide")

st.title("📜 Diagnóstico de Sistema")

st.write("### 1. Verificação de Ambiente")
st.info(f"Versão do Python detectada: {os.sys.version}")

st.write("### 2. Teste de Dependências")
try:
    translator = GoogleTranslator(source='auto', target='en')
    st.success("✅ deep_translator: OK")
except Exception as e:
    st.error(f"❌ deep_translator: FALHOU ({e})")

st.write("### 3. Teste de Motor (PAI)")
if os.path.exists("lay_2_ypo.py"):
    st.success("✅ lay_2_ypo.py: LOCALIZADO")
    try:
        from lay_2_ypo import gera_poema
        st.success("✅ Importação do Motor: OK")
    except Exception as e:
        st.error(f"❌ Falha ao importar Motor: {e}")
else:
    st.warning("⚠️ Arquivo lay_2_ypo.py não encontrado na raiz.")

st.write("---")
st.write("Se você está vendo esta página, o Streamlit está vivo. O erro anterior era provocado por algum componente visual ou importação pesada que o Python 3.14 não aceitou.")
