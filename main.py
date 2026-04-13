import streamlit as st
import os

# --- 1. CONFIGURAÇÃO DE HARDWARE (BEST_VERSION RECOVERED) ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Navegação persistente por Toggle Logic
if 'page' not in st.session_state:
    st.session_state.page = 'DEMO'

st.markdown("""
    <style>
    [data-testid="stHeader"] { display: none !important; }
    
    /* SIDEBAR FIEL (320px) */
    [data-testid="stSidebar"] { min-width: 320px !important; max-width: 320px !important; }

    /* ESTILO TOGGLE BUTTONS (Navegação Superior) */
    .st-key-nav_toggle div.stButton > button {
        border-radius: 0px !important;
        border: none !important;
        border-bottom: 3px solid transparent !important;
        font-weight: 900 !important;
        background-color: transparent !important;
        font-size: 14px !important;
        color: #888 !important;
    }
    
    /* Simulação de Estado Ativo para o Toggle */
    .st-key-nav_active div.stButton > button {
        border-bottom: 3px solid #000 !important;
        color: #000 !important;
    }

    /* CONSOLE DE COMANDO (Os 5 Círculos Pretos) */
    .st-key-cmd_btns div.stButton > button {
        background-color: #f0f2f6 !important;
        color: #000 !important;
        border-radius: 50% !important;
        width: 44px !important;
        height: 44px !important;
        border: 2px solid #000 !important;
        font-size: 22px !important;
        font-weight: 900 !important;
        padding: 0px !important;
    }

    /* INFO BOX (Estética Dicionário) */
    .info-box {
        font-family: 'Georgia', serif;
        font-size: 13px;
        line-height: 1.6;
        background: #fdfdfd;
        padding: 15px;
        border-left: 4px solid #000;
        margin-top: 10px;
    }

    .main .block-container { max-width: 900px !important; margin: 0 auto !important; }
    hr { border: 0; height: 1px; background: #ddd; }
    </style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR (COCKPIT DE PREFERÊNCIAS) ---
with st.sidebar:
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    
    # IDIOMA: Lista Radical Western ABC
    elite = ["Português", "Español", "English", "Français", "Italiano", "Català"]
    others = ["German", "Latin", "Norwegian", "Polish", "Swedish"]
    st.selectbox("🌐 IDIOMA", elite + others, key="sb_lang")
    
    st.divider()

    # ARTE DA PÁGINA
    if os.path.exists("img_demo.jpg"):
        st.image("img_demo.jpg", use_container_width=True)
    
    st.divider()

    # INFO BOX (Dinâmico: lê de \md_files)
    try:
        path = os.path.join("md_files", f"INFO_{st.session_state.page}.md")
        with open(path, "r", encoding="utf-8") as f:
            st.markdown(f"<div class='info-box'>{f.read()}</div>", unsafe_allow_html=True)
    except:
        st.markdown("<div class='info-box'>Aguardando contexto da Machina...</div>", unsafe_allow_html=True)

# --- 3. PALCO SOBERANO (NAVEGAÇÃO TOGGLE) ---

# Menu Superior com Lógica de Toggle (Botão Ativo vs Inativo)
menu = ["DEMO", "yPOEMAS", "EUREKA", "OFF-MACHINA", "COMMENTS", "ABOUT"]
cols = st.columns(len(menu))

for i, item in enumerate(menu):
    # Aplica classe 'nav_active' se for a página atual, senão 'nav_toggle'
    key_type = "nav_active" if st.session_state.page == item else "nav_toggle"
    with cols[i]:
        st.markdown(f"<div class='st-key-{key_type}'>", unsafe_allow_html=True)
        if st.button(item, key=f"btn_{item}"):
            st.session_state.page = item
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# --- 4. CONSOLE DE COMANDO E EXIBIÇÃO ---
c_btns, c_tema, c_som = st.columns([1.8, 1.5, 0.8])
with c_btns:
    st.markdown("<div class='st-key-cmd_btns'>", unsafe_allow_html=True)
    n1, n2, n3, n4, n5 = st.columns(5)
    n1.button("＋", key="cmd_add")
    n2.button("＜", key="cmd_prev")
    n3.button("＊", key="cmd_star")
    n4.button("＞", key="cmd_next")
    n5.button("？", key="cmd_help")
    st.markdown("</div>", unsafe_allow_html=True)

with c_tema:
    st.selectbox("TEMAS", ["Proust", "Metafísica"], key="p_tema")

with c_som:
    st.selectbox("SOM", ["Mudo", "Voz 1"], key="p_som")

st.markdown("<hr>", unsafe_allow_html=True)

# Área de Texto/Imagem do Palco
st.markdown(f"<h2 style='text-align: center; font-family: Georgia;'>{st.session_state.page}</h2>", unsafe_allow_html=True)
