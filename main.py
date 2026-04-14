import streamlit as st
import os

# --- 1. BOOT: HARDWARE ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Inicialização do estado da página
if 'page' not in st.session_state:
    st.session_state.page = 'demo'

# --- 2. CONTEÚDO FIXO (PRESERVAÇÃO DO ORIGINAL) ---
# Injetado aqui para garantir que apareça enquanto o sistema de arquivos oscila
CONTENT_COMMENTS = """
### comentários e impressões
Aqui reside a voz do leitor. Espaço para as impressões colhidas durante a navegação pela Machina.
"""

CONTENT_SOBRE = """
### sobre a Machina
A Machina de Fazer Poesia (yPoemas) é um projeto que une linguística generativa e arte digital. 
O objetivo é a criação de um cockpit de leitura onde o acaso e a precisão técnica coexistem.
"""

# --- 3. CSS: VERNIZ ESSENCIAL ---
st.markdown("""
<style>
    [data-testid="stHeader"] {display: none !important;}
    
    /* BOTÕES: ESTÉTICA LOWER E yPOEMAS */
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

# --- 4. SIDEBAR: COCKPIT NATIVO ---
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    st.selectbox("🌐 idioma", ["português", "español", "english", "français", "italiano", "català"], key="sb_lang")
    st.divider()
    
    c1, c2 = st.columns(2)
    with c1: st.toggle("arte", value=True, key="t_a")
    with c2: st.toggle("som", key="t_s")
    
    st.divider()
    # Busca de imagem (lowercase para o arquivo)
    img_name = st.session_state.page.lower()
    img_path = f"img_{img_name}.jpg"
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    
    st.divider()
    st.markdown("<div class='info-box'>Configurações e Metadados da Página</div>", unsafe_allow_html=True)

# --- 5. NAVEGAÇÃO: ANCORAGEM CALIBRADA ---
menu = ["demo", "yPoemas", "eureka", "off-machina", "comments", "sobre"]
cols_nav = st.columns([1, 1, 1, 1.7, 1.1, 1]) 

for i, item in enumerate(menu):
    with cols_nav[i]:
        tag = 'on' if st.session_state.page == item else 'off'
        st.markdown(f"<div class='st-key-{tag}'>", unsafe_allow_html=True)
        # Rótulo estético
        label = item if item == "yPoemas" else item.lower()
        if st.button(label, key=f"nav_{i}"):
            st.session_state.page = item
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# --- 6. PALCO CENTRAL ---
p = st.session_state.page

if p == "demo":
    f1, more, rand, auto, f2 = st.columns([4, 1, 1, 1, 4])
    with more: st.button("＋", key="cmd_1")
    with rand: st.button("＊", key="cmd_2")
    with auto: st.button("？", key="cmd_3")

elif p == "comments":
    st.markdown(CONTENT_COMMENTS)

elif p == "sobre":
    st.markdown(CONTENT_SOBRE)

elif p == "eureka":
    seed, more, rand, manu, occ = st.columns([2.5, 1.5, 1.5, 0.7, 4])
    with seed: st.text_input("seed", label_visibility="collapsed", placeholder="semente...")

st.divider()
titulo = "yPoemas" if p == "yPoemas" else p.lower()
st.markdown(f"<h1 style='text-align: center; font-family: Georgia; font-weight: 200;'>{titulo}</h1>", unsafe_allow_html=True)
