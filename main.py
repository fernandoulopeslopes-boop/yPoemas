import streamlit as st
import os

# --- 1. CONFIGURAÇÃO DE HARDWARE VIRTUAL (RESTAURO COM LÓGICA DE CONTEXTO) ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inicialização do estado da página (Default: Demo)
if 'page' not in st.session_state:
    st.session_state.page = 'DEMO'

def get_info_content(page_name):
    """Busca o arquivo .md correspondente na pasta md_files"""
    try:
        # Mapeamento para garantir a leitura dos arquivos fornecidos
        filename = f"INFO_{page_name.upper()}.md"
        path = os.path.join("md_files", filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
    except:
        pass
    return "Conteúdo indisponível."

st.markdown("""
    <style>
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stSidebar"] { min-width: 320px !important; max-width: 320px !important; }

    /* MENU SUPERIOR */
    .st-key-nav_btns div.stButton > button {
        border-radius: 20px !important;
        font-weight: 900 !important;
        background-color: #f8f9fa !important;
        border: 1px solid #ddd !important;
        padding: 0px 18px !important;
        height: 32px !important;
        font-size: 13px !important;
    }

    /* CONSOLE DE COMANDO */
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

    /* INFO BOX SIDEBAR (Fiel ao Hardware) */
    .info-box {
        font-family: 'Georgia', serif;
        font-size: 13px;
        line-height: 1.6;
        color: #222;
        background: #fdfdfd;
        padding: 15px;
        border-left: 4px solid #000;
        margin-top: 10px;
    }
    .info-box b { color: #000; }

    .main .block-container {
        max-width: 900px !important;
        margin: 0 auto !important;
        padding-top: 1.5rem !important;
    }

    hr { border: 0; height: 1px; background: #ddd; margin: 15px 0 !important; }
    label { font-weight: 900 !important; font-size: 11px !important; text-transform: uppercase; color: #555; }
    </style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR: O COCKPIT DINÂMICO ---
with st.sidebar:
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    
    # SELETOR DE IDIOMA (Lista Radical)
    elite = ["Português", "Español", "English", "Français", "Italiano", "Català"]
    western = ["Afrikaans", "Basque", "German", "Latin", "Norwegian", "Polish", "Swedish", "Turkish"]
    st.selectbox("🌐 IDIOMA", elite + western, key="sb_lang")
    
    st.divider()

    # ARTE DA PÁGINA
    if os.path.exists("img_demo.jpg"):
        st.image("img_demo.jpg", width='stretch')
    
    st.divider()

    # INFO BOX (Carrega INFO_PAGINA.md dinamicamente)
    info_text = get_info_content(st.session_state.page)
    st.markdown(f"<div class='info-box'>{info_text}</div>", unsafe_allow_html=True)
    
    st.divider()
    st.markdown("<div style='text-align:center; font-weight:900; font-size:11px;'>INSTAGRAM • GITHUB • LINKEDIN</div>", unsafe_allow_html=True)

# --- 3. PALCO CENTRAL ---

# NAVEGAÇÃO SUPERIOR (Atualiza o state da página)
menu = ["Demo", "yPoemas", "Eureka", "Off-Machina", "Comments", "About"]
cols_nav = st.columns(len(menu))

st.markdown("<div class='st-key-nav_btns'>", unsafe_allow_html=True)
for i, item in enumerate(menu):
    if cols_nav[i].button(item.upper(), key=f"nav_{item}"):
        st.session_state.page = item
st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# CONSOLE DE COMANDO
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

# --- 4. ÁREA DE CONTEÚDO ---
st.markdown(f"<h2 style='text-align: center; font-family: Georgia;'>{st.session_state.page}</h2>", unsafe_allow_html=True)
