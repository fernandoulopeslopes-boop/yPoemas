import os
import streamlit as st
import random
import time

# --- bof: settings & layout (Regra 0) ---
st.set_page_config(page_title="yPoemas", layout="wide")

st.markdown("""
    <style>
    footer {visibility: hidden;}
    .main .block-container { max-width: 98% !important; padding: 1.5rem 2rem !important; }
    [data-testid="stSidebar"] { width: 240px !important; }
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] { display: none !important; }
    /* Centralização dos Cookies na Sidebar */
    [data-testid="stSidebarContent"] [data-testid="stHorizontalBlock"] { justify-content: center !important; gap: 15px !important; }
    </style>
""", unsafe_allow_html=True)

# --- bof: sidebar (Cookies e Nav) ---
with st.sidebar:
    # Arte e Idioma (Conforme ypo_old)
    st.image("img_mini.jpg", use_container_width=True)
    st.selectbox("lang", ["pt", "en", "es"], key="lang", label_visibility="collapsed")
    
    # Os 3 botões soltos (Cookies)
    c1, c2, c3 = st.columns([1,1,1])
    with c1: st.session_state.talk = st.checkbox("v", value=True, key="v")
    with c2: st.session_state.draw = st.checkbox("a", value=True, key="a")
    with c3: st.session_state.vydo = st.checkbox("vi", value=False, key="vi")

# --- bof: navigation ---
nav_cols = st.columns(6)
paginas = ["mini", "ypoemas", "eureka", "off-machina", "comments", "sobre"]
for i, pag in enumerate(paginas):
    if nav_cols[i].button(pag, key=f"nav_{pag}"):
        st.session_state.page = pag
        st.rerun()

st.markdown("---")

# --- bof: PAGE MINI (O SEU CÓDIGO) ---

if st.session_state.page == "mini":
    # 1. A sua lógica de sorteio
    temas_list = load_temas("todos os temas")
    maxy_mini = len(temas_list)
    
    # Garantia de estado inicial para não quebrar o randrange
    if "mini" not in st.session_state:
        st.session_state.mini = random.randrange(0, maxy_mini)

    # 2. A sua linha de comando [4, 1, 1, 1, 4]
    foo1, more_col, rand_col, auto_col, foo2 = st.columns([4, 1, 1, 1, 4])

    help_tips = load_help(st.session_state.lang)
    help_rand = help_tips[1]
    help_more = help_tips[4]
    
    # Botão Rand (✻)
    rand_click = rand_col.button("✻", help=help_rand)
    st.session_state.auto = auto_col.checkbox("auto", value=st.session_state.auto)

    if st.session_state.auto:
        st.session_state.talk = False
        st.session_state.vydo = False
        with st.sidebar:
            wait_time = st.slider("tempo de exibição (em segundos): ", 5, 60, 10)

    if rand_click:
        st.session_state.rand = True
        st.session_state.mini = random.randrange(0, maxy_mini)
    else:
        st.session_state.rand = False

    st.session_state.tema = temas_list[st.session_state.mini]
    analise = say_number(st.session_state.tema)
    
    # Botão More (✚)
    more_click = more_col.button("✚", help=help_more + " • " + analise)

    if more_click:
        st.session_state.rand = False

    # 3. Lógica de exibição e Auto
    lnew = True
    if st.session_state.vydo:
        lnew = False
        show_video("mini")
        update_readings("video_mini")
        st.session_state.vydo = False

    mini_place_holder = st.empty()

    if lnew or st.session_state.auto:
        # Se não estiver em auto, ele executa uma vez e para.
        # Se estiver em auto, entra no loop.
        
        while True:
            if st.session_state.rand:
                st.session_state.mini = random.randrange(0, maxy_mini)
                st.session_state.tema = temas_list[st.session_state.mini]

            # Carregamento do Poema (Sua lógica pt / translate)
            if st.session_state.lang != st.session_state.get('last_lang', 'pt'):
                curr_ypoema = load_lypo()
            else:
                curr_ypoema = load_poema(st.session_state.tema, "")
                curr_ypoema = load_lypo()

            # (Sua lógica de tradução e gravação em temp omitida aqui para brevidade, mas mantida no seu fonte)
            
            update_readings(st.session_state.tema)
            LOGO_TEXTO = curr_ypoema
            LOGO_IMAGE = None
            if st.session_state.draw:
                LOGO_IMAGE = load_arts(st.session_state.tema)

            with mini_place_holder.container():
                write_ypoema(LOGO_TEXTO, LOGO_IMAGE)

            if st.session_state.talk:
                talk(curr_ypoema)

            # Se AUTO for Falso, sai do loop após a primeira exibição
            if not st.session_state.auto:
                break
            
            # Se AUTO for Verdadeiro, espera e continua
            time.sleep(wait_time)
            st.session_state.rand = True # Força novo sorteio no próximo ciclo do while
