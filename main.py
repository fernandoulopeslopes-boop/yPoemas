import streamlit as st
import os

# --- 1. BOOT (FIEL AO SEGURO) ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
)

if 'page' not in st.session_state:
    st.session_state.page = 'demo'

# --- 2. MOTOR DE CARGA (COM VERIFICAÇÃO DE EXISTÊNCIA) ---
def load_md_file(file_name):
    # Procura na pasta md_files
    path = os.path.join("md_files", file_name)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return f""

# --- 3. CSS ESSENCIAL ---
st.markdown("""
<style>
    [data-testid="stHeader"] {display: none !important;}
    .stButton>button {
        border-radius: 20px !important;
        font-family: 'Georgia', serif !important;
        width: 100px !important; height: 35px !important;
    }
    .nav-symbol button {
        width: 40px !important; height: 40px !important;
        font-size: 18px !important; border-radius: 50% !important;
    }
    .st-key-on button {background-color: #000 !important; color: #fff !important;}
    .st-key-off button {background-color: #fff !important; color: #aaa !important; border: 1px solid #eee !important;}
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR (PROTEGIDA CONTRA CRASH) ---
with st.sidebar:
    st.markdown("### 🌐 idioma")
    st.selectbox("", ["português", "español", "english", "italiano"], key="lang_v34", label_visibility="collapsed")
    
    st.divider()
    cl, cr = st.columns(2)
    with cl: st.button("<<", key="sb_prev")
    with cr: st.button(">>", key="sb_next")
    
    st.divider()
    
    # PROTEÇÃO CONTRA O ERRO DE IMAGEM:
    p_atual = st.session_state.page.lower()
    img_name = "off-machina" if p_atual == "off-mach" else p_atual
    img_file = f"img_{img_name}.jpg"
    
    if os.path.exists(img_file):
        st.image(img_file)
    else:
        st.warning(f"Imagem {img_file} não encontrada na raiz.")

# --- 5. NAVEGAÇÃO SUPERIOR ---
menu = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
cols = st.columns(6)

for i, item in enumerate(menu):
    with cols[i]:
        tag = 'on' if st.session_state.page == item else 'off'
        if st.button(item.lower() if item != "yPoemas" else "yPoemas", key=f"nav_{i}"):
            st.session_state.page = item
            st.rerun()

st.divider()

# --- 6. RÉGUA DO PALCO (MATEMÁTICA DO 10) ---
p = st.session_state.page
if p == "demo":
    f1, b1, b2, b3, f2 = st.columns([3.5, 1, 1, 1, 3.5])
    with b1: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("＋", key="d1")
    with b2: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("＊", key="d2")
    with b3: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("？", key="d3")
elif p == "yPoemas":
    f1, b1, b2, b3, b4, b5, f2 = st.columns([2.5, 1, 1, 1, 1, 1, 2.5])
    with b1: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("＋", key="y1")
    with b2: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("＜", key="y2")
    with b3: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("＊", key="y3")
    with b4: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("＞", key="y4")
    with b5: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("？", key="y5")

# --- 7. PALCO CENTRAL ---
if p == "opinião":
    st.markdown(load_md_file("ABOUT_COMMENTS.MD"))
elif p == "sobre":
    st.markdown(load_md_file("ABOUT_SOBRE.MD"))
else:
    st.markdown(load_md_file(f"ABOUT_{p.upper()}.MD"))

st.divider()
st.markdown(f"<h1 style='text-align: center; font-family: Georgia; font-weight: 200;'>{p.lower()}</h1>", unsafe_allow_html=True)
