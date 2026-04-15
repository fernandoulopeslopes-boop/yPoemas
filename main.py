import streamlit as st
import os
import random

# --- 1. BOOT & ESTADO (PTC) ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

try: 
    from lay_2_ypo import gera_poema
except Exception as e: 
    def gera_poema(t, p=""): return [f"Erro crítico no motor: {e}"]

# Inicialização limpa de estados
for key, val in {
    'page': 'demo', 'show_help': False, 'idx_tema': 0, 
    'temas_atuais': [], 'som': False, 'arte': False, 'video': False
}.items():
    if key not in st.session_state: st.session_state[key] = val

# --- 2. CSS: ESTÉTICA FINAL ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .main .block-container { max-width: 95%; padding-top: 1rem !important; }
    
    .md-humanista { font-family: 'Georgia', serif; line-height: 1.65; color: #222; font-size: 1.15rem; padding-bottom: 50px; }
    .md-tecnico { 
        font-family: 'Courier New', monospace; background-color: #f8f8f8; 
        padding: 25px; border-left: 5px solid #333; font-size: 1rem; line-height: 1.4; color: #111; 
    }
    
    .typo-title { font-family: 'Georgia', serif; font-size: 1.3rem; font-weight: bold; text-decoration: underline; margin-bottom: 20px; }
    .typo-verse { font-family: 'Georgia', serif; font-size: 1.32rem; line-height: 1.35; margin-bottom: 8px; }
    
    .st-key-nav_p button, .st-key-nav_a button, .st-key-nav_r button, .st-key-nav_n button {
        border-radius: 50% !important; width: 48px !important; height: 48px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. MOTOR DE DOCUMENTAÇÃO (BUSCA EXATA) ---
def busca_documento_estrito(nome_pagina):
    pasta = "md_files"
    if not os.path.exists(pasta): return None
    
    # Mapeamento fixo para evitar adivinhações
    mapa = {
        "about": ["ABOUT", "INFO_ABOUT", "INFO_SOBRE"],
        "ypoemas": ["YPOEMAS"],
        "eureka": ["EUREKA", "ABOUT_EUREKA"],
        "off-mach": ["OFF-MACH"],
        "opinião": ["OPINIAO", "OPINIAO_USER"]
    }
    
    alvos = mapa.get(nome_pagina.lower(), [nome_pagina.upper()])
    arquivos = os.listdir(pasta)
    
    for f in arquivos:
        nome_disco = os.path.splitext(f)[0].upper()
        if nome_disco in alvos:
            try:
                with open(os.path.join(pasta, f), "r", encoding="utf-8") as file:
                    return file.read()
            except: continue
    return None

# --- 4. INTERFACE ---
c1, _, c2 = st.columns([2.5, 0.4, 7.1])

with c1:
    m_cols = st.columns(3)
    if m_cols[0].button("🔊", key="m_s"): st.toast("🔊")
    if m_cols[1].button("🎨", key="m_a"): st.toast("🎨")
    if m_cols[2].button("🎬", key="m_v"): st.toast("🎬")
    st.divider()
    
    if os.path.exists("base"):
        files = sorted([f for f in os.listdir("base") if f.startswith("rol_")])
        acervo = {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}
        lista_l = list(acervo.keys())
        if lista_l:
            sel_l = st.selectbox("Livros", lista_l)
            with open(os.path.join("base", acervo[sel_l]), "r", encoding="utf-8") as f:
                st.session_state.temas_atuais = [line.strip() for line in f if line.strip()]
            
            # Sincronização forçada do índice
            idx_real = st.session_state.idx_tema % len(st.session_state.temas_atuais)
            st.selectbox("Temas", st.session_state.temas_atuais, index=idx_real)
    
    st.selectbox("Idioma", ["Português", "English", "Español", "Latin"], key="l_sel")

with c2:
    # Menu Superior de Navegação
    pgs = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "about"]
    t_cols = st.columns([1, 1, 1, 0.5, 1, 1, 1])
    for i, p in enumerate(pgs[:3]):
        if t_cols[i].button(p, key=f"btn_{p}"): st.session_state.page = p
    with t_cols[3]:
        if st.button("?", key="h_btn"): st.session_state.show_help = not st.session_state.show_help
    for i, p in enumerate(pgs[3:]):
        if t_cols[i+4].button(p, key=f"btn_{p}"): st.session_state.page = p

    st.write("") 
    n_cols = st.columns([2.5, 0.7, 0.7, 0.7, 0.7, 2.5])
    if n_cols[1].button("❮", key="nav_p"): st.session_state.idx_tema -= 1
    if n_cols[2].button("✚", key="nav_a"): st.toast("Semente salva")
    if n_cols[3].button("✱", key="nav_r"): st.session_state.idx_tema = random.randint(0, 999)
    if n_cols[4].button("❯", key="nav_n"): st.session_state.idx_tema += 1
    st.divider()

    # --- LÓGICA DE EXIBIÇÃO SEM BRECHAS ---
    if st.session_state.show_help:
        st.info("A precisão agora dança conforme o instinto.")
    
    elif st.session_state.page == "demo":
        # Bloco Exclusivo de Poesia: isolado de qualquer nome de página
        if st.session_state.temas_atuais:
            tema_final = st.session_state.temas_atuais[st.session_state.idx_tema % len(st.session_state.temas_atuais)]
            st.markdown(f'<div class="typo-title">{tema_final.upper()}</div>', unsafe_allow_html=True)
            # A chamada ao motor poético é limpa e direta
            for v in gera_poema(tema_final, ""):
                st.markdown(f'<div class="typo-verse">{v}</div>', unsafe_allow_html=True)
    
    else:
        # Bloco de Documentação
        conteudo = busca_documento_estrito(st.session_state.page)
        if conteudo:
            classe_css = "md-tecnico" if st.session_state.page == "yPoemas" else "md-humanista"
            st.markdown(f'<div class="{classe_css}">{conteudo}</div>', unsafe_allow_html=True)
        else:
            st.warning(f"O labirinto ainda guarda o segredo de '{st.session_state.page.upper()}'.")
