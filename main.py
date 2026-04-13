import streamlit as stimport streamlit as st
import os

# --- 1. HARDWARE VIRTUAL (BEST_VERSION RECOVERED) ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Navegação por estado (Toggle Logic)
if 'page' not in st.session_state:
    st.session_state.page = 'DEMO'

st.markdown("""
    <style>
    [data-testid="stHeader"] { display: none !important; }
    
    /* SIDEBAR COCKPIT (320px) */
    [data-testid="stSidebar"] { min-width: 320px !important; max-width: 320px !important; }

    /* TOGGLE BUTTONS (Navegação Superior) */
    .st-key-nav_btns div.stButton > button {
        border-radius: 20px !important;
        font-weight: 900 !important;
        background-color: #f8f9fa !important;
        border: 1px solid #ddd !important;
        padding: 0px 18px !important;
        height: 32px !important;
        font-size: 13px !important;
    }

    /* CONSOLE DE COMANDO (Os 5 Círculos do Last Screenshot) */
    .st-key-cmd_btns div.stButton > button {
        background-color: #f0f2f6 !important;
        color: #000 !important;
        border-radius: 50% !important;
        width: 44px !important;
        height: 44px !important;
        border: 2px solid #000 !important;
        font-size: 22px !important;
        font-weight: 900 !important;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0px !important;
    }

    /* INFO BOX (Estética Dicionário) */
    .info-box {
        font-family: 'Georgia', serif;
        font-size: 13px;
        line-height: 1.6;
        color: #1a1a1a;
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
    
    # Idioma (Lista Radical)
    langs = ["Português", "Español", "English", "Français", "Italiano", "Català", "Latin", "German"]
    st.selectbox("🌐 IDIOMA", langs, key="sb_lang")
    
    st.divider()

    # Arte da Página (Identidade)
    if os.path.exists("img_demo.jpg"):
        st.image("img_demo.jpg", use_container_width=True)
    
    st.divider()

    # Info Box Dinâmico (Lê de \md_files)
    try:
        with open(f"md_files/INFO_{st.session_state.page}.md", "r", encoding="utf-8") as f:
            st.markdown(f"<div class='info-box'>{f.read()}</div>", unsafe_allow_html=True)
    except:
        st.markdown("<div class='info-box'>Aguardando contexto...</div>", unsafe_allow_html=True)

# --- 3. PALCO SOBERANO ---

# A. TOGGLE NAVIGATION (Menu Superior)
menu = ["Demo", "yPoemas", "Eureka", "Off-Machina", "Comments", "About"]
cols = st.columns(len(menu))
st.markdown("<div class='st-key-nav_btns'>", unsafe_allow_html=True)
for i, item in enumerate(menu):
    if cols[i].button(item.upper(), key=f"nav_{item}"):
        st.session_state.page = item.upper()
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# B. CONSOLE (Os 5 botões funcionais)
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
    st.selectbox("LIVROS / TEMAS", ["Geral"], key="p_tema")

with c_som:
    st.selectbox("SOM", ["Mudo", "Voz 1", "Voz 2"], key="p_som")

st.markdown("<hr>", unsafe_allow_html=True)

# C. ÁREA DE EXIBIÇÃO (Exemplo: DEMO)
st.markdown(f"<h2 style='text-align: center; font-family: Georgia;'>{st.session_state.page}</h2>", unsafe_allow_html=True)
import os

# --- 1. CONFIGURAÇÃO DE HARDWARE VIRTUAL (RESTAURO TOTAL) ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inicialização do estado da página
if 'page' not in st.session_state:
    st.session_state.page = 'DEMO'

def get_info_content(page_name):
    """Lê INFO_(PAGINA).md da pasta md_files"""
    try:
        filename = f"INFO_{page_name.upper()}.md"
        path = os.path.join("md_files", filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
    except:
        pass
    return ""

st.markdown("""
    <style>
    /* LIMPEZA DE HEADER NATIVO */
    [data-testid="stHeader"] { display: none !important; }
    
    /* SIDEBAR FIEL (320px) */
    [data-testid="stSidebar"] { min-width: 320px !important; max-width: 320px !important; }

    /* MENU SUPERIOR (Navegação Arredondada) */
    .st-key-nav_btns div.stButton > button {
        border-radius: 20px !important;
        font-weight: 900 !important;
        background-color: #f8f9fa !important;
        border: 1px solid #ddd !important;
        padding: 0px 18px !important;
        height: 32px !important;
        font-size: 13px !important;
        letter-spacing: 0.5px;
    }

    /* CONSOLE CENTRAL: OS 5 BOTÕES CIRCULARES */
    .st-key-cmd_btns div.stButton > button {
        background-color: #f0f2f6 !important;
        color: #000 !important;
        border-radius: 50% !important;
        width: 44px !important;
        height: 44px !important;
        border: 2px solid #000 !important;
        font-size: 22px !important;
        font-weight: 900 !important;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0px !important;
    }

    /* INFO BOX SIDEBAR (Estética Dicionário) */
    .info-box {
        font-family: 'Georgia', serif;
        font-size: 13px;
        line-height: 1.6;
        color: #1a1a1a;
        background: #fdfdfd;
        padding: 15px;
        border-left: 4px solid #000;
        margin-top: 10px;
    }

    /* PALCO CENTRALIZADO (900px) */
    .main .block-container {
        max-width: 900px !important;
        margin: 0 auto !important;
        padding-top: 1.5rem !important;
    }

    hr { border: 0; height: 1px; background: #ddd; margin: 15px 0 !important; }
    label { font-weight: 900 !important; font-size: 11px !important; text-transform: uppercase; color: #555; }
    </style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR (O COCKPIT DO LAST_SCREENSHOT) ---
with st.sidebar:
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    
    # IDIOMA (Radical Western ABC)
    elite = ["Português", "Español", "English", "Français", "Italiano", "Català"]
    western = ["German", "Latin", "Norwegian", "Polish", "Swedish", "Turkish", "Latin", "Romanian"]
    full_langs = elite + [l for l in western if l not in elite]
    st.selectbox("🌐 IDIOMA", full_langs, key="sb_lang")
    
    st.divider()

    # ARTE DA PÁGINA
    if os.path.exists("img_demo.jpg"):
        st.image("img_demo.jpg", use_container_width=True)
    
    st.divider()

    # INFO BOX (Conteúdo Dinâmico)
    info_md = get_info_content(st.session_state.page)
    st.markdown(f"<div class='info-box'>{info_md}</div>", unsafe_allow_html=True)
    
    st.divider()
    st.markdown("<div style='text-align:center; font-weight:900; font-size:11px;'>INSTAGRAM • GITHUB • LINKEDIN</div>", unsafe_allow_html=True)

# --- 3. PALCO CENTRAL ---

# A. NAVEGAÇÃO SUPERIOR
menu = ["Demo", "yPoemas", "Eureka", "Off-Machina", "Comments", "About"]
cols_nav = st.columns(len(menu))

st.markdown("<div class='st-key-nav_btns'>", unsafe_allow_html=True)
for i, item in enumerate(menu):
    if cols_nav[i].button(item.upper(), key=f"nav_{item}"):
        st.session_state.page = item
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# B. CONSOLE DE COMANDO (5 Botões + Seletores)
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
    try:
        ypo_files = [f.replace(".ypo", "") for f in os.listdir("data") if f.endswith(".ypo")]
        st.selectbox("LIVROS / TEMAS", ypo_files if ypo_files else ["Geral"], key="p_tema")
    except:
        st.selectbox("LIVROS / TEMAS", ["Geral"], key="p_tema_fallback")

with c_som:
    st.selectbox("SOM / VOZ", ["Mudo", "Voz 1", "Voz 2"], key="p_som")

st.markdown("<hr>", unsafe_allow_html=True)

# --- 4. ÁREA DE EXIBIÇÃO ---
col_img, col_txt = st.columns([1, 1.2])

with col_img:
    if os.path.exists("img_demo.jpg"):
        st.image("img_demo.jpg", use_container_width=True)

with col_txt:
    st.markdown(f"<div style='font-family: Georgia; font-size: 22px; font-weight: bold;'>{st.session_state.page}</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-family: Georgia; font-size: 19px; line-height: 1.8; padding-top: 15px;'><i>Aguardando pulso da Machina...</i></div>", unsafe_allow_html=True)
