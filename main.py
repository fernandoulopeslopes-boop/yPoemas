import streamlit as st
import os

# 1. SETUP E GEOMETRIA DE TOPO (Resgatando as setas da Sidebar)
st.set_page_config(page_title="yPoemas", page_icon="ツ", layout="centered")

st.markdown("""
    <style>
    /* DESATIVAR APENAS O FUNDO DO HEADER PARA MANTER AS SETAS <<< */
    [data-testid="stHeader"] { 
        background-color: rgba(0,0,0,0) !important; 
        color: #f06292 !important;
    }

    /* POSICIONAMENTO DO PALCO */
    .main .block-container {
        max-width: 800px !important;
        padding-top: 0.5rem !important;
        margin-top: -35px !important;
    }

    /* BOTÕES: Ícones em Negrito, 32px, Cor do Chat */
    div.stButton > button {
        background-color: #f0f2f6 !important;
        color: #f06292 !important;
        border-radius: 50% !important;
        width: 32px !important;
        height: 32px !important;
        min-width: 32px !important;
        border: 1px solid #d1d5db !important;
        font-size: 18px !important; /* Aumentado para visibilidade */
        font-weight: 900 !important; /* Negrito extremo */
        padding: 0px !important;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* SELECTBOX: Largura 50% */
    div[data-testid="stSelectbox"] {
        width: 130px !important;
        margin: 0 !important;
    }
    label { display: none !important; }

    /* LINHAS DIVISÓRIAS (HR) ALINHADAS */
    /* No palco */
    .main hr { 
        border: 0; 
        height: 1px; 
        background: #e0e0e0; 
        margin: 10px 0 !important; 
    }
    /* Na sidebar */
    [data-testid="stSidebar"] hr { 
        border: 0; 
        height: 1px; 
        background: #e0e0e0; 
        margin: 14px 0 !important; 
    }

    /* SIDEBAR: Largura 320px */
    [data-testid="stSidebar"] { min-width: 320px !important; max-width: 320px !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. BARRA DE COMANDO (Botões Negrito | Lista 50%) ---
_, col_barra, _ = st.columns([0.1, 2.8, 0.1])

with col_barra:
    c_btns, c_lista = st.columns([1.6, 0.8])
    
    with c_btns:
        n1, n2, n3, n4, n5 = st.columns(5)
        # Ícones originais em strings para garantir renderização limpa
        n1.button("＋", key="v33_3_1") 
        n2.button("＜", key="v33_3_2")
        n3.button("＊", key="v33_3_3")
        n4.button("＞", key="v33_3_4")
        n5.button("？", key="v33_3_5")

    with c_lista:
        try:
            arquivos = [f.replace(".ypo", "") for f in os.listdir("data") if f.endswith(".ypo")]
            st.selectbox("Tema", arquivos, key="main_palco_v33_3")
        except:
            st.write("Erro")

st.markdown("<hr>", unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #f06292;'>ツ Machina</h2>", unsafe_allow_html=True)
    st.selectbox("Idioma", ["Português", "English", "Español"], key="lang_v33_3")
    st.markdown("---") # Linha divisória da sidebar
    
    col_s1, col_s2 = st.columns(2)
    col_s1.button("Talk", key="tk_v33_3", use_container_width=True)
    col_s2.button("Arte", key="art_v33_3", use_container_width=True)

# --- 4. PALCO ---
st.markdown("<div style='text-align: center; color: #b0bec5; font-family: Georgia;'>v.33.3: Ícones em Negrito e Linhas Alinhadas.</div>", unsafe_allow_html=True)
