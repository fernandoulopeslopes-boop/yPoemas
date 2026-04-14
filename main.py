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

# --- 2. MOTOR: RESGATE (LIMPO) ---
def get_md(p):
    path = f"md_files/INFO_{p.upper()}.md"
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""
    return ""

# --- 3. CSS: SINTAXE BLINDADA ---
st.markdown("""
<style>
    [data-testid="stHeader"] {display: none !important;}
    
    /* SIDEBAR CLEAN */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #f0f0f0;
    }

    /* NAV: 11PX CENTRALIZADO */
    .stButton>button {
        width: 100% !important;
        height: 38px !important;
        border-radius: 20px !important;
        font-family: 'Georgia', serif !important;
        font-size: 11px !important; 
        font-weight: 400 !important;
        white-space: nowrap !important; 
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    
    .st-key-on button {background-color: #000 !important; color: #fff !important; border: none !important;}
    .st-key-off button {background-color: #fff !important; color: #aaa !important; border: 1px solid #eee !important;}
    
    /* RÉGUA: COMANDOS */
    .st-key-cmd button {
        border-radius: 4px !important;
        width: 46px !important;
        height: 46px !important;
        font-size: 18px !important;
        background: #fff !important;
        border: 1px solid #ddd !important;
        color: #333 !important;
    }

    /* TIPOGRAFIA 12PX */
    div[data-baseweb="select"], label, .stMarkdown p {
        font-family: 'Georgia', serif !important;
        font-size: 12px !important;
        color: #555 !important;
    }

    .info-box {
        font-family: 'Georgia', serif;
        font-size: 12px;
        line-height: 1.6;
        padding: 12px;
        border-left: 3px solid #000;
        background-color: #fafafa;
    }

    .main .block-container {
        max-width: 900px !important;
        margin: 0 auto !important;
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
    if os.path.exists("img_demo.jpg"):
        st.image("img_demo.jpg", use_container_width=True)
    
    st.divider()
    st.markdown(f"<div class='info-box'>{get_md(st.session_state.page)}</div>", unsafe_allow_html=True)

# --- 5. NAVEGAÇÃO SUPERIOR ---
menu = ["Demo", "yPoemas", "Eureka", "Off-Machina", "Comments", "About"]
c_nav = st.columns(6)
for i, item in enumerate(menu):
    with c_nav[i]:
        tag = 'on' if st.session_state.page == item else 'off'
        st.markdown(f"<div class='st-key-{tag}'>", unsafe_allow_html=True)
        if st.button(item, key=f"nav_{i}"):
            st.session_state.page = item
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# --- 6. RÉGUA DE CONTROLE ---
c_regua = st.columns([2.5, 5, 2.5])

with c_regua[0]: # LISTA LIVROS
    try:
        livros = sorted([f[4:-4] for f in os.listdir("base") if f.startswith("rol_")])
    except Exception:
        livros = ["vazio"]
    st.selectbox("LIVROS", livros, key="s_g", label_visibility="collapsed", help="Biblioteca da Machina")

with c_regua[1]: # COMANDOS CENTRALIZADOS
    cc = st.columns([1, 1, 1, 1, 1, 4.5]) 
    icones = ["＋", "＜", "＊", "＞", "？"]
    for i, icone in enumerate(icones):
        with cc[i]:
            st.markdown("<div class='st-key-cmd'>", unsafe_allow_html=True)
            st.button(icone, key=f"cmd_{i}")
            st.markdown("</div>", unsafe_allow_html=True)

with c_regua[2]: # LISTA TEMAS
    g_sel = st.session_state.get('s_g', livros[0] if (livros and livros[0] != "vazio") else "")
    temas = ["..."]
    if g_sel:
        path_txt = f"base/rol_{g_sel}.txt"
        if os.path.exists(path_txt):
            try:
                with open(path_txt, "r", encoding="utf-8") as f:
                    temas = [l.strip() for l in f.readlines() if l.strip()]
            except Exception:
                pass
    st.selectbox("TEMAS", temas, key="s_t", label_visibility="collapsed", help="Lista de Temas")

st.divider()

# --- 7. PALCO ---
st.markdown(f"<h1 style='text-align: center; font-family: Georgia; font-weight: 200;'>{st.session_state.page}</h1>", unsafe_allow_html=True)
