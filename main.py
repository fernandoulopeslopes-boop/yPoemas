import os
import random
import base64
import socket
import streamlit as st
from lay_2_ypo import gera_poema

# --- CONFIGURAÇÃO ---
st.set_page_config(
    page_title="a máquina de fazer Poesia",
    layout="centered",
    initial_sidebar_state="auto",
)

# CSS: Largura da sidebar (300px) e estética do poema
st.markdown("""
    <style>
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child {
        width: 300px;
    }
    .poema-font {
        font-family: 'serif';
        font-size: 1.35rem;
        line-height: 1.6;
        color: #1a1a1a;
        padding: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# --- ESTADOS DE SESSÃO ---
if "lang" not in st.session_state: st.session_state.lang = "pt"
if "book" not in st.session_state: st.session_state.book = "livro vivo"
if "tema" not in st.session_state: st.session_state.tema = "Fatos"
if "take" not in st.session_state: st.session_state.take = 0
if "draw" not in st.session_state: st.session_state.draw = False
if "talk" not in st.session_state: st.session_state.talk = False

# --- SIDEBAR (O PORTAL - ESTRUTURA PURA) ---

def build_sidebar():
    with st.sidebar:
        # 1. pick_lang (6 colunas)
        c1, c2, c3, c4, c5, c6 = st.columns([1, 1, 1, 1, 1, 1])
        if c1.button("pt"): st.session_state.lang = "pt"
        if c2.button("es"): st.session_state.lang = "es"
        if c3.button("it"): st.session_state.lang = "it"
        if c4.button("fr"): st.session_state.lang = "fr"
        if c5.button("en"): st.session_state.lang = "en"
        if c6.button("⚒️"): st.session_state.lang = "poly"
        
        st.write("---")
        
        # 2. Navegação (Mini, yPoemas, Eureka)
        page = st.radio("", ["Mini", "yPoemas", "Eureka"], 
                        index=1, label_visibility="collapsed")
        
        st.write("---")
        
        # 3. Contexto (Apenas se yPoemas)
        if page == "yPoemas":
            st.selectbox("", ["livro vivo", "todos os temas"], 
                         key="book_sel", label_visibility="collapsed")
            st.selectbox("", ["Fatos", "Amor", "Morte"], 
                         key="tema_sel", label_visibility="collapsed")
            st.write("---")
        
        # 4. Sentidos (Art, Talk)
        st.session_state.draw = st.checkbox("Art", value=st.session_state.draw)
        st.session_state.talk = st.checkbox("Talk", value=st.session_state.talk)
        
        st.write("---")
        
        # 5. Rodapé (Ícones, Show Readings, Share)
        st.write("✨ 📚 ✉️ ☕")
        
        st.checkbox("Show Readings", value=False)
        
        if st.button("Share"):
            st.write("Link copiado!") # Simulação conforme o PAI

        return page

# --- PÁGINA YPOEMAS ---

def show_ypoemas():
    # Comandos de Navegação
    n1, n2, n3, n4 = st.columns([1, 1, 1, 1])
    if n1.button("Anterior"): st.session_state.take -= 1
    if n2.button("Acaso"): st.session_state.take = random.randint(0, 999)
    if n3.button("Próximo"): st.session_state.take += 1
    with n4:
        with st.expander("Help"):
            st.write("A Machina gera variações infinitas.")

    st.write("---")

    # Geração e Exibição
    poema_raw = gera_poema(st.session_state.tema, "")
    poema_html = "<br>".join(poema_raw)

    if st.session_state.draw:
        col_t, col_i = st.columns([1.6, 1])
        with col_t:
            st.markdown(f"<div class='poema-font'>{poema_html}</div>", unsafe_allow_html=True)
        with col_i:
            st.image("https://via.placeholder.com/400x600.png?text=Art", use_container_width=True)
    else:
        st.markdown(f"<div class='poema-font'>{poema_html}</div>", unsafe_allow_html=True)

# --- EXECUÇÃO ---

def main():
    current_page = build_sidebar()
    
    if current_page == "yPoemas":
        show_ypoemas()
    elif current_page == "Mini":
        st.info("Mini")
    elif current_page == "Eureka":
        st.info("Eureka")

if __name__ == "__main__":
    main()
