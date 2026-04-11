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

# --- 2. CSS PENTE-FINO (Botões Rosa, Centralização, Topo Zero) ---
st.markdown("""
    <style>
    /* Layout e Topo */
    .main .block-container { max-width: 800px; padding-top: 1rem !important; }
    header[data-testid="stHeader"] { background: transparent !important; }
    div[data-testid="stStatusWidget"], #MainMenu, footer { visibility: hidden; }

    /* Botões Circulares Rosa na Sidebar */
    div.stButton > button {
        border-radius: 50% !important;
        width: 46px !important;
        height: 46px !important;
        min-width: 46px !important;
        min-height: 46px !important;
        padding: 0px !important;
        background-color: #FFF0F5 !important;
        color: #4A4A4A !important;
        border: 1px solid #FFD1DC !important;
        font-family: monospace;
        font-size: 22px !important;
        font-weight: bold !important;
        line-height: 46px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    div.stButton > button:hover {
        background-color: #FFE4E1 !important;
        transform: scale(1.05);
    }

    /* Centralização dos Versos */
    .stSubheader { text-align: center; font-family: 'Courier New', monospace; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (Navegação Símbolos + Idioma) ---
with st.sidebar:
    st.title("ツ Machina")
    
    idiomas = ["Português", "English", "Español", "Français", "Italiano", "Deutsch"]
    st.selectbox("Idioma", idiomas, label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Navegação { + < * > ? }
    c1, c2, c3, c4, c5 = st.columns(5)
    if c1.button("+"): st.session_state.page = "Demo"
    if c2.button("<"): st.session_state.page = "yPoemas"
    if c3.button("*"): st.session_state.page = "Eureka"
    if c4.button(">"): st.session_state.page = "Off-Machina"
    if c5.button("?"): st.session_state.page = "About"

    st.markdown("---")
    
    col_a, col_b = st.columns(2)
    col_a.button("Talk")
    col_b.button("Arte")

# --- 4. EXECUÇÃO DO MOTOR ---
pagina = st.session_state.page

try:
    from lay_2_ypo import gera_poema
    
    # Parâmetros conforme especificação (nome_do_poema, eureka_seed)
    # Aqui assume-se o tema atual ou "Restos" como exemplo de carga
    tema_ativo = st.session_state.get("tema_atual", "Restos")
    eureka_seed = ""
    
    if pagina == "Eureka":
        eureka_seed = st.text_input("Coords", label_visibility="collapsed")

    # Chamada silenciosa
    versos = gera_poema(tema_ativo, eureka_seed)
    
    if versos:
        st.markdown("<br><br>", unsafe_allow_html=True)
        for v in versos:
            if v.strip() == "":
                st.write("")
            else:
                st.subheader(v)
        st.markdown("---")

except Exception:
    pass
