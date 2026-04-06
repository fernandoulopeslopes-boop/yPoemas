import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Máquina de Fazer Poesia", layout="wide")

# --- PROTOCOLO DE ESTÉTICA: LARGURA E ESTILIZAÇÃO DA MANDALA ---
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

        .mandala-container {
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 200px;
            line-height: 1;
            margin-top: -30px;
            margin-bottom: 20px;
            color: #ff4b4b;
            font-family: serif;
        }

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
    st.markdown('<div class="mandala-container">☸</div>', unsafe_allow_html=True)

    idiomas_opcoes = {
        "Português": "pt",
        "English": "en",
        "Español": "es",
        "Français": "fr",
        "Deutsch": "de",
        "Italiano": "it"
    }
    
    idioma_selecionado = st.selectbox(
        "🌐 Idioma", 
        options=list(idiomas_opcoes.keys()),
        index=0,
        label_visibility="collapsed" 
    )
    
    st.divider()

    st.markdown('<div class="sidebar-text">', unsafe_allow_html=True)
    st.markdown("### 🎨 Navegação & Arte")
    
    st.info(
        "A largura da sidebar agora suporta descrições detalhadas sem comprometer "
        "a estética quando recolhida."
    )
    st.markdown('</div>', unsafe_allow_html=True)

# --- CORPO PRINCIPAL ---
st.title("Máquina de Fazer Poesia")
st.write(f"Idioma atual: **{idioma_selecionado}**")
