import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Máquina de Fazer Poesia", layout="wide")

# --- PROTOCOLO DE ESTÉTICA: LARGURA 300px ---
st.markdown(
    """
    <style>
        [data-testid="stSidebar"][aria-expanded="true"] {
            min-width: 300px;
            max-width: 300px;
        }
        
        .stSelectbox div[data-baseweb="select"] {
            max-width: 180px;
            margin: 0 auto;
        }

        .sidebar-text {
            font-size: 0.95rem;
            line-height: 1.5;
            padding: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- SIDEBAR: MONTAGEM ---
with st.sidebar:
    # 1. Dropdown de Idiomas (Sequência Original Corrigida)
    # O parâmetro 'key' resolve o erro StreamlitDuplicateElementId
    idiomas_opcoes = {
        "Português": "pt",
        "Español": "es",
        "Français": "fr",
        "Italiano": "it",
        "English": "en",
        "Català": "ca"
    }
    
    idioma_selecionado = st.selectbox(
        "Idioma", 
        options=list(idiomas_opcoes.keys()),
        index=0,
        label_visibility="collapsed",
        key="idioma_final_ypoemas"
    )
    
    st.divider()

    # 2. Espaço para Arte e Descrição
    st.markdown('<div class="sidebar-text">', unsafe_allow_html=True)
    
    # Placeholder limpo para o seu conteúdo
    st.info("Espaço destinado à descrição e arte da página.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- CORPO PRINCIPAL ---
st.title("Máquina de Fazer Poesia")
st.write(f"Idioma de processamento: **{idioma_selecionado}**")
