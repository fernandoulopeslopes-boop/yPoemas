import streamlit as st
import os

# 1. SETUP E GEOMETRIA (800px / 320px)
st.set_page_config(page_title="yPoemas", page_icon="ツ", layout="centered")

st.markdown("""
    <style>
    /* SIDEBAR: Largura Fixa Rigorosa */
    [data-testid="stSidebar"] { 
        min-width: 320px !important; 
        max-width: 320px !important; 
    }
    
    /* PALCO: Container 800px com respiro para a Linha Zero */
    .main .block-container { 
        max-width: 800px !important; 
        padding-top: 4rem !important; 
    }

    /* BARRA FIXA NA LINHA ZERO (Topo Absoluto) */
    [data-testid="stHeader"] {
        background-color: rgba(255, 255, 255, 0) !important; /* Transparente para não chocar */
    }
    
    .topo-container {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 50px;
        background-color: #ffffff; /* Fundo limpo */
        z-index: 999999;
        display: flex;
        justify-content: center;
        align-items: center;
        border-bottom: 1px solid #f0f2f6;
    }

    /* BOTÕES: Cor de fundo do chat (#f0f2f6), Diâmetro 30px */
    div.stButton > button {
        background-color: #f0f2f6 !important; 
        color: #f06292 !important;           
        border-radius: 50% !important;
        width: 30px !important;
        height: 30px !important;
        min-width: 30px !important;
        border: 1px solid #e0e0e0 !important;
        font-size: 14px !important;
        padding: 0px !important;
        margin: 0 auto !important;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: none !important;
    }
    
    div.stButton > button:hover {
        background-color: #ffffff !important;
        border-color: #f06292 !important;
    }

    /* SELECTBOX: Centralizado no Palco */
    div[data-testid="stSelectbox"] {
        max-width: 300px;
        margin: 0 auto !important;
    }
    label { display: none !important; }
    
    hr { border: 0; height: 1px; background: linear-gradient(to right, transparent, #e0e0e0, transparent); margin: 1rem 0; }
    </style>
""", unsafe_allow_html=True)

# --- 2. NAVEGAÇÃO LINHA ZERO ---
# Criando o container via Streamlit columns para manter a funcionalidade dos botões
# O CSS acima se encarrega de posicionar este bloco no topo
topo = st.container()
with topo:
    _, col_centro, _ = st.columns([1, 1, 1]) # 1/3 do palco
    with col_centro:
        n1, n2, n3, n4, n5 = st.columns(5)
        n1.button("+", key="btn_add")
        n2.button("<", key="btn_prev")
        n3.button("*", key="btn_rand")
        n4.button(">", key="btn_next")
        n5.button("?", key="btn_help")

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #f06292; font-size: 28px;'>ツ Machina</h1>", unsafe_allow_html=True)
    st.selectbox("Idioma", ["Português", "English", "Español", "Français"], key="lang_v32")
    st.markdown("---")
    c1, c2 = st.columns(2)
    c1.button("Talk", key="tk_v32")
    c2.button("Arte", key="art_v32")
    st.button("Share", key="sh_v32", use_container_width=True)

# --- 4. PALCO: SELETOR DE TEMAS ---
# Logo abaixo da linha zero, centralizado.
st.markdown("<br>", unsafe_allow_html=True)
_, col_p, _ = st.columns([1, 1.5, 1])
with col_p:
    try:
        arquivos = [f.replace(".ypo", "") for f in os.listdir("data") if f.endswith(".ypo")]
        st.selectbox("Selecione o Palco", arquivos, key="palco_select")
    except:
        st.write("Pasta /data não encontrada")

st.markdown("<hr>", unsafe_allow_html=True)

# 5. CONTEÚDO
st.markdown("<div style='text-align: center; color: #b0bec5; font-family: Georgia; font-size: 18px;'>Modo Automático Ativado. Palco em Re-Build.</div>", unsafe_allow_html=True)
