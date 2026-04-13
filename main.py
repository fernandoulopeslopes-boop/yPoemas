import streamlit as st
import os

# --- 1. BOOT: HARDWARE VIRTUAL (MARCO 09-10/ABRIL) ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Bússola de Estado (Sincronizada com o Top Menu)
if 'page' not in st.session_state:
    st.session_state.page = 'DEMO'

def get_md_content(page_name):
    """Resgate técnico dos arquivos na pasta \md_files"""
    try:
        # Normalização do nome para casar com os arquivos enviados
        fname = f"INFO_{page_name.upper().replace('-', '_')}.md"
        path = os.path.join("md_files", fname)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
    except:
        pass
    return "Aguardando pulso da Machina..."

# --- 2. CSS DE BLINDAGEM (SIDEBAR + TOGGLES) ---
st.markdown("""
    <style>
    [data-testid="stHeader"] { display: none !important; }
    
    /* SIDEBAR FIEL (320px) */
    section[data-testid="stSidebar"] {
        min-width: 320px !important;
        max-width: 320px !important;
    }

    /* ESTILO DOS TOGGLE BUTTONS (Navegação Superior) */
    .st-key-nav_btn div.stButton > button {
        border-radius: 20px !important;
        border: 1px solid #ddd !important;
        background-color: #f8f9fa !important;
        color: #888 !important;
        font-weight: 900 !important;
        padding: 0px 20px !important;
        height: 35px !important;
    }
    
    /* ESTADO ATIVO (Toggle Pressionado) */
    .st-key-nav_active div.stButton > button {
        background-color: #000 !important;
        color: #fff !important;
        border: 1px solid #000 !important;
    }

    /* CONSOLE: 5 Círculos Pretos (Last Screenshot) */
    .st-key-cmd_btns div.stButton > button {
        background-color: #f0f2f6 !important;
        color: #000 !important;
        border-radius: 50% !important;
        width: 44px !important;
        height: 44px !important;
        border: 2px solid #000 !important;
        font-size: 22px !important;
        font-weight: 900 !important;
        padding: 0px !important;
    }

    /* INFO BOX (Estética Dicionário) */
    .info-box {
        font-family: 'Georgia', serif;
        font-size: 13px;
        line-height: 1.5;
        color: #1a1a1a;
        background: #fdfdfd;
        padding: 15px;
        border-left: 4px solid #000;
        margin-top: 10px;
    }

    .main .block-container { max-width: 950px !important; margin: 0 auto !important; }
    hr { border: 0; height: 1px; background: #eee; margin: 15px 0 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR (O COCKPIT) ---
with st.sidebar:
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    
    # IDIOMA (Lista Western ABC)
    elite = ["Português", "Español", "English", "Français", "Italiano", "Català"]
    st.selectbox("🌐 IDIOMA", elite, key="sb_lang")
    
    st.divider()

    # ARTE DA PÁGINA
    if os.path.exists("img_demo.jpg"):
        st.image("img_demo.jpg", use_container_width=True)
    
    st.divider()

    # INFO BOX (Carregamento Real dos MDs)
    info_txt = get_md_content(st.session_state.page)
    st.markdown(f"<div class='info-box'>{info_txt}</div>", unsafe_allow_html=True)
    
    st.divider()
    st.markdown("<div style='text-align:center; font-weight:900; font-size:10px;'>YPOEMAS • 2026</div>", unsafe_allow_html=True)

# --- 4. PALCO: NAVEGAÇÃO TOGGLE ---
menu = ["Demo", "yPoemas", "Eureka", "Off-Machina", "Comments", "About"]
cols = st.columns(len(menu))

for i, item in enumerate(menu):
    # Classe ativa vs inativa
    is_active = st.session_state.page == item
    container_key = "nav_active" if is_active else "nav_btn"
    
    with cols[i]:
        st.markdown(f"<div class='st-key-{container_key}'>", unsafe_allow_html=True)
        if st.button(item.upper(), key=f"btn_{item}"):
            st.session_state.page = item
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# --- 5. CONSOLE E ACERVO REAL ---
c_btns, c_tema, c_som = st.columns([1.8, 1.5, 0.8])

with c_btns:
    st.markdown("<div class='st-key-cmd_btns'>", unsafe_allow_html=True)
    b_cols = st.columns(5)
    icons = ["＋", "＜", "＊", "＞", "？"]
    for i, col in enumerate(b_cols):
        col.button(icons[i], key=f"cmd_{i}")
    st.markdown("</div>", unsafe_allow_html=True)

with c_tema:
    # Varredura do acervo .ypo (Sem versão preguiça)
    try:
        acervo = [f.replace(".ypo", "") for f in os.listdir("data") if f.endswith(".ypo")]
        st.selectbox("LIVROS / TEMAS", sorted(acervo) if acervo else ["Vazio"], key="p_tema")
    except:
        st.selectbox("TEMAS", ["Check data/"], key="p_tema_err")

with c_som:
    st.selectbox("SOM", ["Mudo", "Voz 1", "Voz 2"], key="p_som")

st.markdown("<hr>", unsafe_allow_html=True)

# --- 6. DISPLAY ---
st.markdown(f"<h1 style='text-align: center; font-family: Georgia; font-size: 32px;'>{st.session_state.page}</h1>", unsafe_allow_html=True)
