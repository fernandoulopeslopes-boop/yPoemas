import streamlit as st
from ypo_seguro import *

def main():
    # 1. Configuração da Página
    st.set_page_config(
        page_title="a Máquina de Fazer Poesia",
        page_icon="📖",
        layout="centered"
    )

    # 2. Inicialização do Session State (evita erros de chave inexistente)
    if 'lang' not in st.session_state:
        st.session_state.lang = "pt"
    if 'take' not in st.session_state:
        st.session_state.take = 0
    if 'book' not in st.session_state:
        st.session_state.book = "livro vivo"
    if 'visy' not in st.session_state:
        st.session_state.visy = True
    if 'draw' not in st.session_state:
        st.session_state.draw = False
    if 'talk' not in st.session_state:
        st.session_state.talk = False
    if 'fila' not in st.session_state:
        from collections import deque
        st.session_state.fila = deque(maxlen=24)
    if 'find_word' not in st.session_state:
        st.session_state.find_word = ""

    # 3. Carregamento de Estilo (CSS Externo se houver)
    # load_css() 

    # 4. Sidebar - O Cockpit
    with st.sidebar:
        st.title("Machina")
        # Aqui você define o seletor que dita qual página carregar
        menu = ["yPoemas", "Eureka", "Mini", "Off-Machina", "Books", "Poly", "About"]
        choice = st.selectbox("Navegação", menu)

    # 5. Roteamento das Páginas (Chamando as funções do ypo_seguro.py)
    if choice == "yPoemas":
        page_ypoemas()
    elif choice == "Eureka":
        page_eureka()
    elif choice == "Mini":
        page_mini()
    elif choice == "Off-Machina":
        page_off_machina()
    elif choice == "Books":
        page_books()
    elif choice == "Poly":
        page_polys()
    elif choice == "About":
        page_abouts()

if __name__ == "__main__":
    main()
