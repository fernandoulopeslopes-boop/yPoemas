import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Máquina de Fazer Poesia", layout="wide")

# --- PROTOCOLO DE ESTÉTICimport streamlit as st

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
        
        /* Ajuste para o rádio de navegação não ficar apertado */
        .stRadio div[role="radiogroup"] {
            padding: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- SIDEBAR: MONTAGEM COMPLETA ---
with st.sidebar:
    # 1. Dropdown de Idiomas (Sequência: pt, es, fr, it, en, ca)
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

    # 2. Área de Navegação e Arte
    st.markdown("### 🎨 Navegação")
    
    # Simulação das páginas do projeto
    pagina = st.radio(
        "Selecione a variação:",
        [
            "🏠 Início", 
            "📜 Máquina de Poesia", 
            "🧬 Gerador Temático", 
            "📊 Estatísticas Quindecilhantes",
            "⚙️ Configurações"
        ],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # 3. Descrição da Página (Onde o espaço de 300px atua)
    st.markdown('<div class="sidebar-text">', unsafe_allow_html=True)
    st.markdown(f"**Sobre: {pagina}**")
    
    descricoes = {
        "🏠 Início": "Bem-vindo à interface central da Máquina de Fazer Poesia. Aqui você define os parâmetros globais da obra.",
        "📜 Máquina de Poesia": "Acesse o núcleo gerador onde milhões de combinações linguísticas ganham vida em tempo real.",
        "🧬 Gerador Temático": "Explore as variações por categorias específicas, navegando por temas que vão do cotidiano ao abstrato.",
        "📊 Estatísticas Quindecilhantes": "Visualize a escala massiva do projeto e a quantidade de variações possíveis em cada estrutura.",
        "⚙️ Configurações": "Ajustes técnicos de cache, tradução (gTTS) e parâmetros de exportação do sistema."
    }
    
    st.info(descricoes.get(pagina, ""))
    st.markdown('</div>', unsafe_allow_html=True)

# --- CORPO PRINCIPAL ---
st.title("Máquina de Fazer Poesia")
st.subheader(f"Interface: {pagina}")
st.write(f"Idioma de processamento: **{idioma_selecionado}**")A: LARGURA REDUZIDA (300px) ---
st.markdown(
    """
    <style>
        [data-testid="stSidebar"][aria-expanded="true"] {
            min-width: 280px;
            max-width: 330px;
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
