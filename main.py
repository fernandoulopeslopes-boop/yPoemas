import streamlit as st
import os

# --- 1. CONFIGURAÇÃO E ESTADO ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

if 'page' not in st.session_state: st.session_state.page = 'DEMO'
if 'show_help' not in st.session_state: st.session_state.show_help = False

# --- 2. CSS: OURO, PRUMO E SCROLL ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding-top: 1rem !important; overflow: hidden !important;}
    
    /* Painel Lateral Fixo */
    [data-testid="column"]:nth-child(1) {
        position: fixed !important;
        top: 1rem;
        left: 1rem;
        width: 195px !important;
        z-index: 1000;
    }
    [data-testid="column"]:nth-child(3) { margin-left: 215px !important; }

    /* Botões de Controle */
    .stButton button { height: 35px !important; color: #31333F !important; padding: 0 !important; }
    
    /* ESTRELAS OURO (PRECISÃO ABSOLUTA) */
    div.bottom-star button {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        height: 25px !important;
        margin-top: -10px !important;
    }
    div.bottom-star button p { 
        color: #FFD700 !important; 
        font-size: 26px !important; 
        font-weight: bold !important;
    }
    div.bottom-star button:hover p { color: #FFEA00 !important; }

    /* Palco com Scroll Isolado */
    .scroll-stage { height: 78vh; overflow-y: auto; padding-right: 12px; }
    .md-render { font-family: 'Georgia', serif; line-height: 1.6; color: #333; }
    .md-render blockquote { border-left: 3px solid #FFD700; padding-left: 15px; font-style: italic; color: #555; }
</style>
""", unsafe_allow_html=True)

# --- 3. ACERVO E IDIOMAS (LATIN + GERMANIC + SPECIALS) ---
@st.cache_data
def get_books():
    p = "base"
    if not os.path.exists(p): return {}
    files = [f for f in os.listdir(p) if f.startswith("rol_") and f.endswith(".txt")]
    return {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}

ACERVO = get_books()

# Lista purificada: Latinos, Germânicos e os 5 scripts específicos
IDIOMAS = [
    "Português", "Español", "English", "Deutsch", "Nederlands", 
    "Français", "Italiano", "Català", "Română", "Galego", 
    "Latin", "Sardu", "Ελληνικά", "Türkçe", "العربية", 
    "ע Hebrew", "हिन्दी"
]

# --- 4. ENGINE DE RENDERIZAÇÃO ---
def engine_palco(pagina, help_mode):
    nome_f = "COMMENTS" if pagina == "opinião" else pagina.upper()
    st.markdown('<div class="scroll-stage md-render">', unsafe_allow_html=True)
    
    if help_mode:
        for pre in ["ABOUT", "INFO", "MANUAL"]:
            path = f"md_files/{pre}_{nome_f}.md"
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    st.markdown(f.read())
                    st.markdown("---")
    else:
        if pagina == "off-mach":
            st.write(f"### {st.session_state.get('sel_livro', '...')} / {st.session_state.get('sel_tema', '...')}")
            st.info("A engrenagem está pronta para leitura.")
        elif pagina in ["opinião", "sobre"]:
            path = f"md_files/ABOUT_{nome_f}.md"
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f: st.markdown(f.read())
        else:
            st.write(f"### {pagina.lower()}")
            st.write("Sistema operacional.")

    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. INTERFACE ---
c_painel, _, c_palco = st.columns([2, 0.1, 7.9])

with c_painel:
    st.write("### controles")
    ic1, ic2, ic3 = st.columns(3)
    ic1.button("🔈", key="s_on", use_container_width=True)
    ic2.button("🎨", key="a_on", use_container_width=True)
    ic3.button("💬", key="t_on", use_container_width=True)
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
    
    # Navegação
    c_p = st.columns(pesos)
    for i, p in enumerate(paginas):
        with c_p[i]:
            lbl = "yPoemas" if p == "yPoemas" else p.lower()
            if st.button(lbl, key=f"btn_{i}", use_container_width=True):
                st.session_state.page, st.session_state.show_help = p, False
                st.rerun()

    # Stars (Ouro)
    c_s = st.columns(pesos)
    for i, p in enumerate(paginas):
        with c_s[i]:
            st.markdown('<div class="bottom-star">', unsafe_allow_html=True)
            if st.button("★", key=f"star_{i}", use_container_width=True):
                st.session_state.page, st.session_state.show_help = p, True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    engine_palco(st.session_state.page, st.session_state.show_help)
