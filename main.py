import streamlit as st
import os

# --- 1. BOOT ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="expanded")

if 'page' not in st.session_state:
    st.session_state.page = 'demo'

# --- 2. MOTOR DE RESGATE ---
def get_content(p):
    path = f"md_files/ABOUT_{p.upper()}.MD"
    return open(path, "r", encoding="utf-8").read() if os.path.exists(path) else ""

# --- 3. VERNIZ ---
st.markdown("""
<style>
    [data-testid="stHeader"] {display: none !important;}
    .stButton>button {
        border-radius: 20px !important;
        font-family: 'Georgia', serif !important;
        text-transform: none !important;
        width: 100% !important;
    }
    .st-key-on button {background-color: #000 !important; color: #fff !important;}
    .st-key-off button {background-color: #fff !important; color: #aaa !important; border: 1px solid #eee !important;}
    
    /* Moldura de Pergaminho para o Texto */
    .pergaminho-container {
        background-image: url('app/static/Pergaminho.jpg');
        background-size: cover;
        padding: 60px;
        font-family: 'Georgia', serif;
        min-height: 400px;
        color: #2c1e11;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    st.selectbox("🌐 idioma", ["português", "español", "english", "français", "italiano", "català"], key="sb_lang")
    st.divider()
    c1, c2 = st.columns(2)
    with c1: st.toggle("arte", value=True, key="t_a")
    with c2: st.toggle("som", key="t_s")
    st.divider()
    st.markdown(get_content(st.session_state.page))

# --- 5. NAVEGAÇÃO ---
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

# --- 6. RÉGUA COM AS NOVAS IMAGENS ---
p = st.session_state.page

if p == "yPoemas":
    f1, more, last, rand, nest, manu, f2 = st.columns([3, 1, 1, 1, 1, 1, 3])
    with more: st.button("＋", key="y1")
    with last: st.image("Seta_Esquerda.bmp", width=30)
    with rand: st.image("Random_24.ico", width=30)
    with nest: st.image("Seta_Direita.bmp", width=30)
    with manu: st.button("？", key="y5")

# --- 7. PALCO (O PERGAMINHO) ---
st.markdown(f"""
<div class="pergaminho-container">
    <h1 style='text-align: center; font-weight: 200;'>{p if p == "yPoemas" else p.lower()}</h1>
    <br>
    {get_content(p)}
</div>
""", unsafe_allow_html=True)
