import os
import base64
import random
import streamlit as st
from lay_2_ypo import gera_poema

# --- CONFIGURAÇÃO DE PÁGINA (TRAVA O LAYOUT) ---
st.set_page_config(
    page_title="yPoemas",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CSS DE FORÇA BRUTA (PARA MATAR O "LIXÃO") ---
st.markdown(
    """ <style>
    /* 1. TRAVA A LARGURA DO SIDEBAR (CHEGA DE METADE DA TELA) */
    [data-testid="stSidebar"] {
        min-width: 350px !important;
        max-width: 350px !important;
        background-color: #000 !important;
    }

    /* 2. ALINHAMENTO DOS BOTÕES (A RÉGUA) */
    .stButton > button {
        width: 80px !important;
        height: 60px !important;
        border-radius: 0px !important;
        border: 2px solid #000 !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 22px !important;
        margin: 0 auto;
        display: block;
    }

    /* 3. O PALCO (CARA DE HTML PURO) */
    .main { background-color: #dcdcdc !important; }
    
    .palco-moldura {
        background-color: #fff;
        border: 1px solid #000;
        padding: 60px;
        max-width: 900px;
        margin: 40px auto;
        min-height: 800px;
        box-shadow: 30px 30px 0px #999;
        position: relative;
    }

    .poema-texto {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 28px;
        line-height: 1.5;
        color: #111;
    }

    .arte-tema {
        float: right;
        width: 300px;
        border: 1px solid #000;
        margin-left: 30px;
        filter: grayscale(100%);
    }

    /* Esconde elementos inúteis do Streamlit */
    div[data-testid="stToolbar"], footer, header { display: none !important; }
    </style> """,
    unsafe_allow_html=True,
)

# --- LOGICA DE ESTADO ---
if "poema_html" not in st.session_state:
    st.session_state.poema_html = ""

def get_img_b64(tema):
    path = f"./arts/{tema.lower()}.jpg"
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def disparar(tema):
    linhas = gera_poema(tema, "random")
    texto = "<br>".join(linhas)
    img_b64 = get_img_b64(tema)
    
    img_html = f'<img src="data:image/jpg;base64,{img_b64}" class="arte-tema">' if img_b64 else ""
    
    st.session_state.poema_html = f"""
    <div class="palco-moldura">
        {img_html}
        <div class="poema-texto">{texto}</div>
    </div>
    """

# --- SIDEBAR (FIXO EM 350PX) ---
with st.sidebar:
    st.markdown("### MACHINA")
    st.selectbox("LIVRO", ["livro vivo", "arquivo morto"], key="bk")
    st.toggle("Artes", value=True, key="art")

# --- NAVEGAÇÃO (BOTÕES ALINHADOS) ---
# Usamos colunas com pesos iguais para garantir o alinhamento horizontal
_, b1, b2, b3, b4, b5, _ = st.columns([2, 1, 1, 1, 1, 1, 2])

with b1: 
    if st.button("+"): pass
with b2: 
    if st.button("<"): pass
with b3: 
    if st.button("*"): disparar("Fatos")
with b4: 
    if st.button(">"): pass
with b5: 
    if st.button("⚒️"): pass

st.markdown("---")

# --- COMANDO ---
c_in, c_go = st.columns([5, 1])
with c_in:
    t_sel = st.selectbox("Selecione:", ["Fatos", "Tempo", "Anjos"], label_visibility="collapsed")
with c_go:
    if st.button("GO"): disparar(t_sel)

# --- RENDER DO PALCO ---
if st.session_state.poema_html:
    st.markdown(st.session_state.poema_html, unsafe_allow_html=True)
