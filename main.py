import streamlit as st
import os
import random

# --- 1. BOOT & ESTADO (ESTRUTURA DE RESGATE) ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

try: 
    from lay_2_ypo import gera_poema
except Exception as e: 
    def gera_poema(t, p=""): return [f"Erro no motor: {e}"]

# Estados essenciais
if 'page' not in st.session_state: st.session_state.page = 'demo'
if 'idx_tema' not in st.session_state: st.session_state.idx_tema = 0
if 'temas_atuais' not in st.session_state: st.session_state.temas_atuais = []

# --- 2. CSS DE ESTRUTURA (LIMPO) ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .main .block-container { max-width: 95%; padding-top: 1rem !important; }
    .md-humanista { font-family: 'Georgia', serif; line-height: 1.6; color: #222; font-size: 1.15rem; }
    .typo-title { font-family: 'Georgia', serif; font-size: 1.3rem; font-weight: bold; text-decoration: underline; margin-bottom: 20px; }
    .typo-verse { font-family: 'Georgia', serif; font-size: 1.32rem; line-height: 1.35; margin-bottom: 8px; }
    .stButton button { border-radius: 50% !important; width: 46px !important; height: 46px !important; padding: 0px !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. INTERFACE (COLUNAS RÍGIDAS) ---
c1, _, c2 = st.columns([2.5, 0.4, 7.1])

with c1:
    # Botões de Status
    st.columns(3)[0].button("🔊", key="btn_s")
    st.columns(3)[1].button("🎨", key="btn_a")
    st.columns(3)[2].button("🎬", key="btn_v")
    st.divider()
    
    # Gerenciamento de Livros e Temas
    if os.path.exists("base"):
        files = sorted([f for f in os.listdir("base") if f.startswith("rol_")])
        if files:
            acervo = {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}
            sel_l = st.selectbox("Livros", list(acervo.keys()), key="sel_livro")
            
            with open(os.path.join("base", acervo[sel_l]), "r", encoding="utf-8") as f:
                st.session_state.temas_atuais = [line.strip() for line in f if line.strip()]
            
            idx = st.session_state.idx_tema % len(st.session_state.temas_atuais) if st.session_state.temas_atuais else 0
            st.selectbox("Temas", st.session_state.temas_atuais, index=idx, key="sel_tema")
    
    st.selectbox("Idioma", ["Português", "English", "Español", "Latin"], key="sel_lang")

with c2:
    # Menu Superior
    pgs = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "about"]
    t_cols = st.columns([1, 1, 1, 0.5, 1, 1, 1])
    
    for i, p in enumerate(pgs[:3]):
        if t_cols[i].button(p, key=f"pg_{p}"): st.session_state.page = p
    
    if t_cols[3].button("?", key="btn_h"): st.toast("A precisão agora dança conforme o instinto.")
    
    for i, p in enumerate(pgs[3:]):
        if t_cols[i+4].button(p, key=f"pg_{p}"): st.session_state.page = p

    st.write("") 
    # Navegação Inferior
    n_cols = st.columns([2.5, 0.7, 0.7, 0.7, 0.7, 2.5])
    if n_cols[1].button("❮", key="nav_prev"): st.session_state.idx_tema -= 1
    if n_cols[2].button("✚", key="nav_save"): st.toast("Semente Salva")
    if n_cols[3].button("✱", key="nav_rand"): st.session_state.idx_tema = random.randint(0, 999)
    if n_cols[4].button("❯", key="nav_next"): st.session_state.idx_tema += 1
    st.divider()

    # Renderização
    if st.session_state.page == "demo":
        if st.session_state.temas_atuais:
            tema = st.session_state.temas_atuais[st.session_state.idx_tema % len(st.session_state.temas_atuais)]
            st.markdown(f'<div class="typo-title">{tema.upper()}</div>', unsafe_allow_html=True)
            for v in gera_poema(tema, ""):
                st.markdown(f'<div class="typo-verse">{v}</div>', unsafe_allow_html=True)
    else:
        # Busca direta e simplificada para evitar erros de caminho
        nome_arq = f"{st.session_state.page.upper()}.md"
        caminho = os.path.join("md_files", nome_arq)
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                st.markdown(f'<div class="md-humanista">{f.read()}</div>', unsafe_allow_html=True)
        else:
            st.warning(f"Aguardando conteúdo para: {st.session_state.page}")
