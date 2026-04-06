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

        .sidebar-arte {
            display: flex;
            justify-content: center;
            text-align: center;
            padding: 20px 0;
            white-space: pre-wrap;
            font-family: monospace;
        }

        .sidebar-descricao {
            font-size: 0.95rem;
            line-height: 1.6;
            padding: 10px;
            text-align: justify;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- SIDEBAR: MONTAGEM ---
with st.sidebar:
    # 1. Seletor de Idiomas (Sequência Original Estrita)
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
        key="main_lang_selector"
    )
    
    st.divider()

    # 2. Arte da Página
    st.markdown('<div class="sidebar-arte">', unsafe_allow_html=True)
    st.write("((( ๑ )))\n(( ๑ ๑ ))\n( ๑ ๑ ๑ )")
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # 3. Descrição da Página
    st.markdown('<div class="sidebar-descricao">', unsafe_allow_html=True)
    st.subheader("Ais")
    st.write(
        "Variações sobre a dor e o suspiro. Explora a fonética do lamento "
        "em quindecilhões de formas."
    )
    st.markdown('</div>', unsafe_allow_html=True)

# --- CORPO PRINCIPAL ---
st.title("a Máquina de Fazer Poesia")
st.write(f"Variação: **Ais** | Idioma: **{idioma_selecionado}**")
