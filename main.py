import streamlit as st
import os

# --- 1. BOOT: HARDWARE ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    layout="wide", 
    initial_sidebar_state="expanded"
)

if 'page' not in st.session_state:
    st.session_state.page = 'demo'

# --- 2. MOTOR DE RESGATE (RIGOR TOTAL: ABOUT_ + UPPER + .MD) ---
def get_md_content(p):
    # O arquivo físico na pasta \md_files\ é sempre UPPERCASE
    # demo -> ABOUT_DEMO.MD | comments -> ABOUT_COMMENTS.MD
    path = f"md_files/ABOUT_{p.upper()}.MD"
    
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""
    return "" # Silêncio absoluto se não existir, sem textos genéricos

# --- 3. CSS: VERNIZ E RESGATE DO COCKPIT ---
st.markdown("""
<style>
    [data-testid="stHeader"] {display: none !important;}
    
    /* SIDEBAR: FORÇAR ESTADO ABERTO E VISÍVEL */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #f0f0f0 !important;
        min-width: 300px !important;
    }

    /* NAV SUPERIOR: REGRAS ESTÉTICAS DO PTC */
    .stButton>button {
        border-radius: 20px !important;
        font-family: 'Georgia', serif !important;
        font-size: 13px !important;
        letter-spacing: 0.5px;
        white-space: nowrap !important;
        width: 100% !important;
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
        line-height: 1.6;
    }

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
    # Imagem: nome do arquivo em lower()
    img_name = st.session_state.page.lower()
    img_path = f"img_{img_name}.jpg"
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    
    st.divider()
    # Puxa o conteúdo dinâmico para a sidebar do arquivo MD correspondente
    st.markdown(f"<div class='info-box'>{get_md_content(st.session_state.page)}</div>", unsafe_allow_html=True)

# --- 5. NAVEGAÇÃO: ANCORAGEM [1, 1, 1, 1.7, 1.1, 1] ---
menu = ["demo", "yPoemas", "eureka", "off-machina", "comments", "sobre"]
cols_nav = st.columns([1, 1, 1, 1.7, 1.1, 1]) 

for i, item in enumerate(menu):
    with cols_nav[i]:
        tag = 'on' if st.session_state.page == item else 'off'
        st.markdown(f"<div class='st-key-{tag}'>", unsafe_allow_html=True)
        # Rótulo: yPoemas mantém, outros em lower()
        label = item if item == "yPoemas" else item.lower()
        if st.button(label, key=f"nav_{i}"):
            st.session_state.page = item
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# --- 6. RÉGUA E CONTEÚDO ---
p = st.session_state.page

if p == "demo":
    f1, more, rand, auto, f2 = st.columns([4, 1, 1, 1, 4])
    with more: st.button("＋", key="cmd_1")
    with rand: st.button("＊", key="cmd_2")
    with auto: st.button("？", key="cmd_3")

elif p == "eureka":
    seed, more, rand, manu, occ = st.columns([2.5, 1.5, 1.5, 0.7, 4])
    with seed: st.text_input("seed", label_visibility="collapsed", placeholder="semente...")

# Exibição do conteúdo REAL vindo da pasta \md_files\
conteudo_real = get_md_content(p)
if conteudo_real:
    st.markdown(conteudo_real)

st.divider()
titulo = "yPoemas" if p == "yPoemas" else p.lower()
st.markdown(f"<h1 style='text-align: center; font-family: Georgia; font-weight: 200;'>{titulo}</h1>", unsafe_allow_html=True)
