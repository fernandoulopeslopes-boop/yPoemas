import streamlit as st
import os

# --- 1. HARDWARE VIRTUAL (SIMETRIA & ELEGÂNCIA) ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Bússola de Estado
if 'page' not in st.session_state:
    st.session_state.page = 'DEMO'

def get_md(page_name):
    """Resgate direto dos arquivos INFO_ na pasta md_files"""
    try:
        path = os.path.join("md_files", f"INFO_{page_name.upper()}.md")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
    except: pass
    return "Aguardando pulso..."

# --- 2. CSS: O "TUDO OU NADA" DA INTERFACE ---
st.markdown("""
    <style>
    /* RESET TOTAL */
    [data-testid="stHeader"] { display: none !important; }
    
    /* SIDEBAR: A ANCORA DO PROJETO (320px) */
    section[data-testid="stSidebar"] {
        min-width: 320px !important;
        max-width: 320px !important;
        background-color: #fdfdfd !important;
        border-right: 1px solid #eee !important;
    }

    /* TOGGLE BUTTONS: NAVEGAÇÃO SUPERIOR (A SIMETRIA) */
    .st-key-nav_on button {
        background-color: #000 !important;
        color: #fff !important;
        border: 2px solid #000 !important;
        border-radius: 20px !important;
        font-weight: 900 !important;
        height: 38px !important;
    }
    .st-key-nav_off button {
        background-color: #f8f9fa !important;
        color: #777 !important;
        border: 1px solid #ddd !important;
        border-radius: 20px !important;
        font-weight: 900 !important;
        height: 38px !important;
    }

    /* INFO BOX: ESTÉTICA DICIONÁRIO GEORGIA */
    .info-box {
        font-family: 'Georgia', serif;
        font-size: 13px;
        line-height: 1.6;
        color: #1a1a1a;
        background: #fff;
        padding: 15px;
        border-left: 5px solid #000;
        margin-top: 10px;
    }

    /* CONSOLE CIRCULAR (5 BOTÕES) */
    .st-key-cmd_btn button {
        background-color: #f0f2f6 !important;
        border-radius: 50% !important;
        width: 46px !important;
        height: 46px !important;
        border: 2px solid #000 !important;
        font-size: 22px !important;
        font-weight: 900 !important;
        display: flex; align-items: center; justify-content: center;
    }

    .main .block-container { max-width: 950px !important; margin: 0 auto !important; }
    hr { border: 0; height: 1px; background: #ddd; margin: 20px 0 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR (O COCKPIT REAL) ---
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # IDIOMA: Resgate do acervo real (Western ABC)
    langs = ["Português", "Español", "English", "Français", "Italiano", "Català", "Latin", "German"]
    st.selectbox("🌐 IDIOMA", langs, key="sb_lang")
    
    st.divider()
    
    # Arte da Página
    if os.path.exists("img_demo.jpg"):
        st.image("img_demo.jpg", use_container_width=True)
    
    st.divider()

    # INFO BOX (Lê INFO_PAGINA.md de md_files)
    st.markdown(f"<div class='info-box'>{get_md(st.session_state.page)}</div>", unsafe_allow_html=True)

# --- 4. PALCO: NAVEGAÇÃO POR TOGGLE BUTTONS ---
menu = ["Demo", "yPoemas", "Eureka", "Off-Machina", "Comments", "About"]
cols = st.columns(len(menu))

for i, item in enumerate(menu):
    is_active = st.session_state.page == item
    tag = "nav_on" if is_active else "nav_off"
    with cols[i]:
        st.markdown(f"<div class='st-key-{tag}'>", unsafe_allow_html=True)
        if st.button(item.upper(), key=f"btn_{item}"):
            st.session_state.page = item
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# --- 5. CONSOLE DE COMANDO (5 Círculos) ---
c_btns, c_tema, c_som = st.columns([1.8, 1.5, 0.8])

with c_btns:
    b_cols = st.columns(5)
    icons = ["＋", "＜", "＊", "＞", "？"]
    for i, col in enumerate(b_cols):
        with col:
            st.markdown("<div class='st-key-cmd_btn'>", unsafe_allow_html=True)
            st.button(icons[i], key=f"cmd_{i}")
            st.markdown("</div>", unsafe_allow_html=True)

with c_tema:
    # Varredura do acervo .ypo real
    try:
        acervo = [f.replace(".ypo", "") for f in os.listdir("data") if f.endswith(".ypo")]
        st.selectbox("TEMAS / LIVROS", sorted(acervo) if acervo else ["Geral"], key="p_tema")
    except:
        st.selectbox("TEMAS", ["Check data/"], key="p_tema_err")

with c_som:
    st.selectbox("SOM", ["Mudo", "Voz 1", "Voz 2"], key="p_som")

st.markdown("<hr>", unsafe_allow_html=True)

# --- 6. DISPLAY ---
st.markdown(f"<h1 style='text-align: center; font-family: Georgia;'>{st.session_state.page}</h1>", unsafe_allow_html=True)
