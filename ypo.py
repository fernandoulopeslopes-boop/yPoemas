import os
import base64
import streamlit as st
from lay_2_ypo import gera_poema

# --- CONFIGURAÇÃO DE PÁGINA ---
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# --- CSS: O TRATAMENTO DE CHOQUE ---
st.markdown(
    """ <style>
    /* 1. TRAVA A SIDEBAR (300px FIXOS) */
    [data-testid="stSidebar"] {
        min-width: 300px !important;
        max-width: 300px !important;
        background-color: #000 !important;
    }
    [data-testid="stSidebar"] * { color: #fff !important; }

    /* 2. ALINHAMENTO DOS BOTÕES (A RÉGUA) */
    /* Remove o 'gap' que o Streamlit coloca entre colunas */
    [data-testid="column"] {
        display: flex !important;
        justify-content: center !important;
        padding: 0 5px !important;
    }

    .stButton > button {
        width: 85px !important;
        height: 65px !important;
        border-radius: 0px !important;
        border: 2px solid #000 !important;
        background-color: #fff !important;
        color: #000 !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 26px !important;
        font-weight: 600 !important;
        transition: 0.1s;
    }

    .stButton > button:hover {
        background-color: #000 !important;
        color: #fff !important;
        box-shadow: 8px 8px 0px #bbb;
    }

    /* 3. O PALCO (HTML PURO) */
    .stApp { background-color: #f0f0f0 !important; }

    .palco-moldura {
        background-color: #ffffff;
        border: 1px solid #000;
        padding: 70px;
        margin: 40px auto;
        max-width: 900px;
        min-height: 800px;
        box-shadow: 40px 40px 0px #ccc;
        position: relative;
    }

    .poema-texto {
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 300;
        font-size: 32px;
        color: #111;
        line-height: 1.4;
        white-space: pre-wrap;
    }

    /* Limpeza de Interface */
    header, footer, [data-testid="stToolbar"] { display: none !important; }
    </style> """,
    unsafe_allow_html=True,
)

# --- INICIALIZAÇÃO DE ESTADO (EVITA A EXCEÇÃO) ---
if "poema_gerado" not in st.session_state:
    st.session_state.poema_gerado = ""

def acionar_machina(tema):
    try:
        # Gera o poema e limpa a lista para string HTML
        resultado = gera_poema(tema, "random")
        st.session_state.poema_gerado = "<br>".join(resultado)
    except Exception as e:
        st.session_state.poema_gerado = f"Erro na Machina: {e}"

# --- NAVEGAÇÃO DE TOPO (+ < * > ⚒️) ---
# Usamos colunas centrais com pesos idênticos
_, b1, b2, b3, b4, b5, _ = st.columns([3, 1, 1, 1, 1, 1, 3])

with b1: 
    if st.button("+"): pass
with b2: 
    if st.button("<"): pass
with b3: 
    # O botão central '*' dispara o tema padrão para teste
    if st.button("*"): acionar_machina("Fatos")
with b4: 
    if st.button(">"): pass
with b5: 
    if st.button("⚒️"): pass

st.markdown("<br>", unsafe_allow_html=True)

# --- COMANDO DE ENTRADA ---
# Se os nomes aparecem colados, é porque o selectbox precisa de um container limpo
c_in, c_go = st.columns([5, 1])
with c_in:
    opcoes = ["Fatos", "Tempo", "Anjos", "Manifesto"]
    tema_selecionado = st.selectbox("Gatilho:", opcoes, label_visibility="collapsed")
with c_go:
    if st.button("GO"):
        acionar_machina(tema_selecionado)

# --- RENDERIZAÇÃO DO PALCO FINAL ---
if st.session_state.poema_gerado:
    st.markdown(f"""
    <div class="palco-moldura">
        <div class="poema-texto">
            {st.session_state.poema_gerado}
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Estado inicial: Palco vazio ou instrução
    st.markdown("""
    <div class="palco-moldura">
        <div class="poema-texto" style="color: #bbb; text-align: center; margin-top: 200px;">
            Aguardando Gatilho...
        </div>
    </div>
    """, unsafe_allow_html=True)
