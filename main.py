import os
import streamlit as st

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

# Tooltips (Help via HTML Title)
tips = {
    "Português": ["voz (talk)", "arte (draw)", "vídeo (video)"],
    "English": ["voice (talk)", "art (draw)", "video (video)"],
    "Français": ["voix (talk)", "art (draw)", "vidéo (video)"],
    "Español": ["voz (talk)", "arte (draw)", "video (video)"],
    "Italiano": ["voce (talk)", "arte (draw)", "video (video)"],
    st.session_state.poly_name: ["veu (talk)", "art (draw)", "vídeo (video)"]
}

# Regra 0: Look & Feel (A Blindagem Definitiva)
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    .main .block-container { max-width: 95% !important; padding-top: 1.5rem; margin: 0 auto; }
    
    /* Sidebar Fixa */
    [data-testid="stSidebar"] { width: 240px !important; min-width: 240px !important; background-color: #fafafa; }
    
    /* Navegação Superior 111px */
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

    /* CONTAINER DOS RECURSOS: Centralização Real */
    .recursos-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 20px;
        width: 100%;
        padding: 10px 0;
    }

    /* Força o checkbox a ser apenas o quadrado */
    [data-testid="stSidebar"] .stCheckbox {
        margin: 0 !important;
        padding: 0 !important;
        width: fit-content !important;
    }

    .sidebar-header {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 0.85rem;
        font-weight: 600;
        color: #999;
        margin-top: 25px;
        text-transform: lowercase;
        text-align: center;
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
t = tips.get(sel_idioma, tips["Português"])

st.sidebar.markdown("<br>", unsafe_allow_html=True)

# 2. Recursos (O Cockpit Purificado)
# Usamos um container div para agrupar e centralizar
st.sidebar.markdown('<div class="recursos-wrapper">', unsafe_allow_html=True)

# Criamos 3 colunas dentro da sidebar para os checkboxes
c1, c2, c3 = st.sidebar.columns([1, 1, 1])

with c1:
    # O 'title' no markdown flutuante cria o help do navegador
    st.markdown(f'<div title="{t[0]}">', unsafe_allow_html=True)
    st.session_state.audio_on = st.checkbox("v", value=True, key="chk_v", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div title="{t[1]}">', unsafe_allow_html=True)
    st.session_state.draw_on = st.checkbox("a", value=True, key="chk_a", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div title="{t[2]}">', unsafe_allow_html=True)
    st.session_state.video_on = st.checkbox("vi", value=False, key="chk_vi", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown('</div>', unsafe_allow_html=True)

# 3. Contato
st.sidebar.markdown("<div class='sidebar-header'>contato</div>", unsafe_allow_html=True)
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
    st.subheader("ツ mini")
    st.write("Interface calibrada. O minimalismo exige precisão.")
else:
    st.subheader(f"ツ {st.session_state.page}")
