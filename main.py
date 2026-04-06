import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Máquina de Fazer Poesia", layout="wide")

# --- PROTOCOLO DE ESTÉTICA: LARGURA E ESTILIZAÇÃO DA MANDALA ---
st.markdown(
    """
    <style>
        /* Largura da sidebar apenas quando expandida */
        [data-testid="stSidebar"][aria-expanded="true"] {
            min-width: 380px;
            max-width: 450px;
        }
        
        /* Estilização do Selectbox de idiomas */
        .stSelectbox div[data-baseweb="select"] {
            max-width: 200px;
            margin: 0 auto;
        }

        /* Centralização e estilo para a arte da Mandala */
        .mandala-container {
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 200px; /* Tamanho da mandala */
            line-height: 1;
            margin-top: -30px; /* Ajuste vertical para ocupar o topo */
            margin-bottom: 20px;
            color: #ff4b4b; /* Cor da mandala (opcional, ajustável) */
            font-family: serif; /* Garante que o caractere Unicode renderize corretamente */
        }

        /* Ajuste fino para o texto das descrições */
        .sidebar-text {
            font-size: 0.95rem;
            line-height: 1.5;
            padding: 0 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- SIDEBAR: ORGANIZAÇÃO ---
with st.sidebar:
    # 1. Mandala no Topo (Ocupando o espaço da 'tripa')
    # O caractere ☸ é a "Roda do Dharma", muitas vezes usada para representar mandalas
    st.markdown('<div class="mandala-container">☸</div>', unsafe_allow_html=True)

    # 2. Dropdown de Idiomas (Logo abaixo da mandala)
    idiomas_opcoes = {
        "Português": "pt",
        "English": "en",
        "Español": "es
