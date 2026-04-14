import streamlit as st
import os

# --- 1. CONFIGURAÇÃO (DNA DO SEGURO) ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    layout="centered",
    initial_sidebar_state="expanded"
)

if 'page' not in st.session_state:
    st.session_state.page = 'demo'

# --- 2. MOTOR DE RESGATE ---
def load_md_file(file_name):
    path = os.path.join("md_files", file_name)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        print(path)
    return ""

# --- 3. CSS (VERNIZ SEM CONFLITO) ---
st.markdown("""
<style>
    [data-testid="stHeader"] {display: none !important;}
    
    /* Botões Superiores */
    .stButton>button {
        border-radius: 20px !important;
        font-family: 'Georgia', serif !important;
        width: 100px !important; height: 35px !important;
    }

    /* Símbolos do Palco */
    .nav-symbol button {
        width: 42px !important; height: 42px !important;
        font-size: 18px !important; border-radius: 50% !important;
    }
    
    .st-key-on button {background-color: #000 !important; color: #fff !important;}
    .st-key-off button {background-color: #fff !important; color: #aaa !important; border: 1px solid #eee !important;}
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR (O COCKPIT REAL) ---
with st.sidebar:
    st.markdown("### 🌐 cockpit")
    # LISTA PLENA (SEM TRUNCAR)
    idiomas_plenos = [
        "português", "español", "english", "français", 
        "italiano", "català", "latina", "deutsch", 
        "esperanto", "galego", "ελληνικά"
    ]
    st.selectbox("selecionar idioma", idiomas_plenos, key="sb_lang", label_visibility="collapsed")
    
    st.divider()
    cl, cr = st.columns(2)
    with cl: st.button("<<", key="sb_prev")
    with cr: st.button(">>", key="sb_next")
    
    st.divider()
    p_atual = st.session_state.page.lower()
    img_name = "off-machina" if p_atual == "off-mach" else p_atual
    img_file = f"img_{img_name}.jpg"
    if os.path.exists(img_file):
        st.image(img_file)
    
    st.markdown(f"<div style='font-size:12px;'>{load_md_file(f'ABOUT_{st.session_state.page.upper()}.MD')}</div>", unsafe_allow_html=True)

# --- 5. NAVEGAÇÃO SUPERIOR (MENU 6) ---
menu = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
cols = st.columns(6)

for i, item in enumerate(menu):
    with cols[i]:
        tag = 'on' if st.session_state.page == item else 'off'
        label = "yPoemas" if item == "yPoemas" else item.lower()
        if st.button(label, key=f"nav_{i}"):
            st.session_state.page = item
            st.rerun()

st.divider()

# --- 6. RÉGUA DO PALCO ---
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
