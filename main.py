import streamlit as st
import os

# --- 1. BOOT: HARDWARE (IDÊNTICO AO SEU SEGURO) ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'page' not in st.session_state:
    st.session_state.page = 'demo'

# --- 2. MOTOR: CARREGAMENTO (DIRETO DA \MD_FILES) ---
def load_md_content(p):
    # Mapeamento estrito dos nomes de arquivo que você definiu
    mapping = {
        "off-mach": "OFF-MACHINA",
        "opinião": "COMMENTS",
        "sobre": "SOBRE"
    }
    file_name = mapping.get(p, p.upper())
    # Caminho real conforme sua correção: pasta md_files
    path = f"md_files/ABOUT_{file_name}.MD"
    
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# --- 3. CSS: ESTRUTURA E SIMETRIA ---
st.markdown("""
<style>
    [data-testid="stHeader"] {display: none !important;}
    
    /* Largura da Sidebar conforme o seguro */
    [data-testid="stSidebar"] { min-width: 310px !important; }

    /* Botões: Simetria e Redução */
    .stButton>button {
        border-radius: 20px !important;
        font-family: 'Georgia', serif !important;
        text-transform: none !important;
    }

    /* Botões de Navegação Superior */
    .nav-main button { width: 100px !important; height: 35px !important; font-size: 13px !important; }

    /* Botões de Navegação do Palco (Reduzidos conforme solicitado) */
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
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Lista de Idiomas (Início com os 6 pilares)
    idiomas = [
        "português", "español", "english", "français", "italiano", "català",
        "afrikaans", "deutsch", "aragonés", "asturianu", "dansk", "esperanto", 
        "latina", "norsk", "polski", "română", "turkce"
    ]
    st.selectbox("🌐 idioma", idiomas, key="sb_lang")
    
    st.divider()
    
    c1, c2 = st.columns(2)
    with c1: st.toggle("arte", value=True, key="t_a")
    with c2: st.toggle("som", key="t_s")
    
    st.divider()
    
    # Imagem Dinâmica (Pasta raiz conforme ypo_seguro)
    img_key = "off-machina" if st.session_state.page == "off-mach" else st.session_state.page.lower()
    img_path = f"img_{img_key}.jpg"
    if os.path.exists(img_path):
        st.image(img_path, width="stretch")
    
    st.divider()
    # O conteúdo INFO/ABOUT na sidebar
    st.markdown(f"<div style='font-size: 12px; font-family: Georgia;'>{load_md_content(st.session_state.page)}</div>", unsafe_allow_html=True)

# --- 5. NAVEGAÇÃO SUPERIOR ---
menu = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
cols_nav = st.columns(len(menu))

for i, item in enumerate(menu):
    with cols_nav[i]:
        tag = 'on' if st.session_state.page == item else 'off'
        label = "yPoemas" if item == "yPoemas" else item.lower()
        st.markdown(f"<div class='nav-main st-key-{tag}'>", unsafe_allow_html=True)
        if st.button(label, key=f"nav_{i}"):
            st.session_state.page = item
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# --- 6. RÉGUA DE NAVEGAÇÃO DO PALCO (SOMA 10) ---
p = st.session_state.page

if p == "demo":
    f1, more, rand, auto, f2 = st.columns([3.5, 1, 1, 1, 3.5])
    with more: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("＋", key="d1")
    with rand: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("＊", key="d2")
    with auto: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("？", key="d3")

elif p == "yPoemas":
    f1, more, last, rand, nest, manu, f2 = st.columns([2.5, 1, 1, 1, 1, 1, 2.5])
    with more: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("＋", key="y1")
    with last: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("＜", key="y2")
    with rand: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("＊", key="y3")
    with nest: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("＞", key="y4")
    with manu: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("？", key="y5")

# --- 7. CONTEÚDO CENTRAL ---
# Exibe o texto completo no palco para Opinião e Sobre
if p in ["opinião", "sobre"]:
    st.markdown(load_md_content(p))

st.divider()
titulo = "yPoemas" if p == "yPoemas" else p.lower()
st.markdown(f"<h1 style='text-align: center; font-family: Georgia; font-weight: 200;'>{titulo}</h1>", unsafe_allow_html=True)
