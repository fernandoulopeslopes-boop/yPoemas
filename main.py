import streamlit as st
import os

# --- 1. CONFIGURAÇÃO E ESTADO ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

if 'page' not in st.session_state: st.session_state.page = 'DEMO'
if 'show_help' not in st.session_state: st.session_state.show_help = False

# --- 2. CSS: CORREÇÃO DE PRUMO E SCROLL ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding-top: 1rem !important; overflow: hidden !important;}
    
    /* Painel de Controles (Fixed Top-Left) */
    [data-testid="column"]:nth-child(1) {
        position: fixed !important;
        top: 1rem;
        left: 1rem;
        width: 200px !important;
        z-index: 1000;
    }
    [data-testid="column"]:nth-child(3) { margin-left: 230px !important; }

    /* Forçar botões dos controles em linha (Fim da escada) */
    .control-row { display: flex; justify-content: space-between; gap: 5px; margin-bottom: 10px; }
    .control-row button { flex: 1; height: 35px !important; padding: 0 !important; }

    /* Estilo das Estrelas (Bottom-Star) */
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
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS DO ACERVO (\base) ---
@st.cache_data
def get_books():
    p = "base"
    if not os.path.exists(p): return {}
    files = [f for f in os.listdir(p) if f.startswith("rol_") and f.endswith(".txt")]
    return {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}

ACERVO = get_books()
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
    # Uso de botões em linha sem colunas do Streamlit para evitar "escada"
    col1, col2, col3 = st.columns(3)
    with col1: st.button("🔈", key="s_on")
    with col2: st.button("🎨", key="a_on")
    with col3: st.button("💬", key="t_on")
    
    st.divider()
    
    # Seleção de Livro e Temas (Lista Real)
    nome_livro = st.selectbox("livros", list(ACERVO.keys()) if ACERVO else ["-"])
    if ACERVO:
        with open(os.path.join("base", ACERVO[nome_livro]), "r", encoding="utf-8") as f:
            lista_temas = [linha.strip() for linha in f if linha.strip()]
        st.selectbox("temas", lista_temas)
    
    st.selectbox("idioma", IDIOMAS)

with c_palco:
    pesos = [0.8, 0.9, 0.8, 1.2, 1.0, 0.8]
    paginas = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    
    # Navegação
    c_p = st.columns(pesos)
    for i, p in enumerate(paginas):
        with c_p[i]:
            if st.button(p.lower() if p != "yPoemas" else "yPoemas", key=f"btn_{i}", use_container_width=True):
                st.session_state.page, st.session_state.show_help = p, False
                st.rerun()

    # Stars
    c_s = st.columns(pesos)
    for i, p in enumerate(paginas):
        with c_s[i]:
            st.markdown('<div class="bottom-star">', unsafe_allow_html=True)
            if st.button("★", key=f"star_{i}", use_container_width=True):
                st.session_state.page, st.session_state.show_help = p, True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    
    # Renderização (Palco Isolado)
    p, h = st.session_state.page, st.session_state.show_help
    nome_base = "COMMENTS" if p == "opinião" else p.upper()
    
    st.markdown('<div class="scroll-stage md-render">', unsafe_allow_html=True)
    if h:
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
            st.write(f"### {p.lower()}")
    st.markdown('</div>', unsafe_allow_html=True)
