import streamlit as st
import os
import random

# --- CONFIGURAÇÃO E AMBIENTE ---
st.set_page_config(page_title="yPoemas - Machina", layout="wide")

# CSS para garantir os botões de 116px e o design da Machina
st.markdown("""
    <style>
    div.stButton > button {
        width: 116px;
        height: 40px;
        border-radius: 5px;
        border: 1px solid #ccc;
    }
    .min-button {
        width: 60px !important;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def abre(tema_alvo):
    """
    Mecânica com cache (st.cache_data) para leitura de arquivos.
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    pasta_temas = "temas" 
    full_name = os.path.join(base_path, pasta_temas, f"{tema_alvo}.txt")
    
    try:
        with open(full_name, encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return None

def gerar_poema(conteudo):
    """
    Permutação das variações originais.
    """
    if not conteudo: return ""
    linhas = [l.strip() for row in conteudo.strip().split('\n') if (l := row.strip())]
    random.shuffle(linhas)
    return "\n".join(linhas)

# --- SIDEBAR (NAVEGAÇÃO DE PÁGINAS) ---
with st.sidebar:
    st.title("🌀 Configurações")
    pagina = st.radio("Navegar para:", ["Poesia", "Sobre", "Ajuda", "Config"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("### @fernandoulopeslopes-boop's Machina")

# --- CONTEÚDO PRINCIPAL (PÁGINA POESIA) ---
if pagina == "Poesia":
    st.title("🌀 yPoemas")

    # Navegador de topo (Buttons com 116px de largura)
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        if st.button("+"): st.session_state.cmd = "more"
    with col2:
        if st.button("<"): st.session_state.cmd = "last"
    with col3:
        if st.button("*"): st.session_state.cmd = "rand"
    with col4:
        if st.button(">"): st.session_state.cmd = "nest"
    with col5:
        if st.button("?"): st.session_state.cmd = "help"
    with col6:
        if st.button("@"): st.session_state.cmd = "love"

    st.markdown("---")

    # Espaço de Operação e Seleção de Conteúdo
    col_input, col_min = st.columns([3, 1])
    
    with col_input:
        tema_escolhido = st.text_input("Escolha um tema:", value="", placeholder="Digite o tema...")

    with col_min:
        # Navegador com min_buttons para conteúdos/variações da página
        st.write("Variações")
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            if st.button("V1", key="v1", help="Variação 1"): pass
        with m_col2:
            if st.button("V2", key="v2", help="Variação 2"): pass

    if st.button("GERAR POESIA", use_container_width=True):
        if tema_escolhido:
            conteudo_fiel = abre(tema_escolhido.lower().strip())
            if conteudo_fiel:
                st.markdown("---")
                resultado = gerar_poema(conteudo_fiel)
                st.text_area(label="", value=resultado, height=500)
            else:
                st.error(f"Arquivo {tema_escolhido}.txt não encontrado na pasta 'temas'.")

elif pagina == "Sobre":
    st.subheader("Sobre a Machina")
    st.write("Projeto de poesia generativa por permutação.")

# MANDALA
st.markdown("---")
st.markdown("✨ *A máquina de fazer poesia está ativa.*")
