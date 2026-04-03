import os
import streamlit as st
import random
import time

### bof: settings

st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="auto")

# Inicialização de Estados (Baseado no seu fonte)
if "page" not in st.session_state: st.session_state.page = "mini"
if "mini" not in st.session_state: st.session_state.mini = 0
if "auto" not in st.session_state: st.session_state.auto = False
if "rand" not in st.session_state: st.session_state.rand = True

# Regra 0: Look & Feel (Palco Elástico e Blindado)
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    .main .block-container { max-width: 98% !important; padding: 1.5rem 2rem !important; margin: 0 auto !important; }
    [data-testid="stMainViewContainer"] { width: 100% !important; }
    [data-testid="stSidebar"] { width: 240px !important; min-width: 240px !important; }
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"], [data-testid="stSidebar"] button[title="View help"] { display: none !important; }
    [data-testid="stSidebarContent"] [data-testid="stHorizontalBlock"] { justify-content: center !important; gap: 15px !important; }
    
    /* Estilo do Poema (Mini) */
    .poema-display {
        font-family: 'IBM Plex Serif', serif;
        font-size: 1.8rem;
        text-align: center;
        padding: 50px;
        min-height: 300px;
        display: flex; align-items: center; justify-content: center;
    }
    </style> """,
    unsafe_allow_html=True,
)

### bof: logic (Motores do ypo_old)

def load_temas(categoria):
    # Simulação: Aqui você carregaria sua lista de temas real
    return ["caos", "eros", "cosmos", "silêncio", "máquina", "abismo"]

def load_poema(tema, sub):
    # Simulação da sua função load_poema do ypo_old
    poemas = {
        "caos": "o sistema desaba\nem bits de fúria\nrecomeço.",
        "eros": "pele de código\no toque que não\nprocessa.",
        "cosmos": "estrelas binárias\nno vácuo da\nmemória."
    }
    return poemas.get(tema, "verso de teste\nlinha dois\nfim de transmissão.")

def write_ypoema(texto, imagem=None):
    """A função de exibição que você definiu no old"""
    st.markdown(f'<div class="poema-display">{texto.replace("\n", "<br>")}</div>', unsafe_allow_html=True)
    if imagem: st.image(imagem)

### bof: navigation

nav_cols = st.columns(6)
paginas = ["mini", "ypoemas", "eureka", "off-machina", "comments", "sobre"]
for i, pag in enumerate(paginas):
    with nav_cols[i]:
        if st.button(f"ツ {pag}" if pag=="mini" else pag, key=f"n_{pag}"):
            st.session_state.page = pag
            st.rerun()

st.markdown("---")

### bof: sidebar

with st.sidebar:
    # Arte e Idioma
    st.image("img_mini.jpg", use_container_width=True) #Placeholder
    st.selectbox("lang", ["pt", "en", "es"], key="lang", label_visibility="collapsed")
    
    # Os Cookies (v, a, vi)
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1,1])
    with c1: st.session_state.talk = st.checkbox("v", value=True, key="chk_v")
    with c2: st.session_state.draw = st.checkbox("a", value=True, key="chk_a")
    with c3: st.session_state.vydo = st.checkbox("vi", value=False, key="chk_vi")

### bof: page_mini (O SEU CÓDIGO FONTE)

if st.session_state.page == "mini":
    temas_list = load_temas("todos os temas")
    maxy_mini = len(temas_list)

    if st.session_state.mini >= maxy_mini: st.session_state.mini = 0

    # Layout de Controles Superior
    foo1, col_more, col_rand, col_auto, foo2 = st.columns([4, 1, 1, 1, 4])
    
    btn_rand = col_rand.button("✻") # Rand do ypo_old
    st.session_state.auto = col_auto.checkbox("auto", value=st.session_state.auto)

    if st.session_state.auto:
        st.session_state.talk = False
        st.session_state.vydo = False
        with st.sidebar:
            wait_time = st.slider("tempo (s):", 5, 60, 10)

    if btn_rand:
        st.session_state.rand = True
        st.session_state.mini = random.randrange(0, maxy_mini)
    else:
        st.session_state.rand = False

    st.session_state.tema = temas_list[st.session_state.mini]
    btn_more = col_more.button("✚") # More do ypo_old

    if btn_more:
        st.session_state.rand = False
        # No seu original aqui ele incrementava ou mudava o estado

    # --- O Loop de Exibição ---
    mini_place_holder = st.empty()

    if not st.session_state.auto:
        # Modo Manual
        texto = load_poema(st.session_state.tema, "")
        with mini_place_holder.container():
            write_ypoema(texto)
    else:
        # Modo Automático (A Máquina Viva)
        while st.session_state.auto:
            if st.session_state.rand:
                st.session_state.mini = random.randrange(0, maxy_mini)
                st.session_state.tema = temas_list[st.session_state.mini]
            
            texto = load_poema(st.session_state.tema, "")
            with mini_place_holder.container():
                write_ypoema(texto)
            
            # Contador de espera
            time.sleep(wait_time)
            st.rerun() # Reinicia para o próximo ciclo do loop
