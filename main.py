import streamlit as st
import os

# --- 1. CONFIGURAÇÃO E INICIALIZAÇÃO (BLINDAGEM) ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

if 'page' not in st.session_state: st.session_state.page = 'DEMO'
if 'show_help' not in st.session_state: st.session_state.show_help = False

# --- 2. CSS: ANCORAGEM FIXA E PARADIGMA BOTTOM-STAR ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding-top: 1rem !important;}
    
    [data-testid="column"]:nth-child(1) {
        position: fixed !important;
        top: 1rem;
        left: 1rem;
        width: 18% !important;
        z-index: 1000;
    }
    [data-testid="column"]:nth-child(3) { margin-left: 21% !important; }

    .stButton button { height: 35px !important; color: #31333F !important; }
    .bottom-star button {
        height: 25px !important;
        color: #FFD700 !important; 
        background-color: transparent !important;
        border: none !important;
        font-size: 20px !important;
        margin-top: -8px !important;
    }

    .md-render { font-family: 'Georgia', serif; line-height: 1.6; color: #333; }
    .md-render blockquote { border-left: 3px solid #FFD700; padding-left: 15px; font-style: italic; color: #555; }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS DO ACERVO (\base) ---
@st.cache_data
def load_acervo_real():
    p = "base"
    if not os.path.exists(p): return {}
    # Busca os 13 livros reais
    files = [f for f in os.listdir(p) if f.startswith("rol_") and f.endswith(".txt")]
    return {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}

ACERVO = load_acervo_real()
IDIOMAS = [
    "Português", "Español", "English", "Français", "Italiano", "Català", 
    "Română", "Galego", "Latin", "Ladin", "Occitan", "Sardu",
    "Deutsch", "Nederlands", "Polski", "Ελληνικά", "Türkçe",
    "العربية", "ע Hebrew", "हिन्दी", "한국어"
]

# --- 4. ENGINE DE RENDERIZAÇÃO ---
def render_machina(pagina, help_mode):
    nome_f = "COMMENTS" if pagina == "opinião" else pagina.upper()
    if help_mode:
        for pre in ["ABOUT", "INFO", "MANUAL"]:
            path = f"md_files/{pre}_{nome_f}.md"
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    st.markdown(f'<div class="md-render">{f.read()}</div>', unsafe_allow_html=True)
                    st.divider()
    else:
        if pagina in ["opinião", "sobre"]:
            path = f"md_files/ABOUT_{nome_f}.md"
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    st.markdown(f'<div class="md-render">{f.read()}</div>', unsafe_allow_html=True)
        else:
            st.write(f"### {pagina.lower()} operando")

# --- 5. INTERFACE ---
c_painel, _, c_palco = st.columns([2, 0.1, 7.9])

with c_painel:
    st.write("### controles")
    i1, i2, i3 = st.columns(3)
    i1.button("🔈", key="s_on")
    i2.button("🎨", key="a_on")
    i3.button("💬", key="t_on")
    st.divider()
    
    livro_sel = st.selectbox("livros", list(ACERVO.keys()) if ACERVO else ["-"])
    if ACERVO:
        with open(os.path.join("base", ACERVO[livro_sel]), "r", encoding="utf-8") as f:
            temas = [l.strip() for l in f if l.strip()]
        st.selectbox("temas", temas)
    
    st.selectbox("idioma", IDIOMAS)

with c_palco:
    pesos = [0.8, 0.9, 0.8, 1.2, 1.0, 0.8]
    paginas = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    
    # Linha 1: Texto
    cols_t = st.columns(pesos)
    for i, item in enumerate(paginas):
        with cols_t[i]:
            if st.button(item.lower() if item != "yPoemas" else "yPoemas", key=f"p_{i}", use_container_width=True):
                st.session_state.page, st.session_state.show_help = item, False
                st.rerun()

    # Linha 2: Estrelas
    cols_s = st.columns(pesos)
    for i, item in enumerate(paginas):
        with cols_s[i]:
            st.markdown('<div class="bottom-star">', unsafe_allow_html=True)
            if st.button("★", key=f"h_{i}", use_container_width=True):
                st.session_state.page, st.session_state.show_help = item, True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    render_machina(st.session_state.page, st.session_state.show_help)
