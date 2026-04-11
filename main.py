import streamlit as st
import os

# --- 1. CONFIGURAÇÃO DE AMBIENTE ---
if "page" not in st.session_state:
    st.session_state.page = "Demo"

st.set_page_config(
    page_title="a Máquina de Fazer Poesia",
    page_icon="ツ",
    layout="centered"
)

# --- 2. CSS PENTE-FINO (Navegação Centralizada no Topo do Palco) ---
st.markdown("""
    <style>
    /* Layout e Topo */
    .main .block-container { max-width: 800px; padding-top: 0rem !important; }
    header[data-testid="stHeader"] { background: transparent !important; }
    div[data-testid="stStatusWidget"], #MainMenu, footer { visibility: hidden; }

    /* Ajuste de Margem das Colunas de Navegação */
    [data-testid="column"] {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    /* BOTÕES CIRCULARES ROSA NO PALCO */
    div.stButton > button {
        border-radius: 50% !important;
        width: 52px !important;
        height: 52px !important;
        min-width: 52px !important;
        min-height: 52px !important;
        padding: 0px !important;
        background-color: #FFF0F5 !important;
        color: #4A4A4A !important;
        border: 1px solid #FFD1DC !important;
        font-family: 'Courier New', monospace;
        font-size: 24px !important;
        font-weight: bold !important;
        line-height: 52px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.3s ease;
        box-shadow: 1px 1px 4px rgba(0,0,0,0.05);
    }
    
    div.stButton > button:hover {
        background-color: #FFE4E1 !important;
        transform: scale(1.1);
        border-color: #FFB6C1 !important;
        color: #000 !important;
    }

    /* Estilo dos Versos (Palco) */
    .stSubheader { 
        text-align: center; 
        font-family: 'Courier New', monospace;
        color: #333;
        padding: 0.2rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. NAVEGAÇÃO: TOPO DO PALCO { + < * > ? } ---
st.markdown("<br>", unsafe_allow_html=True)
# Sete colunas: 1 de respiro, 5 para botões, 1 de respiro (Centralização Óptica)
nav_cols = st.columns([1.5, 1, 1, 1, 1, 1, 1.5])

with nav_cols[1]:
    if st.button("+"): st.session_state.page = "Demo"
with nav_cols[2]:
    if st.button("<"): st.session_state.page = "yPoemas"
with nav_cols[3]:
    if st.button("*"): st.session_state.page = "Eureka"
with nav_cols[4]:
    if st.button(">"): st.session_state.page = "Off-Machina"
with nav_cols[5]:
    if st.button("?"): st.session_state.page = "About"

# --- 4. SIDEBAR (Configurações Silenciosas) ---
with st.sidebar:
    st.title("ツ Machina")
    idiomas = ["Português", "English", "Español", "Français", "Italiano", "Deutsch"]
    st.selectbox("Idioma", idiomas, label_visibility="collapsed")
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    c1.button("Talk")
    c2.button("Arte")

# --- 5. OPERAÇÃO DO MOTOR ---
pagina = st.session_state.page

try:
    from lay_2_ypo import gera_poema
    
    # Gerenciamento de Tema e Semente
    tema_ativo = st.session_state.get("tema_atual", "Restos")
    eureka_seed = ""
    
    if pagina == "Eureka":
        # Campo de entrada minimalista para coordenadas
        eureka_seed = st.text_input("Coords", label_visibility="collapsed", placeholder="Semente...")

    # Chamada do Motor (Parâmetros: nome_arquivo, seed_eureka)
    versos = gera_poema(tema_ativo, eureka_seed)
    
    if versos:
        st.markdown("<br>", unsafe_allow_html=True)
        # Palco Renderizado
        for v in versos:
            if v.strip() == "":
                st.write("")
            else:
                st.subheader(v)
        st.markdown("<br><hr>", unsafe_allow_html=True)

except Exception:
    pass
