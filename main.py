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

# Configuração de Recursos (Dicionário central)
recursos_info = {
    "Português": {"v": "voz", "a": "arte", "vi": "vídeo"},
    "English": {"v": "voice", "a": "art", "vi": "video"},
    "Français": {"v": "voix", "a": "art", "vi": "vidéo"},
    "Español": {"v": "voz", "a": "arte", "vi": "vídeo"},
    "Italiano": {"v": "voce", "a": "arte", "vi": "video"},
    st.session_state.poly_name: {"v": "veu", "a": "art", "vi": "vídeo"}
}

# Regra 0: Look & Feel (Foco em Centralização e Limpeza)
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    .main .block-container { max-width: 95% !important; padding-top: 1.5rem; margin: 0 auto; }
    
    [data-testid="stImage"] button, [data-testid="stElementToolbar"] { display: none !important; }
    [data-testid="stImage"] img { pointer-events: none; }

    /* Sidebar 240px */
    [data-testid="stSidebar"] { width: 240px !important; min-width: 240px !important; background-color: #fafafa; }
    
    /* Navegação Superior 111px */
    [data-testid="stHorizontalBlock"] { display: flex !important; flex-wrap: nowrap !important; gap: 8px !important; }
    [data-testid="column"] { flex: 0 0 auto !important; width: 115px !important; }
    
    div.stButton > button {
        width: 111px !important; border-radius: 12px; height: 3.2em;
        background-color: #ffffff; border: 1px solid #d1d5db; font-size: 11px;
    }

    /* CENTRALIZAÇÃO DOS RECURSOS NA SIDEBAR */
    .st-emotion-cache-1678806 { /* Container de colunas na sidebar */
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        gap: 15px !important;
    }

    /* Esconder labels dos checkboxes/toggles na sidebar */
    [data-testid="stSidebar"] label p { display: none !important; }
    
    /* Reduzir o espaço que o Streamlit reserva para o widget */
    [data-testid="stSidebar"] .stCheckbox, [data-testid="stSidebar"] .stToggle {
        width: fit-content !important;
        margin: 0 auto !important;
    }

    .sidebar-header {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 0.85rem;
        font-weight: 600;
        color: #999;
        margin-top: 25px;
        margin-bottom: 12px;
        text-transform: lowercase;
        text-align: center; /* Centraliza o título 'contato' */
    }

    .contato-links {
        display: flex; 
        flex-direction: column; 
        gap: 8px; 
        align-items: center; /* Centraliza os links de contato */
        font-family: 'IBM Plex Sans', sans-serif; 
        font-size: 0.9rem;
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

# Artes Dinâmicas
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

# 2. Recursos (Foco em Centralização e Help via Atributo Nativo)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

# Usamos colunas com pesos iguais e uma vazia em cada ponta para "espremer" os ícones no centro
_, c1, c2, c3, _ = st.sidebar.columns([1, 1, 1, 1, 1])

lang_tips = recursos_info.get(sel_idioma, recursos_info["Português"])

with c1:
    # O 'help' aqui volta a ser usado mas sem o balão de interrogação graças ao CSS label p {display:none}
    st.session_state.audio_on = st.checkbox("v", value=True, key="chk_v", help=lang_tips["v"])
with c2:
    st.session_state.draw_on = st.checkbox("a", value=True, key="chk_a", help=lang_tips["a"])
with c3:
    st.session_state.video_on = st.checkbox("vi", value=False, key="chk_vi", help=lang_tips["vi"])

# 3. Contato (Também Centralizado)
st.sidebar.markdown("<div class='sidebar-header'>contato</div>", unsafe_allow_html=True)
st.sidebar.markdown(f"""
<div class="contato-links">
    <a href="#" style="text-decoration: none; color: #444;">📸 instagram</a>
    <a href="#" style="text-decoration: none; color: #444;">✉️ email</a>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption(f"Phenix Machina | {st.session_state.page}")

### bof: pages

if st.session_state.page == "mini":
    st.subheader("ツ mini")
    st.write("Recursos centralizados. Passe o mouse nos quadrados para ler as funções.")
else:
    st.subheader(f"ツ {st.session_state.page}")
