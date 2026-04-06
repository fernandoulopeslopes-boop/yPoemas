import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="a Máquina de Fazer Poesia", layout="wide")

# --- PROTOCOLO DE ESTÉTICA: LARGURA 300px ---
st.markdown(
    """
    <style>
        [data-testid="stSidebar"][aria-expanded="true"] {
            min-width: 300px;
            max-width: 300px;
        }
        .stSelectbox div[data-baseweb="select"] {
            max-width: 200px;
            margin: 0 auto;
        }
        .sidebar-text {
            font-size: 0.95rem;
            line-height: 1.5;
            padding: 10px;
            text-align: justify;
        }
        .sidebar-arte {
            font-family: monospace;
            white-space: pre;
            display: flex;
            justify-content: center;
            padding: 20px 0;
            color: #ff4b4b;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- DADOS DO PROJETO (ARTES E DESCRIÇÕES) ---
conteudo_temas = {
    "Ais": {
        "arte": "((( ๑ )))\n(( ๑ ๑ ))\n( ๑ ๑ ๑ )",
        "desc": "Variações sobre a dor e o suspiro. Explora a fonética do lamento em quindecilhões de formas."
    },
    "Amaré": {
        "arte": ".~~~~.\n<  ♥  >\n'~~~~'",
        "desc": "A fluidez do verbo amar conjugada com o movimento das marés. Poesia líquida e constante."
    },
    "Anjos": {
        "arte": "  _\\/_  \n  \\  /  \n   \\/   ",
        "desc": "Ascensão e queda. Versos que tocam o metafísico através da estrutura da 'máquina'."
    }
}

# --- SIDEBAR: MONTAGEM COMPLETA ---
with st.sidebar:
    # 1. Seletor de Idiomas (Sequência Original)
    idiomas_opcoes = {
        "Português": "pt",
        "Español": "es",
        "Italiano": "it",
        "Français": "fr",
        "English": "en",
        "Català": "ca"
    }
    
    idioma_selecionado = st.selectbox(
        "Idioma", 
        options=list(idiomas_opcoes.keys()),
        index=0,
        label_visibility="collapsed",
        key="key_idioma_ypoemas"
    )
    
    st.divider()

    # 2. Seletor de Tema (Navegação)
    tema_selecionado = st.selectbox(
        "Selecione o Tema:",
        options=list(conteudo_temas.keys()),
        key="key_tema_navegacao"
    )

    # 3. Arte da Página (Dinâmica)
    st.markdown('<div class="sidebar-arte">', unsafe_allow_html=True)
    st.text(conteudo_temas[tema_selecionado]["arte"])
    st.markdown('</div>', unsafe_allow_html=True)

    # 4. Descrição da Página (Corpo da Sidebar)
    st.markdown('<div class="sidebar-text">', unsafe_allow_html=True)
    st.markdown(f"### {tema_selecionado}")
    st.write(conteudo_temas[tema_selecionado]["desc"])
    
    st.divider()
    st.caption(f"Processando em: {idiomas_opcoes[idioma_selecionado].upper()}")
    st.markdown('</div>', unsafe_allow_html=True)

# --- CORPO PRINCIPAL ---
st.title("a Máquina de Fazer Poesia")
st.header(f"Variação: {tema_selecionado}")
st.info(f"Aguardando geração de versos em {idioma_selecionado}...")
