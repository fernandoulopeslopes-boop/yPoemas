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
        except: return ""
    return ""

# --- 3. CSS: VERNIZ E RESGATE DA SIDEBAR ---
st.markdown("""
<style>
    [data-testid="stHeader"] {display: none !important;}
    
    /* FORÇAR SIDEBAR A REAPARECER */
    section[data-testid="stSidebar"] {
        display: block !important;
        visibility: visible !important;
        background-color: #ffffff !important;
        border-right: 1px solid #f0f0f0 !important;
    }

    /* BOTÕES: ESTILO UNIFICADO 13PX */
    .stButton>button {
        border-radius: 20px !important;
        font-family: 'Georgia', serif !important;
        font-size: 13px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        white-space: nowrap !important;
        width: 100% !important;
    }
    
    .st-key-on button {background-color: #000 !important; color: #fff !important; border: none !important;}
    .st-key-off button {background-color: #fff !important; color: #aaa !important; border: 1px solid #eee !important;}
    
    /* RÉGUA E COMANDOS QUADRADOS */
    .st-key-cmd button {
        border-radius: 4px !important;
        width: 42px !important;
        height: 42px !important;
        font-size: 18px !important;
    }

    .main .block-container {
        max-width: 1100px !important;
        margin: 0 auto !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR: COCKPIT ---
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    st.selectbox("🌐 IDIOMA", ["Português", "Español", "English", "Français", "Italiano", "Català"], key="sb_lang")
    st.divider()
    col_a, col_s = st.columns(2)
    with col_a: st.toggle("ARTE", value=True, key="t_a")
    with col_s: st.toggle("SOM", key="t_s")
    st.divider()
    img_path = f"img_{st.session_state.page.lower()}.jpg"
    if os.path.exists(img_path): st.image(img_path, use_container_width=True)
    elif os.path.exists("img_demo.jpg"): st.image("img_demo.jpg", use_container_width=True)
    st.divider()
    st.markdown(f"<div style='font-size:12px; font-family:Georgia; padding:10px; border-left:3px solid #000; background:#fafafa;'>{get_md(st.session_state.page)}</div>", unsafe_allow_html=True)

# --- 5. NAVEGAÇÃO: TOP (PROPORÇÃO CALIBRADA) ---
menu = ["Demo", "yPoemas", "Eureka", "Off-Machina", "Comments", "About"]
cols_nav = st.columns([1, 1, 1, 1.7, 1.1, 1]) 

for i, item in enumerate(menu):
    with cols_nav[i]:
        tag = 'on' if st.session_state.page == item else 'off'
        st.markdown(f"<div class='st-key-{tag}'>", unsafe_allow_html=True)
        if st.button(item, key=f"nav_{i}"):
            st.session_state.page = item
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# --- 6. RÉGUA: COMANDOS POR PÁGINA (ESTÉTICA ORIGINAL) ---
p = st.session_state.page

if p == "Demo":
    foo1, more, rand, auto, foo2 = st.columns([4, 1, 1, 1, 4])
    with more: st.button("＋", key="cmd_more")
    with rand: st.button("＊", key="cmd_rand")
    with auto: st.button("？", key="cmd_auto")

elif p == "yPoemas":
    foo1, more, last, rand, nest, manu, foo2 = st.columns([3, 1, 1, 1, 1, 1, 3])
    with more: st.button("＋", key="y_more")
    with last: st.button("＜", key="y_last")
    with rand: st.button("＊", key="y_rand")
    with nest: st.button("＞", key="y_next")
    with manu: st.button("？", key="y_manu")

elif p == "Eureka":
    seed, more, rand, manu, occurrences = st.columns([2.5, 1.5, 1.5, 0.7, 4])
    with seed: st.text_input("SEED", label_visibility="collapsed", placeholder="Semente...")
    with more: st.button("CULTIVAR", key="e_more")
    with occurrences: st.markdown("*Ocorrências da Semente*")

elif p == "Off-Machina":
    foo1, last, rand, nest, love, manu, foo2 = st.columns([2.5, 1, 1, 1, 1, 1, 2.5])
    with last: st.button("＜", key="o_last")
    with rand: st.button("＊", key="o_rand")
    with nest: st.button("＞", key="o_next")
    with love: st.button("♥", key="o_love")
    with manu: st.button("？", key="o_manu")

st.divider()

# --- 7. PALCO CENTRAL ---
st.markdown(f"<h1 style='text-align: center; font-family: Georgia; font-weight: 200;'>{st.session_state.page}</h1>", unsafe_allow_html=True)
