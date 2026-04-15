import streamlit as st
import os

# --- 1. CONFIGURAÇÃO E ESTADO ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

if 'page' not in st.session_state: st.session_state.page = 'DEMO'
if 'show_help' not in st.session_state: st.session_state.show_help = False

# --- 2. CSS: PRUMO E SCROLL ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding-top: 1rem !important; overflow: hidden !important;}
    
    /* Painel Fixo */
    [data-testid="column"]:nth-child(1) {
        position: fixed !important;
        top: 1rem;
        left: 1rem;
        width: 190px !important;
        z-index: 1000;
    }
    [data-testid="column"]:nth-child(3) { margin-left: 210px !important; }

    /* Botões de Controle em Linha */
    .stButton button { height: 35px !important; color: #31333F !important; padding: 0px !important; }
    
    /* Estrelas */
    .bottom-star button {
        height: 25px !important;
        color: #FFD700 !important; 
        background-color: transparent !important;
        border: none !important;
        font-size: 20px !important;
        margin-top: -8px !important;
    }

    .scroll-stage { height: 75vh; overflow-y: auto; padding-right: 15px; }
    .md-render { font-family: 'Georgia', serif; line-height: 1.6; color: #333; }
    .md-render blockquote { border-left: 3px solid #FFD700; padding-left: 15px; font-style: italic; color: #555; }
</style>
""", unsafe_allow_html=True)

# --- 3. ACERVO DINÂMICO ---
@st.cache_data
def get_acervo():
    p = "base"
    if not os.path.exists(p): return {}
    files = [f for f in os.listdir(p) if f.startswith("rol_") and f.endswith(".txt")]
    return {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}

ACERVO = get_acervo()
IDIOMAS = [
    "Português", "Español", "English", "Français", "Italiano", "Català", 
    "Română", "Galego", "Latin", "Ladin", "Occitan", "Sardu",
    "Deutsch", "Nederlands", "Polski", "Ελληνικά", "Türkçe",
    "العربية", "ע Hebrew", "हिन्दी"
]

# --- 4. INTERFACE ---
c_painel, _, c_palco = st.columns([2, 0.1, 7.9])

with c_painel:
    st.write("### controles")
    # Três botões em uma linha sem quebra
    ic1, ic2, ic3 = st.columns(3)
    ic1.button("🔈", key="s_on", use_container_width=True)
    ic2.button("🎨", key="a_on", use_container_width=True)
    ic3.button("💬", key="t_on", use_container_width=True)
    
    st.divider()
    
    # Livros e Temas
    livro_nome = st.selectbox("livros", list(ACERVO.keys()) if ACERVO else ["-"])
    
    if ACERVO:
        with open(os.path.join("base", ACERVO[livro_nome]), "r", encoding="utf-8") as f:
            temas = [l.strip() for l in f if l.strip()]
        st.selectbox("temas", temas, key="sel_tema")
    else:
        st.selectbox("temas", ["-"])
        
    st.selectbox("idioma", IDIOMAS)

with c_palco:
    pesos = [0.8, 0.9, 0.8, 1.2, 1.0, 0.8]
    paginas = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    
    # Régua Superior
    cols_p = st.columns(pesos)
    for i, p in enumerate(paginas):
        with cols_p[i]:
            if st.button(p.lower() if p != "yPoemas" else "yPoemas", key=f"p_{i}", use_container_width=True):
                st.session_state.page, st.session_state.show_help = p, False
                st.rerun()

    # Régua Inferior (Stars)
    cols_s = st.columns(pesos)
    for i, p in enumerate(paginas):
        with cols_s[i]:
            st.markdown('<div class="bottom-star">', unsafe_allow_html=True)
            if st.button("★", key=f"s_{i}", use_container_width=True):
                st.session_state.page, st.session_state.show_help = p, True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    
    # Palco de Renderização
    p_atual, h_atual = st.session_state.page, st.session_state.show_help
    nome_base = "COMMENTS" if p_atual == "opinião" else p_atual.upper()
    
    st.markdown('<div class="scroll-stage md-render">', unsafe_allow_html=True)
    if h_atual:
        for pre in ["ABOUT", "INFO", "MANUAL"]:
            path = f"md_files/{pre}_{nome_base}.md"
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    st.markdown(f.read())
                    st.markdown("---")
    else:
        path = f"md_files/ABOUT_{nome_base}.md"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                st.markdown(f.read())
        else:
            st.write(f"### {p_atual.lower()}")
    st.markdown('</div>', unsafe_allow_html=True)
