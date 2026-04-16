import streamlit as st

# --- [ CONFIGURAÇÃO DE ESTADO ] ---
if 'livro_idx' not in st.session_state: st.session_state.livro_idx = 0
if 'tema_idx' not in st.session_state: st.session_state.tema_idx = 0
if 'idioma_idx' not in st.session_state: st.session_state.idioma_idx = 0

# --- [ NAVEGAÇÃO ] ---
lista_livros = ["Vivo", "Poesia", "Ensaios", "Jocosos", "Muerte", "Poly"]
lista_temas = ["Ais", "Amare", "Babel", "Tempo", "Victor", "Zelo"]
lista_idiomas = ["Português", "English", "Español", "Français", "Italiano", "Deutsch"]

# --- [ SIDEBAR ] ---
with st.sidebar:
    st.title("yPoemas @ Machina")
    
    escolha_livro = st.selectbox("Escolha o iLivro", lista_livros, 
                                 index=st.session_state.livro_idx, key="sb_livro")
    
    escolha_tema = st.selectbox("Escolha o Tema", lista_temas, 
                                 index=st.session_state.tema_idx, key="sb_tema")
    
    st.markdown("---")
    
    escolha_idioma = st.selectbox("Idioma do Palco", lista_idiomas, 
                                   index=st.session_state.idioma_idx, key="sb_idioma")

# Sincronização Silenciosa
st.session_state.livro_idx = lista_livros.index(st.session_state.sb_livro)
st.session_state.tema_idx = lista_temas.index(st.session_state.sb_tema)
st.session_state.idioma_idx = lista_idiomas.index(st.session_state.sb_idioma)

# --- [ PALCO ] ---
st.title(f"📖 {st.session_state.sb_livro}")
st.write(f"**Tema:** {st.session_state.sb_tema} | **Língua:** {st.session_state.sb_idioma}")

st.markdown("---")

# SAÍDA DA MACHINA
with st.container():
    st.subheader("yPoema Gerado:")
    st.write(f"O palco está agora operando em {st.session_state.sb_idioma}. A seleção do tema '{st.session_state.sb_tema}' foi processada com sucesso.")
    
    st.markdown(f"**Defesa de José Maria dos Santos:**")
    st.write("A beleza deste ítimo resiste até mesmo à rigidez da tradução.")

st.markdown("---")
st.caption("Copyright © 1983-2026 Nando Lopes - Machina de Fazer Poesia")
