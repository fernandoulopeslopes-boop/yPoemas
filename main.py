import streamlit as st
import os

# --- 1. BOOT: HARDWARE VIRTUAL ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    layout="wide",
    initial_sidebar_state="expanded",
)

if 'page' not in st.session_state:
    st.session_state.page = 'Demo'

def get_md_content(page_name):
    """Resgate real dos arquivos INFO_*.md"""
    path = f"md_files/INFO_{page_name.upper()}.md"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "Aguardando pulso da Machina..."

# --- 2. CSS: ARQUITETURA DE SIMETRIA ---
st.markdown("""
    <style>
    [data-testid="stHeader"] { display: none !important; }
    
    /* SIDEBAR FORÇADA (320px) */
    section[data-testid="stSidebar"] {
        min-width: 320px !important;
        max-width: 320px !important;
        background-color: #fdfdfd !important;
        border-right: 1px solid #ddd !important;
    }

    /* BOTÕES DE NAVEGAÇÃO: LARGURA IDÊNTICA */
    .stButton > button {
        width: 100% !important;
        height: 42px !important;
        border-radius: 20px !important;
        font-weight: 900 !important;
        font-size: 11px !important;
        text-transform: uppercase;
    }

    .st-key-nav_on button {
        background-color: #000 !important;
        color: #fff !important;
        border: 2px solid #000 !important;
    }

    .st-key-nav_off button {
        background-color: #f8f9fa !important;
        color: #888 !important;
        border: 1px solid #ddd !important;
    }

    /* RÉGUA: OS 5 BOTÕES QUADRADOS */
    .st-key-cmd_btn button {
        border-radius: 8px !important;
        border: 1px solid #ccc !important;
        background-color: #fff !important;
        width: 52px !important;
        height: 52px !important;
        font-size: 24px !important;
        font-weight: 900 !important;
    }

    .info-box {
        font-family: 'Georgia', serif; font-size: 13px; line-height: 1.6;
        background: #fff; padding: 15px; border-left: 5px solid #000;
    }

    .main .block-container { max-width: 1100px !important; margin: 0 auto !important; }
    div[data-testid="stHorizontalBlock"] { align-items: center !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR: COCKPIT ---
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    
    idiomas = ["Português", "Español", "English", "Français", "Italiano", "Català", "German", "Latin"]
    st.selectbox("🌐 IDIOMA", idiomas, key="sb_lang")
    
    st.divider()
    if os.path.exists("img_demo.jpg"):
        st.image("img_demo.jpg", use_container_width=True)
    
    st.divider()
    st.markdown(f"<div class='info-box'>{get_md_content(st.session_state.page)}</div>", unsafe_allow_html=True)

# --- 4. PALCO: NAVEGAÇÃO SUPERIOR (6 ABAS) ---
menu = ["Demo", "yPoemas", "Eureka", "Off-Machina", "Comments", "About"]
cols_nav = st.columns(len(menu))

for i, item in enumerate(menu):
    is_active = st.session_state.page == item
    tag = "nav_on" if is_active else "nav_off"
    with cols_nav[i]:
        st.markdown(f"<div class='st-key-{tag}'>", unsafe_allow_html=True)
        if st.button(item, key=f"nav_{item}", use_container_width=True):
            st.session_state.page = item
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# --- 5. A RÉGUA DE COMANDO (SIMETRIA) ---

# Linha 1: 5 Quadrados
c_cmd = st.columns([1, 1, 1, 1, 1, 7.5])
icons = ["＋", "＜", "＊", "＞", "？"]
for i, col in enumerate(c_cmd[:5]):
    with col:
        st.markdown("<div class='st-key-cmd_btn'>", unsafe_allow_html=True)
        st.button(icons[i], key=f"cmd_{i}")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

# Linha 2: Seletores (Varredura de \base)
row_sel = st.columns([1.1, 1.4, 1.8, 2, 1.1])

# ARTE
with row_sel[0]:
    c_t, c_l = st.columns([1, 2])
    c_t.toggle("A", value=True, key="t_arte", label_visibility="collapsed")
    c_l.markdown("<span style='font-size:13px; font-weight:900;'>ARTE</span>", unsafe_allow_html=True)

# IDIOMA
with row_sel[1]:
    st.selectbox("L", idiomas[:3], key="s_lang", label_visibility="collapsed")

# GRUPO (Varredura real de \base)
with row_sel[2]:
    try:
        grupos_base = [f.replace("rol_", "").replace(".txt", "") for f in os.listdir("base") if f.startswith("rol_")]
        grupo_sel = st.selectbox("G", sorted(grupos_base), key="s_group", label_visibility="collapsed")
    except:
        grupo_sel = st.selectbox("G", ["todos os temas"], key="s_group_fail", label_visibility="collapsed")

# TEMA (Leitura do rol selecionado)
with row_sel[3]:
    try:
        with open(f"base/rol_{grupo_sel}.txt", "r", encoding="utf-8") as f:
            temas = [l.strip() for l in f.readlines() if l.strip()]
        st.selectbox("T", temas, key="s_tema", label_visibility="collapsed")
    except:
        st.selectbox("T", ["Amaré"], key="s_tema_fail", label_visibility="collapsed")

# SOM
with row_sel[4]:
    c_t_s, c_l_s = st.columns([1, 2])
    c_t_s.toggle("S", value=False, key="t_som", label_visibility="collapsed")
    c_l_s.markdown("<span style='font-size:13px; font-weight:900;'>SOM</span>", unsafe_allow_html=True)

st.divider()

# --- 6. DISPLAY ---
st.markdown(f"<h1 style='text-align: center; font-family: Georgia;'>{st.session_state.page}</h1>", unsafe_allow_html=True)
