import streamlit as st
import os
import random

# Configuração da Página
st.set_page_config(page_title="yPoemas - Máquina de Fazer Poesia", layout="centered")

def abre(tema_alvo):
    """
    Função para localizar e abrir os arquivos de texto.
    Busca o caminho absoluto para evitar o FileNotFoundError no servidor.
    """
    # Descobre o diretório onde o main.py está localizado
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Define o nome da pasta (ajuste 'temas' se o nome no GitHub for outro)
    pasta_temas = "temas" 
    
    # Monta o caminho completo do arquivo .txt
    full_name = os.path.join(base_path, pasta_temas, f"{tema_alvo}.txt")
    
    try:
        with open(full_name, encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return f"Erro: O arquivo {tema_alvo}.txt não foi encontrado na pasta {pasta_temas}."

def gerar_poema(conteudo):
    """
    Lógica para processar as variações e gerar a poesia.
    """
    linhas = conteudo.strip().split('\n')
    # Exemplo simples de permutação (ajuste conforme sua lógica de variações)
    random.shuffle(linhas)
    return "\n".join(linhas[:10]) # Retorna as primeiras 10 linhas permutadas

# --- INTERFACE STREAMLIT ---

st.title("🌀 yPoemas")
st.subheader("@fernandoulopeslopes-boop's Machina")

# Navegação em linha única conforme seu design
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    if st.button("more"):
        st.session_state.acao = "more"
with col2:
    if st.button("last"):
        st.session_state.acao = "last"
with col3:
    if st.button("rand"):
        st.session_state.acao = "rand"
with col4:
    if st.button("nest"):
        st.session_state.acao = "nest"
with col5:
    if st.button("help"):
        st.info("Ajuda: Selecione um tema para gerar a poesia.")
with col6:
    if st.button("love"):
        st.heart("Feito com amor.")

# Seleção de Tema (Exemplo com os temas da sua máquina)
tema_escolhido = st.selectbox("Escolha um tema:", ["amor", "tempo", "mar", "noite", "silencio"])

if st.button("GERAR POESIA"):
    conteudo_fiel = abre(tema_escolhido.lower())
    
    if "Erro:" in conteudo_fiel:
        st.error(conteudo_fiel)
    else:
        poesia = gerar_poema(conteudo_fiel)
        st.markdown(f"### Poesia Gerada: {tema_escolhido}")
        st.text_area("", value=poesia, height=400)

# Rodapé ou Mandala visual
st.markdown("---")
st.markdown("✨ *A máquina de fazer poesia está ativa.*")
