import os
import random
import streamlit as st
from gtts import gTTS

# --- 1. ARQUITETURA VISUAL E CSS (RIGOR 300px) ---
st.set_page_config(
    page_title='a Máquina de Fazer Poesia',
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    /* Fixa a Sidebar em 300px conforme o Guia */
    [data-testid="stSidebar"] { width: 300px !important; }
    
    /* Estética Cockpit: Botões e Fontes */
    .stButton>button { width: 100%; border-radius: 2px; height: 3.5em; font-weight: 600; }
    .logo-text { font-family: 'IBM Plex Sans'; font-size: 22px; font-weight: 700; text-align: center; padding-bottom: 20px; }
    
    /* Ajuste de Padding para o Palco */
    .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True
)

# --- 2. ENGENHARIA DE ESTADO (PERSISTÊNCIA PTC) ---
def init_session_state():
    """Garante a integridade das variáveis de controle conforme o Guia"""
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

# --- 3. FERRAMENTAS DE CARGA (MD & ROL) ---
@st.cache_data
def load_md(file_name):
    """Lê documentos respeitando o encerramento <eof>"""
    try:
        path = os.path.join("./md_files/", file_name)
        with open(path, encoding="utf-8") as f:
            content = f.read()
            return content.split("<eof>")[0] if "<eof>" in content else content
    except: return "⚠️ Erro na carga da documentação."

# --- 4. CENTRO DE CONTROLE (SIDEBAR EXCLUSIVA) ---
def cockpit_control():
    with st.sidebar:
        st.markdown('<p class="logo-text">MACHINA 2026</p>', unsafe_allow_html=True)
        
        # NAVEGAÇÃO PRINCIPAL (Botões de Ação Direta)
        if st.button("🎭 yPoemas"): st.session_state.page = "yPoemas"
        if st.button("🔍 eureka"): st.session_state.page = "eureka"
        if st.button("📚 livros"): st.session_state.page = "livros"
        if st.button("🌐 poly"): st.session_state.page = "poly"
        if st.button("💬 opiniões"): st.session_state.page = "opiniões"
        if st.button("📖 Sobre"): st.session_state.page = "Sobre"
        
        st.markdown("---")
        
        # IDIOMAS (Filtro Ocidental Oficial)
        langs = ["pt", "es", "it", "fr", "en", "ca"]
        st.session_state.lang = st.selectbox("Linguagem", langs)
        
        st.markdown("---")
        st.write("🌌 Estética Ativa")

# --- 5. O PALCO (ÁREA DE EXIBIÇÃO) ---
def stage_render():
    # TOPO DA TELA: Botões Global [Talk] e [Arts]
    col_t, col_a = st.columns(2)
    with col_t:
        label_t = "🗣️ Talk [ON]" if st.session_state.talk else "🗣️ Talk"
        if st.button(label_t): st.session_state.talk = not st.session_state.talk
    with col_a:
        label_a = "🎨 Arts [ON]" if st.session_state.arts else "🎨 Arts"
        if st.button(label_a): st.session_state.arts = not st.session_state.arts

    st.divider()
    
    pg = st.session_state.page

    # Implementação das Páginas conforme o Palco
    if pg == "yPoemas":
        c1, c2, c3, c4 = st.columns([1,1,1,1])
        with c1: st.button("<-")
        with c2: st.button("⭐")
        with c3: st.button("->")
        with c4: 
            if st.button("?"): st.info(load_md("help_ypoemas.md"))
        st.write("### [Processamento Poético Ativo]")

    elif pg == "eureka":
        c_in, c_p, c_s, c_h = st.columns([4,1,1,1])
        with c_in: st.session_state.find_what = st.text_input("find_what", label_visibility="collapsed")
        with c_p: st.button("+")
        with c_s: st.button("⭐")
        with c_h:
            if st.button("?"): st.info(load_md("help_eureka.md"))

    elif pg == "Sobre":
        try:
            files = [f for f in os.listdir("./md_files/") if f.startswith("ABOUT_")]
            names = [f.replace("ABOUT_", "").replace(".md", "") for f in files]
            choice = st.selectbox("Selecione o Capítulo", names)
            if choice:
                st.markdown(load_md(f"ABOUT_{choice}.md"), unsafe_allow_html=True)
        except: st.error("Erro no diretório md_files.")

# --- EXECUÇÃO FINAL ---
cockpit_control()
stage_render()
