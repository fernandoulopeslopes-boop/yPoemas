import streamlit as st
import os
import random

# --- 1. BOOT & ESTADO (RIGOR TOTAL) ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

try: 
    from lay_2_ypo import gera_poema
except Exception as e: 
    def gera_poema(t, p=""): return [f"Erro no motor: {e}"]

# Inicialização de estados sem ambiguidades
if 'page' not in st.session_state: st.session_state.page = 'demo'
if 'idx_tema' not in st.session_state: st.session_state.idx_tema = 0
if 'temas_atuais' not in st.session_state: st.session_state.temas_atuais = []

# --- 2. CSS: O DESIGN ANALISADO ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .main .block-container { max-width: 95%; padding-top: 1rem !important; }
    
    /* Tipografia Humanista */
    .md-humanista { font-family: 'Georgia', serif; line-height: 1.6; color: #222; font-size: 1.15rem; }
    .typo-title { font-family: 'Georgia', serif; font-size: 1.3rem; font-weight: bold; text-decoration: underline; margin-bottom: 20px; }
    .typo-verse { font-family: 'Georgia', serif; font-size: 1.32rem; line-height: 1.35; margin-bottom: 8px; }

    /* Botões Menu Superior (Retangulares) */
    .stButton > button { width: 100%; border-radius: 4px; height: 38px; border: 1px solid #ccc; }

    /* Botões de Navegação (Circulares) */
    div.nav-circles button {
        border-radius: 50% !important;
        width: 48px !important;
        height: 48px !important;
        padding: 0px !important;
        font-size: 1.2rem !important;
        display: flex; align-items: center; justify-content: center;
        border: 1px solid #333 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. INTERFACE ---
c1, _, c2 = st.columns([2.5, 0.4, 7.1])

with c1:
    m_cols = st.columns(3)
    m_cols[0].button("🔊", key="ctrl_s")
    m_cols[1].button("🎨", key="ctrl_a")
    m_cols[2].button("🎬", key="ctrl_v")
    st.divider()
    
    if os.path.exists("base"):
        # Filtro rigoroso de arquivos
        arquivos = sorted([f for f in os.listdir("base") if f.startswith("rol_") and f.endswith(".txt")])
        if arquivos:
            acervo = {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in arquivos}
            lista_livros = list(acervo.keys())
            
            sel_livro = st.selectbox("Livros", lista_livros, key="sb_livros")
            
            # Carregamento seguro da lista de temas
            with open(os.path.join("base", acervo[sel_livro]), "r", encoding="utf-8") as f:
                st.session_state.temas_atuais = [line.strip() for line in f if line.strip()]
            
            if st.session_state.temas_atuais:
                # Sincronia do índice com o selectbox
                idx_v = st.session_state.idx_tema % len(st.session_state.temas_atuais)
                st.selectbox("Temas", st.session_state.temas_atuais, index=idx_v, key="sb_temas")
    
    st.selectbox("Idioma", ["Português", "English", "Español", "Latin"], key="sb_lang")

with c2:
    # Menu Superior
    pgs = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "about"]
    t_cols = st.columns([1, 1, 1, 0.5, 1, 1, 1])
    
    for i, p in enumerate(pgs[:3]):
        if t_cols[i].button(p, key=f"nav_{p}"): st.session_state.page = p
    
    if t_cols[3].button("?", key="nav_help"): st.toast("A precisão agora dança conforme o instinto.")
    
    for i, p in enumerate(pgs[3:]):
        if t_cols[i+4].button(p, key=f"nav_{p}"): st.session_state.page = p

    st.write("") 
    # Navegação Inferior (Design de Círculos)
    n_cols = st.columns([2.5, 0.7, 0.7, 0.7, 0.7, 2.5])
    
    with n_cols[1]:
        st.markdown('<div class="nav-circles">', unsafe_allow_html=True)
        if st.button("❮", key="nav_prev"): st.session_state.idx_tema -= 1
        st.markdown('</div>', unsafe_allow_html=True)
    
    with n_cols[2]:
        st.markdown('<div class="nav-circles">', unsafe_allow_html=True)
        if st.button("✚", key="nav_save"): st.toast("Salvo")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with n_cols[3]:
        st.markdown('<div class="nav-circles">', unsafe_allow_html=True)
        if st.button("✱", key="nav_rand"): st.session_state.idx_tema = random.randint(0, 9999)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with n_cols[4]:
        st.markdown('<div class="nav-circles">', unsafe_allow_html=True)
        if st.button("❯", key="nav_next"): st.session_state.idx_tema += 1
        st.markdown('</div>', unsafe_allow_html=True)
    st.divider()

    # --- RENDERIZAÇÃO ---
    if st.session_state.page == "demo":
        if st.session_state.temas_atuais:
            # Proteção contra erro de arquivo: garantimos que o nome do tema seja limpo
            tema_nome = st.session_state.temas_atuais[st.session_state.idx_tema % len(st.session_state.temas_atuais)]
            st.markdown(f'<div class="typo-title">{tema_nome.upper()}</div>', unsafe_allow_html=True)
            
            try:
                # O motor gera_poema é chamado. O erro de FileNotFoundError indica
                # que ele espera arquivos que não estão mapeados corretamente.
                versos = gera_poema(tema_nome, "")
                for v in versos:
                    st.markdown(f'<div class="typo-verse">{v}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"O motor poético encontrou um obstáculo: {e}")
    else:
        # Busca de documentos MD
        nome_doc = f"{st.session_state.page.upper()}.md"
        caminho_doc = os.path.join("md_files", nome_doc)
        if os.path.exists(caminho_doc):
            with open(caminho_doc, "r", encoding="utf-8") as f:
                st.markdown(f'<div class="md-humanista">{f.read()}</div>', unsafe_allow_html=True)
        else:
            st.warning(f"Aguardando o arquivo: {nome_doc}")
