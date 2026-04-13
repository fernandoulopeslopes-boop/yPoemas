import streamlit as st
import os

# --- 1. CONFIGURAÇÃO DE HARDWARE VIRTUAL (RESTAURO TOTAL) ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Navegação por Estado (Bússola Central)
if 'page' not in st.session_state:
    st.session_state.page = 'Demo'

def get_info_content(page_name):
    """Resgate dinâmico dos arquivos de ajuda"""
    try:
        path = os.path.join("md_files", f"INFO_{page_name.upper()}.md")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
    except:
        pass
    return ""

st.markdown("""
    <style>
    [data-testid="stHeader"] { display: none !important; }
    
    /* SIDEBAR FIEL (320px) */
    [data-testid="stSidebar"] { min-width: 320px !important; max-width: 320px !important; }

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
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0px !important;
    }

    /* PALCO CENTRALIZADO */
    .main .block-container {
        max-width: 900px !important;
        margin: 0 auto !important;
        padding-top: 1.5rem !important;
    }

    hr { border: 0; height: 1px; background: #ddd; margin: 15px 0 !important; }
    label { font-weight: 900 !important; font-size: 11px !important; text-transform: uppercase; color: #555; }
    </style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR (O COCKPIT REAL) ---
with st.sidebar:
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    
    # IDIOMA: Radical Western ABC
    elite = ["Português", "Español", "English", "Français", "Italiano", "Català"]
    western_ext = ["German", "Latin", "Norwegian", "Polish", "Swedish", "Turkish", "Romanian"]
    st.selectbox("🌐 IDIOMA", elite + western_ext, key="sb_lang")
    
    st.divider()

    # ARTE DA PÁGINA
    if os.path.exists("img_demo.jpg"):
        st.image("img_demo.jpg", use_container_width=True)
    
    st.divider()

    # INFO BOX (Lógica INFO_PAGINA.md)
    info_md = get_info_content(st.session_state.page)
    st.markdown(f"<div class='info-box'>{info_md}</div>", unsafe_allow_html=True)
    
    st.divider()
    st.markdown("<div style='text-align:center; font-weight:900; font-size:11px;'>INSTAGRAM • GITHUB • LINKEDIN</div>", unsafe_allow_html=True)

# --- 3. PALCO CENTRAL: NAVEGAÇÃO POR TOGGLE BUTTONS ---

# O resgate da lógica de botões de estado que agem como abas
menu_options = ["Demo", "yPoemas", "Eureka", "Off-Machina", "Comments", "About"]

# Implementação robusta de Toggle Buttons (Segmented Control se disponível, ou loop de colunas)
# Aqui usamos o segmented_control para garantir o estado "pressionado" visual
st.session_state.page = st.segmented_control(
    "NAVEGAÇÃO", 
    options=menu_options, 
    default="Demo",
    label_visibility="collapsed",
    key="nav_toggle"
)

st.divider()

# --- 4. CONSOLE DE COMANDO (DINÂMICO) ---
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
    # FIM DA VERSÃO PREGUIÇA: Varredura real da pasta data
    try:
        temas_reais = [f.replace(".ypo", "") for f in os.listdir("data") if f.endswith(".ypo")]
        if not temas_reais: temas_reais = ["Nenhum tema encontrado"]
        st.selectbox("LIVROS / TEMAS", sorted(temas_reais), key="p_tema")
    except:
        st.selectbox("LIVROS / TEMAS", ["Erro na pasta data"], key="p_tema_err")

with c_som:
    st.selectbox("SOM / VOZ", ["Mudo", "Voz 1", "Voz 2"], key="p_som")

st.markdown("<hr>", unsafe_allow_html=True)

# --- 5. ÁREA DE EXIBIÇÃO ---
st.markdown(f"<div style='text-align: center; font-family: Georgia; font-size: 24px;'>{st.session_state.page}</div>", unsafe_allow_html=True)

col_img, col_txt = st.columns([1, 1.2])
with col_img:
    if os.path.exists("img_demo.jpg"):
        st.image("img_demo.jpg", use_container_width=True)
