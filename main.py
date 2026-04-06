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
            max-width: 180px;
            margin: 0 auto;
        }

        .sidebar-text {
            font-size: 0.95rem;
            line-height: 1.5;
            padding: 10px;
        }
        
        .sidebar-arte {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- SIDEBAR: MONTAGEM FINAL ---
with st.sidebar:
    # 1. Dropdown de Idiomas (Sequência Original Corrigida)
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
        key="idioma_sidebar_final"
    )
    
    st.divider()

    # 2. Arte da Página Selecionada
    # Espaço para renderizar o elemento visual/temático
    st.markdown('<div class="sidebar-arte">', unsafe_allow_html=True)
    # Exemplo de placeholder para a arte temática do projeto
    st.write("✨ **[ARTE TEMÁTICA]** ✨")
    st.markdown('</div>', unsafe_allow_html=True)

    # 3. Descrição da Página e Conteúdo do Corpo
    st.markdown('<div class="sidebar-text">', unsafe_allow_html=True)
    
    st.subheader("Sobre esta variação")
    # Aqui o código recebe a descrição dinâmica baseada na página atual
    st.write(
        "Descrição detalhada da página que agora ocupa a largura de 300px, "
        "permitindo uma leitura fluida sem quebras excessivas de linha."
    )
    
    st.divider()
    
    # Outros elementos do corpo (ex: métricas ou infos rápidas)
    st.caption("Status da Máquina:")
    st.success("Gerador Ativo")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- CORPO PRINCIPAL ---
st.title("Máquina de Fazer Poesia")
st.write(f"Idioma de processamento: **{idioma_selecionado}**")
