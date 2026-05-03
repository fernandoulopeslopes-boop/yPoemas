import os
import random
import streamlit as st
from gtts import gTTS

# --- 1. CONFIGURAÇÃO DE AMBIENTE E ESTILO (300px) ---
st.set_page_config(
    page_title='a Máquina de Fazer Poesia',
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] { width: 300px !important; }
    .stButton>button { width: 100%; border-radius: 4px; height: 3em; }
    .logo-text { font-family: 'IBM Plex Sans'; font-size: 20px; font-weight: 700; text-align: center; }
    /* Ajuste para botões lado a lado no topo */
    div[data-testid="column"] { padding: 0px; }
    </style>
    """, unsafe_allow_html=True
)

# --- 2. ENGENHARIA DE ESTADO (PTC) ---
def init_session_state():
    defaults = {
        "page": "yPoemas",
        "lang": "pt",
        "book": "livro vivo",
        "take_tema": 0,
        "talk": False,
        "arts": False,
        "find_what": ""
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# --- 3. LOADERS E FILTROS OCIDENTAIS ---
@st.cache_data
def load_md(file_name):
    try:
        path = os.path.join("./md_files/", file_name)
        with open(path, encoding="utf-8") as f:
            content = f.read()
            return content.split("<eof>")[0] if "<eof>" in content else content
    except:
        return "⚠️ Documento de ajuda não encontrado."

@st.cache_data
def load_temas(book):
    try:
        path = os.path.join("./base/", f"{book}.rol")
        with open(path, encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return ["erro_na_base"]

# --- 4. CENTRO DE CONTROLE (SIDEBAR) ---
def sidebar_cockpit():
    with st.sidebar:
        st.markdown('<p class="logo-text">a Máquina de Fazer Poesia</p>', unsafe_allow_html=True)
        
        # TOPO DA TELA: Botões Talk e Arts (Substituem o vídeo)
        col_t, col_a = st.columns(2)
        with col_t:
            if st.button("🗣️ Talk"): st.session_state.talk = not st.session_state.talk
        with col_a:
            if st.button("🎨 Arts"): st.session_state.arts = not st.session_state.arts
        
        st.markdown("---")
        
        # NAVEGAÇÃO PRINCIPAL
        if st.button("🎭 yPoemas"): st.session_state.page = "yPoemas"
        if st.button("🔍 eureka"): st.session_state.page = "eureka"
        if st.button("📚 livros"): st.session_state.page = "livros"
        if st.button("🌐 poly"): st.session_state.page = "poly"
        if st.button("💬 opiniões"): st.session_state.page = "opiniões"
        if st.button("📖 Sobre"): st.session_state.page = "Sobre"
        
        st.markdown("---")
        
        # IDIOMAS: Sequência oficial ocidental
        langs_oficiais = ["pt", "es", "it", "fr", "en", "ca"]
        st.session_state.lang = st.selectbox("Idioma (Western Only)", langs_oficiais)
        
        # MANDALA ARTÍSTICA (Placeholder visual conforme Guia)
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Mandala_66.svg/200px-Mandala_66.svg.png", width=120)

# --- 5. O PALCO (PÁGINAS) ---
def render_page():
    pg = st.session_state.page
    
    # 1. yPoemas
    if pg == "yPoemas":
        col1, col2, col3, col4 = st.columns([1,1,1,1])
        with col1: st.button("<-")
        with col2: st.button("⭐")
        with col3: st.button("->")
        with col4: 
            if st.button("?"): st.info(load_md("help_ypoemas.md"))
        st.divider()
        st.write("Aqui a Machina exibe seus versos...")

    # 2. eureka
    elif pg == "eureka":
        col_in, col_p, col_s, col_h = st.columns([4,1,1,1])
        with col_in: st.session_state.find_what = st.text_input("Localizar no léxico:", value=st.session_state.find_what)
        with col_p: st.button("+")
        with col_s: st.button("⭐")
        with col_h:
            if st.button("?"): st.info(load_md("help_eureka.md"))

    # 3. livros
    elif pg == "livros":
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1: st.button("<-")
        with col2: st.button("⭐")
        with col3: st.button("->")
        with col4: st.button("❤️", help="temas mais lidos")
        with col5:
            if st.button("?"): st.info(load_md("help_off-machina.md"))

    # 4. poly
    elif pg == "poly":
        col1, col2 = st.columns([1,1])
        with col1: st.button("❤️", help="temas mais lidos")
        with col2:
            if st.button("?"): st.info(load_md("help_poly.md"))

    # 5. opiniões
    elif pg == "opiniões":
        if st.button("?", key="help_op"): st.info(load_md("help_comments.md"))
        st.subheader("Mural de Depoimentos")
        st.write("Espaço reservado a amigos e escritores.")

    # 6. Sobre
    elif pg == "Sobre":
        # Dropdown dinâmico baseado em arquivos ABOUT_*.md
        try:
            files = [f for f in os.listdir("./md_files/") if f.startswith("ABOUT_") and f.endswith(".md")]
            clean_names = [f.replace("ABOUT_", "").replace(".md", "") for f in files]
            
            choice = st.selectbox("Documentação Dinâmica", clean_names)
            if choice:
                st.markdown(load_md(f"ABOUT_{choice}.md"), unsafe_allow_html=True)
        except:
            st.error("Pasta /md_files não acessível.")

# --- EXECUÇÃO ---
sidebar_cockpit()
render_page()
