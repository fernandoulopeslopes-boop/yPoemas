import streamlit as st
import os

# --- 1. CONFIGURAÇÃO E ESTADO ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

if 'page' not in st.session_state: st.session_state.page = 'DEMO'
if 'show_help' not in st.session_state: st.session_state.show_help = False

# --- 2. CSS: O SEGREDO DO SCROLL INTERNO ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding-top: 1rem !important; overflow: hidden !important;}
    
    /* Coluna de Controles (Fixa) */
    [data-testid="column"]:nth-child(1) {
        position: fixed !important;
        top: 1rem;
        left: 1rem;
        width: 18% !important;
        z-index: 1000;
    }

    /* Margem do Palco */
    [data-testid="column"]:nth-child(3) { margin-left: 21% !important; }

    /* Estética dos Botões */
    .stButton button { height: 35px !important; color: #31333F !important; }
    .bottom-star button {
        height: 25px !important;
        color: #FFD700 !important; 
        background-color: transparent !important;
        border: none !important;
        font-size: 20px !important;
        margin-top: -8px !important;
    }

    /* O PALCO COM SCROLL ISOLADO */
    .scroll-stage {
        height: 72vh; /* Altura fixa para forçar o scroll interno */
        overflow-y: auto;
        padding-right: 15px;
        margin-top: 10px;
    }

    /* Personalização da Barra de Scroll (Cara do Pai) */
    .scroll-stage::-webkit-scrollbar { width: 6px; }
    .scroll-stage::-webkit-scrollbar-thumb { background: #FFD700; border-radius: 10px; }
    .scroll-stage::-webkit-scrollbar-track { background: #f1f1f1; }

    .md-render { font-family: 'Georgia', serif; line-height: 1.6; color: #333; }
    .md-render blockquote { border-left: 3px solid #FFD700; padding-left: 15px; font-style: italic; color: #555; }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS E ENGINE ---
@st.cache_data
def load_acervo():
    p = "base"
    if not os.path.exists(p): return {}
    files = [f for f in os.listdir(p) if f.startswith("rol_") and f.endswith(".txt")]
    return {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}

def render_content(pagina, help_mode):
    nome_f = "COMMENTS" if pagina == "opinião" else pagina.upper()
    diretorio = "md_files"
    conteudo = ""
    
    if help_mode:
        for pre in ["ABOUT", "INFO", "MANUAL"]:
            path = os.path.join(diretorio, f"{pre}_{nome_f}.md")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    conteudo += f.read() + "\n\n---\n\n"
    else:
        path = os.path.join(diretorio, f"ABOUT_{nome_f}.md")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                conteudo = f.read()
        else:
            conteudo = f"### {pagina.lower()} em operação"

    # Encapsulando na div de scroll isolado
    st.markdown(f'<div class="scroll-stage md-render">{conteudo}</div>', unsafe_allow_html=True)

# --- 4. INTERFACE ---
ACERVO = load_acervo()
c_painel, _, c_palco = st.columns([2, 0.1, 7.9])

with c_painel:
    st.write("### controles")
    st.columns(3)[0].button("🔈", key="s_on")
    st.columns(3)[1].button("🎨", key="a_on")
    st.columns(3)[2].button("💬", key="t_on")
    st.divider()
    livro_sel = st.selectbox("livros", list(ACERVO.keys()) if ACERVO else ["-"])
    st.selectbox("idioma", ["Português", "Español", "English", "Français", "Italiano"])

with c_palco:
    pesos = [0.8, 0.9, 0.8, 1.2, 1.0, 0.8]
    paginas = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    
    cols_t = st.columns(pesos)
    for i, item in enumerate(paginas):
        with cols_t[i]:
            if st.button(item.lower() if item != "yPoemas" else "yPoemas", key=f"p_{i}", use_container_width=True):
                st.session_state.page, st.session_state.show_help = item, False
                st.rerun()

    cols_s = st.columns(pesos)
    for i, item in enumerate(paginas):
        with cols_s[i]:
            st.markdown('<div class="bottom-star">', unsafe_allow_html=True)
            if st.button("★", key=f"h_{i}", use_container_width=True):
                st.session_state.page, st.session_state.show_help = item, True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    render_content(st.session_state.page, st.session_state.show_help)
