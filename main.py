import streamlit as st
import os

# --- 1. CONFIGURAÇÃO SOBERANA ---
st.set_page_config(page_title="yPoemas - a Máquina", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS: O PARADIGMA DA SIMPLICIDADE ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding-top: 1rem !important;}
    div[data-testid="stHorizontalBlock"] { align-items: center !important; gap: 0px !important; }

    /* Estilo dos Botões de Navegação */
    .stButton button {
        height: 35px !important;
        margin: 0px !important;
        padding: 0px 5px !important;
        color: #31333F !important;
        border-radius: 4px !important;
    }

    /* O Paradigma: Estrela Amarela Bottom */
    .bottom-star button {
        height: 25px !important;
        color: #FFD700 !important; 
        background-color: transparent !important;
        border: none !important;
        font-size: 18px !important;
        margin-top: -8px !important;
    }
    .bottom-star button:hover { color: #FFEA00 !important; }

    div[data-testid="column"] { padding: 0 1px !important; }
    .md-render { font-family: 'Georgia', serif; line-height: 1.6; margin-top: 20px; }
</style>
""", unsafe_allow_html=True)

# --- 3. GESTÃO DE ACERVO DINÂMICO (PASTA \BASE) ---
@st.cache_data
def get_livros_reais():
    pasta_base = "base"
    if not os.path.exists(pasta_base):
        return ["Erro: pasta 'base' não encontrada"]
    
    # Lista arquivos rol_*.txt e extrai o nome do livro
    arquivos = [f for f in os.listdir(pasta_base) if f.startswith("rol_") and f.endswith(".txt")]
    livros = {f.replace("rol_", "").replace(".txt", "").replace("_", " ").title(): f for f in arquivos}
    return livros

def get_temas_do_livro(arquivo_nome):
    caminho = os.path.join("base", arquivo_nome)
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return [linha.strip() for linha in f.readlines() if linha.strip()]
    return ["Erro ao carregar temas"]

# --- 4. ENGINE DE CARREGAMENTO MD ---
def load_md(name):
    clean_name = name.strip().upper()
    caminho = os.path.join("md_files", f"ABOUT_{clean_name}.md")
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    return f"Erro: {caminho} não encontrado."

# --- 5. ESTADO E DADOS ---
if 'page' not in st.session_state: st.session_state.page = 'DEMO'
if 'show_help' not in st.session_state: st.session_state.show_help = False

DIT_LIVROS = get_livros_reais()
IDIOMAS = ["Português", "Español", "English", "Français", "Italiano", "Català", "Română", "Galego", "Latin", "Ladin", "Occitan", "Sardu", "Deutsch", "Nederlands", "Русский", "Polski", "Ελληνικά", "Türkçe", "العربية", "ע Hebrew", "हिन्दी", "日本語", "中文", "한국어"]

# --- 6. ARQUITETURA (PAINEL 2 | PALCO 8) ---
c_painel, c_vazio, c_palco = st.columns([2, 0.1, 7.9])

with c_painel:
    st.write("### controles")
    i1, i2, i3 = st.columns(3)
    i1.button("🔈", key="s_on", use_container_width=True)
    i2.button("🎨", key="a_on", use_container_width=True)
    i3.button("💬", key="t_on", use_container_width=True)
    st.divider()
    
    # Seletores Populados Realmente
    livro_selecionado = st.selectbox("livros", list(DIT_LIVROS.keys()), key="sel_b")
    temas = get_temas_do_livro(DIT_LIVROS[livro_selecionado])
    st.selectbox("temas", temas, key="sel_t")
    st.selectbox("idioma", IDIOMAS, key="sel_l")

with c_palco:
    # --- RÉGUA DUPLA: TEXTO (TOP) E ESTRELA (BOTTOM) ---
    pesos = [0.94, 0.56, 0.60, 0.4, 0.55, 0.75]
    paginas = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    
    # Linha 1: Texto
    regua_t = st.columns(pesos)
    for i, item in enumerate(paginas):
        with regua_t[i]:
            lbl = "yPoemas" if item == "yPoemas" else item.lower()
            if st.button(lbl, key=f"p_{i}", use_container_width=True):
                st.session_state.page, st.session_state.show_help = item, False
                st.rerun()

    # Linha 2: Estrela (Bottom-Star)
    regua_s = st.columns(pesos)
    for i, item in enumerate(paginas):
        with regua_s[i]:
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
        file_name = "COMMENTS" if p == "opinião" else p
        st.markdown(load_md(file_name))
    else:
        st.write(f"### {p.lower()}")
    st.markdown('</div>', unsafe_allow_html=True)
