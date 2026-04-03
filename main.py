import os
import streamlit as st
import random
import time

# --- 1. GÊNESE: BLOCO DE EXISTÊNCIA (O MURO DE ARRIMO) ---
if 'page' not in st.session_state: st.session_state.page = "mini"
if 'mini' not in st.session_state: st.session_state.mini = 0
if 'auto' not in st.session_state: st.session_state.auto = False
if 'rand' not in st.session_state: st.session_state.rand = True
if 'lang' not in st.session_state: st.session_state.lang = "pt"
if 'tema' not in st.session_state: st.session_state.tema = ""
if 'talk' not in st.session_state: st.session_state.talk = True
if 'draw' not in st.session_state: st.session_state.draw = True
if 'vydo' not in st.session_state: st.session_state.vydo = False

# --- 2. AS FUNÇÕES DO ORÁCULO (Resgatadas do ypo_old.py) ---

def load_temas(book):
    """Lê a lista de temas de ./base/rol_[book].txt"""
    path = f"./base/rol_{book}.txt"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return [linha.strip() for linha in f.readlines() if linha.strip()]
    return ["silêncio", "caos", "máquina"] # fallback

def load_poema(nome_tema, seed_eureka):
    """Gera o poema, salva no temporário e retorna a string com <br>"""
    # Aqui a Māchina chama o gera_poema() interno que você tem
    # Por enquanto, simulamos o retorno que o ypo_old espera:
    return "o verso que a máquina sopra<br>no meio do vazio digital<br>agora."

def write_ypoema(LOGO_TEXTO, LOGO_IMAGE=None):
    """A estética visual da Māchina"""
    st.markdown(f"""
        <div class="mini-card">
            {LOGO_TEXTO}
        </div>
    """, unsafe_allow_html=True)
    if LOGO_IMAGE:
        st.image(LOGO_IMAGE)

def load_help(lang):
    # Dicionário de dicas conforme o idioma do st.session_state.lang
    return {1: "sortear novo", 4: "mais deste tema"}

def say_number(tema):
    return "análise: 1.0"

def load_arts(tema):
    return None # Busca em ./arts/ conforme o tema

# --- 3. CONFIGURAÇÃO & LOOK & FEEL (Regra 0) ---
st.set_page_config(page_title="yPoemas - A Máquina", layout="wide")

st.markdown("""
    <style>
    footer {visibility: hidden;}
    .main .block-container { max-width: 98% !important; padding: 1.5rem 2rem !important; }
    .mini-card {
        font-family: 'IBM Plex Serif', serif;
        font-size: 1.8rem; line-height: 2; color: #1a1a1a;
        text-align: center; padding: 60px; background: #fff;
        border-radius: 25px; border: 1px solid #f0f0f0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.02);
        max-width: 750px; margin: 30px auto;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. NAVEGAÇÃO ---
nav_cols = st.columns(6)
paginas = ["mini", "ypoemas", "eureka", "off-machina", "comments", "sobre"]
for i, pag in enumerate(paginas):
    if nav_cols[i].button(pag, key=f"nav_{pag}"):
        st.session_state.page = pag
        st.rerun()

st.markdown("---")

# --- 5. O PALCO (PÁGINA MINI) ---
if st.session_state.page == "mini":
    # Agora sim, load_temas existe!
    temas_list = load_temas("todos os temas")
    maxy_mini = len(temas_list)
    
    foo1, col_more, col_rand, col_auto, foo2 = st.columns([4, 1, 1, 1, 4])
    help_tips = load_help(st.session_state.lang)
    
    if col_rand.button("✻", help=help_tips[1]):
        st.session_state.rand = True
        st.session_state.mini = random.randrange(0, maxy_mini)
        st.rerun()

    st.session_state.auto = col_auto.checkbox("auto", value=st.session_state.auto)
    st.session_state.tema = temas_list[st.session_state.mini]
    
    if col_more.button("✚", help=help_tips[4]):
        st.session_state.rand = False

    mini_placeholder = st.empty()

    if not st.session_state.auto:
        # Modo Manual
        curr_ypoema = load_poema(st.session_state.tema, "")
        with mini_placeholder.container():
            write_ypoema(curr_ypoema, load_arts(st.session_state.tema) if st.session_state.draw else None)
    else:
        # Modo Automático
        while st.session_state.auto:
            st.session_state.mini = random.randrange(0, maxy_mini)
            st.session_state.tema = temas_list[st.session_state.mini]
            curr_ypoema = load_poema(st.session_state.tema, "")
            with mini_placeholder.container():
                write_ypoema(curr_ypoema, load_arts(st.session_state.tema) if st.session_state.draw else None)
            time.sleep(10) # Tempo de exibição
            st.rerun()
