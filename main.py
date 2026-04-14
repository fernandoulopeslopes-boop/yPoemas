import streamlit as st
import os

# --- 1. BOOT: INTEGRIDADE DO PROJETO ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    layout="wide", 
    initial_sidebar_state="expanded"
)

if 'page' not in st.session_state:
    st.session_state.page = 'demo'

# --- 2. MOTOR: RESGATE DE CONTEÚDO (RIGOR ABSOLUTO) ---
def get_content(p):
    # \md_files\ABOUT_[PAGINA_UPPER].MD
    path = f"md_files/ABOUT_{p.upper()}.MD"
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except: return ""
    return ""

# --- 3. VERNIZ: SOBRIEDADE ---
st.markdown("""
<style>
    [data-testid="stHeader"] {display: none !important;}
    
    .stButton>button {
        border-radius: 20px !important;
        font-family: 'Georgia', serif !important;
        font-size: 13px !important;
        text-transform: none !important;
        width: 100% !important;
    }
    
    .st-key-on button {background-color: #000 !important; color: #fff !important; border: none !important;}
    .st-key-off button {background-color: #fff !important; color: #aaa !important; border: 1px solid #eee !important;}
    
    .main .block-container {
        max-width: 1050px !important;
        margin: 0 auto !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR: COCKPIT ---
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    st.selectbox("🌐 idioma", ["português", "español", "english", "français", "italiano", "català"], key="sb_lang")
    st.divider()
    
    c1, c2 = st.columns(2)
    with c1: st.toggle("arte", value=True, key="t_a")
    with c2: st.toggle("som", key="t_s")
    
    st.divider()
    img_path = f"img_{st.session_state.page.lower()}.jpg"
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    
    st.divider()
    st.markdown(get_content(st.session_state.page))

# --- 5. NAVEGAÇÃO: ANCORAGEM CALIBRADA ---
menu = ["demo", "yPoemas", "eureka", "off-machina", "comments", "sobre"]
cols_nav = st.columns([1, 1, 1, 1.7, 1.1, 1]) 

for i, item in enumerate(menu):
    with cols_nav[i]:
        tag = 'on' if st.session_state.page == item else 'off'
        label = "yPoemas" if item == "yPoemas" else item.lower()
        st.markdown(f"<div class='st-key-{tag}'>", unsafe_allow_html=True)
        if st.button(label, key=f"nav_{i}"):
            st.session_state.page = item
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# --- 6. RÉGUA E CONTEÚDO (CONFORME ORIGINAL_SEGURO) ---
p = st.session_state.page

if p == "demo":
    f1, more, rand, auto, f2 = st.columns([4, 1, 1, 1, 4])
    with more: st.button("＋", key="d1")
    with rand: st.button("＊", key="d2")
    with auto: st.button("？", key="d3")

elif p == "yPoemas":
    f1, more, last, rand, nest, manu, f2 = st.columns([3, 1, 1, 1, 1, 1, 3])
    with more: st.button("＋", key="y1")
    with last: st.button("＜", key="y2")
    with rand: st.button("＊", key="y3")
    with nest: st.button("＞", key="y4")
    with manu: st.button("？", key="y5")

elif p == "eureka":
    seed, more, rand, manu, occ = st.columns([2.5, 1.5, 1.5, 0.7, 4])
    with seed: st.text_input("seed", label_visibility="collapsed")
    with more: st.button("cultivar", key="e1")

elif p == "off-machina":
    f1, last, rand, nest, love, manu, f2 = st.columns([2.5, 1, 1, 1, 1, 1, 2.5])
    with last: st.button("＜", key="o1")
    with rand: st.button("＊", key="o2")
    with nest: st.button("＞", key="o3")
    with love: st.button("♥", key="o4")
    with manu: st.button("？", key="o5")

# Exibição do Conteúdo (Comments / Sobre)
if p in ["comments", "sobre"]:
    st.markdown(get_content(p))

st.divider()
titulo = "yPoemas" if p == "yPoemas" else p.lower()
st.markdown(f"<h1 style='text-align: center; font-family: Georgia; font-weight: 200;'>{titulo}</h1>", unsafe_allow_html=True)
