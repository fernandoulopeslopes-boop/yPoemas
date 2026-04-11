import streamlit as st
import os

# 1. SETUP E REFORMATAÇÃO DO CONTAINER (Aumentando a "estatura" do palco)
st.set_page_config(page_title="yPoemas", page_icon="ツ", layout="centered")

st.markdown("""
    <style>
    /* 1. DESATIVAR HEADER PADRÃO (Ocupa espaço fantasma) */
    [data-testid="stHeader"] { visibility: hidden; height: 0% !important; }

    /* 2. REFORMATAÇÃO DO CONTAINER PRINCIPAL (O PALCO) */
    .main .block-container {
        max-width: 800px !important;
        padding-top: 0rem !important;    /* Remove o recuo superior */
        padding-bottom: 0rem !important;
        margin-top: -60px !important;    /* Sobe o container inteiro para o limite da tela */
        height: 100vh;                   /* Força a altura para ocupar a visão toda */
    }

    /* 3. BOTÕES NA LINHA ZERO (Sutis e Integrados) */
    div.stButton > button {
        background-color: #f0f2f6 !important; /* Cor do chat */
        color: #f06292 !important;
        border-radius: 50% !important;
        width: 30px !important;
        height: 30px !important;
        min-width: 30px !important;
        border: 1px solid #e0e0e0 !important;
        font-size: 14px !important;
        margin: 0 auto !important;
        padding: 0px !important;
        box-shadow: none !important;
    }

    /* 4. SELECTBOX (LISTA DE TEMAS): Colada nos botões */
    div[data-testid="stSelectbox"] {
        max-width: 250px;
        margin: -10px auto 0 auto !important; /* Sobe para quase encostar nos botões */
    }
    
    label { display: none !important; }

    /* 5. SIDEBAR: 320px */
    [data-testid="stSidebar"] { min-width: 320px !important; max-width: 320px !important; }

    hr { border: 0; height: 1px; background: linear-gradient(to right, transparent, #e0e0e0, transparent); margin: 1rem 0; }
    </style>
""", unsafe_allow_html=True)

# --- 2. NAVEGAÇÃO (LINHA ZERO) ---
# Centralizada em 1/3 do palco, mas agora no topo físico da página
_, col_nav, _ = st.columns([1, 1, 1])
with col_nav:
    n1, n2, n3, n4, n5 = st.columns(5)
    n1.button("+", key="n1")
    n2.button("<", key="n2")
    n3.button("*", key="n3")
    n4.button(">", key="n4")
    n5.button("?", key="n5")

# --- 3. SELETOR DE TEMAS (PALCO) ---
_, col_t, _ = st.columns([1, 1.2, 1])
with col_t:
    try:
        arquivos = [f.replace(".ypo", "") for f in os.listdir("data") if f.endswith(".ypo")]
        st.selectbox("Palco", arquivos, key="main_palco")
    except:
        st.write("Erro /data")

st.markdown("<hr>", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #f06292;'>ツ Machina</h1>", unsafe_allow_html=True)
    st.selectbox("Idioma", ["Português", "English", "Español"], key="lang")
    st.markdown("---")
    c1, c2 = st.columns(2)
    c1.button("Talk", key="tk")
    c2.button("Arte", key="art")

# --- 5. RENDERIZAÇÃO ---
st.markdown("<div style='text-align: center; color: #b0bec5; font-family: Georgia;'>v.32.8: Container expandido e deslocado para o Topo Absoluto.</div>", unsafe_allow_html=True)
