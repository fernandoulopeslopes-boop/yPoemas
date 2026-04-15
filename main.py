import streamlit as st
import os
import random
from deep_translator import GoogleTranslator

# MOTOR REAL
try: from lay_2_ypo import gera_poema
except: def gera_poema(t, p=""): return ["Erro: motor não encontrado."]

# --- 1. BOOT & ESTADO (LIMPEZA TOTAL) ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

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

# Navegação de Temas
def prox_tema():
    if st.session_state.temas_atuais:
        st.session_state.idx_tema = (st.session_state.idx_tema + 1) % len(st.session_state.temas_atuais)
def ante_tema():
    if st.session_state.temas_atuais:
        st.session_state.idx_tema = (st.session_state.idx_tema - 1) % len(st.session_state.temas_atuais)
def sorteio_tema():
    if st.session_state.temas_atuais:
        st.session_state.idx_tema = random.randint(0, len(st.session_state.temas_atuais) - 1)

# --- 2. CSS: ARQUITETURA E SCROLL INTERNO ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    html, body, [data-testid="stAppViewContainer"] { overflow: hidden !important; }
    .block-container {padding: 1rem !important;}
    
    [data-testid="column"]:nth-child(1) { position: fixed !important; top: 1rem; left: 1.5rem; width: 220px !important; z-index: 1000; }
    [data-testid="column"]:nth-child(3) { 
        margin-left: 260px !important; height: 95vh !important; overflow-y: auto !important; padding-right: 20px;
    }

    .star-mestra-wrapper { display: flex; justify-content: center; align-items: center; height: 100%; }
    .star-mestra-wrapper button {
        background: transparent !important; border: none !important;
        color: #f1c40f !important; font-size: 1.4rem !important; margin-top: 4px !important;
    }

    .nav-rim-box button { background: transparent !important; border: none !important; font-size: 1.4rem !important; color: #777 !important; }
    .lypo-container { margin-top: 10px; padding-bottom: 50px; }
    .typo-verse { font-family: 'Georgia', serif; font-size: 1.65rem; line-height: 1.7; color: #1a1a1a; min-height: 1.5rem; }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS & HELP (A CORREÇÃO) ---
@st.cache_data
def get_help_text(id_clic):
    # Procura o arquivo .txt ou .md correspondente ao ID_CLIC na pasta 'docs'
    path = f"docs/help_{id_clic}.txt"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "Texto de ajuda ainda não redigido para este ambiente."

@st.cache_data
def get_acervo():
    if not os.path.exists("base"): return {}
    files = sorted([f for f in os.listdir("base") if f.startswith("rol_")])
    return {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}

ACERVO = get_acervo()

# --- 4. INTERFACE ---
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
    # Navegação com Star Mestra Centralizada
    cols = st.columns([1, 1, 1, 0.4, 1, 1, 1])
    pgs = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    
    for i, p in enumerate(pgs[:3]): cols[i].button(p, on_click=nav_to, args=(p,))
    with cols[3]:
        st.markdown('<div class="star-mestra-wrapper">', unsafe_allow_html=True)
        if st.button("★", key="master_star"): st.session_state.show_help = not st.session_state.show_help
        st.markdown('</div>', unsafe_allow_html=True)
    for i, p in enumerate(pgs[3:]): cols[i+4].button(p, on_click=nav_to, args=(p,))

    # Régua [ + < * > ]
    st.markdown('<div class="nav-rim-box">', unsafe_allow_html=True)
    _, col_cent, _ = st.columns([3, 4, 3])
    with col_cent:
        bn = st.columns(4); bn[0].button("+"); bn[1].button("<", on_click=ante_tema); bn[2].button("*", on_click=sorteio_tema); bn[3].button(">", on_click=prox_tema)
    st.markdown('</div>', unsafe_allow_html=True)
    st.divider()

    # --- 5. RENDERIZAÇÃO (MAPEAMENTO ID_CLIC) ---
    if st.session_state.show_help:
        ctx = st.session_state.ID_CLIC
        st.markdown(f"### Ajuda: {ctx.upper()}")
        # CORREÇÃO: Busca o texto real do arquivo
        texto_help = get_help_text(ctx)
        st.markdown(texto_help) 
        if st.button("Fechar Ajuda"): 
            st.session_state.show_help = False
            st.rerun()
    else:
        p = st.session_state.page
        st.session_state.ID_CLIC = p # Garante o contexto atualizado
        
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
                except Exception as e: st.error(f"Erro: {e}")
        else:
            st.write(f"### {p.lower()}")
            st.info(f"O ambiente '{p}' está ativo. Clique na estrela acima para ver as instruções deste contexto.")
