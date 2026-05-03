import os
import random
import streamlit as st
from gtts import gTTS

# --- 1. ARQUITETURA VISUAL (300px & Cockpit) ---
st.set_page_config(
    page_title='a Máquina de Fazer Poesia',
    layout="centered",
    initial_sidebar_state="expanded"
)

# CSS Rígido: Sidebar 300px e Estética de Cockpit
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] { width: 300px !important; }
    .stButton>button { width: 100%; border-radius: 2px; height: 3.5em; font-weight: 600; }
    .logo-text { font-family: 'IBM Plex Sans'; font-size: 22px; font-weight: 700; text-align: center; padding-bottom: 20px; }
    div[data-testid="stVerticalBlock"] > div:has(div.stButton) { padding: 2px; }
    </style>
    """, unsafe_allow_html=True
)

# --- 2. ENGENHARIA DE ESTADO ---
def init_session_state():
    if "page" not in st.session_state: st.session_state.page = "yPoemas"
    if "lang" not in st.session_state: st.session_state.lang = "pt"
    if "talk" not in st.session_state: st.session_state.talk = False
    if "arts" not in st.session_state: st.session_state.arts = False
    if "book" not in st.session_state: st.session_state.book = "livro vivo"
    if "take_tema" not in st.session_state: st.session_state.take_tema = 0

init_session_state()

# --- 3. FERRAMENTAS CORE (MD & TEMAS) ---
@st.cache_data
def load_md(file_name):
    try:
        path = os.path.join("./md_files/", file_name)
        with open(path, encoding="utf-8") as f:
            content = f.read()
            return content.split("<eof>")[0] if "<eof>" in content else content
    except: return "⚠️ Erro de leitura."

# --- 4. CENTRO DE CONTROLE (SIDEBAR) ---
with st.sidebar:
    st.markdown('<p class="logo-text">MACHINA 2026</p>', unsafe_allow_html=True)
    
    # NAVEGAÇÃO POR BOTÕES (Sem menus dropdown/preguiça)
    if st.button("🎭 yPoemas"): st.session_state.page = "yPoemas"
    if st.button("🔍 eureka"): st.session_state.page = "eureka"
    if st.button("📚 livros"): st.session_state.page = "livros"
    if st.button("🌐 poly"): st.session_state.page = "poly"
    if st.button("💬 opiniões"): st.session_state.page = "opiniões"
    if st.button("📖 Sobre"): st.session_state.page = "Sobre"
    
    st.markdown("---")
    
    # IDIOMAS OCIDENTAIS
    langs = ["pt", "es", "it", "fr", "en", "ca"]
    st.session_state.lang = st.selectbox("Linguagem", langs)
    
    # ESPAÇO PARA MANDALA
    st.write("") 

# --- 5. O PALCO (PÁGINAS) ---

# TOPO: Botões Talk e Arts (Substituem o Vídeo)
col_talk, col_arts = st.columns(2)
with col_talk:
    if st.button("🗣️ Talk"): st.session_state.talk = not st.session_state.talk
with col_arts:
    if st.button("🎨 Arts"): st.session_state.arts = not st.session_state.arts

st.divider()

pg = st.session_state.page

if pg == "yPoemas":
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.button("<-")
    with c2: st.button("⭐")
    with c3: st.button("->")
    with c4: 
        if st.button("?"): st.info(load_md("help_ypoemas.md"))
    st.write("### [Área de Versos]")

elif pg == "eureka":
    col_in, col_btn = st.columns([3, 1])
    with col_in: st.text_input("find_what", label_visibility="collapsed")
    with col_btn:
        if st.button("?"): st.info(load_md("help_eureka.md"))
    # Outros componentes conforme o Guia...

elif pg == "livros":
    c1, c2, c3, c4, c5 = st.columns(5)
    with c4: st.button("❤️", help="temas mais lidos")
    with c5:
        if st.button("?"): st.info(load_md("help_off-machina.md"))

elif pg == "Sobre":
    # Dropdown dinâmico para os arquivos ABOUT_*.md
    try:
        files = [f for f in os.listdir("./md_files/") if f.startswith("ABOUT_")]
        options = [f.replace("ABOUT_", "").replace(".md", "") for f in files]
        choice = st.selectbox("Capítulo", options)
        if choice:
            st.markdown(load_md(f"ABOUT_{choice}.md"), unsafe_allow_html=True)
    except: st.error("Erro na pasta md_files.")

# ... Outras páginas conforme a Guia de Arquitetura.
