import streamlit as st
import os

# 1. SETUP E GEOMETRIA DE TOPO
st.set_page_config(page_title="yPoemas", page_icon="ツ", layout="centered")

st.markdown("""
    <style>
    /* ZERAR HEADER E SUBIR PALCO */
    [data-testid="stHeader"] { visibility: hidden; height: 0px !important; }
    .main .block-container {
        max-width: 800px !important;
        padding-top: 0rem !important;
        margin-top: -55px !important;
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

    /* SELECTBOX: Largura reduzida por 2 (Compacta) */
    div[data-testid="stSelectbox"] {
        margin: 0 !important;
        width: 130px !important; /* Metade do tamanho anterior */
    }
    label { display: none !important; }

    /* SIDEBAR: 320px */
    [data-testid="stSidebar"] { min-width: 320px !important; max-width: 320px !important; }
    
    hr { border: 0; height: 1px; background: linear-gradient(to right, transparent, #e0e0e0, transparent); margin: 0.5rem 0; }
    </style>
""", unsafe_allow_html=True)

# --- 2. BARRA DE COMANDO (Botões à Esquerda | Lista 50% à Direita) ---
# Centralizado no Palco
_, col_barra, _ = st.columns([0.2, 2.6, 0.2])

with col_barra:
    # Proporção 1.8 para 0.7 garante a lista curta e os botões agrupados
    c_btns, c_lista = st.columns([1.8, 0.7])
    
    with c_btns:
        # Grupo de 5 botões de ação colados
        n1, n2, n3, n4, n5 = st.columns(5)
        n1.button("+", key="v33_2_1")
        n2.button("<", key="v33_2_2")
        n3.button("*", key="v33_2_3")
        n4.button(">", key="v33_2_4")
        n5.button("?", key="v33_2_5")

    with c_lista:
        try:
            # Lista com largura cortada para temas curtos
            arquivos = [f.replace(".ypo", "") for f in os.listdir("data") if f.endswith(".ypo")]
            st.selectbox("Tema", arquivos, key="main_palco_v33_2")
        except:
            st.write("Erro /data")

st.markdown("<hr>", unsafe_allow_html=True)

# --- 3. SIDEBAR (Estrutura ypo_seguro.py) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #f06292;'>ツ Machina</h1>", unsafe_allow_html=True)
    st.selectbox("Idioma", ["Português", "English", "Español", "Français"], key="lang_v33_2")
    st.markdown("---")
    col_s1, col_s2 = st.columns(2)
    col_s1.button("Talk", key="tk_v33_2")
    col_s2.button("Arte", key="art_v33_2")

# --- 4. CONTEÚDO ---
st.markdown("<div style='text-align: center; color: #b0bec5; font-family: Georgia;'>v.33.2: Botões Prioritários | Lista 50% de largura.</div>", unsafe_allow_html=True)
