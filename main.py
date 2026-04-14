import streamlit as st
import os

# --- 1. CONFIGURAÇÃO SOBERANA ---
st.set_page_config(
    page_title="a máquina de fazer Poesia", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. CSS DE PRECISÃO (FIM DA MONTANHA RUSSA E CORES ISOLADAS) ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding-top: 1rem !important;}
    
    /* Alinhamento vertical da régua */
    div[data-testid="stHorizontalBlock"] { align-items: center !important; }

    /* Botão de Página (Texto) - Cor Padrão Estrita */
    .stButton button {
        height: 35px !important;
        margin: 0px !important;
        padding: 0px 5px !important;
        line-height: 1 !important;
        color: #31333F !important;
    }

    /* Estrela Amarela (Side Button) - CSS Isolado por Classe */
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

# --- 3. IDIOMAS DA MÁQUINA (LISTA COMPLETA REESTABELECIDA) ---
IDIOMAS_MAQUINA = [
    "Português", "Español", "English", "Français", "Italiano", "Català", 
    "Română", "Galego", "Latin", "Ladin", "Occitan", "Sardu",
    "Deutsch", "Nederlands", "Русский", "Polski", "Ελληνικά", "Türkçe",
    "العربية", "עברית", "हिन्दी", "日本語", "中文", "한국어"
]

# --- 4. ENGINE DE CARREGAMENTO (DIRETÓRIO \MD_FILES + CAPITAL_LETTERS.MD) ---
def load_content(filename):
    # Força CAPITAL_LETTERS.MD conforme especificado
    clean_name = filename.strip().upper()
    caminho = os.path.join("md_files", f"{clean_name}.md")
    
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    return f"Erro: {caminho} não encontrado."

# --- 5. ESTADO GLOBAL ---
if 'page' not in st.session_state: st.session_state.page = 'DEMO'
if 'show_help' not in st.session_state: st.session_state.show_help = False

# --- 6. ARQUITETURA ---
c_painel, c_vazio, c_palco = st.columns([2, 0.1, 7.9])

# --- 7. PAINEL DE CONTROLE (SEM RANDOM / SEM FORMULA 1) ---
with c_painel:
    st.write("### controles")
    
    # Interruptores (Som, Arts, Talk)
    i1, i2, i3 = st.columns(3)
    i1.button("🔈", key="btn_som", use_container_width=True)
    i2.button("🎨", key="btn_arts", use_container_width=True)
    i3.button("💬", key="btn_talk", use_container_width=True)
    
    st.divider()
    
    # Seletor de Idioma Completo
    st.selectbox("livros", ["Lista em breve..."], key="sel_livro")
    st.selectbox("idioma", IDIOMAS_MAQUINA, key="sel_lang")

# --- 8. PALCO E RÉGUA (PESOS DECIMAIS E ESTRELAS AMARELAS) ---
with c_palco:
    pesos_user = [0.94, 0.1, 0.56, 0.1, 0.60, 0.1, 0.4, 0.1, 0.55, 0.1, 0.75, 0.1]
    regua = st.columns(pesos_user)
    
    paginas = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    
    for i, item in enumerate(paginas):
        col_btn = i * 2
        col_star = col_btn + 1
        
        # Botão de Navegação (Texto)
        with regua[col_btn]:
            label = "yPoemas" if item == "yPoemas" else item.lower()
            if st.button(label, key=f"p_{i}", use_container_width=True):
                st.session_state.page = item
                st.session_state.show_help = False
                st.rerun()
        
        # Side-Button (Estrela Amarela ★)
        with regua[col_star]:
            st.markdown('<div class="side-star">', unsafe_allow_html=True)
            if st.button("★", key=f"h_{i}", use_container_width=True):
                st.session_state.page = item
                st.session_state.show_help = True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # --- 9. RENDERIZAÇÃO FINAL (TRATAMENTO DE ARQUIVOS) ---
    p, h = st.session_state.page, st.session_state.show_help
    
    st.markdown('<div class="md-render">', unsafe_allow_html=True)
    if h:
        # Busca: md_files/ABOUT_DEMO.MD, ABOUT_YPOEMAS.MD, etc.
        st.markdown(load_content(f"ABOUT_{p}"))
    else:
        # Busca páginas específicas na pasta \md_files
        if p == "opinião":
            st.markdown(load_content("COMMENTS"))
        elif p == "sobre":
            st.markdown(load_content("SOBRE"))
        else:
            st.write(f"### {p.lower()}")
    st.markdown('</div>', unsafe_allow_html=True)
