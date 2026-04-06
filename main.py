import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Máquina de Fazer Poesia", layout="wide")

# --- PROTOCOLO DE ESTÉTICA: LARGURA INTELIGENTE ---
st.markdown(
    """
    <style>
        [data-testid="stSidebar"][aria-expanded="true"] {
            min-width: 380px;
            max-width: 450px;
        }
        
        .stSelectbox div[data-baseweb="select"] {
            max-width: 200px;
            margin: 0 auto;
        }

        .sidebar-text {
            font-size: 0.95rem;
            line-height: 1.5;
            padding: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- SIDEBAR: ORGANIZAÇÃO ---
with st.sidebar:
    idiomas_opcoes = {
        "Português": "pt",
        "English": "en",
        "Español": "es",
        "Français": "fr",
        "Deutsch": "de",
        "Italiano": "it"
    }
    
    idioma_selecionado = st.selectbox(
        "Idioma", 
        options=list(idiomas_opcoes.keys()),
        index=0,
        label_visibility="collapsed"
    )
    
    st.divider()

    st.markdown('<div class="sidebar-text">', unsafe_allow_html=True)
    st.markdown("### 🎨 Navegação & Arte")
    
    st.info(
        "Descrição da página com espaço ampliado para evitar a fragmentação do texto "
        "em linhas muito curtas."
    )
    st.markdown('</div>', unsafe_allow_html=True)

# --- CORPO PRINCIPAL ---
st.title("Máquina de Fazer Poesia")
st.write(f"Idioma selecionado: **{idioma_selecionado}**")
