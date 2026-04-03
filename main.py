import os
import streamlit as st
import random
import time

# --- 1. GÊNESE: BLOCO DE EXISTÊNCIA (OBRIGATÓRIO NO TOPO) ---
# Impede o AttributeError na linha 44 e em qualquer interação subsequente.
if 'page' not in st.session_state: st.session_state.page = "mini"
if 'mini' not in st.session_state: st.session_state.mini = 0
if 'auto' not in st.session_state: st.session_state.auto = False
if 'rand' not in st.session_state: st.session_state.rand = True
if 'lang' not in st.session_state: st.session_state.lang = "pt"
if 'tema' not in st.session_state: st.session_state.tema = ""
if 'talk' not in st.session_state: st.session_state.talk = True
if 'draw' not in st.session_state: st.session_state.draw = True
if 'vydo' not in st.session_state: st.session_state.vydo = False
if 'last_lang' not in st.session_state: st.session_state.last_lang = "pt"

# --- 2. CONFIGURAÇÃO & LOOK & FEEL (REGRA 0) ---
st.set_page_config(page_title="a máquina de fazer Poesia", layout="wide")

st.markdown("""
    <style>
    footer {visibility: hidden;}
    .main .block-container { max-width: 98% !important; padding: 1.5rem 2rem !important; margin: 0 auto; }
    [data-testid="stMainViewContainer"] { width: 100% !important; }
    [data-testid="stSidebar"] { width: 240px !important; min-width: 240px !important; }
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"], 
    [data-testid="stSidebar"] button[title="View help"] { display: none !important; }
    [data-testid="stSidebarContent"] [data-testid="stHorizontalBlock"] { justify-content: center !important; gap: 15px !important; }
    
    /* Estilo do Card de Poesia */
    .mini-card {
        font-family: 'IBM Plex Serif', serif;
        font-size: 1.8rem;
        line-height: 2;
        color: #1a1a1a;
        text-align: center;
        padding: 60px;
        background: #fff;
        border-radius: 25px;
        border: 1px solid #f0f0f0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.02);
        max-width: 750px;
        margin: 30px auto;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. NAVEGAÇÃO ---
nav_cols = st.columns(6)
paginas = ["mini", "ypoemas", "eureka", "off-machina", "comments", "sobre"]
labels = ["ツ mini", "ypoemas", "eureka", "off-machina", "comments", "sobre"]

for i, pag in enumerate(paginas):
    if nav_cols[i].button(labels[i], key=f"nav_{pag}"):
        st.session_state.page = pag
        st.rerun()

st.markdown("---")

# --- 4. SIDEBAR (COOKIES) ---
with st.sidebar:
    # Arte e Idioma
    st.image("img_mini.jpg", use_container_width=True)
    st.selectbox("lang", ["pt", "en", "es", "fr", "it"], key="lang_selector", label_visibility="collapsed")
    
    # Cookies soltos e centralizados
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1,1])
    st.session_state.talk = c1.checkbox("v", value=st.session_state.talk, key="chk_v")
    st.session_state.draw = c2.checkbox("a", value=st.session_state.draw, key="chk_a")
    st.session_state.vydo = c3.checkbox("vi", value=st.session_state.vydo, key="chk_vi")

# --- 5. PÁGINA MINI (LINHA 44 PROTEGIDA) ---
if st.session_state.page == "mini":
    # 5.1 Lógica do ypo_old resgatada
    temas_list = load_temas("todos os temas")
    maxy_mini = len(temas_list)
    
    # Interface de comandos [4, 1, 1, 1, 4]
    foo1, col_more, col_rand, col_auto, foo2 = st.columns([4, 1, 1, 1, 4])
    
    help_tips = load_help(st.session_state.lang)
    
    # Botão Sorteio (✻)
    if col_rand.button("✻", help=help_tips[1]):
        st.session_state.rand = True
        st.session_state.mini = random.randrange(0, maxy_mini)
        st.rerun()

    # Checkbox Auto
    st.session_state.auto = col_auto.checkbox("auto", value=st.session_state.auto)

    if st.session_state.auto:
        st.session_state.talk = False
        st.session_state.vydo = False
        with st.sidebar:
            wait_time = st.slider("tempo:", 5, 60, 10)

    # Definição do Tema
    st.session_state.tema = temas_list[st.session_state.mini]
    analise = say_number(st.session_state.tema)
    
    # Botão Mais (✚)
    if col_more.button("✚", help=help_tips[4] + " • " + analise):
        st.session_state.rand = False

    # 5.2 Exibição (O Coração da Māchina)
    mini_placeholder = st.empty()

    if not st.session_state.auto:
        # Modo Manual: Carrega o poema e exibe uma vez
        curr_ypoema = load_poema(st.session_state.tema, "")
        with mini_placeholder.container():
            # Função write_ypoema deve estar definida no seu escopo global
            write_ypoema(curr_ypoema, load_arts(st.session_state.tema) if st.session_state.draw else None)
    else:
        # Modo Automático: Loop infinito enquanto 'auto' for True
        while st.session_state.auto:
            st.session_state.mini = random.randrange(0, maxy_mini)
            st.session_state.tema = temas_list[st.session_state.mini]
            curr_ypoema = load_poema(st.session_state.tema, "")
            
            with mini_placeholder.container():
                write_ypoema(curr_ypoema, load_arts(st.session_state.tema) if st.session_state.draw else None)
            
            time.sleep(wait_time)
            st.rerun()

elif st.session_state.page == "ypoemas":
    st.write("Em construção...")
