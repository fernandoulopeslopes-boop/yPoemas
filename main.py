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

# --- 2. MOTOR: RESGATE (SINCRONIZADO COM LOWER) ---
def get_md(p):
    # Mantém a busca compatível com a nova estética
    filename = "yPoemas" if p == "yPoemas" else p.lower()
    path = f"md_files/INFO_{filename}.md"
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except: return ""
    return ""

# --- 3. CSS: ESTÉTICA LOWER E RESGATE ---
st.markdown("""
<style>
    [data-testid="stHeader"] {display: none !important;}
    
    /* SIDEBAR: RESET TOTAL PARA FORÇAR EXIBIÇÃO */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #f0f0f0 !important;
    }

    /* BOTÕES: ESTÉTICA LOWER (EXCETO yPOEMAS VIA LOGICA PYTHON) */
    .stButton>button {
        border-radius: 20px !important;
        font-family: 'Georgia', serif !important;
        font-size: 13px !important;
        letter-spacing: 0.5px;
        white-space: nowrap !important;
        width: 100% !important;
        text-transform: none !important; /* Remove o UPPER automático */
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
    
    col_a, col_s = st.columns(2)
    with col_a: st.toggle("arte", value=True, key="t_a")
    with col_s: st.toggle("som", key="t_s")
    
    st.divider()
    # Imagem baseada no nome da página
    img_name = "ypoemas" if st.session_state.page == "yPoemas" else st.session_state.page.lower()
    img_path = f"img_{img_name}.jpg"
    
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    elif os.path.exists("img_demo.jpg"):
        st.image("img_demo.jpg", use_container_width=True)
    
    st.divider()
    st.markdown(f"<div class='info-box'>{get_md(st.session_state.page)}</div>", unsafe_allow_html=True)

# --- 5. NAVEGAÇÃO: TOP (LOWER EXCEPT yPOEMAS) ---
menu = ["Demo", "yPoemas", "Eureka", "Off-Machina", "Comments", "About"]
cols_nav = st.columns([1, 1, 1, 1.7, 1.1, 1]) 

for i, item in enumerate(menu):
    with cols_nav[i]:
        tag = 'on' if st.session_state.page == item else 'off'
        # Aplica a regra estética: yPoemas mantém, outros lower()
        label = item if item == "yPoemas" else item.lower()
        
        st.markdown(f"<div class='st-key-{tag}'>", unsafe_allow_html=True)
        if st.button(label, key=f"nav_{i}"):
            st.session_state.page = item
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# --- 6. RÉGUA DE COMANDOS (PROPORÇÕES ORIGINAIS) ---
p = st.session_state.page

if p == "Demo":
    f1, more, rand, auto, f2 = st.columns([4, 1, 1, 1, 4])
    with more: st.button("＋", key="c1")
    with rand: st.button("＊", key="c2")
    with auto: st.button("？", key="c3")

elif p == "yPoemas":
    f1, more, last, rand, nest, manu, f2 = st.columns([3, 1, 1, 1, 1, 1, 3])
    with more: st.button("＋", key="y1")
    with last: st.button("＜", key="y2")
    with rand: st.button("＊", key="y3")
    with nest: st.button("＞", key="y4")
    with manu: st.button("？", key="y5")

elif p == "Eureka":
    seed, more, rand, manu, occ = st.columns([2.5, 1.5, 1.5, 0.7, 4])
    with seed: st.text_input("seed", label_visibility="collapsed", placeholder="semente...")
    with more: st.button("cultivar", key="e1")

elif p == "Off-Machina":
    f1, last, rand, nest, love, manu, f2 = st.columns([2.5, 1, 1, 1, 1, 1, 2.5])
    with last: st.button("＜", key="o1")
    with rand: st.button("＊", key="o2")
    with nest: st.button("＞", key="o3")
    with love: st.button("♥", key="o4")
    with manu: st.button("？", key="o5")

st.divider()

# --- 7. PALCO ---
titulo = p if p == "yPoemas" else p.lower()
st.markdown(f"<h1 style='text-align: center; font-family: Georgia; font-weight: 200;'>{titulo}</h1>", unsafe_allow_html=True)
