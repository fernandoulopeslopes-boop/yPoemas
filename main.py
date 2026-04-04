import streamlit as st
import os
import random

# Configuração da Página
st.set_page_config(page_title="yPoemas - Machina", layout="centered")

def abre(tema_alvo):
    """
    Mecânica de busca: localiza o arquivo .txt na pasta 'temas' 
    usando o caminho absoluto do servidor.
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
    linhas = [linha.strip() for row in conteudo.strip().split('\n') if (linha := row.strip())]
    random.shuffle(linhas)
    return "\n".join(linhas)

# --- AMBIENTE @fernandoulopeslopes-boop's Machina ---

st.title("🌀 yPoemas")
st.markdown("### @fernandoulopeslopes-boop's Machina")

# Painel de Navegação em Linha Única (Simbolismo Original)
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

# Input de Operação
tema_escolhido = st.text_input("Escolha um tema:", value="")

if st.button("GERAR POESIA"):
    if tema_escolhido:
        conteudo_fiel = abre(tema_escolhido.lower().strip())
        
        if conteudo_fiel is not None:
            st.markdown("---")
            resultado = gerar_poema(conteudo_fiel)
            st.text_area(label="", value=resultado, height=500)
        else:
            st.error(f"Arquivo {tema_escolhido}.txt não encontrado.")

# MANDALA
st.markdown("---")
st.markdown("✨ *A máquina de fazer poesia está ativa.*")
