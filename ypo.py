import os
import base64
import streamlit as st
from lay_2_ypo import gera_poema

# --- CONFIGURAÇÃO ---
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# --- CSS DE IMPACTO (TRAVA SIDEBAR E BOTÕES) ---
st.markdown(
    """ <style>
    /* 1. TRAVA A SIDEBAR (IMPEDE QUE OCUPE METADE DA TELA) */
    [data-testid="stSidebar"] {
        min-width: 300px !important;
        max-width: 300px !important;
        width: 300px !important;
    }

    /* 2. FUNDO DO SITE (CARA DE HTML, NÃO DASHBOARD) */
    .stApp {
        background-color: #dfdfdf !important;
    }

    /* 3. ALINHAMENTO DOS BOTÕES (+ < * > ⚒️) */
    /* Remove o espaçamento bizarro entre colunas do Streamlit */
    [data-testid="column"] {
        display: flex !important;
        justify-content: center !important;
        padding: 0 !important;
    }

    .stButton > button {
        width: 80px !important;
        height: 60px !important;
        border-radius: 0px !important;
        border: 2px solid #000 !important;
        background-color: #fff !important;
        color: #000 !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 24px !important;
        font-weight: 600 !important;
        line-height: 1 !important;
    }

    .stButton > button:hover {
        background-color: #000 !important;
        color: #fff !important;
    }

    /* 4. O PALCO (A MOLDURA DO POEMA) */
    .palco-moldura {
        background-color: #ffffff;
        border: 1px solid #000;
        padding: 50px 70px;
        margin: 20px auto;
        width: 90% !important;
        max-width: 950px !important; /* Evita desproporção em telas ultra-wide */
        min-height: 700px;
        box-shadow: 30px 30px 0px #ababab;
        position: relative;
    }

    .poema-texto {
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 300;
        font-size: 30px;
        color: #111;
        line-height: 1.4;
    }

    .arte-tema {
        float: right;
        width: 320px;
        margin-left: 30px;
        border: 1px solid #000;
        filter: grayscale(100%);
    }

    /* Limpeza de UI */
    footer, header, [data-testid="stToolbar"] { display: none !important; }
    </style> """,
    unsafe_allow_html=True,
)

# --- NAVEGAÇÃO ---
# O segredo do alinhamento: colunas com a mesma proporção [1,1,1,1,1]
_, b1, b2, b3, b4, b5, _ = st.columns([3, 1, 1, 1, 1, 1, 3])

with b1: st.button("+")
with b2: st.button("<")
with b3: 
    if st.button("*"): 
        st.session_state.poema = gera_poema("Fatos", "random")
with b4: st.button(">")
with b5: st.button("⚒️")

st.markdown("---")

# --- AREA DE COMANDO ---
c1, c2 = st.columns([5, 1])
with c1:
    tema = st.selectbox("Gatilho:", ["Fatos", "Tempo", "Anjos"], label_visibility="collapsed")
with c2:
    if st.button("GO"):
        st.session_state.poema = gera_poema(tema, "random")

# --- RENDER DO PALCO ---
if "poema" in st.session_state:
    texto_formatado = "<br>".join(st.session_state.poema)
    st.markdown(f"""
    <div class="palco-moldura">
        <div class="poema-texto">
            {texto_formatado}
        </div>
    </div>
    """, unsafe_allow_html=True)
