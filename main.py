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

# Dicionário de Help Tips (Poliglota)
help_dict = {
    "Português": "ajuste os adornos da leitura",
    "English": "adjust the reading ornaments",
    "Français": "ajuster les ornements de lecture",
    "Español": "ajusta los adornos de lectura",
    "Italiano": "regolare gli ornamenti di lettura",
    st.session_state.poly_name: "ajusta els ornaments de lectura"
}

# Regra 0: Look & Feel (O DNA Visual da Phenix)
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    
    /* PALCO FLUIDO: Ocupa o espaço quando a sidebar recolhe */
    .main .block-container { 
        max-width: 95% !important; 
        padding-top: 1.5rem; 
        margin: 0 auto;
        transition: max-width 0.3s ease;
    }
    
    /* BLINDAGEM: Remove Fullscreen e Toolbars de imagens */
    [data-testid="stImage"] button, [data-testid="stElementToolbar"] { display: none !important; }
    [data-testid="stImage"] img { pointer-events: none; }

    /* SIDEBAR: Esguia (240px) */
    [data-testid="stSidebar"] { 
        width: 240px !important; 
        min-width: 240px !important;
        background-color: #fafafa; 
    }
    
    /* NAVEGAÇÃO: O Trilho de 111px */
    [data-testid="stHorizontalBlock"] { 
        display: flex !important; 
        flex-wrap: nowrap !important; 
        gap: 8px !important; 
    }
    
    [data-testid="column"] { 
        flex: 0 0 auto !important; 
        width: 115px !important; 
    }
    
    div.stButton > button {
        width: 111px !important; 
        border-radius: 12px; 
        height: 3.2em;
        background-color: #ffffff; 
        border: 1px solid #d1d5db; 
        font-size: 11px;
    }
    
    div.stButton > button:hover { 
        border-color: powderblue; 
        color: powderblue; 
    }

    .sidebar-header {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 0.85rem;
        font-weight: 600;
        color: #999;
        margin-top: 20px;
        margin-bottom: 8px;
        text-transform: lowercase;
    }
    </style> """,
    unsafe_allow_html=True,
)

### bof: navigation (O Trilho Superior)

nav_cols = st.columns(6)
paginas = ["mini", "ypoemas", "eureka", "off-machina", "comments", "sobre"]
labels = ["ツ mini", "ypoemas", "eureka", "off-machina", "comments", "sobre"]

for i in range(6):
    with nav_cols[i]:
        if st.button(labels[i], key=f"btn_nav_{paginas[i]}"):
            st.session_state.page = paginas[i]
            st.rerun()

st.markdown("---")

### bof: sidebar (Cockpit & Contato)

# 1. Artes Dinâmicas
mapeamento_artes = {
    "mini": "img_mini.jpg", 
    "ypoemas": "img_ypoemas.jpg", 
    "eureka": "img_eureka.jpg",
    "off-machina": "img_off-machina.jpg", 
    "comments": "img_poly.jpg", 
    "sobre": "img_about.jpg"
}

arte_atual = mapeamento_artes.get(st.session_state.page)
if arte_atual and os.path.exists(arte_atual):
    st.sidebar.image(arte_atual, use_container_width=True)

st.sidebar.markdown("<br>", unsafe_allow_html=True)

# 2. Seletor de Idioma (Minimalista)
lista_idiomas = ["Português", "English", "Français", "Español", "Italiano", st.session_state.poly_name]
sel_idioma = st.sidebar.selectbox("idioma", lista_idiomas, key="sel_lang", label_visibility="collapsed")
current_help = help_dict.get(sel_idioma, help_dict["Português"])

# 3. Recursos (Trindade Horizontal)
st.sidebar.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3 = st.sidebar.columns(3)
with c1:
    st.session_state.audio_on = st.checkbox("🎙️", value=True, help=f"voz: {current_help}")
with c2:
    st.session_state.draw_on = st.checkbox("🎨", value=True, help=f"arte: {current_help}")
with c3:
    st.session_state.video_on = st.checkbox("🎬", value=False, help=f"vídeo: {current_help}")

# 4. Contato com o Autor (Substituído Github por Facebook)
st.sidebar.markdown("<div class='sidebar-header'>contato</div>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style="display: flex; flex-direction: column; gap: 8px; padding-left: 5px; font-family: 'IBM Plex Sans', sans-serif; font-size: 0.9rem;">
    <a href="https://instagram.com/seu_perfil" target="_blank" style="text-decoration: none; color: #444;">📸 instagram</a>
    <a href="https://facebook.com/seu_perfil" target="_blank" style="text-decoration: none; color: #444;">👥 facebook</a>
    <a href="mailto:seu_email@dominio.com" style="text-decoration: none; color: #444;">✉️ email</a>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption(f"Phenix Machina | {st.session_state.page}")

### bof: pages (O Palco)

if st.session_state.page == "mini":
    st.subheader("ツ mini")
    st.info(f"Idioma: {sel_idioma} | Recursos prontos.")
elif st.session_state.page == "ypoemas":
    st.subheader("ツ ypoemas")
elif st.session_state.page == "eureka":
    st.subheader("ツ eureka")
elif st.session_state.page == "off-machina":
    st.subheader("ツ off-machina")
elif st.session_state.page == "comments":
    st.subheader("ツ comments")
elif st.session_state.page == "sobre":
    st.subheader("ツ sobre")

st.write("")
