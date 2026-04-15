import streamlit as st
import os
import random
from deep_translator import GoogleTranslator

# MOTOR REAL: Conexão direta com lay_2_ypo
try: 
    from lay_2_ypo import gera_poema
except ImportError: 
    def gera_poema(t, p=""): return ["Erro: motor lay_2_ypo não encontrado."]

# --- 1. BOOT & ESTADO (ID_CLIC ÚNICO) ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

# Inicialização limpa de estados essenciais
for key, val in {
    'page': 'demo', 
    'show_help': False, 
    'ID_CLIC': 'demo', 
    'idx_tema': 0, 
    'temas_atuais': []
}.items():
    if key not in st.session_state: st.session_state[key] = val

def nav_to(p):
    st.session_state.page = p
    st.session_state.show_help = False
    st.session_state.ID_CLIC = p

# Callbacks de Navegação (Sem lógica duplicada)
def prox_tema():
    if st.session_state.temas_atuais:
        st.session_state.idx_tema = (st.session_state.idx_tema + 1) % len(st.session_state.temas_atuais)

def ante_tema():
    if st.session_state.temas_atuais:
        st.session_state.idx_tema = (st.session_state.idx_tema - 1) % len(st.session_state.temas_atuais)

def sorteio_tema():
    if st.session_state.temas_atuais:
        st.session_state.idx_tema = random.randint(0, len(st.session_state.temas_atuais) - 1)

# --- 2. CSS: ARQUITETURA DE PALCO FIXO E SCROLL INTERNO ---
st.markdown("""
<style>
    /* Limpeza de elementos padrão do Streamlit */
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    html, body, [data-testid="stAppViewContainer"] { overflow: hidden !important; }
    .block-container {padding: 1rem !important;}
    
    /* Painel Lateral Fixo (Esquerda) */
    [data-testid="column"]:nth-child(1) { 
        position: fixed !important; top: 1rem; left: 1.5rem; width: 220px !important; z-index: 1000; 
    }
    
    /* Palco de Conteúdo com Scroll Independente (Direita) */
    [data-testid="column"]:nth-child(3) { 
        margin-left: 260px !important; 
        height: 95vh !important;
        overflow-y: auto !important;
        padding-right: 20px;
    }

    /* Star Mestra: Alinhamento Centralizado e Estética Limpa */
    .star-mestra-container {
        display: flex; justify-content: center; align-items: center; height: 100%;
    }
    .star-mestra-container button {
        background: transparent !important; border: none !important;
        color: #f1c40f !important; font-size: 1.4rem !important;
        margin-top: 5px !important;
    }

    /* Régua de Navegação [ + < * > ] */
    .nav-rim-box button { 
        background: transparent !important; border: none !important; 
        font-size: 1.4rem !important; color: #777 !important; 
    }
    .nav-rim-box button:hover { color: #000 !important; }
    
    /* LYPO & TYPO: A alma do Poema */
    .lypo-container { margin-top: 10px; padding-bottom: 60px; }
    .typo-verse { 
        font-family: 'Georgia', serif; font-size: 1.65rem; 
        line-height: 1.7; color: #1a1a1a; min-height: 1.5rem; 
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS ---
@st.cache_data
def get_acervo():
    path = "base"
    if not os.path.exists(path): return {}
    files = sorted([f for f in os.listdir(path) if f.startswith("rol_")])
    return {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}

ACERVO = get_acervo()

# --- 4. INTERFACE: ESTRUTURA DE COLUNAS ---
c1, _, c2 = st.columns([2, 0.1, 7.9])

with c1:
    st.write("### controles")
    ic = st.columns(3)
    ic[0].button("🔈"); ic[1].button("🎨"); ic[2].button("🎬")
    st.divider()
    
    livro_sel = st.selectbox("livros", list(ACERVO.keys()) if ACERVO else ["-"], key="sl")
    if ACERVO:
        with open(os.path.join("base", ACERVO[livro_sel]), "r", encoding="utf-8") as f:
            temas_disco = [l.strip() for l in f if l.strip()]
            if temas_disco != st.session_state.temas_atuais:
                st.session_state.temas_atuais = temas_disco
                st.session_state.idx_tema = 0
    
    st.selectbox("temas", st.session_state.temas_atuais, 
                 index=min(st.session_state.idx_tema, len(st.session_state.temas_atuais)-1),
                 key="st_combo", on_change=lambda: st.session_state.update({"idx_tema": st.session_state.temas_atuais.index(st.session_state.st_combo)}))
    
    st.selectbox("idioma", ["Português", "English", "Español", "Deutsch", "Français"], key="si")

with c2:
    # Topo: 6 Páginas e a Star Mestra (Eixo Central)
    cols = st.columns([1, 1, 1, 0.4, 1, 1, 1])
    pgs = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    
    cols[0].button(pgs[0], on_click=nav_to, args=(pgs[0],))
    cols[1].button(pgs[1], on_click=nav_to, args=(pgs[1],))
    cols[2].button(pgs[2], on_click=nav_to, args=(pgs[2],))
    
    with cols[3]: # A STAR MESTRA ÚNICA
        st.markdown('<div class="star-mestra-container">', unsafe_allow_html=True)
        if st.button("★", key="master_star"):
            st.session_state.show_help = not st.session_state.show_help
        st.markdown('</div>', unsafe_allow_html=True)
        
    cols[4].button(pgs[3], on_click=nav_to, args=(pgs[3],))
    cols[5].button(pgs[4], on_click=nav_to, args=(pgs[4],))
    cols[6].button(pgs[5], on_click=nav_to, args=(pgs[5],))

    # Régua Centralizada de Navegação
    st.markdown('<div class="nav-rim-box">', unsafe_allow_html=True)
    _, col_cent, _ = st.columns([3, 4, 3])
    with col_cent:
        bn = st.columns(4)
        bn[0].button("+")
        bn[1].button("<", on_click=ante_tema)
        bn[2].button("*", on_click=sorteio_tema)
        bn[3].button(">", on_click=prox_tema)
    st.markdown('</div>', unsafe_allow_html=True)
    st.divider()

    # --- 5. RENDERIZAÇÃO: PALCO CONTEXTUAL ---
    if st.session_state.show_help:
        ctx = st.session_state.ID_CLIC
        st.markdown(f"### Ajuda: {ctx.upper()}")
        st.info(f"O sensor de contexto ID_CLIC está focado em: {ctx}.")
    else:
        p = st.session_state.page
        st.session_state.ID_CLIC = p # Declaração de Identidade Automática
        
        if p == "demo":
            if st.session_state.temas_atuais:
                try:
                    tema_alvo = st.session_state.temas_atuais[st.session_state.idx_tema]
                    poema = gera_poema(tema_alvo, "")
                    st.markdown('<div class="lypo-container">', unsafe_allow_html=True)
                    for v in poema:
                        if v == '\n': st.write("")
                        else: st.markdown(f'<div class="typo-verse">{v}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Erro na geração: {e}")
        else:
            st.write(f"### {p.lower()}")
            st.write(f"Ambiente ativo. O ID_CLIC '{st.session_state.ID_CLIC}' está pronto para o Help.")
