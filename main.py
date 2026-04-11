import streamlit as st
import random
import os

# 1. ARQUITETURA DE INTERFACE (Refinamento v.30)
st.set_page_config(page_title="a Máquina de Fazer Poesia", page_icon="ツ", layout="centered")

st.markdown("""
    <style>
    /* Reset de margens e centralização */
    .block-container { padding-top: 2rem; }
    
    /* Botões Circulares Rosa (Identidade Visual) */
    div.stButton > button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 50% !important;
        width: 50px !important;
        height: 50px !important;
        border: none;
        font-weight: bold;
        font-size: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: auto;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: 0.2s;
    }
    div.stButton > button:hover {
        background-color: #ff3333;
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.2);
    }
    
    /* Estilo dos Versos (Subheaders limpos) */
    .stSubheader {
        font-family: 'serif';
        font-weight: 400;
        text-align: center;
        color: #1E1E1E;
        padding: 0.2rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# 2. GESTÃO DE ESTADO (PTC: Persistent State)
if "page" not in st.session_state: st.session_state.page = "Demo"
if "tema_atual" not in st.session_state: st.session_state.tema_atual = "Mirante"

# 3. O MOTOR (Baseado nas análises de filtro de metadados)
def motor_v30(tema):
    try:
        caminho = f"data/{tema}.ypo"
        with open(caminho, "r", encoding="utf-8") as f:
            linhas = f.read().splitlines()
        
        poema = []
        for l in linhas:
            txt = l.strip()
            # Filtros aplicados conforme suas análises:
            if (not txt or                     # Linhas vazias
                txt.startswith("#") or         # Comentários
                txt.startswith("*-") or        # Separadores de build
                txt.startswith("<EOF>") or     # Fim de arquivo
                txt == "F" or                  # Marcador F
                txt.isdigit() or               # IDs numéricos (00, 02, 10...)
                "_" in txt):                   # Tags de build (ex: Mirante_0402)
                continue
                
            if "|" in txt:
                poema.append(random.choice(txt.split("|")))
            else:
                poema.append(txt)
        return poema
    except Exception as e:
        return [f"Erro: {e}"]

# 4. SIDEBAR (Talk, Arte, Share)
with st.sidebar:
    st.title("ツ Machina")
    try:
        arquivos = [f.replace(".ypo", "") for f in os.listdir("data") if f.endswith(".ypo")]
        st.session_state.tema_atual = st.selectbox("Selecione o Palco", arquivos, 
                                                   index=arquivos.index(st.session_state.tema_atual) if st.session_state.tema_atual in arquivos else 0)
    except:
        st.error("Diretório /data não encontrado.")
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1: st.button("Talk")
    with c2: st.button("Arte")
    st.button("Share", use_container_width=True)

# 5. NAVEGAÇÃO SUPERIOR ( + < * > ? )
nav = st.columns(5)
btns = ["+", "<", "*", ">", "?"]
pgs = ["Demo", "yPoemas", "Eureka", "Off-Machina", "About"]

for i, col in enumerate(nav):
    with col:
        if st.button(btns[i]):
            st.session_state.page = pgs[i]

# 6. RENDERIZAÇÃO DO PALCO
st.markdown("---")

if st.session_state.page == "Demo":
    versos = motor_v30(st.session_state.tema_atual)
    for v in versos:
        st.subheader(v)
else:
    st.write(f"### Seção {st.session_state.page}")
    st.info("Em desenvolvimento...")

st.markdown("---")
