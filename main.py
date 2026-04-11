import streamlit as st
import os

# --- MOTOR LÉXICO (Importando do seu lay_2_ypo.py) ---
try:
    from lay_2_ypo import gera_poema, translate, talk, have_internet
except ImportError:
    st.error("Erro: Arquivo 'lay_2_ypo.py' não encontrado na mesma pasta.")

# =================================================================
# 🛠️ CONFIGURAÇÕES PRO & CACHE (Timeline 2026)
# =================================================================

st.set_page_config(
    page_title="a Máquina de Fazer Poesia",
    page_icon="ツ",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Cache moderno: substitui o antigo @st.cache
@st.cache_data(show_spinner=False)
def load_md_file(file_name):
    try:
        path = os.path.join("./base", file_name)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
    except:
        return ""
    return ""

# Estilização para manter a identidade visual
st.markdown("""
    <style>
    [data-testid="stSidebar"] { width: 310px; }
    .main .block-container { padding-top: 1rem; }
    div.stButton > button { width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# =================================================================
# 🧭 NAVEGAÇÃO NATIVA (Plano B / Sem pkg_resources)
# =================================================================

def main():
    if 'lang' not in st.session_state: st.session_state.lang = "pt"
    
    st.sidebar.title("ツ Machina")
    
    # Menu robusto e imune a erros de instalação
    menu = {
        "1": "Mini",
        "2": "yPoemas",
        "3": "Eureka",
        "4": "Off-Machina",
        "5": "Books",
        "6": "Poly",
        "7": "About"
    }
    
    # O st.sidebar.radio que substitui o stx.TabBar
    chosen_id = st.sidebar.radio(
        "Navegação", 
        options=list(menu.keys()), 
        format_func=lambda x: menu[x].upper(),
        index=1
    )

    # --- BOTÕES DE AÇÃO NA SIDEBAR ---
    st.sidebar.markdown("---")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Talk"):
            st.session_state.talk = True
    with col2:
        if st.button("Arte"):
            st.session_state.draw = True

    # --- LÓGICA DE EXIBIÇÃO DE INFO ---
    info_map = {
        "1": "INFO_MINI.md", "2": "INFO_YPOEMAS.md", "3": "INFO_EUREKA.md",
        "4": "INFO_OFF-MACHINA.md", "5": "INFO_BOOKS.md", "6": "INFO_POLY.md",
        "7": "INFO_ABOUT.md"
    }
    
    info_content = load_md_file(info_map.get(chosen_id, ""))
    if info_content:
        st.sidebar.info(info_content)

    # --- RENDERIZAÇÃO DA PÁGINA ---
    tipo_selecionado = menu[chosen_id].lower()
    render_engine(tipo_selecionado)

def render_engine(tipo):
    st.title(f"Modo: {tipo.capitalize()}")
    
    # Interface de geração simplificada para teste
    if st.button(f"Gerar {tipo.capitalize()}"):
        with st.spinner("A Machina está processando..."):
            poema = gera_poema(tipo)
            if poema:
                st.markdown("---")
                for linha in poema:
                    st.write(linha)
                st.markdown("---")

if __name__ == "__main__":
    main()
