import streamlit as st
import random
import os

# 1. CONFIGURAÇÃO E ESTILO (O "Esmero" Visual)
st.set_page_config(page_title="a Máquina de Fazer Poesia", page_icon="ツ", layout="centered")

st.markdown("""
    <style>
    /* Botões Circulares Rosa */
    div.stButton > button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        border: none;
        font-weight: bold;
        font-size: 20px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #ff3333;
        transform: scale(1.1);
    }
    /* Estética do Palco */
    .stSubheader {
        font-weight: 300;
        color: #31333F;
        letter-spacing: -0.5px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. INICIALIZAÇÃO DE ESTADO
if "page" not in st.session_state:
    st.session_state.page = "Demo"
if "tema_atual" not in st.session_state:
    st.session_state.tema_atual = "Mirante"

# 3. MOTOR DA MACHINA (Integrado v.28)
def motor_v28(tema):
    try:
        caminho = f"data/{tema}.ypo"
        with open(caminho, "r", encoding="utf-8") as f:
            linhas = f.read().splitlines()
        
        poema = []
        for l in linhas:
            txt = l.strip()
            # Filtro de metadados e marcas técnicas (F, números, caminhos de build)
            if (not txt or txt.startswith("#") or txt.startswith("*-") or 
                txt.startswith("<EOF>") or txt == "F" or txt.isdigit() or 
                "_" in txt):
                continue
                
            if "|" in txt:
                poema.append(random.choice(txt.split("|")))
            else:
                poema.append(txt)
        return poema
    except Exception as e:
        return [f"Erro no motor: {e}"]

# 4. SIDEBAR REFINADA
with st.sidebar:
    st.title("ツ Machina")
    try:
        arquivos = [f.replace(".ypo", "") for f in os.listdir("data") if f.endswith(".ypo")]
        st.session_state.tema_atual = st.selectbox("Palco", arquivos, index=arquivos.index(st.session_state.tema_atual) if st.session_state.tema_atual in arquivos else 0)
    except:
        st.error("Diretório /data inacessível")
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    c1.button("Talk")
    c2.button("Arte")
    st.button("Share", use_container_width=True)

# 5. NAVEGAÇÃO DE TOPO (Botões Circulares)
nav = st.columns([1,1,1,1,1])
botoes = ["+", "<", "*", ">", "?"]
paginas = ["Demo", "yPoemas", "Eureka", "Off-Machina", "About"]

for i, col in enumerate(nav):
    with col:
        if st.button(botoes[i]):
            st.session_state.page = paginas[i]

# 6. RENDERIZAÇÃO DO PALCO
st.markdown("---")

# Filtro de Página
if st.session_state.page == "Demo":
    versos = motor_v28(st.session_state.tema_atual)
    for v in versos:
        st.subheader(v)
else:
    st.info(f"Página {st.session_state.page} em construção.")

st.markdown("---")
