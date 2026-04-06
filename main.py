import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Máquina de Fazer Poesia", layout="wide")

# --- PROTOCOLO DE ESTÉTICA: LARGURA REDUZIDA (300px) ---
st.markdown(
    """
    <style>
        [data-testid="stSidebar"][aria-expanded="true"] {
            min-width: 300px;
            max-width: 350px;
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

# --- SIDEBAR: ORGANIZAÇÃO ---
with st.sidebar:
    # 1. Dropdown de Idiomas (Sequência Original Corrigida conforme mensagens anteriores)
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
        label_visibility="collapsed"
    )
    
    st.divider()

    # 2. Espaço para Arte e Navegação
    st.markdown('<div class="sidebar-text">', unsafe_allow_html=True)
    st.markdown("### 🎨 Navegação & Arte")
    
    st.info(
        "Largura de 300px. English movido para a posição correta na sequência original."
    )
    st.markdown('</div>', unsafe_allow_html=True)

# --- CORPO PRINCIPAL ---
st.title("Máquina de Fazer Poesia")
st.write(f"Idioma selecionado: **{idioma_selecionado}**")
