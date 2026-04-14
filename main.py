import streamlit as st
import os

# --- 1. BOOT: HARDWARE (SINTAXE 2026) ---
st.set_page_config(
    page_title="yPoemas", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

if 'page' not in st.session_state:
    st.session_state.page = 'demo'

# --- 2. MOTOR: RESGATE (RIGOR UPPERCASE) ---
def get_content(p):
    mapping = {
        "off-mach": "OFF-MACHINA",
        "opinião": "COMMENTS",
        "sobre": "SOBRE"
    }
    file_key = mapping.get(p, p.upper())
    path = f"md_files/ABOUT_{file_key}.MD"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# --- 3. CSS: ESTRUTURA LIMPA ---
st.markdown("""
<style>
    [data-testid="stHeader"] {display: none !important;}
    
    /* BOTÕES: SIMETRIA TOTAL */
    .stButton>button {
        border-radius: 20px !important;
        font-family: 'Georgia', serif !important;
        font-size: 13px !important;
        width: 100px !important; 
        height: 35px !important;
        margin: 0 auto !important;
        display: block !important;
        text-transform: none !important;
    }
    
    .st-key-on button {background-color: #000 !important; color: #fff !important; border: none !important;}
    .st-key-off button {background-color: #fff !important; color: #aaa !important; border: 1px solid #eee !important;}
    
    .info-box {
        font-size: 12px;
        font-family: 'Georgia', serif;
        padding: 12px;
        border-left: 3px solid #000;
        background: #fafafa;
    }

    .main .block-container {
        max-width: 1100px !important;
        margin: 0 auto !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR: COCKPIT (SEM OBSTRUÇÕES) ---
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    
    idiomas_ptc = [
        "português", "español", "english", "français", "italiano", "català",
        "afrikaans", "deutsch", "aragonés", "asturianu", "dansk", "esperanto", 
        "latina", "norsk", "polski", "română", "turkce"
    ]
    
    st.selectbox("🌐 idioma", idiomas_ptc, key="sb_lang")
    st.divider()
    
    c1, c2 = st.columns(2)
    with c1: st.toggle("arte", value=True, key="t_a")
    with c2: st.toggle("som", key="t_s")
    
    st.divider()
    img_key = "off-machina" if st.session_state.page == "off-mach" else st.session_state.page.lower()
    img_path = f"img_{img_key}.jpg"
    if os.path.exists(img_path):
        # ATUALIZADO: width='stretch' substitui use_container_width
        st.image(img_path, width="stretch")
    
    st.divider()
    st.markdown(f"<div class='info-box'>{get_content(st.session_state.page)}</div>", unsafe_allow_html=True)

# --- 5. NAVEGAÇÃO: BOTÕES UNIFORMES ---
menu = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
cols_nav = st.columns(len(menu)) 

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

# --- 6. RÉGUA E PALCO (A MATEMÁTICA DO 10) ---
p = st.session_state.page

if p == "demo":
    # Soma = 3.5 + 1 + 1 + 1 + 3.5 = 10
    f1, more, rand, auto, f2 = st.columns([3.5, 1, 1, 1, 3.5])
    with more: st.button("＋", key="d1")
    with rand: st.button("＊", key="d2")
    with auto: st.button("？", key="d3")

elif p == "yPoemas":
    # Soma = 2.5 + 1 + 1 + 1 + 1 + 1 + 2.5 = 10
    f1, more, last, rand, nest, manu, f2 = st.columns([2.5, 1, 1, 1, 1, 1, 2.5])
    with more: st.button("＋", key="y1")
    with last: st.button("＜", key="y2")
    with rand: st.button("＊", key="y3")
    with nest: st.button("＞", key="y4")
    with manu: st.button("？", key="y5")

# Conteúdo principal
conteudo_principal = get_content(p)
if conteudo_principal:
    st.markdown(conteudo_principal)

st.divider()

# --- 7. TÍTULO ---
titulo = "yPoemas" if p == "yPoemas" else p.lower()
st.markdown(f"<h1 style='text-align: center; font-family: Georgia; font-weight: 200;'>{titulo}</h1>", unsafe_allow_html=True)
