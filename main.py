import streamlit as st
import os
import random

# Configuração da Página
st.set_page_config(page_title="yPoemas - Machina", layout="centered")

@st.cache_data
def abre(tema_alvo):
    """
    Mecânica de busca com cache: localiza o arquivo .txt na pasta 'temas'.
    Usa st.cache_data conforme a migração que fizemos para performance.
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
    Mecânica de permutação: embaralha as variações originais.
    """
    if not conteudo:
        return ""
    # Processamento de linhas (preservando o conteúdo fiel)
    linhas = [linha.strip() for row in conteudo.strip().split('\n') if (linha := row.strip())]
    random.shuffle(linhas)
    return "\n".join(linhas)

# --- AMBIENTE @fernandoulopeslopes-boop's Machina ---

st.title("🌀 yPoemas")
st.markdown("### @fernandoulopeslopes-boop's Machina")

# Painel de Navegação (Linha Única - Sequência Original)
# more / last / rand / nest / help / love
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    if st.button("+"): # more
        st.session_state.comando = "more"
with col2:
    if st.button("<"): # last
        st.session_state.comando = "last"
with col3:
    if st.button("*"): # rand
        st.session_state.comando = "rand"
with col4:
    if st.button(">"): # nest
        st.session_state.comando = "nest"
with col5:
    if st.button("?"): # help
        st.session_state.comando = "help"
with col6:
    if st.button("@"): # love
        st.session_state.comando = "love"

# Espaço de Operação
tema_escolhido = st.text_input("Escolha um tema:", value="", placeholder="Digite o tema...")

if st.button("GERAR POESIA"):
    if tema_escolhido:
        # Busca o conteúdo usando o cache
        conteudo_fiel = abre(tema_escolhido.lower().strip())
        
        if conteudo_fiel is not None:
            st.markdown("---")
            resultado = gerar_poema(conteudo_fiel)
            # Saída da Machina
            st.text_area(label="", value=resultado, height=500)
        else:
            st.error(f"Arquivo {tema_escolhido}.txt não encontrado na pasta 'temas'.")
    else:
        st.warning("Por favor, insira um tema.")

# MANDALA
st.markdown("---")
st.markdown("✨ *A máquina de fazer poesia está ativa.*")
