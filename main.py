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

# Dicionário de Nomes para Tooltips (Injetados via CSS)
tips = {
    "Português": ["voz", "arte", "vídeo"],
    "English": ["voice", "art", "video"],
    "Français": ["voix", "art", "vidéo"],
    "Español": ["voz", "arte", "vídeo"],
    "Italiano": ["voce", "arte", "video"],
    st.session_state.poly_name: ["veu", "art", "vídeo"]
}
t = tips.get(st.session_state.get("sel_lang", "Português"), tips["Português"])

# Regra 0: Look & Feel (A MANDALA de Estilo)
st.markdown(
    f""" <style>
    footer {{visibility: hidden;}}
    .main .block-container {{ max-width: 95% !important; padding-top: 1.5rem; margin: 0 auto; }}
    
    [data-testid="stImage"] button, [data-testid="stElementToolbar"] {{ display: none !important; }}
    [data-testid="stImage"] img {{ pointer-events: none; }}

    /* Sidebar 240px */
    [data-testid="stSidebar"] {{ width: 240px !important; min-width: 240px !important; background-color: #fafafa; }}
    
    /* Navegação Superior 111px */
    [data-testid="stHorizontalBlock"] {{ display: flex !important; flex-wrap: nowrap !important; gap: 8px !important; }}
    [data-testid="column"] {{ flex: 0 0 auto !important; width: 115px !important; }}
    
    div.stButton > button {{
        width: 111px !important; border-radius: 12px; height: 3.2em;
        background-color: #ffffff; border: 1px solid #d1d5db; font-size: 11px;
    }}
    
    /* TOOLTIP PERSONALIZADO (Substitui o balão de ?) */
    .custom-tip {{
        position: relative;
        display: inline-block;
    }}
    .custom-tip:hover::after {{
        content: attr(data-tooltip);
        position: absolute;
        bottom: 120%;
        left: 50%;
        transform: translateX(-50%);
        background-color: #333;
        color: #fff;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 10px;
        white-space: nowrap;
        z-index: 999;
    }}

    /* Esconde o label e o balão original */
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] {{ display: none !important; }}
    [data-testid="stSidebar"] button[title="View help"] {{ display: none !important; }}
    
    /* Espaçamento do Grupo de Recursos */
    [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {{
        gap: 20px !important; /* Aumenta o respiro entre os quadrados */
        margin-left: 10px !important;
        margin-top: 10px !important;
    }}

    .sidebar-header {{
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 0.85rem;
        font-weight: 600;
        color: #999;
        margin-top: 15px;
        margin-bottom: 8px;
        text-transform: lowercase;
    }}
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

# 1. Idioma
lista_idiomas = ["Português", "English", "Français", "Español", "Italiano", st.session_state.poly_name]
sel_idioma = st.sidebar.selectbox("idioma", lista_idiomas, key="sel_lang", label_visibility="collapsed")

st.sidebar.markdown("<br>", unsafe_allow_html=True)

# 2. Recursos (3 Quadrados com Tooltip Invisível)
col_rec = st.sidebar.columns([1, 1, 1, 3]) 

with col_rec[0]:
    st.markdown(f'<div class="custom-tip" data-tooltip="{t[0]}">', unsafe_allow_html=True)
    st.session_state.audio_on = st.checkbox("v", value=True, key="chk_v", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
with col_rec[1]:
    st.markdown(f'<div class="custom-tip" data-tooltip="{t[1]}">', unsafe_allow_html=True)
    st.session_state.draw_on = st.checkbox("a", value=True, key="chk_a", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
with col_rec[2]:
    st.markdown(f'<div class="custom-tip" data-tooltip="{t[2]}">', unsafe_allow_html=True)
    st.session_state.video_on = st.checkbox("vi", value=False, key="chk_vi", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

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
    st.write(f"Cockpit calibrado. Passe o mouse nos quadrados para ver as funções em: **{sel_idioma}**.")
else:
    st.subheader(f"ツ {st.session_state.page}")
