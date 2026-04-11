import streamlit as st
import os

# 1. SETUP E GEOMETRIA (800px / 320px)
st.set_page_config(page_title="yPoemas", page_icon="ツ", layout="centered")

st.markdown("""
    <style>
    /* ZERAR HEADER E PADDING SUPERIOR */
    [data-testid="stHeader"] { visibility: hidden; height: 0px !important; }
    .main .block-container {
        max-width: 800px !important;
        padding-top: 0rem !important;
        margin-top: -50px !important;
    }

    /* BARRA ÚNICA: Flexbox para alinhar botões e lista */
    .comando-unica {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        width: 100%;
    }

    /* BOTÕES: 30px, Cor do Chat */
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

    /* SELETOR: Integrado na linha */
    div[data-testid="stSelectbox"] {
        width: 200px !important; /* Largura fixa para não empurrar os botões */
        margin: 0 !important;
    }
    label { display: none !important; }

    /* SIDEBAR: 320px */
    [data-testid="stSidebar"] { min-width: 320px !important; max-width: 320px !important; }
    
    hr { border: 0; height: 1px; background: linear-gradient(to right, transparent, #e0e0e0, transparent); margin: 0.5rem 0; }
    </style>
""", unsafe_allow_html=True)

# --- 2. BARRA DE COMANDO ALINHADA (Topo) ---
# Usando colunas para garantir que o conjunto ocupe o centro
_, col_barra, _ = st.columns([0.5, 2, 0.5])

with col_barra:
    # Criamos uma estrutura de colunas interna para alinhar tudo na mesma linha
    # 2 botões | Seletor | 3 botões
    c1, c2, c_sel, c3, c4, c5 = st.columns([0.2, 0.2, 1.2, 0.2, 0.2, 0.2])
    
    with c1: st.button("+", key="n1")
    with c2: st.button("<", key="n2")
    
    with c_sel:
        try:
            arquivos = [f.replace(".ypo", "") for f in os.listdir("data") if f.endswith(".ypo")]
            st.selectbox("Tema", arquivos, key="main_palco")
        except:
            st.write("Erro")
            
    with c3: st.button("*", key="n3")
    with c4: st.button(">", key="n4")
    with c5: st.button("?", key="n5")

st.markdown("<hr>", unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #f06292;'>ツ Machina</h1>", unsafe_allow_html=True)
    st.selectbox("Idioma", ["Português", "English", "Español"], key="lang")
    st.markdown("---")
    col_s1, col_s2 = st.columns(2)
    col_s1.button("Talk", key="tk")
    col_s2.button("Arte", key="art")

# --- 4. RENDERIZAÇÃO ---
st.markdown("<div style='text-align: center; color: #b0bec5; font-family: Georgia;'>v.32.9: Comando Único Alinhado. Espaço máximo liberado.</div>", unsafe_allow_html=True)
