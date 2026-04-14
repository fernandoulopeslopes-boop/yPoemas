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

# --- 3. CSS: REFINAMENTO CIRÚRGICO ---
st.markdown("""
<style>
    [data-testid="stHeader"] {display: none !important;}
    
    /* SIDEBAR: FORÇAR COMPORTAMENTO */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #f0f0f0 !important;
        min-width: 300px !important;
    }

    /* NAV SUPERIOR: CENTRALIZAÇÃO E DISTÂNCIA REGULAR */
    .nav-container {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-bottom: 20px;
    }

    .stButton>button {
        border-radius: 20px !important;
        font-family: 'Georgia', serif !important;
        font-size: 11px !important; 
        text-transform: uppercase;
        letter-spacing: 0.8px;
        transition: all 0.2s;
    }
    
    .st-key-on button {background-color: #000 !important; color: #fff !important;}
    .st-key-off button {background-color: #fff !important; color: #aaa !important; border: 1px solid #eee !important;}
    
    /* RÉGUA: COMANDOS */
    .st-key-cmd button {
        border-radius: 4px !important;
        width: 44px !important;
        height: 44px !important;
        font-size: 18px !important;
        background: #fff !important;
        border: 1px solid #ddd !important;
    }

    /* LISTAS: CORPO MAIOR (14PX) E CENTRALIZAÇÃO */
    div[data-baseweb="select"] {
        font-family: 'Georgia', serif !important;
        font-size: 14px !important; /* Aumento conforme solicitado */
    }

    .main .block-container {
        max-width: 850px !important; /* Redução para facilitar a leitura */
        margin: 0 auto !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR: COCKPIT ---
# A sidebar muda dinamicamente conforme session_state.page
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    idiomas = ["Português", "Español", "English", "Français", "Italiano", "Català", "German", "Latin"]
    st.selectbox("🌐 IDIOMA", idiomas, key="sb_lang")
    st.divider()
    
    col_a, col_s = st.columns(2)
    with col_a: st.toggle("ARTE", value=True, key="t_a")
    with col_s: st.toggle("SOM", key="t_s")
    
    st.divider()
    # Imagem dinâmica baseada na página (se houver padrão de nomeação)
    img_path = f"img_{st.session_state.page.lower()}.jpg"
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    elif os.path.exists("img_demo.jpg"):
        st.image("img_demo.jpg", use_container_width=True)
    
    st.divider()
    st.markdown(f"<div class='info-box'>{get_md(st.session_state.page)}</div>", unsafe_allow_html=True)

# --- 5. NAVEGAÇÃO: TOP CENTRALIZADO ---
menu = ["Demo", "yPoemas", "Eureka", "Off-Machina", "Comments", "About"]
cols_nav = st.columns(len(menu))
for i, item in enumerate(menu):
    with cols_nav[i]:
        tag = 'on' if st.session_state.page == item else 'off'
        st.markdown(f"<div class='st-key-{tag}'>", unsafe_allow_html=True)
        if st.button(item, key=f"nav_{i}"):
            st.session_state.page = item
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# --- 6. RÉGUA: PROPORÇÃO REDUZIDA E CENTRALIZADA ---
# [Lista 2] [Comandos 4] [Lista 2] - Total 8, centralizado por colunas vazias (2-8-2)
_, c_regua, _ = st.columns([1, 10, 1])

with c_regua:
    col_l, col_c, col_t = st.columns([2.5, 5, 2.5])
    
    with col_l: # LIVROS
        livros = sorted([f[4:-4] for f in os.listdir("base") if f.startswith("rol_")]) if os.path.exists("base") else ["vazio"]
        st.selectbox("L", livros, key="s_g", 
                     label_visibility="collapsed", 
                     help="Livros disponíveis")

    with col_c: # COMANDOS
        cc = st.columns(5)
        icones = ["＋", "＜", "＊", "＞", "？"]
        for i, icone in enumerate(icones):
            with cc[i]:
                st.markdown("<div class='st-key-cmd'>", unsafe_allow_html=True)
                st.button(icone, key=f"cmd_{i}")
                st.markdown("</div>", unsafe_allow_html=True)

    with col_t: # TEMAS (FOLHAS)
        g_sel = st.session_state.get('s_g', "")
        temas = ["..."]
        if g_sel:
            path_txt = f"base/rol_{g_sel}.txt"
            if os.path.exists(path_txt):
                with open(path_txt, "r", encoding="utf-8") as f:
                    temas = [l.strip() for l in f.readlines() if l.strip()]
        
        st.selectbox("T", temas, key="s_t", 
                     label_visibility="collapsed", 
                     help=f"Folhas -> {g_sel}")

st.divider()

# --- 7. PALCO ---
st.markdown(f"<h1 style='text-align: center; font-family: Georgia; font-weight: 200;'>{st.session_state.page}</h1>", unsafe_allow_html=True)
