import streamlit as st
import os

# --- 1. SETUP ---
st.set_page_config(page_title="a máquina de fazer Poesia", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS DE PRECISÃO ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding-top: 1rem !important;}
    div[data-testid="stHorizontalBlock"] { align-items: center !important; }
    
    /* Botões de Navegação (Texto) */
    .stButton button { 
        height: 35px !important; 
        margin: 0px !important; 
        color: #31333F !important; 
    }
    
    /* Side-Button (Estrela Amarela) */
    .side-star button { 
        height: 35px !important; 
        color: #FFD700 !important; 
        background-color: transparent !important; 
        border: none !important; 
        font-size: 20px !important; 
    }
    
    div[data-testid="column"] { padding: 0 1px !important; }
    .md-render { font-family: 'Georgia', serif; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS REAIS ---
IDIOMAS_MAQUINA = [
    "Português", "Español", "English", "Français", "Italiano", "Català", 
    "Română", "Galego", "Latin", "Ladin", "Occitan", "Sardu",
    "Deutsch", "Nederlands", "Русский", "Polski", "Ελληνικά", "Türkçe",
    "العربية", "עברית", "हिन्दी", "日本語", "中文", "한국어"
]

# --- 4. ENGINE DE CARREGAMENTO (NOME UPPER + EXTENSÃO lower) ---
def load_content(filename):
    clean_name = filename.strip().upper()
    # Retorno ao padrão solicitado: CAPITAL_NAME.md
    caminho = os.path.join("md_files", f"{clean_name}.md")
    
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    return f"Erro: {caminho} não encontrado."

# --- 5. ESTADO ---
if 'page' not in st.session_state: st.session_state.page = 'DEMO'
if 'show_help' not in st.session_state: st.session_state.show_help = False

# --- 6. ARQUITETURA ---
c_painel, c_vazio, c_palco = st.columns([2, 0.1, 7.9])

with c_painel:
    st.write("### controles")
    i1, i2, i3 = st.columns(3)
    i1.button("🔈", key="btn_som", use_container_width=True)
    i2.button("🎨", key="btn_arts", use_container_width=True)
    i3.button("💬", key="btn_talk", use_container_width=True)
    st.divider()
    st.selectbox("livros", ["Lista em breve..."], key="sel_livro")
    st.selectbox("idioma", IDIOMAS_MAQUINA, key="sel_lang")

with c_palco:
    # Régua com pesos decimais do usuário
    pesos_user = [0.94, 0.1, 0.56, 0.1, 0.60, 0.1, 0.4, 0.1, 0.55, 0.1, 0.75, 0.1]
    regua = st.columns(pesos_user)
    paginas = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    
    for i, item in enumerate(paginas):
        col_btn, col_star = i * 2, (i * 2) + 1
        with regua[col_btn]:
            lbl = "yPoemas" if item == "yPoemas" else item.lower()
            if st.button(lbl, key=f"p_{i}", use_container_width=True):
                st.session_state.page, st.session_state.show_help = item, False
                st.rerun()
        with regua[col_star]:
            st.markdown('<div class="side-star">', unsafe_allow_html=True)
            if st.button("★", key=f"h_{i}", use_container_width=True):
                st.session_state.page, st.session_state.show_help = item, True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    
    # RENDERIZAÇÃO
    p, h = st.session_state.page, st.session_state.show_help
    st.markdown('<div class="md-render">', unsafe_allow_html=True)
    if h:
        st.markdown(load_content(f"ABOUT_{p}"))
    else:
        if p == "opinião": st.markdown(load_content("COMMENTS"))
        elif p == "sobre": st.markdown(load_content("SOBRE"))
        else: st.write(f"### {p.lower()}")
    st.markdown('</div>', unsafe_allow_html=True)
