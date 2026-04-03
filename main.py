import os
import streamlit as st
from datetime import datetime

### bof: settings

st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="wide",
    initial_sidebar_state="auto",
)

# Inicialização de Estados
if "page" not in st.session_state: st.session_state.page = "mini"
if "poly_lang" not in st.session_state: st.session_state.poly_lang = "ca"
if "poly_name" not in st.session_state: st.session_state.poly_name = "català"

# Dicionário de Help Tips (Tooltips puros)
help_tips = {
    "Português": ["voz (talk)", "arte (draw)", "vídeo (video)"],
    "English": ["voice (talk)", "art (draw)", "video (video)"],
    "Français": ["voix (talk)", "art (draw)", "vidéo (video)"],
    "Español": ["voz (talk)", "arte (draw)", "video (video)"],
    "Italiano": ["voce (talk)", "arte (draw)", "video (video)"],
    st.session_state.poly_name: ["veu (talk)", "art (draw)", "vídeo (video)"]
}

# Regra 0: Look & Feel (Ajuste Fino de CSS)
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    .main .block-container { max-width: 95% !important; padding-top: 1.5rem; margin: 0 auto; }
    
    /* Blindagem contra elementos de imagem */
    [data-testid="stImage"] button, [data-testid="stElementToolbar"] { display: none !important; }
    [data-testid="stImage"] img { pointer-events: none; }

    /* Sidebar 240px */
    [data-testid="stSidebar"] { width: 240px !important; background-color: #fafafa; }
    
    /* Navegação 111px */
    [data-testid="stHorizontalBlock"] { display: flex !important; flex-wrap: nowrap !important; gap: 8px !important; }
    [data-testid="column"] { flex: 0 0 auto !important; width: 115px !important; }
    div.stButton > button {
        width: 111px !important; border-radius: 12px; height: 3.2em;
        background-color: #ffffff; border: 1px solid #d1d5db; font-size: 11px;
    }
    div.stButton > button:hover { border-color: powderblue; color: powderblue; }

    /* CSS MÁGICO: Esconde o label do checkbox para sobrarem apenas as 3 caixas */
    [data-testid="stSidebar"] [data-testid="stCheckbox"] p {
        display: none !important;
    }
    [data-testid="stSidebar"] [data-testid="stCheckbox"] {
        margin-left: 10px;
    }

    .sidebar-header {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 0.85rem;
        font-weight: 600;
        color: #999;
        margin-top: 25px;
        margin-bottom: 8px;
        text-transform: lowercase;
    }
    </style> """,
    unsafe_allow_html=True,
)

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

mapeamento_artes = {
    "mini": "img_mini.jpg", "ypoemas": "img_ypoemas.jpg", "eureka": "img_eureka.jpg",
    "off-machina": "img_off-machina.jpg", "comments": "img_poly.jpg", "sobre": "img_about.jpg"
}

arte_atual = mapeamento_artes.get(st.session_state.page)
if arte_atual and os.path.exists(arte_atual):
    st.sidebar.image(arte_atual, use_container_width=True)

st.sidebar.markdown("<br>", unsafe_allow_html=True)

# 1. Idioma
lista_idiomas = ["Português", "English", "Français", "Español", "Italiano", st.session_state.poly_name]
sel_idioma = st.sidebar.selectbox("idioma", lista_idiomas, key="sel_lang", label_visibility="collapsed")

tips = help_tips.get(sel_idioma, help_tips["Português"])

# 2. Recursos (Agora sim: 3 quadrados puros)
st.sidebar.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.sidebar.columns(3)

with col1:
    st.session_state.audio_on = st.sidebar.checkbox("v", value=True, help=tips[0], key="chk_v")
with col2:
    st.session_state.draw_on = st.sidebar.checkbox("a", value=True, help=tips[1], key="chk_a")
with col3:
    st.session_state.video_on = st.sidebar.checkbox("vi", value=False, help=tips[2], key="chk_vi")

# 3. Contato
st.sidebar.markdown("<div class='sidebar-header'>contato</div>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style="display: flex; flex-direction: column; gap: 8px; padding-left: 5px; font-family: 'IBM Plex Sans', sans-serif; font-size: 0.9rem;">
    <a href="#" style="text-decoration: none; color: #444;">📸 instagram</a>
    <a href="#" style="text-decoration: none; color: #444;">✉️ email</a>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption(f"Phenix Machina | {st.session_state.page}")

### bof: pages

if st.session_state.page == "mini":
    st.subheader("ツ mini")
    st.write(f"Cockpit calibrado. Tooltips ativos em: **{sel_idioma}**.")
else:
    st.subheader(f"ツ {st.session_state.page}")

st.write("")
