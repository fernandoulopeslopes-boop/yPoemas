import os
import streamlit as st
import random
import time

# --- 1. GÊNESE (ESTADOS) ---
if 'page' not in st.session_state: st.session_state.page = "mini"
if 'auto' not in st.session_state: st.session_state.auto = False
if 'mini' not in st.session_state: st.session_state.mini = 0

# --- 2. REGRA 0: LOOK & FEEL (O PALCO ELÁSTICO) ---
st.set_page_config(page_title="yPoemas", layout="wide")

st.markdown("""
    <style>
    footer {visibility: hidden;}
    /* PALCO EXPANSÍVEL */
    .main .block-container { max-width: 95% !important; padding: 1.5rem 2rem !important; margin: 0 auto; }
    [data-testid="stMainViewContainer"] { width: 100% !important; }
    
    /* SIDEBAR VISÍVEL E LIMPA */
    [data-testid="stSidebar"] { width: 240px !important; min-width: 240px !important; visibility: visible !important; }
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] { display: none !important; }
    
    .mini-card {
        font-family: 'IBM Plex Serif', serif;
        font-size: 2rem; line-height: 1.7; color: #1a1a1a;
        text-align: center; padding: 80px 40px;
        background: #fff; border-radius: 15px;
        border: 1px solid #f0f0f0; max-width: 700px; margin: 40px auto;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR (RENDERIZA ANTES DO PALCO PARA NÃO SUMIR) ---
with st.sidebar:
    st.image("img_mini.jpg", use_container_width=True) # Arte da Mini
    st.selectbox("lang", ["pt", "en", "es"], key="lang", label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    # Cookies
    st.session_state.v = c1.checkbox("v", value=True)
    st.session_state.a = c2.checkbox("a", value=True)
    st.session_state.vi = c3.checkbox("vi", value=False)
    
    if st.session_state.auto:
        st.write("Modo Auto Ativo")
        wait_time = st.slider("tempo", 5, 60, 10)

# --- 4. NAVEGAÇÃO ---
nav_cols = st.columns(6)
paginas = ["mini", "ypoemas", "eureka", "off-machina", "comments", "sobre"]
for i, pag in enumerate(paginas):
    if nav_cols[i].button(pag, key=f"btn_{pag}"):
        st.session_state.page = pag
        st.rerun()

st.markdown("---")

# --- 5. O PALCO (PÁGINA MINI) ---
if st.session_state.page == "mini":
    # 5.1 CARREGAR TEMAS DO ORÁCULO
    # (Supondo que load_temas e load_poema estão definidos conforme o ypo_old)
    temas_list = load_temas("todos os temas")
    maxy_mini = len(temas_list)

    # 5.2 CONTROLES [4, 1, 1, 1, 4]
    f1, col_more, col_rand, col_auto, f2 = st.columns([4, 1, 1, 1, 4])
    
    if col_rand.button("✻"):
        st.session_state.mini = random.randrange(0, maxy_mini)
        st.rerun()

    # O check do AUTO altera o estado e dá rerun para evitar travar o loop
    auto_check = col_auto.checkbox("auto", value=st.session_state.auto)
    if auto_check != st.session_state.auto:
        st.session_state.auto = auto_check
        st.rerun()

    # 5.3 EXIBIÇÃO DO SOPRO
    st.session_state.tema = temas_list[st.session_state.mini]
    
    placeholder = st.empty()

    if not st.session_state.auto:
        # MODO MANUAL (Sorteia uma vez e para)
        texto = load_poema(st.session_state.tema, "")
        placeholder.markdown(f'<div class="mini-card">{texto}</div>', unsafe_allow_html=True)
    else:
        # MODO AUTO (Usa rerun para não travar o sidebar nem o palco)
        texto = load_poema(st.session_state.tema, "")
        placeholder.markdown(f'<div class="mini-card">{texto}</div>', unsafe_allow_html=True)
        
        # Em vez de um 'while True' que mata o app, esperamos e reiniciamos
        time.sleep(10) # ou wait_time se definido
        st.session_state.mini = random.randrange(0, maxy_mini)
        st.rerun()
