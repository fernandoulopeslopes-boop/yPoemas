import streamlit as st
import os

# --- 1. BOOT (ESTRUTURA COMPLETA DO YPO_SEGURO) ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
)

if 'page' not in st.session_state:
    st.session_state.page = 'demo'

# --- 2. MOTOR DE CARGA (DIRETO DA MD_FILES) ---
def load_md(file_name):
    # Tradução direta para evitar erro de busca
    mapping = {
        "OPINIÃO": "COMMENTS",
        "SOBRE": "SOBRE",
        "OFF-MACH": "OFF-MACHINA"
    }
    key = mapping.get(file_name.upper(), file_name.upper())
    path = f"md_files/ABOUT_{key}.MD"
    
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# --- 3. CSS (LIMPO E FUNCIONAL) ---
st.markdown("""
<style>
    [data-testid="stHeader"] {display: none !important;}
    
    /* Botões de Navegação Superior */
    .stButton>button {
        border-radius: 20px !important;
        font-family: 'Georgia', serif !important;
        text-transform: none !important;
    }
    .nav-main button { width: 100px !important; height: 35px !important; font-size: 13px !important; }

    /* Botões de Controle do Palco (Reduzidos) */
    .nav-symbol button {
        width: 42px !important; 
        height: 42px !important;
        font-size: 18px !important;
        border-radius: 50% !important;
    }
    
    .st-key-on button {background-color: #000 !important; color: #fff !important; border: none !important;}
    .st-key-off button {background-color: #fff !important; color: #aaa !important; border: 1px solid #eee !important;}
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR: COCKPIT ---
with st.sidebar:
    st.markdown("### 🌐 idioma")
    idiomas = ["português", "español", "english", "français", "italiano", "català", "latina"]
    st.selectbox("", idiomas, key="sb_lang", label_visibility="collapsed")
    
    st.divider()
    c1, c2 = st.columns(2)
    with c1: st.toggle("arte", value=True, key="t_a")
    with c2: st.toggle("som", key="t_s")
    
    st.divider()
    # Botões de Navegação Interna da Sidebar
    sl, sr = st.columns(2)
    with sl: st.button("<<", key="side_l")
    with sr: st.button(">>", key="side_r")
    
    st.divider()
    img_key = "off-machina" if st.session_state.page == "off-mach" else st.session_state.page.lower()
    img_path = f"img_{img_key}.jpg"
    if os.path.exists(img_path):
        st.image(img_path)
    
    st.markdown(load_md(st.session_state.page))

# --- 5. NAVEGAÇÃO DE PÁGINAS (SUPERIOR) ---
menu = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
cols = st.columns(len(menu))

for i, item in enumerate(menu):
    with cols[i]:
        tag = 'on' if st.session_state.page == item else 'off'
        label = "yPoemas" if item == "yPoemas" else item.lower()
        st.markdown(f"<div class='nav-main st-key-{tag}'>", unsafe_allow_html=True)
        if st.button(label, key=f"btn_{i}"):
            st.session_state.page = item
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

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

# --- 7. PALCO CENTRAL (RENDERIZAÇÃO FORÇADA) ---
# Exibe o conteúdo de todas as páginas conforme o menu
conteudo = load_md(p)
if conteudo:
    st.markdown(conteudo)

st.divider()
st.markdown(f"<h1 style='text-align: center; font-family: Georgia; font-weight: 200;'>{p.lower()}</h1>", unsafe_allow_html=True)
