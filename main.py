import os
import streamlit as st
import random

### bof: settings

st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="wide",
    initial_sidebar_state="auto",
)

# Inicialização de Estados
if "page" not in st.session_state: st.session_state.page = "mini"
if "poly_name" not in st.session_state: st.session_state.poly_name = "català"

# Regra 0: Look & Feel (A BLINDAGEM TOTAL DO PALCO)
st.markdown(
    """ <style>
    footer {visibility: hidden;}

    /* EXPANSÃO DO PALCO: Ocupa 100% da tela quando a sidebar recolhe */
    .main .block-container { 
        max-width: 98% !important; 
        padding-top: 1.5rem !important; 
        padding-left: 2rem !important; 
        padding-right: 2rem !important; 
        margin: 0 auto !important;
    }
    [data-testid="stMainViewContainer"] { width: 100% !important; }

    /* SIDEBAR: Largura Fixa e Estética */
    [data-testid="stSidebar"] { width: 240px !important; min-width: 240px !important; background-color: #fafafa; }
    
    /* NAVEGAÇÃO: Botões de 111px */
    [data-testid="stHorizontalBlock"] { display: flex !important; flex-wrap: nowrap !important; gap: 8px !important; }
    [data-testid="column"] { flex: 0 0 auto !important; width: 115px !important; }
    div.stButton > button {
        width: 111px !important; border-radius: 12px; height: 3.2em;
        background-color: #ffffff; border: 1px solid #d1d5db; font-size: 11px;
    }

    /* MATADOR DE INTERROGAÇÕES E LABELS */
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"], 
    [data-testid="stSidebar"] button[title="View help"] { 
        display: none !important; 
    }

    /* CENTRALIZAÇÃO DOS COOKIES NA SIDEBAR */
    [data-testid="stSidebarContent"] [data-testid="stHorizontalBlock"] {
        justify-content: center !important;
        gap: 15px !important;
    }

    /* ESTILO DO POEMA (PÁGINA MINI) */
    .poema-box {
        font-family: 'IBM Plex Serif', serif;
        font-size: 1.6rem;
        line-height: 2;
        color: #2c3e50;
        padding: 60px;
        background-color: #ffffff;
        border-radius: 20px;
        text-align: center;
        border: 1px solid #f0f0f0;
        margin: 40px auto;
        max-width: 800px;
    }
    </style> """,
    unsafe_allow_html=True,
)

### bof: logic (Mini-Māchina)

def get_mini_verse():
    # Simulação rápida para o palco não ficar vazio
    versos = [
        "o silêncio da máquina",
        "ecoando no papel digital",
        "breve como um clique",
        "algoritmos de outono",
        "a poesia é um erro de sistema"
    ]
    return "<br>".join(random.sample(versos, 3))

### bof: navigation

nav_cols = st.columns(6)
paginas = ["mini", "ypoemas", "eureka", "off-machina", "comments", "sobre"]
labels = ["ツ mini", "ypoemas", "eureka", "off-machina", "comments", "sobre"]

for i in range(6):
    with nav_cols[i]:
        if st.button(labels[i], key=f"btn_nav_{paginas[i]}"):
            st.session_state.page = paginas[i]
            st.rerun()

st.markdown("---")

### bof: sidebar

# Artes
mapeamento_artes = {
    "mini": "img_mini.jpg", "ypoemas": "img_ypoemas.jpg", "eureka": "img_eureka.jpg",
    "off-machina": "img_off-machina.jpg", "comments": "img_poly.jpg", "sobre": "img_about.jpg"
}
arte_atual = mapeamento_artes.get(st.session_state.page)
if arte_atual and os.path.exists(arte_atual):
    st.sidebar.image(arte_atual, use_container_width=True)

# 1. Idioma
lista_idiomas = ["Português", "English", "Français", "Español", "Italiano", st.session_state.poly_name]
sel_idioma = st.sidebar.selectbox("idioma", lista_idiomas, key="sel_lang", label_visibility="collapsed")

# 2. Recursos (Os Cookies)
st.sidebar.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3 = st.sidebar.columns([1, 1, 1])
with c1: st.session_state.audio_on = st.checkbox("v", value=True, key="chk_v", label_visibility="collapsed")
with c2: st.session_state.draw_on = st.checkbox("a", value=True, key="chk_a", label_visibility="collapsed")
with c3: st.session_state.video_on = st.checkbox("vi", value=False, key="chk_vi", label_visibility="collapsed")

# 3. Contato
st.sidebar.markdown("<p style='text-align:center; color:#999; font-size:0.8rem; margin-top:20px;'>contato</p>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style="text-align: center; display: flex; flex-direction: column; gap: 8px; font-family: 'IBM Plex Sans', sans-serif; font-size: 0.9rem;">
    <a href="#" style="text-decoration: none; color: #444;">📸 instagram</a>
    <a href="#" style="text-decoration: none; color: #444;">✉️ email</a>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption(f"Phenix Machina | {st.session_state.page}")

### bof: pages

if st.session_state.page == "mini":
    st.markdown("<h2 style='text-align: center;'>ツ mini-māchina</h2>", unsafe_allow_html=True)
    
    # O Poema
    st.markdown(f'<div class="poema-box">{get_mini_verse()}</div>', unsafe_allow_html=True)
    
    # Botão de Geração Centralizado
    _, col_btn, _ = st.columns([1, 0.4, 1])
    with col_btn:
        if st.button("novo sopro", use_container_width=True):
            st.rerun()

elif st.session_state.page == "ypoemas":
    st.subheader("ツ ypoemas")
