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

# --- 3. CSS: O ESQUADRO REFINADO ---
st.markdown("""<style>
    [data-testid="stHeader"] {display: none !important;}
    
    /* SIDEBAR FIXA */
    section[data-testid="stSidebar"] {
        min-width: 300px !important;
        max-width: 300px !important;
    }

    /* NAV: BOTÕES PADRONIZADOS (FONTE GEORGIA 13PX) */
    .stButton>button {
        width: 100% !important;
        height: 42px !important;
        border-radius: 20px !important;
        font-family: 'Georgia', serif !important;
        font-size: 13px !important;
        font-weight: 400 !important;
        text-transform: none !important;
    }
    .st-key-on button {background-color: #000 !important; color: #fff !important;}
    .st-key-off button {background-color: #f8f9fa !important; color: #888 !important; border: 1px solid #eee !important;}
    
    /* RÉGUA: QUADRADOS 52PX */
    .st-key-cmd button {
        border-radius: 8px !important;
        width: 52px !important;
        height: 52px !important;
        font-size: 24px !important;
        font-weight: 900 !important;
        background: #fff !important;
        border: 1px solid #ccc !important;
    }

    /* INFO BOX GEORGIA */
    .info-box {
        font-family: 'Georgia', serif;
        font-size: 13px;
        line-height: 1.6;
        padding: 15px;
        border-left: 5px solid #000;
        background-color: #ffffff;
    }

    .main .block-container {
        max-width: 1100px !important;
        margin: 0 auto !important;
    }
</style>""", unsafe_allow_html=True)

# --- 4. SIDEBAR: COCKPIT COMPLETO ---
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    idiomas = ["Português", "Español", "English", "Français", "Italiano", "Català", "German", "Latin"]
    st.selectbox("🌐 IDIOMA", idiomas, key="sb_lang")
    
    st.divider()
    
    # CONTROLES DE ARTE E SOM MUDARAM PARA CÁ
    col_a, col_s = st.columns(2)
    with col_a:
        st.toggle("ARTE", value=True, key="t_a")
    with col_s:
        st.toggle("SOM", key="t_s")
        
    st.divider()
    
    if os.path.exists("img_demo.jpg"):
        st.image("img_demo.jpg", use_container_width=True)
    
    st.divider()
    st.markdown(f"<div class='info-box'>{get_md(st.session_state.page)}</div>", unsafe_allow_html=True)

# --- 5. NAVEGAÇÃO: PALCO SUPERIOR ---
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

# --- 6. RÉGUA DE COMANDO (PROPORÇÃO 7.5) ---
c_cmd = st.columns([1, 1, 1, 1, 1, 7.5])
icones = ["＋", "＜", "＊", "＞", "？"]
for i, icone in enumerate(icones):
    with c_cmd[i]:
        st.markdown("<div class='st-key-cmd'>", unsafe_allow_html=True)
        st.button(icone, key=f"cmd_{i}")
        st.markdown("</div>", unsafe_allow_html=True)

st.write("") 

# RÉGUA DE SELEÇÃO (L-idioma removido, Arte/Som movidos)
# Proporção ajustada para os seletores centrais G e T
c_sel = st.columns([1.5, 3.5, 6.0])

with c_sel[0]: # GRUPO
    grupos = sorted([f[4:-4] for f in os.listdir("base") if f.startswith("rol_")])
    g_sel = st.selectbox("G", grupos, key="s_g", label_visibility="collapsed")

with c_sel[1]: # TEMA
    path_txt = f"base/rol_{g_sel}.txt"
    with open(path_txt, "r", encoding="utf-8") as f:
        temas = [l.strip() for l in f.readlines() if l.strip()]
    st.selectbox("T", temas, key="s_t", label_visibility="collapsed")

st.divider()

# --- 7. DISPLAY ---
st.markdown(f"<h1 style='text-align: center; font-family: Georgia;'>{st.session_state.page}</h1>", unsafe_allow_html=True)
