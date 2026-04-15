import streamlit as st
import os

# --- 1. CONFIGURAÇÃO SOBERANA ---
st.set_page_config(
    page_title="a máquina de fazer Poesia", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. CSS DE PRECISÃO (PARADIGMA BOTTOM-STAR) ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding-top: 1rem !important;}
    
    /* Alinhamento das linhas da régua */
    div[data-testid="stHorizontalBlock"] { 
        align-items: center !important; 
        gap: 0px !important;
    }

    /* Botão de Página (Linha Superior) */
    .stButton button {
        height: 35px !important;
        margin: 0px !important;
        padding: 0px 5px !important;
        line-height: 1 !important;
        color: #31333F !important;
        border-radius: 4px !important;
    }

    /* Estrela Amarela (Linha Inferior) */
    .bottom-star button {
        height: 25px !important;
        color: #FFD700 !important; 
        background-color: transparent !important;
        border: none !important;
        font-size: 18px !important;
        margin-top: -5px !important; /* Aproxima da linha de texto */
    }
    
    .bottom-star button:hover { color: #FFEA00 !important; }

    div[data-testid="column"] { padding: 0 1px !important; }
    .md-render { font-family: 'Georgia', serif; line-height: 1.6; margin-top: 20px; }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS RÍGIDOS DA MACHINA ---
LIVROS_MACHINA = ["Livro de Amaré", "Anjos de Vidro", "O Tempo e a Máquina", "A Outra Margem", "Labirintos", "Eros", "Cosmos"]
TEMAS_MACHINA = ["Amaré", "Anjos", "Tempo", "A Outra Margem", "Labirintos", "Eros", "Cosmos"]
IDIOMAS_MAQUINA = [
    "Português", "Español", "English", "Français", "Italiano", "Català", 
    "Română", "Galego", "Latin", "Ladin", "Occitan", "Sardu",
    "Deutsch", "Nederlands", "Русский", "Polski", "Ελληνικά", "Türkçe",
    "العربية", "עברית", "हिन्दी", "日本語", "中文", "한국어"
]

# --- 4. ENGINE DE CARREGAMENTO (ABOUT_ + NOME.md) ---
def load_md(name):
    clean_name = name.strip().upper()
    caminho = os.path.join("md_files", f"ABOUT_{clean_name}.md")
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    return f"Erro: {caminho} não encontrado."

# --- 5. ESTADO GLOBAL ---
if 'page' not in st.session_state: st.session_state.page = 'DEMO'
if 'show_help' not in st.session_state: st.session_state.show_help = False

# --- 6. ARQUITETURA (PAINEL 2 | PALCO 8) ---
c_painel, c_vazio, c_palco = st.columns([2, 0.1, 7.9])

with c_painel:
    st.write("### controles")
    i1, i2, i3 = st.columns(3)
    i1.button("🔈", key="s_on", use_container_width=True)
    i2.button("🎨", key="a_on", use_container_width=True)
    i3.button("💬", key="t_on", use_container_width=True)
    st.divider()
    st.selectbox("livros", LIVROS_MACHINA, key="sel_b")
    st.selectbox("temas", TEMAS_MACHINA, key="sel_t")
    st.selectbox("idioma", IDIOMAS_MAQUINA, key="sel_l")

with c_palco:
    # --- LINHA 1: PÁGINAS (TEXTO) ---
    pesos_paginas = [0.94, 0.56, 0.60, 0.4, 0.55, 0.75]
    regua_texto = st.columns(pesos_paginas)
    paginas = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    
    for i, item in enumerate(paginas):
        with regua_texto[i]:
            lbl = "yPoemas" if item == "yPoemas" else item.lower()
            if st.button(lbl, key=f"p_{i}", use_container_width=True):
                st.session_state.page, st.session_state.show_help = item, False
                st.rerun()

    # --- LINHA 2: SIDE-BUTTONS (ESTRELAS AO FUNDO) ---
    # Usamos os mesmos pesos para garantir o alinhamento vertical perfeito
    regua_stars = st.columns(pesos_paginas)
    for i, item in enumerate(paginas):
        with regua_stars[i]:
            st.markdown('<div class="bottom-star">', unsafe_allow_html=True)
            if st.button("★", key=f"h_{i}", use_container_width=True):
                st.session_state.page, st.session_state.show_help = item, True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    
    # --- 7. RENDERIZAÇÃO ---
    p, h = st.session_state.page, st.session_state.show_help
    st.markdown('<div class="md-render">', unsafe_allow_html=True)
    
    if h or p in ["opinião", "sobre"]:
        file_to_load = "COMMENTS" if p == "opinião" else p
        st.markdown(load_md(file_to_load))
    else:
        st.write(f"### {p.lower()}")
    st.markdown('</div>', unsafe_allow_html=True)
