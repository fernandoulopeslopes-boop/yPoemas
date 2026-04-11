import streamlit as st
import os

# 1. SETUP E GEOMETRIA DE PRECISÃO
st.set_page_config(page_title="yPoemas", page_icon="ツ", layout="centered")

st.markdown("""
    <style>
    /* ZERAR ESPAÇOS DO TOPO */
    [data-testid="stHeader"] { visibility: hidden; height: 0px !important; }
    .main .block-container {
        max-width: 800px !important;
        padding-top: 0rem !important;
        margin-top: -50px !important;
    }

    /* BOTÕES: 30px, Cor do Chat (#f0f2f6) */
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
        box-shadow: none !important;
    }

    /* SELETOR: Ajuste para alinhamento à esquerda */
    div[data-testid="stSelectbox"] {
        margin: 0 !important;
    }
    label { display: none !important; }

    /* SIDEBAR: 320px */
    [data-testid="stSidebar"] { min-width: 320px !important; max-width: 320px !important; }
    
    hr { border: 0; height: 1px; background: linear-gradient(to right, transparent, #e0e0e0, transparent); margin: 0.5rem 0; }
    </style>
""", unsafe_allow_html=True)

# --- 2. BARRA DE COMANDO (Linha Única: Tema à Esquerda, Botões à Direita) ---
# Usamos colunas para ocupar o 1/3 central do palco (aprox. 300-350px)
_, col_barra, _ = st.columns([0.2, 2.6, 0.2])

with col_barra:
    # Divisão interna: 40% para a lista, 60% para os 5 botões agrupados
    c_lista, c_btns = st.columns([1.2, 1.4])
    
    with c_lista:
        try:
            arquivos = [f.replace(".ypo", "") for f in os.listdir("data") if f.endswith(".ypo")]
            st.selectbox("Tema", arquivos, key="main_palco_v33")
        except:
            st.write("Erro /data")
            
    with c_btns:
        # Sub-colunas para os 5 botões ficarem colados à direita
        n1, n2, n3, n4, n5 = st.columns(5)
        n1.button("+", key="v33_1")
        n2.button("<", key="v33_2")
        n3.button("*", key="v33_3")
        n4.button(">", key="v33_4")
        n5.button("?", key="v33_5")

st.markdown("<hr>", unsafe_allow_html=True)

# --- 3. SIDEBAR (Resgatando o ypo_seguro.py) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #f06292;'>ツ Machina</h1>", unsafe_allow_html=True)
    st.selectbox("Idioma", ["Português", "English", "Español", "Français"], key="lang_v33")
    st.markdown("---")
    col_s1, col_s2 = st.columns(2)
    col_s1.button("Talk", key="tk_v33")
    col_s2.button("Arte", key="art_v33")
    st.button("Share", key="sh_v33", use_container_width=True)

# --- 4. RENDERIZAÇÃO ---
st.markdown("<div style='text-align: center; color: #b0bec5; font-family: Georgia;'>v.33.0: Lista à Esquerda | Botões à Direita.</div>", unsafe_allow_html=True)
