import streamlit as st
import os

# --- 1. BOOT: HARDWARE ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    layout="wide", 
    initial_sidebar_state="expanded"
)

if 'page' not in st.session_state:
    st.session_state.page = 'Demo'

# --- 2. MOTOR: RESGATE ---
def get_md(p):
    path = f"md_files/INFO_{p.upper()}.md"
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except:
            return ""
    return ""

# --- 3. CSS: AJUSTE DE PRECISÃO ---
st.markdown("""
<style>
    [data-testid="stHeader"] {display: none !important;}
    
    /* SIDEBAR: FORÇAR VISIBILIDADE */
    [data-testid="stSidebar"] {
        visibility: visible !important;
        background-color: #ffffff !important;
    }

    /* NAV SUPERIOR: COLUNAS IGUAIS E BOTÕES REDUZIDOS */
    .stButton>button {
        width: 80% !important; /* Redução de 20% conforme solicitado */
        margin: 0 auto !important;
        display: block !important;
        border-radius: 20px !important;
        font-family: 'Georgia', serif !important;
        font-size: 13px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        white-space: nowrap !important;
        padding: 2px 10px !important;
    }
    
    .st-key-on button {background-color: #000 !important; color: #fff !important; border: none !important;}
    .st-key-off button {background-color: #fff !important; color: #aaa !important; border: 1px solid #eee !important;}
    
    /* RÉGUA: COMANDOS */
    .st-key-cmd button {
        border-radius: 4px !important;
        width: 40px !important;
        height: 40px !important;
        font-size: 16px !important;
        background: #fff !important;
        border: 1px solid #ddd !important;
    }

    /* LISTAS */
    div[data-baseweb="select"] {
        font-family: 'Georgia', serif !important;
        font-size: 13px !important;
    }

    .main .block-container {
        max-width: 1000px !important;
        margin: 0 auto !important;
        padding-top: 1rem !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR: COCKPIT ---
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    idiomas = ["Português", "Español", "English", "Français", "Italiano", "Català", "German", "Latin"]
    st.selectbox("🌐 IDIOMA", idiomas, key="sb_lang")
    st.divider()
    
    col_a, col_s = st.columns(2)
    with col_a: st.toggle("ARTE", value=True, key="t_a")
    with col_s: st.toggle("SOM", key="t_s")
    
    st.divider()
    img_path = f"img_{st.session_state.page.lower()}.jpg"
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    elif os.path.exists("img_demo.jpg"):
        st.image("img_demo.jpg", use_container_width=True)
    
    st.divider()
    st.markdown(f"<div style='font-size:12px; font-family:Georgia; padding:10px; border-left:3px solid #000; background:#fafafa;'>{get_md(st.session_state.page)}</div>", unsafe_allow_html=True)

# --- 5. NAVEGAÇÃO: ESPAÇAMENTO IDÊNTICO ---
menu = ["Demo", "yPoemas", "Eureka", "Off-Machina", "Comments", "About"]
# Criando 6 colunas rigorosamente iguais
cols_nav = st.columns([1, 1, 1, 1, 1, 1])
for i, item in enumerate(menu):
    with cols_nav[i]:
        tag = 'on' if st.session_state.page == item else 'off'
        st.markdown(f"<div class='st-key-{tag}'>", unsafe_allow_html=True)
        if st.button(item, key=f"nav_{i}"):
            st.session_state.page = item
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# --- 6. RÉGUA: LARGURA ÚTIL ---
c_regua = st.columns([3, 4, 3])

with c_regua[0]: # LIVROS
    try:
        livros = sorted([f[4:-4] for f in os.listdir("base") if f.startswith("rol_")])
    except:
        livros = ["vazio"]
    st.selectbox("L", livros, key="s_g", label_visibility="collapsed", help="Livros disponíveis")

with c_regua[1]: # COMANDOS
    cc = st.columns(5)
    icones = ["＋", "＜", "＊", "＞", "？"]
    for i, icone in enumerate(icones):
        with cc[i]:
            st.markdown("<div class='st-key-cmd'>", unsafe_allow_html=True)
            st.button(icone, key=f"cmd_{i}")
            st.markdown("</div>", unsafe_allow_html=True)

with c_regua[2]: # TEMAS
    g_sel = st.session_state.get('s_g', "")
    temas = ["..."]
    if g_sel:
        path_txt = f"base/rol_{g_sel}.txt"
        if os.path.exists(path_txt):
            with open(path_txt, "r", encoding="utf-8") as f:
                temas = [l.strip() for l in f.readlines() if l.strip()]
    st.selectbox("T", temas, key="s_t", label_visibility="collapsed", help=f"Folhas -> {g_sel}")

st.divider()

# --- 7. PALCO ---
st.markdown(f"<h1 style='text-align: center; font-family: Georgia; font-weight: 200;'>{st.session_state.page}</h1>", unsafe_allow_html=True)
