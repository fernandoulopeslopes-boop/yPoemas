import os
import random
import asyncio
import edge_tts
import streamlit as st
from deep_translator import GoogleTranslator

# --- 1. CONFIGURAÇÃO E LISTA OFICIAL (CPC) ---
IDIOMAS_OFICIAIS = {
    "Português": "pt", "Espanhol": "es", "Italiano": "it", "Francês": "fr",
    "Inglês": "en", "Catalão": "ca", "Córsico": "co", "Galego": "gl",
    "Basco": "eu", "Esperanto": "eo", "Latin": "la", "Galês": "cy",
    "Sueco": "sv", "Polonês": "pl", "Holandês": "nl", "Norueguês": "no",
    "Finlandês": "fi", "Dinamarquês": "da", "Irlandês": "ga", "Romeno": "ro", "Russo": "ru"
}

def init_session():
    """ Exorcismo: Inicializa as chaves que o log disse que estavam faltando """
    if "lang" not in st.session_state:
        st.session_state.lang = "pt"
    if "last_lang" not in st.session_state:
        st.session_state.last_lang = "pt"
    if "off_book" not in st.session_state:
        st.session_state.off_book = 0

def translate(text):
    if st.session_state.lang == "pt": return text
    try:
        return GoogleTranslator(source='pt', target=st.session_state.lang).translate(text)
    except: return text

# --- 2. SELECTOR DE IDIOMAS (SEM BOTÕES ANTIGOS) ---
def language_selector():
    lang_inv = {v: k for k, v in IDIOMAS_OFICIAIS.items()}
    lista_nomes = list(IDIOMAS_OFICIAIS.keys())
    
    # Garante que o idioma atual seja o primeiro da lista visual
    nome_atual = lang_inv.get(st.session_state.lang, "Português")
    if nome_atual in lista_nomes:
        lista_nomes.insert(0, lista_nomes.pop(lista_nomes.index(nome_atual)))

    selecionado = st.selectbox("↓ " + translate("idioma"), lista_nomes, key="cpc_selector")
    novo_code = IDIOMAS_OFICIAIS[selecionado]

    if novo_code != st.session_state.lang:
        st.session_state.last_lang = st.session_state.lang
        st.session_state.lang = novo_code
        st.rerun()

# --- 3. ÍCONES SOCIAIS (CORRIGIDOS) ---
def show_social_icons():
    st.sidebar.write("---")
    # HTML robusto para os 4 ícones
    social_html = """
    <div style="display: flex; justify-content: space-around; font-size: 25px;">
        <a href="https://facebook.com" title="Facebook">📘</a>
        <a href="mailto:seu-email@provedor.com" title="E-mail">✉️</a>
        <a href="https://instagram.com" title="Instagram">📸</a>
        <a href="https://wa.me/seunumerowhats" title="WhatsApp">🟢</a>
    </div>
    """
    st.sidebar.markdown(social_html, unsafe_allow_html=True)

# --- 4. AJUSTE EUREKA E OFF-MACHINA ---
def page_eureka():
    # Largura aumentada conforme pedido (Item 3)
    c1, c2, c3, c4, c5 = st.columns([2.5, 1.2, 1.2, 0.7, 6.0]) 
    with c1:
        st.text_input(label=translate("buscar..."))
    # ... resto da lógica

# --- 5. EXECUÇÃO PRINCIPAL ---
def main():
    init_session() # Chave do sucesso: inicializa antes de usar
    
    with st.sidebar:
        language_selector() # Aparece no TOPO
        st.write("---")
        # Remova aqui qualquer código antigo de botões manuais (en, es, pt...)
        show_social_icons()

    # NAVEGAÇÃO
    # Renomeie sua aba/botão de 5 para "livros" aqui no seu componente de menu
    st.title(translate("Livros")) 

if __name__ == "__main__":
    if not os.path.exists("./temp"): os.makedirs("./temp")
    main()
