import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Máquina de Fazer Poesia", layout="wide")

# --- PROTOCOLO DE ESTÉTICA: LARGURA DA SIDEBAR ---
# Injeção de CSS para evitar que as descrições virem uma "tripa"
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            min-width: 380px;
            max-width: 500px;
        }
        /* Ajuste opcional para o conteúdo da sidebar não ficar colado nas bordas */
        .sidebar-content {
            padding: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- SIDEBAR: ORGANIZAÇÃO ---
with st.sidebar:
    # 1. Dropdown de Idiomas no Topo (Recolhível)
    idiomas_opcoes = {
        "Português": "pt",
        "English": "en",
        "Español": "es",
        "Français": "fr",
        "Deutsch": "de",
        "Italiano": "it"
    }
    
    idioma_selecionado = st.selectbox(
        "🌐 Idioma / Language", 
        options=list(idiomas_opcoes.keys()),
        index=0
    )
    
    st.divider()

    # 2. Espaço para Arte e Navegação
    # Agora com mais largura para descrições longas
    st.markdown("### 🎨 Navegação & Arte")
    
    # Exemplo de como as descrições agora respiram melhor
    st.info(
        "Esta é uma descrição de página que, na largura padrão do Streamlit, "
        "ficaria extremamente verticalizada e difícil de ler. Com o novo ajuste, "
        "o texto flui naturalmente, preservando a estética do projeto."
    )

# --- CORPO PRINCIPAL ---
st.title("Máquina de Fazer Poesia")
st.subheader(f"Versão Multilingue: {idioma_selecionado}")

# Lógica de cache (st.cache_data) e tradução entrariam aqui
# ...
