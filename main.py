import streamlit as st
import os

# --- 1. CONFIGURAÇÃO DE HARDWARE VIRTUAL (Sem intrusos) ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
    <style>
    /* DESATIVAR HEADER PADRÃO */
    [data-testid="stHeader"] { display: none !important; }

    /* SIDEBAR: Fixa em 320px | Título Removido (Zap) */
    [data-testid="stSidebar"] { 
        min-width: 320px !important; 
        max-width: 320px !important; 
        padding-top: 0px !important;
    }

    /* PALCO: Centralização absoluta no espaço restante */
    .main .block-container {
        max-width: 800px !important;
        margin: 0 auto !important;
        padding-top: 1rem !important;
    }

    /* BOTÕES: Black Negrito Profundo com Espaçamento (Gap) */
    div.stButton > button {
        background-color: #f0f2f6 !important;
        color: #000000 !important;
        border-radius: 50% !important;
        width: 34px !important;
        height: 34px !important;
        min-width: 34px !important;
        border: 2px solid #000000 !important;
        font-size: 20px !important;
        font-weight: 900 !important;
        padding: 0px !important;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: 0.2s;
    }
    
    /* Forçar espaçamento entre colunas de botões */
    [data-testid="column"] {
        padding-left: 5px !important;
        padding-right: 5px !important;
    }

    /* SELECTBOX: 50% de largura, integrada à direita */
    div[data-testid="stSelectbox"] {
        width: 140px !important;
        margin-left: 15px !important; /* Afasta o seletor do último botão (?) */
    }
    label { display: none !important; }

    /* RÉGUAS SINCRONIZADAS (HR) */
    hr { border: 0; height: 1px; background: #e0e0e0; margin: 15px 0 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR FIXA (Sem Título Intruso) ---
with st.sidebar:
    # Espaço vazio no topo para manter o alinhamento
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    st.selectbox("Idioma", ["Português", "English", "Español", "Français"], key="lang_v37")
    st.markdown("---")
    
    col_s1, col_s2 = st.columns(2)
    col_s1.button("Talk", key="tk_v37", use_container_width=True)
    col_s2.button("Arte", key="art_v37", use_container_width=True)

# --- 3. BARRA DE COMANDO CENTRALIZADA (Botões com Respiro ← Lista) ---
_, col_barra, _ = st.columns([0.6, 2.8, 0.6])

with col_barra:
    # Aumentei o espaço para os botões (2.0) e mantive a lista compacta (0.8)
    c_btns, c_lista = st.columns([2.0, 0.8])
    
    with c_btns:
        # Colunas com gap via CSS para os 5 botões
        n1, n2, n3, n4, n5 = st.columns(5)
        n1.button("＋", key="v37_1") 
        n2.button("＜", key="v37_2")
        n3.button("＊", key="v37_3")
        n4.button("＞", key="v37_4")
        n5.button("？", key="v37_5")

    with c_lista:
        try:
            arquivos = [f.replace(".ypo", "") for f in os.listdir("data") if f.endswith(".ypo")]
            st.selectbox("Tema", arquivos, key="main_palco_v37")
        except:
            st.write("Erro /data")

st.markdown("<hr>", unsafe_allow_html=True)

# --- 4. RENDERIZAÇÃO ---
st.markdown("<div style='text-align: center; color: #b0bec5; font-family: Georgia;'>v.33.7: Intrusos eliminados. Botões com espaçamento de segurança.</div>", unsafe_allow_html=True)
