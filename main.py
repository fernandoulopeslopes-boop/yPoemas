import streamlit as st
import os

# --- 1. CONFIGURAÇÃO E ESTADO ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

if 'page' not in st.session_state:
    st.session_state.page = 'demo'
if 'show_help' not in st.session_state:
    st.session_state.show_help = False

# --- 2. CSS: OURO REAL E ESTRUTURA FIXA ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding-top: 1rem !important; overflow: hidden !important; background-color: #ffffff;}
    
    /* Painel Lateral Fixo */
    [data-testid="column"]:nth-child(1) {
        position: fixed !important;
        top: 1rem;
        left: 1rem;
        width: 200px !important;
        z-index: 1001;
    }
    [data-testid="column"]:nth-child(3) { margin-left: 230px !important; }

    /* Botões de Navegação */
    .stButton button { 
        height: 38px !important; 
        color: #31333F !important; 
        width: 100% !important;
        border-radius: 4px !important;
    }
    
    /* ESTRELAS OURO (#FFD700) */
    div.bottom-star button {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        height: 30px !important;
        margin-top: -10px !important;
        padding: 0 !important;
    }
    div.bottom-star button p { 
        color: #FFD700 !important; 
        font-size: 30px !important; 
        font-weight: bold !important;
        line-height: 1 !important;
        margin: 0 !important;
    }
    div.bottom-star button:hover p { color: #FFEA00 !important; }

    /* Palco com Scroll Isolado */
    .scroll-stage { 
        height: 78vh; 
        overflow-y: auto; 
        padding-right: 20px; 
        border-top: 1px solid #eee;
        margin-top: 10px;
    }
    .md-render { font-family: 'Georgia', serif; line-height: 1.7; color: #1a1a1a; }
    .md-render blockquote { 
        border-left: 4px solid #FFD700; 
        padding-left: 20px; 
        font-style: italic; 
        color: #444; 
        margin: 20px 0;
    }
    .md-render hr { border: 0; border-top: 1px solid #eee; margin: 25px 0; }
</style>
""", unsafe_allow_html=True)

# --- 3. GESTÃO DE DADOS ---
@st.cache_data
def load_acervo():
    p = "base"
    if not os.path.exists(p): return {}
    files = sorted([f for f in os.listdir(p) if f.startswith("rol_") and f.endswith(".txt")])
    return {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}

ACERVO = load_acervo()
IDIOMAS = [
    "Português", "Español", "English", "Deutsch", "Nederlands", 
    "Français", "Italiano", "Català", "Română", "Galego", 
    "Latin", "Sardu", "Ελληνικά", "Türkçe", "العربية", 
    "ע Hebrew", "हिन्दी"
]

# --- 4. INTERFACE ---
c_painel, _, c_palco = st.columns([2, 0.1, 7.9])

with c_painel:
    st.write("### controles")
    ic1, ic2, ic3 = st.columns(3)
    ic1.button("🔈", key="s_on")
    ic2.button("🎨", key="a_on")
    ic3.button("💬", key="t_on")
    st.divider()
    
    livro_sel = st.selectbox("livros", list(ACERVO.keys()) if ACERVO else ["-"], key="sel_livro")
    if ACERVO:
        with open(os.path.join("base", ACERVO[livro_sel]), "r", encoding="utf-8") as f:
            temas = [l.strip() for l in f if l.strip()]
        st.selectbox("temas", temas, key="sel_tema")
    st.selectbox("idioma", IDIOMAS, key="sel_lang")

with c_palco:
    pesos = [0.8, 0.9, 0.8, 1.2, 1.0, 0.8]
    paginas = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    
    # Navegação Superior
    cols_p = st.columns(pesos)
    for i, p in enumerate(paginas):
        with cols_p[i]:
            lbl = "yPoemas" if p == "yPoemas" else p.lower()
            if st.button(lbl, key=f"btn_nav_{i}", use_container_width=True):
                st.session_state.page = p
                st.session_state.show_help = False
                st.rerun()

    # Navegação de Estrelas (Ouro)
    cols_s = st.columns(pesos)
    for i, p in enumerate(paginas):
        with cols_s[i]:
            st.markdown('<div class="bottom-star">', unsafe_allow_html=True)
            if st.button("★", key=f"star_nav_{i}", use_container_width=True):
                st.session_state.page = p
                st.session_state.show_help = True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # --- 5. RENDERIZAÇÃO DO PALCO ---
    p_atual = st.session_state.page
    h_mode = st.session_state.show_help
    nome_base = "COMMENTS" if p_atual == "opinião" else p_atual.upper()
    
    st.markdown('<div class="scroll-stage md-render">', unsafe_allow_html=True)
    
    if h_mode:
        for pre in ["ABOUT", "INFO", "MANUAL"]:
            path = f"md_files/{pre}_{nome_base}.md"
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    st.markdown(f.read())
                    st.markdown("---")
    else:
        if p_atual in ["opinião", "sobre"]:
            path = f"md_files/ABOUT_{nome_base}.md"
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f: st.markdown(f.read())
        elif p_atual == "off-mach":
            st.write(f"### {st.session_state.sel_livro} / {st.session_state.sel_tema}")
            st.info("Interface Off-Machina operacional.")
        else:
            st.write(f"### {p_atual.lower()}")
            st.write("Módulo funcional ativo.")
            
    st.markdown('</div>', unsafe_allow_html=True)
