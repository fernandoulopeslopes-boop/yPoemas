import streamlit as st
import os

# --- 1. CONFIGURAÇÃO E ESTADO ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

if 'page' not in st.session_state: st.session_state.page = 'demo'
if 'show_help' not in st.session_state: st.session_state.show_help = False

def nav(p, h):
    st.session_state.page = p
    st.session_state.show_help = h

# --- 2. CSS: OURO E PRUMO ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding: 1rem !important;}
    [data-testid="column"]:nth-child(1) {position: fixed !important; top: 1rem; left: 1rem; width: 190px !important; z-index: 1001;}
    [data-testid="column"]:nth-child(3) {margin-left: 220px !important;}

    /* ESTRELAS OURO (#FFD700) */
    .bottom-star button {background: transparent !important; border: none !important; box-shadow: none !important; height: 35px !important;}
    .bottom-star button p {
        color: #FFD700 !important;
        font-size: 32px !important;
        font-weight: 900 !important;
        line-height: 1 !important;
        -webkit-text-fill-color: #FFD700 !important;
    }
    .bottom-star button:hover p {color: #FFEA00 !important;}
    .scroll-stage {height: 75vh; overflow-y: auto; padding: 10px; border-top: 1px solid #ddd;}
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS ---
@st.cache_data
def get_acervo():
    if not os.path.exists("base"): return {}
    f = sorted([f for f in os.listdir("base") if f.startswith("rol_")])
    return {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in f}

ACERVO = get_acervo()
IDIOMAS = ["Português", "Español", "English", "Deutsch", "Nederlands", "Français", "Italiano", "Català", "Ελληνικά", "Türkçe", "العربية", "ע Hebrew", "हिन्दी"]

# --- 4. INTERFACE ---
c1, _, c2 = st.columns([2, 0.1, 7.9])

with c1:
    st.write("### controles")
    i1, i2, i3 = st.columns(3)
    i1.button("🔈", key="s")
    i2.button("🎨", key="a")
    i3.button("💬", key="t")
    st.divider()
    l_sel = st.selectbox("livros", list(ACERVO.keys()) if ACERVO else ["-"], key="l")
    if ACERVO:
        with open(os.path.join("base", ACERVO[l_sel]), "r", encoding="utf-8") as f:
            t = [l.strip() for l in f if l.strip()]
        st.selectbox("temas", t, key="sel_tema")
    st.selectbox("idioma", IDIOMAS, key="lang")

with c2:
    ps = [0.8, 0.9, 0.8, 1.2, 1.0, 0.8]
    pgs = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    
    cols_p = st.columns(ps)
    for i, p in enumerate(pgs):
        cols_p[i].button(p.lower() if p != "yPoemas" else p, key=f"n{i}", on_click=nav, args=(p, False), use_container_width=True)

    cols_s = st.columns(ps)
    for i, p in enumerate(pgs):
        with cols_s[i]:
            st.markdown('<div class="bottom-star">', unsafe_allow_html=True)
            st.button("★", key=f"st{i}", on_click=nav, args=(p, True), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    st.markdown('<div class="scroll-stage">', unsafe_allow_html=True)
    curr_p, curr_h = st.session_state.page, st.session_state.show_help
    name = "COMMENTS" if curr_p == "opinião" else curr_p.upper()

    if curr_h:
        for pre in ["ABOUT", "INFO", "MANUAL"]:
            path = f"md_files/{pre}_{name}.md"
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f: st.markdown(f.read())
                st.divider()
    else:
        if curr_p in ["opinião", "sobre"]:
            path = f"md_files/ABOUT_{name}.md"
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f: st.markdown(f.read())
        elif curr_p == "off-mach":
            st.subheader(f"{st.session_state.l} / {st.session_state.get('sel_tema', '')}")
        else:
            st.write(f"### {curr_p.lower()} ativa")
    st.markdown('</div>', unsafe_allow_html=True)
