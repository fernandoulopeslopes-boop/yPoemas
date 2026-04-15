import streamlit as st
import os
import random

# --- 1. BOOT & ESTADO (PTC) ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

try: 
    from lay_2_ypo import gera_poema
except Exception: 
    def gera_poema(t, p=""): return ["A precisão dança conforme o instinto.", "O labirinto aguarda."]

# Inicialização de estados
for key, val in {
    'page': 'demo', 'show_help': False, 'idx_tema': 0, 
    'temas_atuais': [], 'som': False, 'arte': False, 'video': False
}.items():
    if key not in st.session_state: st.session_state[key] = val

# --- 2. CSS: DUALIDADE ESTÉTICA (POESIA vs. ENGENHARIA) ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .main .block-container { max-width: 95%; padding-top: 1rem !important; }
    
    .md-humanista { 
        font-family: 'Georgia', serif; line-height: 1.65; color: #222; 
        font-size: 1.15rem; padding-bottom: 50px; 
    }
    
    .md-tecnico { 
        font-family: 'Courier New', monospace; background-color: #f9f9f9; 
        padding: 25px; border-left: 5px solid #444; font-size: 1rem;
        line-height: 1.4; color: #111;
    }

    .typo-title { font-family: 'Georgia', serif; font-size: 1.3rem; font-weight: bold; text-decoration: underline; margin-bottom: 20px; }
    .typo-verse { font-family: 'Georgia', serif; font-size: 1.32rem; line-height: 1.35; margin-bottom: 8px; }

    .st-key-nav_p button, .st-key-nav_a button, .st-key-nav_r button, .st-key-nav_n button {
        border-radius: 50% !important; width: 48px !important; height: 48px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. MOTOR DE BUSCA ROBUSTO (CHAVE MESTRA) ---
def busca_documento_robusto(nome_pagina):
    pasta = "md_files"
    if not os.path.exists(pasta): return f"ERRO: Pasta '{pasta}' não encontrada."
    
    alvo = nome_pagina.upper()
    # Tenta o nome direto, com ABOUT_, com INFO_ e o caso especial INFO_SOBRE
    tentativas = [alvo, f"ABOUT_{alvo}", f"INFO_{alvo}"]
    if alvo == "ABOUT": tentativas.append("INFO_SOBRE")
    
    arquivos_locais = os.listdir(pasta)
    for f in arquivos_locais:
        nome_puro = os.path.splitext(f)[0].upper()
        if nome_puro in tentativas:
            try:
                with open(os.path.join(pasta, f), "r", encoding="utf-8") as file:
                    return file.read()
            except Exception as e:
                return f"ERRO ao ler {f}: {e}"
    
    return f"DEBUG_NOT_FOUND: Tentativas {tentativas} | Arquivos na pasta: {arquivos_locais}"

# --- 4. INTERFACE ---
c1, _, c2 = st.columns([2.5, 0.4, 7.1])

with c1:
    m_cols = st.columns(3)
    if m_cols[0].button("🔊", key="m_s"): st.toast("Som")
    if m_cols[1].button("🎨", key="m_a"): st.toast("Arte")
    if m_cols[2].button("🎬", key="m_v"): st.toast("Vídeo")
    st.divider()
    
    if os.path.exists("base"):
        files = sorted([f for f in os.listdir("base") if f.startswith("rol_")])
        acervo = {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}
        lista_l = list(acervo.keys())
        if lista_l:
            sel_l = st.selectbox("Livros", lista_l)
            with open(os.path.join("base", acervo[sel_l]), "r", encoding="utf-8") as f:
                st.session_state.temas_atuais = [line.strip() for line in f if line.strip()]
            
            idx = st.session_state.idx_tema % len(st.session_state.temas_atuais) if st.session_state.temas_atuais else 0
            st.selectbox("Temas", st.session_state.temas_atuais, index=idx)
    
    st.selectbox("Idioma", ["Português", "English", "Español", "Latin"], key="l_sel")

with c2:
    # Menu Superior - Sintaxe Corrigida aqui
    pgs = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "about"]
    t_cols = st.columns([1, 1, 1, 0.5, 1, 1, 1])
    
    for i, p in enumerate(pgs[:3]):
        if t_cols[i].button(p, key=f"btn_{p}"): st.session_state.page = p
    
    with t_cols[3]:
        if st.button("?", key="h_btn"): st.session_state.show_help = not st.session_state.show_help
    
    for i, p in enumerate(pgs[3:]):
        if t_cols[i+4].button(p, key=f"btn_{p}"): st.session_state.page = p

    st.write("") 
    n_
