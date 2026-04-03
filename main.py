import os
import streamlit as st
import random
import time

# --- 1. A PONTE COM O ORÁCULO (O FIM DO NAMEERROR) ---
# Importamos as funções exatamente como estão no seu ypo_old.py
try:
    from ypo_old import load_temas, load_poema, load_help, say_number, load_arts, write_ypoema
except ImportError:
    st.error("Erro: ypo_old.py não encontrado no diretório. A Máquina precisa do Oráculo.")
    st.stop()

# --- 2. GÊNESE (ESTADOS) ---
if 'page' not in st.session_state: st.session_state.page = "mini"
if 'mini' not in st.session_state: st.session_state.mini = 0
if 'auto' not in st.session_state: st.session_state.auto = False
if 'lang' not in st.session_state: st.session_state.lang = "pt"

# --- 3. CONFIGURAÇÃO (O PALCO ELÁSTICO) ---
st.set_page_config(page_title="yPoemas - 1983", layout="wide")

st.markdown("""
    <style>
    footer {visibility: hidden;}
    .main .block-container { max-width: 98% !important; padding: 1.5rem 2rem !important; margin: 0 auto; }
    [data-testid="stSidebar"] { width: 240px !important; min-width: 240px !important; visibility: visible !important; }
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR (RENDERIZAÇÃO GARANTIDA) ---
with st.sidebar:
    # Arte e Idioma
    st.image("img_mini.jpg", use_container_width=True)
    st.selectbox("lang", ["pt", "en", "es"], key="sb_lang", label_visibility="collapsed")
    
    # Cookies (v, a, vi)
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    st.session_state.v = c1.checkbox("v", value=True)
    st.session_state.a = c2.checkbox("a", value=True)
    st.session_state.vi = c3.checkbox("vi", value=False)

# --- 5. NAVEGAÇÃO ---
nav_cols = st.columns(6)
paginas = ["mini", "ypoemas", "eureka", "off-machina", "comments", "sobre"]
for i, pag in enumerate(paginas):
    if nav_cols[i].button(pag, key=f"btn_{pag}"):
        st.session_state.page = pag
        st.rerun()

st.markdown("---")

# --- 6. O PALCO: PÁGINA MINI (LINHA 65 PROTEGIDA) ---
if st.session_state.page == "mini":
    # Agora o Python sabe o que é load_temas porque importamos da ypo_old
    temas_list = load_temas("todos os temas")
    maxy_mini = len(temas_list)
    
    # Controles [4, 1, 1, 1, 4]
    _, col_more, col_rand, col_auto, _ = st.columns([4, 1, 1, 1, 4])
    
    if col_rand.button("✻"):
        st.session_state.mini = random.randrange(0, maxy_mini)
        st.rerun()
        
    st.session_state.auto = col_auto.checkbox("auto", value=st.session_state.auto)
    st.session_state.tema = temas_list[st.session_state.mini]
    
    placeholder = st.empty()
    
    if not st.session_state.auto:
        # Modo Manual usando o sopro real do Oráculo
        curr_ypoema = load_poema(st.session_state.tema, "")
        with placeholder.container():
            write_ypoema(curr_ypoema, load_arts(st.session_state.tema) if st.session_state.a else None)
    else:
        # Modo Auto (Rerun para manter o app vivo)
        st.session_state.mini = random.randrange(0, maxy_mini)
        st.session_state.tema = temas_list[st.session_state.mini]
        curr_ypoema = load_poema(st.session_state.tema, "")
        with placeholder.container():
            write_ypoema(curr_ypoema, load_arts(st.session_state.tema) if st.session_state.a else None)
        
        time.sleep(10)
        st.rerun()
