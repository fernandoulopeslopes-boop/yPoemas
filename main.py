import streamlit as st
import os

# --- 1. BOOT: HARDWARE ---
st.set_page_config(
    page_title="yPoemas", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

if 'page' not in st.session_state:
    st.session_state.page = 'demo'

# --- 2. MOTOR: RESGATE (RIGOR UPPERCASE) ---
def get_content(p):
    file_key = "OFF-MACHINA" if p == "off-mach" else p.upper()
    path = f"md_files/ABOUT_{file_key}.MD"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# --- 3. CSS: ESTRUTURA RÍGIDA E SIMETRIA ---
st.markdown("""
<style>
    [data-testid="stHeader"] {display: none !important;}
    
    /* FORÇAR VISIBILIDADE DA SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #f0f0f0 !important;
        min-width: 320px !important;
    }

    /* BOTÕES: WIDTH FIXO E ALINHAMENTO MILIMÉTRICO */
    .stButton>button {
        border-radius: 20px !important;
        font-family: 'Georgia', serif !important;
        font-size: 13px !important;
        width: 120px !important; 
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

# --- 4. SIDEBAR: COCKPIT (EXPANSÃO DE IDIOMAS RADICAL) ---
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Lista expandida conforme o novo protocolo de integração multi-idioma
    idiomas_ptc = [
        "português", "afrikaans", "shqip", "deutsch", "aragonés", "asturianu", 
        "brezhoneg", "català", "corsu", "dansk", "español", "esperanto", 
        "euskara", "suomi", "français", "frysk", "galego", "isizulu", 
        "idunnu", "english", "italiano", "latina", "lingua franca nova", 
        "lombard", "magyar", "norsk", "occitan", "polski", "română", 
        "turkce", "viettel"
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
        st.image(img_path, use_container_width=True)
    
    st.divider()
    st.markdown(f"<div class='info-box'>{get_content(st.session_state.page)}</div>", unsafe_allow_html=True)

# --- 5. NAVEGAÇÃO: BOTÕES UNIFORMES ---
menu = ["demo", "yPoemas", "eureka", "off-mach", "comments", "sobre"]
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

# --- 6. RÉGUA E PALCO ---
p = st.session_state.page
conteudo_principal = get_content(p)

if p == "demo":
    f1, more, rand, auto, f2 = st.columns([4, 1, 1, 1, 4])
    with more: st.button("＋", key="d1")
    with rand: st.button("＊", key="d2")
    with auto: st.button("？", key="d3")

elif p == "yPoemas":
    f1, more, last, rand, nest, manu, f2 = st.columns([2.5, 1, 1, 1, 1, 1, 2.5])
    with more: st.button("＋", key="y1")
    with last: st.button("＜", key="y2")
    with rand: st.button("＊", key="y3")
    with nest: st.button("＞", key="y4")
    with manu: st.button("？", key="y5")

if conteudo_principal:
    st.markdown(conteudo_principal)

st.divider()
titulo = "yPoemas" if p == "yPoemas" else p.lower()
st.markdown(f"<h1 style='text-align: center; font-family: Georgia; font-weight: 200;'>{titulo}</h1>", unsafe_allow_html=True)
