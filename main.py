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

# Dicionário de Help Tips
help_dict = {
    "Português": "escolha como a machina deve atuar",
    "English": "choose how the machine should act",
    "Français": "choisissez comment la machine deve agir",
    "Español": "elige cómo deve actuar la máquina",
    "Italiano": "scegli come deve agire la macchina",
    st.session_state.poly_name: "tria com ha d'actuar la màquina"
}

# Regra 0: Look & Feel
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    .main .block-container { max-width: 95% !important; padding-top: 1.5rem; margin: 0 auto; }
    
    [data-testid="stImage"] button, [data-testid="stElementToolbar"] { display: none !important; }
    [data-testid="stImage"] img { pointer-events: none; }

    [data-testid="stSidebar"] { width: 240px !important; background-color: #fafafa; }
    
    /* Navegação Superior - 111px */
    [data-testid="stHorizontalBlock"] { display: flex !important; flex-wrap: nowrap !important; gap: 8px !important; }
    [data-testid="column"] { flex: 0 0 auto !important; width: 115px !important; }
    div.stButton > button {
        width: 111px !important; border-radius: 12px; height: 3.2em;
        background-color: #ffffff; border: 1px solid #d1d5db; font-size: 12px;
    }
    div.stButton > button:hover { border-color: powderblue; color: powderblue; }

    /* Ajuste fino para os botões horizontais na sidebar */
    .sidebar-header {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 0.85rem;
        font-weight: 600;
        color: #999;
        margin-top: 15px;
        text-transform: lowercase;
    }
    </style> """,
    unsafe_allow_html=True,
)

### bof: navigation (Trilho Superior)

nav_cols = st.columns(6)
paginas = ["mini", "ypoemas", "eureka", "off-machina", "comments", "sobre"]
labels = ["ツ mini", "ypoemas", "eureka", "off-machina", "comments", "sobre"]

for i in range(6):
    with nav_cols[i]:
        if st.button(labels[i], key=f"btn_nav_{paginas[i]}"):
            st.session_state.page = paginas[i]
            st.rerun()

st.markdown("---")

### bof: sidebar (Cockpit & Contatos)

mapeamento_artes = {
    "mini": "img_mini.jpg", "ypoemas": "img_ypoemas.jpg", "eureka": "img_eureka.jpg",
    "off-machina": "img_off-machina.jpg", "comments": "img_poly.jpg", "sobre": "img_about.jpg"
}

arte_atual = mapeamento_artes.get(st.session_state.page)
if arte_atual and os.path.exists(arte_atual):
    st.sidebar.image(arte_atual, use_container_width=True)

# 1. Seletor de Idioma
lista_idiomas = ["Português", "English", "Français", "Español", "Italiano", st.session_state.poly_name]
sel_idioma = st.sidebar.selectbox("idioma_selector", lista_idiomas, key="sel_lang", label_visibility="collapsed")
current_help = help_dict.get(sel_idioma, help_dict["Português"])

# 2. Recursos em Horizontal (Talk, Draw, Video)
st.sidebar.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3 = st.sidebar.columns(3)
with c1:
    st.session_state.audio_on = st.checkbox("🎙️", value=True, help=f"voz: {current_help}", key="chk_talk")
with c2:
    st.session_state.draw_on = st.checkbox("🎨", value=True, help=f"arte: {current_help}", key="chk_draw")
with c3:
    st.session_state.video_on = st.checkbox("🎬", value=False, help=f"vídeo: {current_help}", key="chk_video")

# 3. Contato com o Autor (Redes Sociais)
st.sidebar.markdown("<div class='sidebar-header'>contato</div>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style="display: flex; flex-direction: column; gap: 8px; padding-left: 5px; font-family: 'IBM Plex Sans', sans-serif; font-size: 0.9rem;">
    <a href="https://instagram.com/seu_perfil" target="_blank" style="text-decoration: none; color: #444;">📸 instagram</a>
    <a href="https://github.com/seu_usuario" target="_blank" style="text-decoration: none; color: #444;">🐙 github</a>
    <a href="mailto:seu_email@dominio.com" style="text-decoration: none; color: #444;">✉️ email</a>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption(f"Phenix Machina | {st.session_state.page}")

### bof: pages

if st.session_state.page == "mini":
    st.subheader("ツ mini")
    st.write("Recursos ativos:")
    resumo = []
    if st.session_state.audio_on: resumo.append("Voz 🎙️")
    if st.session_state.draw_on: resumo.append("Arte 🎨")
    if st.session_state.video_on: resumo.append("Vídeo 🎬")
    st.info(", ".join(resumo) if resumo else "Nenhum recurso ativo.")
else:
    st.subheader(f"ツ {st.session_state.page}")
