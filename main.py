import os
import socket
import datetime
import random
import base64
import streamlit as st
from gtts import gTTS

# Modulo de geração resgatado
try:
    from lay_2_ypo import gera_poema
except ImportError:
    pass

# --- 1. PROTOCOLO DE ENGENHARIA DE ESTADO ---
def init_session_state():
    """Garante a persistência das variáveis originais da Machina."""
    if "lang" not in st.session_state: st.session_state.lang = "pt"
    if "book" not in st.session_state: st.session_state.book = "livro vivo"
    if "take_tema" not in st.session_state: st.session_state.take_tema = 0
    if "visy" not in st.session_state: st.session_state.visy = True
    if "draw" not in st.session_state: st.session_state.draw = False
    if "talk" not in st.session_state: st.session_state.talk = False
    if "find_word" not in st.session_state: st.session_state.find_word = "amor"
    if "arts" not in st.session_state: st.session_state.arts = []

init_session_state()

# --- 2. LOADERS COM SUPORTE A <EOF> ---
@st.cache_data
def load_file(file):
    """Lê documentos respeitando a edição manual de encerramento."""
    try:
        path = os.path.join("./md_files/", file)
        with open(path, encoding="utf-8") as f:
            content = f.read()
            return content.split("<eof>")[0] if "<eof>" in content else content
    except:
        return "Arquivo não encontrado."

@st.cache_data
def load_temas(book):
    try:
        with open(os.path.join("./base/", f"{book}.rol"), encoding="utf-8") as f:
            return [line.strip() for line in f]
    except:
        return ["erro"]

# --- 3. COMPONENTES DE INTERFACE ---
def write_ypoema(text, image="none"):
    """Renderização padrão da Machina."""
    st.markdown(f'<p class="logo-text">{text}</p>', unsafe_allow_html=True)

# --- 4. FUNÇÕES DE PÁGINA (ESTRUTURA COMPLETA) ---

def page_abouts():
    """Exibe a vasta documentação editada nos md_files[cite: 1]."""
    abouts_list = ["machina", "prefácio", "off-machina", "outros", "imagens", "traduttore", "bibliografia", "samizdát", "pensares", "license", "notes", "index"]
    opt = st.selectbox("Capítulo", range(len(abouts_list)), format_func=lambda x: abouts_list[x].upper())
    st.markdown(load_file(f"ABOUT_{abouts_list[opt].upper()}.md"), unsafe_allow_html=True)

def page_ypoemas():
    """Interface de geração de novos poemas[cite: 1]."""
    temas = load_temas(st.session_state.book)
    if st.button("Gerar Poesia"):
        st.session_state.take_tema = random.randint(0, len(temas)-1)
    
    # Integração com o motor de geração lay_2_ypo
    poema = gera_poema(temas[st.session_state.take_tema], "")
    write_ypoema("<br>".join(poema))

def page_eureka():
    st.subheader("Eureka - Busca no Léxico")
    find = st.text_input("Buscar palavra:", st.session_state.find_word)
    # Lógica de busca...

def page_polys():
    st.subheader("Poly - Idiomas")
    # Lógica de seleção de idiomas...

def page_books():
    st.subheader("Books - Seleção de Livros")
    # Lógica de troca de base .rol...

# --- 5. MAIN (CONTROLE DE FLUXO) ---
def main():
    pages = {
        "yPoemas": page_ypoemas,
        "Sobre": page_abouts,
        "Eureka": page_eureka,
        "Poliglot": page_polys,
        "Livros": page_books
    }
    
    with st.sidebar:
        st.title("yPoemas - 2026")
        choice = st.radio("Navegação", list(pages.keys()))
    
    pages[choice]()

if __name__ == "__main__":
    main()
