import streamlit as st
import os
import random

# --- 1. BOOT & ESTADO ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

try: 
    from lay_2_ypo import gera_poema
except Exception as e: 
    def gera_poema(t, p=""): return [f"Erro no motor: {e}"]

if 'page' not in st.session_state: st.session_state.page = 'demo'
if 'idx_tema' not in st.session_state: st.session_state.idx_tema = 0
if 'temas_atuais' not in st.session_state: st.session_state.temas_atuais = []

# --- 2. CSS DE PRECISÃO (O FIM DO LIXO) ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .main .block-container { max-width: 95%; padding-top: 1rem !important; }
    
    /* Fontes e Textos */
    .md-humanista { font-family: 'Georgia', serif; line-height: 1.6; color: #222; font-size: 1.15rem; }
    .typo-title { font-family: 'Georgia', serif; font-size: 1.3rem; font-weight: bold; text-decoration: underline; margin-bottom: 20px; }
    .typo-verse { font-family: 'Georgia', serif; font-size: 1.32rem; line-height: 1.35; margin-bottom: 8px; }

    /* RESET DE BOTÕES: Apenas os botões de navegação serão circulares */
    /* Usamos o seletor de chave específica para não afetar o menu superior */
    div[st-marker="nav_button"] button {
        border-radius: 50% !important;
        width: 48px !important;
        height: 48px !important;
        padding: 0px !important;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Botões do Menu Superior e Status (Retangulares e Alinhados) */
    div[st-marker="menu_button"] button {
        border-radius: 4px !important;
        width: 100% !important;
        height: auto !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. INTERFACE ---
c1, _, c2 = st.columns([2.5, 0.4, 7.1])

with c1:
    # Botões de Status (Retangulares)
    m_cols = st.columns(3)
    with m_cols[0]: st.markdown('<div st-marker="menu_button">', unsafe_allow_html=True); st.button("🔊", key="s_on"); st.markdown('</div>', unsafe_allow_html=True)
    with m_cols[1]: st.markdown('<div st-marker="menu_button">', unsafe_allow_html=True); st.button("🎨", key="a_on"); st.markdown('</div>', unsafe_allow_html=True)
    with m_cols[2]: st.markdown('<div st-marker="menu_button">', unsafe_allow_html=True); st.button("🎬", key="v_on"); st.markdown('</div>', unsafe_allow_html=True)
    st.divider()
    
    if os.path.exists("base"):
        files = sorted([f for f in os.listdir("base") if f.startswith("rol_")])
        if files:
            acervo = {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}
            sel_l = st.selectbox("Livros", list(acervo.keys()), key="livro_box")
            with open(os.path.join("base", acervo[sel_l]), "r", encoding="utf-8") as f:
                st.session_state.temas_atuais = [line.strip() for line in f if line.strip()]
            
            idx = st.session_state.idx_tema % len(st.session_state.temas_atuais) if st.session_state.temas_atuais else 0
            st.selectbox("Temas", st.session_state.temas_atuais, index=idx, key="tema_box")
    
    st.selectbox("Idioma", ["Português", "English", "Español", "Latin"], key="lang_box")

with c2:
    # Menu Superior (Retangulares)
    pgs = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "about"]
    t_cols = st.columns([1, 1, 1, 0.5, 1, 1, 1])
    
    for i, p in enumerate(pgs[:3]):
        with t_cols[i]:
            st.markdown('<div st-marker="menu_button">', unsafe_allow_html=True)
            if st.button(p, key=f"p_{p}"): st.session_state.page = p
            st.markdown('</div>', unsafe_allow_html=True)
            
    with t_cols[3]:
        st.markdown('<div st-marker="menu_button">', unsafe_allow_html=True)
        if st.button("?", key="h_mark"): st.toast("A precisão agora dança conforme o instinto.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    for i, p in enumerate(pgs[3:]):
        with t_cols[i+4]:
            st.markdown('<div st-marker="menu_button">', unsafe_allow_html=True)
            if st.button(p, key=f"p_{p}"): st.session_state.page = p
            st.markdown('</div>', unsafe_allow_html=True)

    st.write("") 
    # Navegação Inferior (CIRCULARES)
    n_cols = st.columns([2.5, 0.7, 0.7, 0.7, 0.7, 2.5])
    
    with n_cols[1]: st.markdown('<div st-marker="nav_button">', unsafe_allow_html=True); st.button("❮", key="go_p"); st.markdown('</div>', unsafe_allow_html=True)
    with n_cols[2]: st.markdown('<div st-marker="nav_button">', unsafe_allow_html=True); st.button("✚", key="go_s"); st.markdown('</div>', unsafe_allow_html=True)
    with n_cols[3]: st.markdown('<div st-marker="nav_button">', unsafe_allow_html=True); st.button("✱", key="go_r"); st.markdown('</div>', unsafe_allow_html=True)
    with n_cols[4]: st.markdown('<div st-marker="nav_button">', unsafe_allow_html=True); st.button("❯", key="go_n"); st.markdown('</div>', unsafe_allow_html=True)
    st.divider()

    # Renderização
    if st.session_state.page == "demo":
        if st.session_state.temas_atuais:
            tema = st.session_state.temas_atuais[st.session_state.idx_tema % len(st.session_state.temas_atuais)]
            st.markdown(f'<div class="typo-title">{tema.upper()}</div>', unsafe_allow_html=True)
            for v in gera_poema(tema, ""):
                st.markdown(f'<div class="typo-verse">{v}</div>', unsafe_allow_html=True)
    else:
        path_md = os.path.join("md_files", f"{st.session_state.page.upper()}.md")
        if os.path.exists(path_md):
            with open(path_md, "r", encoding="utf-8") as f:
                st.markdown(f'<div class="md-humanista">{f.read()}</div>', unsafe_allow_html=True)
        else:
            st.warning(f"Aguardando: {st.session_state.page}")
