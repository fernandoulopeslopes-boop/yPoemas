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
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# --- 3. CSS: REFINAMENTO TIPOGRÁFICO ---
st.markdown("""<style>
    [data-testid="stHeader"] {display: none !important;}
    
    section[data-testid="stSidebar"] { width: 300px !important; }

    /* NAV: FONTE REDUZIDA PARA 11PX (ELEGÂNCIA E ESPAÇO) */
    .stButton>button {
        width: 100% !important;
        height: 38px !important; /* Reduzi levemente a altura acompanhando a fonte */
        border-radius: 20px !important;
        font-family: 'Georgia', serif !important;
        font-size: 11px !important; 
        font-weight: 400 !important;
        white-space: nowrap !important; 
        text-transform: uppercase; /* Pequena caixa alta para compensar o tamanho */
        letter-spacing: 0.5px;
    }
    
    .st-key-on button {background-color: #000 !important; color: #fff !important;}
    .st-key-off button {background-color: #f8f9fa !important; color: #888 !important; border: 1px solid #eee !important;}
    
    /* RÉGUA: COMANDOS FIXOS */
    .st-key-cmd button {
        border-radius: 8px !important;
        width: 50px !important;
        height: 50px !important;
        font-size: 20px !important;
        background: #fff !important;
        border: 1px solid #ccc !important;
    }

    /* SELETORES (LIVROS/TEMAS): FONTE 12PX */
    div[data-baseweb="select"] {
        font-family: 'Georgia', serif !important;
        font-size: 12px !important;
    }

    .info-box {
        font-family: 'Georgia', serif;
        font-size: 13px;
        line-height: 1.6;
        padding: 15px;
        border-left: 5px solid #000;
        background-color: #ffffff;
    }

    .main .block-container {
        max-width: 95% !important;
        margin: 0 auto !important;
    }
</style>""", unsafe_allow_html=True)

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
        st.image("img_demo.jpg", width='stretch')
    st.divider()
    st.markdown(f"<div class='info-box'>{get_md(st.session_state.page)}</div>", unsafe_allow_html=True)

# --- 5. NAVEGAÇÃO: TOP ---
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

# --- 6. RÉGUA DE CONTROLE: SIMETRIA COM FONTE LEVE ---
c_regua = st.columns([3.5, 6, 3.5])

with c_regua[0]: # LIVROS
    livros = sorted([f[4:-4] for f in os.listdir("base") if f.startswith("rol_")])
    st.selectbox("LIVROS", livros, key="s_g", label_visibility="collapsed")

with c_regua[1]: # COMANDOS (CENTRO 7.5)
    cc_nav = st.columns([1, 1, 1, 1, 1, 7.5])
    icones = ["＋", "＜", "＊", "＞", "？"]
    for i, icone in enumerate(icones):
        with cc_nav[i]:
            st.markdown("<div class='st-key-cmd'>", unsafe_allow_html=True)
            st.button(icone, key=f"cmd_{i}")
            st.markdown("</div>", unsafe_allow_html=True)

with c_regua[2]: # TEMAS
    g_sel = st.session_state.s_g
    path_txt = f"base/rol_{g_sel}.txt"
    temas = open(path_txt, "r", encoding="utf-8").read().splitlines() if os.path.exists(path_txt) else ["..."]
    st.selectbox("TEMAS", temas, key="s_t", label_visibility="collapsed")

st.divider()

# --- 7. PALCO ---
st.markdown(f"<h1 style='text-align: center; font-family: Georgia;'>{st.session_state.page}</h1>", unsafe_allow_html=True)
