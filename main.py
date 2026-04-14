import streamlit as st
import os

# --- 1. CONFIGURAÇÃO SOBERANA (PLANO B) ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS DE LIMPEZA E PRECISÃO ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding-top: 1rem !important; padding-left: 1rem !important; padding-right: 1rem !important;}
    
    /* Botões da Régua Superior */
    .stButton>button {
        border-radius: 5px 0px 0px 5px !important;
        height: 38px !important;
        font-family: 'Georgia', serif !important;
    }
    
    /* Estilo do Side-Button (Estrela) */
    .side-btn button {
        border-radius: 0px 5px 5px 0px !important;
        background-color: #f8f9fa !important;
        border-left: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. INICIALIZAÇÃO DO ESTADO ---
if 'page' not in st.session_state:
    st.session_state.page = 'demo'
if 'show_help' not in st.session_state:
    st.session_state.show_help = False

# --- 4. FUNÇÃO DE RESGATE (MD) ---
def load_content(page_name, is_help):
    if is_help:
        path = os.path.join("md_files", f"ABOUT_{page_name.upper()}.MD")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return f"### Manual de {page_name} em breve..."
    return None

# --- 5. LAYOUT: TORRE (2) | PALCO (8) ---
col_ctrl, col_stage = st.columns([2, 8])

# --- 6. TORRE DE CONTROLE (IMEXÍVEL) ---
with col_ctrl:
    st.markdown("### ⚙️ cockpit")
    
    # Interruptores (Som, Arte, Vídeo)
    i1, i2, i3 = st.columns(3)
    with i1: st.button("🔈", key="t_sound")
    with i2: st.button("🎨", key="t_art")
    with i3: st.button("🎬", key="t_video")
    
    st.divider()
    
    # Drop-down Lists
    st.selectbox("biblioteca", ["livro alpha", "livro beta", "livro gamma"], key="sel_book")
    st.selectbox("temas", ["tema 1", "tema 2", "tema 3"], key="sel_theme")
    
    st.divider()
    
    # Idiomas Plenos
    langs = ["português", "español", "english", "français", "italiano", "català", "ελληνικά"]
    st.selectbox("idioma", langs, key="sel_lang")
    
    st.divider()
    if st.button("🎲 RANDOM"):
        pass # Futura lógica de sorteio de index

# --- 7. PALCO CENTRAL SOBERANO ---
with col_stage:
    # A RÉGUA DE COMANDO DUPLO
    menu = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    m_cols = st.columns(len(menu))
    
    for i, item in enumerate(menu):
        with m_cols[i]:
            sub1, sub2 = st.columns([3, 1])
            with sub1:
                # Botão Principal da Página
                if st.button(item if item != "yPoemas" else "yPoemas", key=f"btn_{i}"):
                    st.session_state.page = item
                    st.session_state.show_help = False
                    st.rerun()
            with sub2:
                # Side-Button (Estrela)
                st.markdown("<div class='side-btn'>", unsafe_allow_html=True)
                if st.button("⭐", key=f"star_{i}"): # Placeholder para Star_yes.ico
                    st.session_state.page = item
                    st.session_state.show_help = True
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # ÁREA DE RENDERIZAÇÃO (O PALCO)
    p = st.session_state.page
    h = st.session_state.show_help
    
    if h:
        st.markdown(load_content(p, True))
    else:
        # Aqui o esqueleto aguarda as chamadas das suas rotinas
        st.markdown(f"<h1 style='text-align: center; font-weight: 200;'>{p.lower()}</h1>", unsafe_allow_html=True)
        st.info(f"O palco está pronto para a rotina da página: {p}")
