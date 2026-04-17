# main.py

import streamlit as st
import os
# RETIFICAÇÃO ABSOLUTA: O motor reside em lay_2_ypo.py
from lay_2_ypo import gera_poema

# 1. CONFIGURAÇÃO DE PÁGINA
st.set_page_config(
    page_title="yPoemas @ Machina",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ESTADO DA SESSÃO
if 'poema_atual' not in st.session_state:
    st.session_state.poema_atual = []
if 'tema_selecionado' not in st.session_state:
    st.session_state.tema_selecionado = "FATOS"

# 3. SIDEBAR (Design Nativo - 300px)
with st.sidebar:
    st.title("yPoemas @ Machina")
    
    with st.container():
        lista_livros = ["Vivo", "Poesia", "Ensaios", "Jocosos", "Muerte", "Poly"]
        idiomas_opcoes = {
            'Português': 'pt', 'Español': 'es', 'Italiano': 'it', 
            'Français': 'fr', 'English': 'en', 'Català': 'ca',
            'Deutsch': 'de', 'Nederlands': 'nl', 'Dansk': 'da',
            'Svenska': 'sv', 'Norsk': 'no'
        }
        
        livro_escolhido = st.selectbox("Escolha o iLivro", lista_livros)
        
        pasta_data = "./data/"
        try:
            temas = [f.replace(".ypo", "") for f in os.listdir(pasta_data) if f.endswith(".ypo")]
            temas.sort()
        except FileNotFoundError:
            temas = ["FATOS"]

        tema_escolhido = st.selectbox(
            "Escolha o Tema", 
            temas, 
            index=temas.index(st.session_state.tema_selecionado) if st.session_state.tema_selecionado in temas else 0
        )
        
        idioma = st.radio("Idioma do Palco", list(idiomas_opcoes.keys()), horizontal=True)
        
        st.divider()
        
        seed = st.text_input("Semente Eureka (opcional)", placeholder="palavra ➪ Tema_0000")

    st.divider()
    
    if st.button("Gerar yPoema", use_container_width=True, type="primary"):
        st.session_state.tema_selecionado = tema_escolhido
        # Chamada ao motor lay_2_ypo
        st.session_state.poema_atual = gera_poema(tema_escolhido, seed)
        st.rerun()

    st.caption("Copyright © 1983-2026 Nando Lopes")

# 4. ÁREA PRINCIPAL (Palco)
st.title(f"📖 {livro_escolhido}")
st.write(f"**Tema:** {st.session_state.tema_selecionado} | **Língua:** {idioma}")
st.markdown("---")

col_l, col_main, col_r = st.columns([1, 4, 1])

with col_main:
    if st.session_state.poema_atual:
        with st.container(border=True):
            for verso in st.session_state.poema_atual:
                if verso == "\n":
                    st.write("")
                else:
                    st.markdown(verso, unsafe_allow_html=True)
            
            st.write("")
            st.markdown("**Defesa de José Maria dos Santos:**")
            st.write("A beleza deste ritmo resiste até mesmo à rigidez da tradução.")
    else:
        st.info("Clique em 'Gerar yPoema' para começar.")
