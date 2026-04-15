import streamlit as st
import os
import random

# --- 1. CONFIGURAÇÃO DE BASE (RESTAURAÇÃO V.45) ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

# Motor Poético
try: 
    from lay_2_ypo import gera_poema
except Exception as e: 
    def gera_poema(t, p=""): return [f"Erro de conexão com o motor: {e}"]

# Estados de Sessão - Limpeza Total
if 'page' not in st.session_state: st.session_state.page = 'demo'
if 'idx_tema' not in st.session_state: st.session_state.idx_tema = 0
if 'temas_atuais' not in st.session_state: st.session_state.temas_atuais = []

# --- 2. CSS ESTÁVEL (SEM INTERFERÊNCIAS) ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .main .block-container { max-width: 95%; padding-top: 1rem !important; }
    
    .md-humanista { font-family: 'Georgia', serif; line-height: 1.6; color: #222; font-size: 1.15rem; }
    .typo-title { font-family: 'Georgia', serif; font-size: 1.3rem; font-weight: bold; text-decoration: underline; margin-bottom: 20px; }
    .typo-verse { font-family: 'Georgia', serif; font-size: 1.32rem; line-height: 1.35; margin-bottom: 8px; }
    
    /* Botões de Navegação Inferior: Circulares por classe específica */
    .stButton > button { border-radius: 4px; } /* Padrão para menu */
    
    /* Identificador visual para os botões circulares da base */
    div.nav-circles button {
        border-radius: 50% !important;
        width: 50px !important;
        height: 50px !important;
        padding: 0px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. LÓGICA DE NAVEGAÇÃO ---
def mudar_indice(delta):
    if st.session_state.temas_atuais:
        st.session_state.idx_tema = (st.session_state.idx_tema + delta) % len(st.session_state.temas_atuais)

def set_random():
    if st.session_state.temas_atuais:
        st.session_state.idx_tema = random.randint(0, len(st.session_state.temas_atuais) - 1)

# --- 4. INTERFACE ---
c1, _, c2 = st.columns([2.5, 0.4, 7.1])

with c1:
    # Status/Mídia
    col_m = st.columns(3)
    col_m[0].button("🔊", key="m_som")
    col_m[1].button("🎨", key="m_art")
    col_m[2].button("🎬", key="m_vid")
    st.divider()
    
    # Carregamento de Dados
    if os.path.exists("base"):
        arquivos = sorted([f for f in os.listdir("base") if f.startswith("rol_")])
        if arquivos:
            acervo = {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in arquivos}
            livro_sel = st.selectbox("Livros", list(acervo.keys()), key="sb_livro")
            
            with open(os.path.join("base", acervo[livro_sel]), "r", encoding="utf-8") as f:
                st.session_state.temas_atuais = [line.strip() for line in f if line.strip()]
            
            # Selectbox de temas sincronizado com o idx_tema
            def on_tema_change():
                st.session_state.idx_tema = st.session_state.temas_atuais.index(st.session_state.new_tema)

            if st.session_state.temas_atuais:
                idx_atual = st.session_state.idx_tema % len(st.session_state.temas_atuais)
                st.selectbox("Temas", st.session_state.temas_atuais, index=idx_atual, key="new_tema", on_change=on_tema_change)
    
    st.selectbox("Idioma", ["Português", "English", "Español", "Latin"], key="sb_idioma")

with c2:
    # Menu Superior
    pgs = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "about"]
    t_cols = st.columns([1, 1, 1, 0.5, 1, 1, 1])
    
    for i, p in enumerate(pgs[:3]):
        if t_cols[i].button(p, key=f"pg_{p}"): st.session_state.page = p
    
    if t_cols[3].button("?", key="pg_h"): st.toast("A precisão agora dança conforme o instinto.")
    
    for i, p in enumerate(pgs[3:]):
        if t_cols[i+4].button(p, key=f"pg_{p}"): st.session_state.page = p

    st.write("") 
    
    # Navegação de Temas (Botões Circulares)
    n_cols = st.columns([2.5, 0.7, 0.7, 0.7, 0.7, 2.5])
    
    with n_cols[1]:
        st.markdown('<div class="nav-circles">', unsafe_allow_html=True)
        if st.button("❮", key="nav_p"): mudar_indice(-1)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with n_cols[2]:
        st.markdown('<div class="nav-circles">', unsafe_allow_html=True)
        if st.button("✚", key="nav_s"): st.toast("Semente Salva")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with n_cols[3]:
        st.markdown('<div class="nav-circles">', unsafe_allow_html=True)
        if st.button("✱", key="nav_r"): set_random()
        st.markdown('</div>', unsafe_allow_html=True)
        
    with n_cols[4]:
        st.markdown('<div class="nav-circles">', unsafe_allow_html=True)
        if st.button("❯", key="nav_n"): mudar_indice(1)
        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # Renderização de Conteúdo
    if st.session_state.page == "demo":
        if st.session_state.temas_atuais:
            tema_final = st.session_state.temas_atuais[st.session_state.idx_tema % len(st.session_state.temas_atuais)]
            st.markdown(f'<div class="typo-title">{tema_final.upper()}</div>', unsafe_allow_html=True)
            for verso in gera_poema(tema_final, ""):
                st.markdown(f'<div class="typo-verse">{verso}</div>', unsafe_allow_html=True)
    else:
        # Busca de MD de forma direta
        path_md = os.path.join("md_files", f"{st.session_state.page.upper()}.md")
        if os.path.exists(path_md):
            with open(path_md, "r", encoding="utf-8") as f:
                st.markdown(f'<div class="md-humanista">{f.read()}</div>', unsafe_allow_html=True)
        else:
            st.warning(f"Aguardando conteúdo: {st.session_state.page}")
