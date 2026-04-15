import streamlit as st
import os

# --- 1. BOOT & ESTADO ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

if 'page' not in st.session_state: st.session_state.page = 'demo'
if 'show_help' not in st.session_state: st.session_state.show_help = False

def nav_trigger(p, h):
    st.session_state.page = p
    st.session_state.show_help = h

# --- 2. CSS DE ALTA PRECISÃO (OURO E FUNCIONALIDADE) ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding: 1rem !important;}
    
    /* Painel Lateral Fixo */
    [data-testid="column"]:nth-child(1) {
        position: fixed !important;
        top: 1rem; left: 1rem; width: 190px !important; z-index: 1001;
    }
    [data-testid="column"]:nth-child(3) { margin-left: 220px !important; }

    /* ESTRELAS OURO (#FFD700) */
    div.bottom-star button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        height: 40px !important;
    }
    
    /* Seletor agressivo para a cor amarela */
    div.bottom-star button div[data-testid="stMarkdownContainer"] p {
        color: #FFD700 !important;
        font-size: 35px !important;
        font-weight: 900 !important;
        -webkit-text-fill-color: #FFD700 !important;
        line-height: 1 !important;
        margin: 0 !important;
    }

    .scroll-stage {
        height: 75vh;
        overflow-y: auto;
        padding: 15px;
        border-top: 1px solid #eee;
        z-index: 1;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS ---
@st.cache_data
def get_acervo():
    if not os.path.exists("base"): return {}
    files = sorted([f for f in os.listdir("base") if f.startswith("rol_")])
    return {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in files}

ACERVO = get_acervo()
IDIOMAS = ["Português", "Español", "English", "Deutsch", "Nederlands", "Français", "Italiano", "Català", "Ελληνικά", "Türkçe", "العربية", "ע Hebrew", "हिन्दी"]

# --- 4. INTERFACE ---
c1, _, c2 = st.columns([2, 0.1, 7.9])

with c1:
    st.write("### controles")
    i1, i2, i3 = st.columns(3)
    i1.button("🔈", key="v_on")
    i2.button("🎨", key="c_on")
    i3.button("💬", key="m_on")
    st.divider()
    
    l_key = st.selectbox("livros", list(ACERVO.keys()) if ACERVO else ["-"], key="sel_l")
    if ACERVO:
        with open(os.path.join("base", ACERVO[l_key]), "r", encoding="utf-8") as f:
            temas = [l.strip() for l in f if l.strip()]
        st.selectbox("temas", temas, key="sel_t")
    st.selectbox("idioma", IDIOMAS, key="sel_i")

with c2:
    pesos = [0.8, 0.9, 0.8, 1.2, 1.0, 0.8]
    paginas = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    
    # Navegação de Texto
    cp = st.columns(pesos)
    for i, p in enumerate(paginas):
        cp[i].button(p.lower() if p != "yPoemas" else p, key=f"n_{i}", 
                     on_click=nav_trigger, args=(p, False), use_container_width=True)

    # Navegação de Estrelas (Ouro)
    cs = st.columns(pesos)
    for i, p in enumerate(paginas):
        with cs[i]:
            st.markdown('<div class="bottom-star">', unsafe_allow_html=True)
            st.button("★", key=f"s_{i}", on_click=nav_trigger, args=(p, True), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # --- 5. RENDERIZAÇÃO ---
    st.markdown('<div class="scroll-stage">', unsafe_allow_html=True)
    p_cur, h_cur = st.session_state.page, st.session_state.show_help
    file_id = "COMMENTS" if p_cur == "opinião" else p_cur.upper()

    if h_cur:
        for pre in ["ABOUT", "INFO", "MANUAL"]:
            path = f"md_files/{pre}_{file_id}.md"
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f: st.markdown(f.read())
                st.divider()
    else:
        if p_cur in ["opinião", "sobre"]:
            path = f"md_files/ABOUT_{file_id}.md"
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f: st.markdown(f.read())
        elif p_cur == "off-mach":
            st.subheader(f"{st.session_state.sel_l} / {st.session_state.get('sel_t', '')}")
        else:
            st.write(f"### {p_cur.lower()} operacional")
    st.markdown('</div>', unsafe_allow_html=True)
