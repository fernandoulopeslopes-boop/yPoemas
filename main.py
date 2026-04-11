import streamlit as st
import random
import os

# 1. SETUP INICIAL
st.set_page_config(page_title="a Máquina de Fazer Poesia", page_icon="ツ", layout="centered")

# 2. ESTADO
if "page" not in st.session_state:
    st.session_state.page = "Demo"
if "tema_atual" not in st.session_state:
    st.session_state.tema_atual = "Mirante"

# 3. MOTOR REFINADO (Lê o arquivo .ypo respeitando os metadados)
def motor_ypo(tema):
    try:
        caminho = f"data/{tema}.ypo"
        with open(caminho, "r", encoding="utf-8") as f:
            linhas = f.read().splitlines()
        
        poema = []
        for l in linhas:
            # Ignora metadados e linhas de controle do fim do arquivo
            if l.startswith("#") or l.startswith("<EOF>") or not l.strip():
                continue
            # Ignora linhas que são apenas números de controle (ex: 00, 02, 12)
            if l.strip().isdigit():
                continue
                
            if "|" in l:
                poema.append(random.choice(l.split("|")))
            else:
                poema.append(l)
        return poema
    except Exception as e:
        return [f"Erro ao acessar {tema}: {e}"]

# 4. SIDEBAR (Configurações)
with st.sidebar:
    st.title("ツ Machina")
    # Dropdown de temas
    arquivos = [f.replace(".ypo", "") for f in os.listdir("data") if f.endswith(".ypo")]
    st.session_state.tema_atual = st.selectbox("Palco", arquivos, index=arquivos.index(st.session_state.tema_atual) if st.session_state.tema_atual in arquivos else 0)
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    c1.button("Talk")
    c2.button("Arte")
    st.button("Share")

# 5. NAVEGAÇÃO ( + < * > ? )
nav = st.columns(5)
with nav[0]: 
    if st.button("+"): st.session_state.page = "Demo"
with nav[1]: 
    if st.button("<"): st.session_state.page = "yPoemas"
with nav[2]: 
    if st.button("*"): st.session_state.page = "Eureka"
with nav[3]: 
    if st.button(">"): st.session_state.page = "Off-Machina"
with nav[4]: 
    if st.button("?"): st.session_state.page = "About"

# 6. O PALCO
st.markdown("---")
versos = motor_ypo(st.session_state.tema_atual)

for v in versos:
    st.subheader(v)
