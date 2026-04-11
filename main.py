import streamlit as st
import os

# 1. SETUP E GEOMETRIA RADICAL
st.set_page_config(page_title="yPoemas", page_icon="ツ", layout="centered")

st.markdown("""
    <style>
    /* SIDEBAR: Fixa em 320px */
    [data-testid="stSidebar"] { min-width: 320px !important; max-width: 320px !important; }
    
    /* PALCO: 800px */
    .main .block-container { max-width: 800px !important; padding-top: 1rem; }

    /* FORÇAR TAMANHO E COR DOS BOTÕES (Identidade v.32.1) */
    div.stButton > button {
        background-color: #fce4ec !important; /* Rosa muito suave (quase off-white) */
        color: #f06292 !important;           /* Texto rosa mais escuro para contraste */
        border-radius: 50% !important;
        width: 32px !important;               /* Diâmetro pequeno e elegante */
        height: 32px !important;
        min-width: 32px !important;
        border: 1px solid #f8bbd0 !important;
        font-size: 14px !important;
        margin: 0 auto !important;
        padding: 0px !important;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Centralizar o bloco de navegação em 1/3 do palco */
    .nav-container {
        width: 33%;
        margin: 0 auto;
    }

    /* Ajuste de margem do Selectbox no Palco */
    .stSelectbox {
        max-width: 300px;
        margin: 0 auto !important;
        padding-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. NAVEGAÇÃO (Centralizada e Reduzida)
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)
with col1: st.button("+")
with col2: st.button("<")
with col3: st.button("*")
with col4: st.button(">")
with col5: st.button("?")
st.markdown('</div>', unsafe_allow_html=True)

# 3. SELETOR DE TEMAS (Agora no Palco)
st.markdown("---")
# Centralizado abaixo da navegação
_, col_center, _ = st.columns([1, 2, 1])
with col_center:
    try:
        arquivos = [f.replace(".ypo", "") for f in os.listdir("data") if f.endswith(".ypo")]
        st.selectbox("Palco", arquivos, label_visibility="collapsed", key="palco_palco")
    except:
        st.write("Verifique a pasta /data")

st.markdown("---")

# 4. CONTEÚDO (Poesia)
st.markdown("<div style='text-align: center; font-family: Georgia; font-style: italic;'>O palco está pronto.</div>", unsafe_allow_html=True)
