import streamlit as st
import os

# --- 1. BOOT & ESTADO ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

if 'page' not in st.session_state: st.session_state.page = 'demo'
if 'show_help' not in st.session_state: st.session_state.show_help = False

# Callbacks de Navegação
def nav_to(p, h):
    st.session_state.page = p
    st.session_state.show_help = h

# --- 2. CSS BLINDADO (Sem seletores experimentais que causam tela branca) ---
st.markdown("""
<style>
    /* Reset Geral */
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding: 1rem !important;}
    
    /* Painel Lateral Fixo (Largura Segura) */
    [data-testid="column"]:nth-child(1) {
        position: fixed !important;
        top: 1rem;
        left: 1rem;
        width: 180px !important;
        z-index: 9999;
    }
    
    /* Palco de Renderização */
    [data-testid="column"]:nth-child(3) { margin-left: 210px !important; }

    /* ESTRELAS OURO - Usando seletor de parágrafo simplificado */
    .bottom-star button {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        height: 30px !important;
    }
    .bottom-star button p {
        color: #FFD700 !important;
        font-size: 30px !important;
        font-weight: bold !important;
        margin: 0 !important;
    }

    /* Scroll Isolado */
    .scroll-stage {
        height: 75vh;
        overflow-y: auto;
        padding: 10px;
        border-top: 1px solid #eee;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS (ACERVO & IDIOMAS) ---
@st.cache_data
def get_books():
    p = "base"
    if not os.path.exists(p): return {}
    files = sorted([f for f in os.listdir(p) if f.startswith("rol_") and f.endswith(".txt")])
    return {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}

ACERVO = get_books()
IDIOMAS = ["Português", "Español", "English", "Deutsch", "Nederlands", "Français", "Italiano", "Català", "Ελληνικά", "Türkçe", "العربية", "ע Hebrew", "हिन्दी"]

# --- 4. INTERFACE ---
c_painel, _, c_palco = st.columns([2, 0.1, 7.9])

with c_painel:
    st.write("### controles")
    ic1, ic2, ic3 = st.columns(3)
    ic1.button("🔈", key="s_on")
    ic2.button("🎨", key="a_on")
    ic3.button("💬", key="t_on")
    
    st.divider()
    
    livro = st.selectbox("livros", list(ACERVO.keys()) if ACERVO else ["-"], key="sel_livro")
    if ACERVO:
        with open(os.path.join("base", ACERVO[livro]), "r", encoding="utf-8") as f:
            temas = [l.strip() for l in f if l.strip()]
        st.selectbox("temas", temas, key="sel_tema")
    st.selectbox("idioma", IDIOMAS, key="sel_lang")

with c_palco:
    pesos = [0.8, 0.9, 0.8, 1.2, 1.0, 0.8]
    paginas = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    
    # Botões de Navegação
    cp = st.columns(pesos)
    for i, p in enumerate(paginas):
        cp[i].button(p.lower() if p != "yPoemas" else p, key=f"btn_{i}", 
                     on_click=nav_to, args=(p, False), use_container_width=True)

    # Estrelas (Navegação Star)
    cs = st.columns(pesos)
    for i, p in enumerate(paginas):
        with cs[i]:
            st.markdown('<div class="bottom-star">', unsafe_allow_html=True)
            st.button("★", key=f"star_{i}", on_click=nav_to, args=(p, True), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # --- 5. RENDERIZAÇÃO DO CONTEÚDO ---
    p_atual = st.session_state.page
    h_mode = st.session_state.show_help
    nome_f = "COMMENTS" if p_atual == "opinião" else p_atual.upper()
    
    st.markdown('<div class="scroll-stage">', unsafe_allow_html=True)
    if h_mode:
        for pre in ["ABOUT", "INFO", "MANUAL"]:
            path = f"md_files/{pre}_{nome_f}.md"
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f: st.markdown(f.read())
                st.markdown("---")
    else:
        if p_atual in ["opinião", "sobre"]:
            path = f"md_files/ABOUT_{nome_f}.md"
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f: st.markdown(f.read())
            else: st.info(f"Página {p_atual.lower()} pronta.")
        elif p_atual == "off-mach":
            st.subheader(f"{st.session_state.sel_livro} / {st.session_state.get('sel_tema', '')}")
        else:
            st.write(f"### {p_atual.lower()} em operação")
    st.markdown('</div>', unsafe_allow_html=True)
