import streamlit as st
import os

# --- 1. CONFIGURAÇÃO SOBERANA ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS: ANCORAGEM FIXA E EQUILÍBRIO VISUAL ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding-top: 1rem !important;}
    
    /* COLUNA ESQUERDA FIXA NO TOP-LEFT */
    [data-testid="column"]:nth-child(1) {
        position: fixed !important;
        top: 1rem;
        left: 1rem;
        width: 18% !important; /* Ajuste conforme necessidade */
        z-index: 1000;
    }

    /* COMPENSAÇÃO DO PALCO PARA NÃO SOBREPOR A COLUNA FIXA */
    [data-testid="column"]:nth-child(3) {
        margin-left: 22% !important;
    }

    div[data-testid="stHorizontalBlock"] { align-items: center !important; gap: 0px !important; }

    /* BOTÕES: Ajuste de cor e forma */
    .stButton button {
        height: 35px !important;
        margin: 0px !important;
        padding: 0px 2px !important;
        color: #31333F !important;
        border-radius: 4px !important;
        font-size: 14px !important;
    }

    /* ESTRELA AMARELA BOTTOM */
    .bottom-star button {
        height: 25px !important;
        color: #FFD700 !important; 
        background-color: transparent !important;
        border: none !important;
        font-size: 20px !important;
        margin-top: -8px !important;
    }
    .bottom-star button:hover { color: #FFEA00 !important; }

    .md-render { font-family: 'Georgia', serif; line-height: 1.6; margin-top: 25px; }
</style>
""", unsafe_allow_html=True)

# --- 3. GESTÃO DE ACERVO DINÂMICO ---
@st.cache_data
def get_acervo():
    pasta = "base"
    if not os.path.exists(pasta): return {}
    arquivos = [f for f in os.listdir(pasta) if f.startswith("rol_") and f.endswith(".txt")]
    return {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in arquivos}

def load_md(name):
    # Padrão: ABOUT_PAGINA.md
    path = os.path.join("md_files", f"ABOUT_{name.strip().upper()}.md")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f: return f.read()
    return f"*Arquivo {path} não localizado.*"

# --- 4. ESTADO ---
if 'page' not in st.session_state: st.session_state.page = 'DEMO'
if 'show_help' not in st.session_state: st.session_state.show_help = False

ACERVO = get_acervo()
IDIOMAS = ["Português", "Español", "English", "Français", "Italiano", "Català", "Deutsch", "Русский", "中文", "日本語"]

# --- 5. ARQUITETURA ---
c_painel, c_vazio, c_palco = st.columns([2, 0.1, 7.9])

with c_painel:
    st.write("### controles")
    i1, i2, i3 = st.columns(3)
    i1.button("🔈", key="s_on")
    i2.button("🎨", key="a_on")
    i3.button("💬", key="t_on")
    st.divider()
    livro = st.selectbox("livros", list(ACERVO.keys()) if ACERVO else ["Vazio"])
    st.selectbox("idioma", IDIOMAS)

with c_palco:
    # REBALANCEAMENTO DAS LARGURAS (PESOS AJUSTADOS)
    # off-mach recebeu mais espaço (0.8), outros foram levemente reduzidos
    pesos = [0.8, 0.9, 0.8, 1.2, 1.0, 0.8] 
    paginas = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    
    # LINHA 1: TEXTO
    cols_t = st.columns(pesos)
    for i, item in enumerate(paginas):
        with cols_t[i]:
            if st.button(item.lower() if item != "yPoemas" else "yPoemas", key=f"p_{i}", use_container_width=True):
                st.session_state.page, st.session_state.show_help = item, False
                st.rerun()

    # LINHA 2: STARS
    cols_s = st.columns(pesos)
    for i, item in enumerate(paginas):
        with cols_s[i]:
            st.markdown('<div class="bottom-star">', unsafe_allow_html=True)
            if st.button("★", key=f"h_{i}", use_container_width=True):
                st.session_state.page, st.session_state.show_help = item, True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    
    # --- 6. RENDERIZAÇÃO ---
    p, h = st.session_state.page, st.session_state.show_help
    st.markdown('<div class="md-render">', unsafe_allow_html=True)
    
    if h:
        # Modo Help: Renderiza o ABOUT_ correspondente
        st.info(f"MODO HELP: {p}")
        st.markdown(load_md(p if p != "opinião" else "COMMENTS"))
    else:
        # Modo Página: Conteúdo funcional
        if p == "opinião": st.markdown(load_md("COMMENTS"))
        elif p == "sobre": st.markdown(load_md("SOBRE"))
        else:
            st.subheader(f"Página {p}")
            st.write("Engrenagem ativa. Conteúdo principal aqui.")
    st.markdown('</div>', unsafe_allow_html=True)
