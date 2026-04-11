import streamlit as st
import random
import os

# 1. Configuração inicial (Obrigatório ser a primeira)
st.set_page_config(page_title="yPoemas", layout="centered")

# 2. Inicialização de Estado
if "page" not in st.session_state:
    st.session_state.page = "Demo"
if "tema_atual" not in st.session_state:
    st.session_state.tema_atual = "Restos"

# 3. Sidebar Minimalista
with st.sidebar:
    st.title("ツ Machina")
    # Tenta listar arquivos da pasta data
    try:
        arquivos = [f.replace(".ypo", "") for f in os.listdir("data") if f.endswith(".ypo")]
        st.session_state.tema_atual = st.selectbox("Palco", arquivos)
    except:
        st.error("Pasta /data não encontrada")
    
    st.markdown("---")
    st.button("Talk")
    st.button("Arte")

# 4. Navegação de Topo (Simples para teste)
cols = st.columns(5)
with cols[0]:
    if st.button("+"): st.session_state.page = "Demo"
with cols[1]:
    if st.button("<"): st.session_state.page = "yPoemas"
with cols[2]:
    if st.button("*"): st.session_state.page = "Eureka"
with cols[3]:
    if st.button(">"): st.session_state.page = "Off-Machina"
with cols[4]:
    if st.button("?"): st.session_state.page = "About"

# 5. O Motor (Integrado para evitar erros de import)
def gera_poema_raiz(tema):
    try:
        caminho = f"data/{tema}.ypo"
        with open(caminho, "r", encoding="utf-8") as f:
            linhas = f.read().splitlines()
        
        resultado = []
        for l in linhas:
            if "|" in l:
                resultado.append(random.choice(l.split("|")))
            else:
                resultado.append(l)
        return resultado
    except Exception as e:
        return [f"Erro no motor: {e}"]

# 6. Renderização no Palco
st.markdown("---")
poema = gera_poema_raiz(st.session_state.tema_atual)

for verso in poema:
    if verso.strip() == "":
        st.write("")
    else:
        st.subheader(verso)
