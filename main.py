import streamlit as st
import os

# 1. SETUP E GEOMETRIA (800px / 320px)
st.set_page_config(page_title="yPoemas", page_icon="ツ", layout="centered")

st.markdown("""
    <style>
    /* SIDEBAR: Largura Fixa e Cor Sutil */
    [data-testid="stSidebar"] { 
        min-width: 320px !important; 
        max-width: 320px !important; 
        background-color: #fafafa;
    }
    
    /* PALCO: Container 800px Centralizado */
    .main .block-container { 
        max-width: 800px !important; 
        padding-top: 1.5rem; 
    }

    /* MENU NAVEGAÇÃO: Limitado a 1/3 do Palco */
    .nav-wrapper {
        width: 33%;
        margin: 0 auto;
    }

    /* BOTÕES: Rosa Pastel, 32px Diâmetro */
    div.stButton > button {
        background-color: #fce4ec !important;
        color: #f06292 !important;
        border-radius: 50% !important;
        width: 32px !important;
        height: 32px !important;
        min-width: 32px !important;
        border: 1px solid #f8bbd0 !important;
        font-size: 14px !important;
        padding: 0px !important;
        margin: 0 auto !important;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: 0.2s;
    }
    div.stButton > button:hover {
        background-color: #f8bbd0 !important;
        transform: scale(1.1);
    }

    /* SELECTBOX NO PALCO: Sem label e centralizado */
    .stSelectbox label { display: none !important; }
    div[data-testid="stSelectbox"] {
        max-width: 280px;
        margin: 0 auto !important;
    }
    
    hr { border: 0; height: 1px; background: linear-gradient(to right, transparent, #f8bbd0, transparent); margin: 1.5rem 0; }
    </style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR (Reintegração do Controle) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #f06292;'>ツ Machina</h1>", unsafe_allow_html=True)
    
    # Lista de Idiomas Ocidentais (O Pacto)
    idiomas = ["Português", "English", "Español", "Français", "Italiano", "Deutsch", "Nederlands"]
    st.selectbox("Idioma", idiomas, key="side_lang")
    
    st.markdown("---")
    
    # Botões de Ação Lateral (Baseados no ypo_seguro.py)
    c1, c2 = st.columns(2)
    c1.button("Talk", key="side_tk")
    c2.button("Arte", key="side_art")
    
    st.markdown("---")
    st.button("Share", key="side_sh", use_container_width=True)

# --- 3. PALCO: NAVEGAÇÃO (1/3 da largura) ---
_, col_nav, _ = st.columns([1, 1, 1])
with col_nav:
    n1, n2, n3, n4, n5 = st.columns(5)
    n1.button("+")
    n2.button("<")
    n3.button("*")
    n4.button(">")
    n5.button("?")

# --- 4. PALCO: SELETOR DE TEMAS ---
st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
_, col_tema, _ = st.columns([1, 1.5, 1])
with col_tema:
    try:
        arquivos = [f.replace(".ypo", "") for f in os.listdir("data") if f.endswith(".ypo")]
        st.selectbox("Palco", arquivos, key="palco_main")
    except:
        st.error("Pasta /data não encontrada")

st.markdown("<hr>", unsafe_allow_html=True)

# 5. RENDERIZAÇÃO
st.markdown("<div style='text-align: center; color: #f06292; font-family: Georgia;'>Palco e Sidebar reintegrados.</div>", unsafe_allow_html=True)
