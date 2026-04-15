import streamlit as st
import os
import random

# --- 1. BOOT & ESTADOS ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

try: 
    from lay_2_ypo import gera_poema
except Exception as e: 
    def gera_poema(t, p=""): return [f"Erro no motor: {e}"]

if 'page' not in st.session_state: st.session_state.page = 'demo'
if 'idx_tema' not in st.session_state: st.session_state.idx_tema = 0
if 'temas_atuais' not in st.session_state: st.session_state.temas_atuais = []

# --- 2. CSS: ARQUITETURA VISUAL ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .main .block-container { max-width: 95%; padding-top: 1rem !important; }
    
    .md-humanista { font-family: 'Georgia', serif; line-height: 1.65; color: #222; font-size: 1.15rem; }
    
    .md-tecnico { 
        font-family: 'Courier New', monospace; 
        background-color: #f4f4f4; 
        padding: 25px; 
        border-left: 6px solid #111;
        font-size: 0.95rem;
        color: #111;
        line-height: 1.4;
    }
    
    .typo-title { font-family: 'Georgia', serif; font-size: 1.3rem; font-weight: bold; text-decoration: underline; margin-bottom: 20px; }
    .typo-verse { font-family: 'Georgia', serif; font-size: 1.32rem; line-height: 1.35; margin-bottom: 8px; }
    
    .stButton button { border-radius: 50% !important; width: 48px !important; height: 48px !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. MOTOR DE BUSCA DE DOCUMENTOS ---
def buscar_doc(nome_pagina):
    pasta = "md_files"
    if not os.path.exists(pasta): return None
    
    mapa = {
        "ypoemas": ["YPOEMAS", "YPOEMA"],
        "about": ["ABOUT", "INFO_SOBRE"],
        "eureka": ["EUREKA"],
        "off-mach": ["OFF-MACH"],
        "opinião": ["OPINIAO"]
    }
    
    alvos = mapa.get(nome_pagina.lower(), [nome_pagina.upper()])
    if not os.path.exists(pasta): return None
    
    for f in os.listdir(pasta):
        nome_puro = os.path.splitext(f)[0].upper()
        if nome_puro in alvos:
            try:
                with open(os.path.join(pasta, f), "r", encoding="utf-8") as file:
                    return file.read()
            except: continue
    return None

# --- 4. INTERFACE ---
c1, _, c2 = st.columns([2.5, 0.4, 7.1])

with c1:
    m_cols = st.columns(3)
    if m_cols[0].button("🔊", key="vol"): st.toast("🔊 Som Ativo")
    if m_cols[1].button("🎨", key="art"): st.toast("🎨 Galeria")
    if m_cols[2].button("🎬", key="vid"): st.toast("🎬 Projeção")
    st.divider()
    
    if os.path.exists("base"):
        files = sorted([f for f in os.listdir("base") if f.startswith("rol_")])
        acervo = {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}
        lista_livros = list(acervo.keys())
        if lista_livros:
            sel_l = st.selectbox("Livros", lista_livros)
            with open(os.path.join("base", acervo[sel_l]), "r", encoding="utf-8") as f:
                st.session_state.temas_atuais = [line.strip() for line in f if line.strip()]
            
            idx_s = st.session_state.idx_tema % len(st.session_state.temas_atuais) if st.session_state.temas_atuais else 0
            st.selectbox("Temas", st.session_state.temas_atuais, index=idx_s)
    
    st.selectbox("Idioma", ["Português", "English", "Español", "Latin"], key="lang_sel")

with c2:
    pgs = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "about"]
    t_cols = st.columns([1, 1, 1, 0.5, 1, 1, 1])
    
    for i, p in enumerate(pgs[:3]):
        if t_cols[i].button(p, key=f"btn_{p}"): st.session_state.page = p
    
    if t_cols[3].button("?", key="h_btn"): 
        st.toast("A precisão agora dança conforme o instinto.")
    
    for i, p in enumerate(pgs[3:]):
        if t_cols[i+4].button(p, key=f"btn_{p}"): st.session_state.page = p

    st.write("") 
    n_cols = st.columns([2.5, 0.7, 0.7, 0.7, 0.7, 2.5])
    if n_cols[1].button("❮", key="p_v"): st.session_state.idx_tema -= 1
    if n_cols[2].button("✚", key="a_d"): st.toast("Semente Salva")
    if n_cols[3].button("✱", key="r_n"): st.session_state.idx_tema = random.randint(0, 999)
    if n_cols[4].button("❯", key="n_x"): st.session_state.idx_tema += 1
    st.divider()

    if st.session_state.page == "demo":
        if st.session_state.temas_atuais:
            t_nome = st.session_state.temas_atuais[st.session_state.idx_tema % len(st.session_state.temas_atuais)]
            st.markdown(f'<div class="typo-title">{t_nome.upper()}</div>', unsafe_allow_html=True)
            for v in gera_poema(t_nome, ""):
                st.markdown(f'<div class="typo-verse">{v}</div>', unsafe_allow_html=True)
    else:
        conteudo = buscar_doc(st.session_state.page)
        if conteudo:
            estilo = "md-tecnico" if st.session_state.page.lower() == "ypoemas" else "md-humanista"
            st.markdown(f'<div class="{estilo}">', unsafe_allow_html=True)
            st.markdown(conteudo)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning(f"O documento '{st.session_state.page}' não foi localizado.")
