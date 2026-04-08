import streamlit as st
import extra_streamlit_components as stx
from deep_translator import GoogleTranslator
import os
import random

# --- [PROTOCOL] MOTOR SOBERANO ---
from lay_2_ypo import gera_poema

def normalizar_e_traduzir(conteudo, idioma):
    if not conteudo: return ""
    texto_unificado = "\n".join(conteudo) if isinstance(conteudo, list) else conteudo
    texto_final = texto_unificado
    if "Português" not in idioma:
        try:
            codigos = {"ES - Español": "es", "IT - Italiano": "it", "EN - English": "en"}
            target = codigos.get(idioma, 'en')
            texto_final = GoogleTranslator(source='auto', target=target).translate(texto_unificado)
        except Exception: pass
    return texto_final.replace('\r\n', '\n').replace('\n\n', '\n').strip()

def aplicar_estetica_machina():
    st.markdown("""
        <style>
            header[data-testid="stHeader"] { visibility: hidden; height: 0px; }
            footer { visibility: hidden; }
            .block-container { padding-top: 0rem !important; }
            div.stButton > button {
                border-radius: 50% !important;
                width: 50px !important;
                height: 50px !important;
                border: 1px solid #333 !important;
                background-color: white !important;
                margin: 0 10px !important;
            }
            .book-header { font-size: 0.85em; font-weight: bold; color: #666; margin-bottom: 2px; font-family: monospace; }
        </style>
    """, unsafe_allow_html=True)

# Mapeamento Estrito dos Livros (\base)
MAPA_BOOKS = {
    "livro vivo": "rol_livro_vivo.txt",
    "poemas": "rol_poemas.txt",
    "ensaios": "rol_ensaios.txt",
    "jocosos": "rol_jocosos.txt",
    "variações": "rol_variações.txt",
    "metalinguagem": "rol_metalinguagem.txt",
    "sociais": "rol_sociais.txt",
    "outros autores": "rol_outros autores.txt",
    "todos os temas": "rol_poemas.txt",
    "todos os signos": "rol_todos os signos.txt",
    "temas mini": "rol_temas_mini.txt"
}

def carregar_temas(nome_book):
    arquivo = MAPA_BOOKS.get(nome_book, "rol_poemas.txt")
    caminho = os.path.join("base", arquivo)
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return [l.strip() for l in f if l.strip() and not l.startswith("[")]
    return ["Fatos"]

def main():
    st.set_page_config(layout="wide", page_title="yPoemas")
    aplicar_estetica_machina()

    PAGINAS_APP = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
    
    if 'current_tab_idx' not in st.session_state: st.session_state.current_tab_idx = 1
    if 'book_em_foco' not in st.session_state: st.session_state.book_em_foco = "poemas"
    if 'tema_idx_por_book' not in st.session_state: st.session_state.tema_idx_por_book = {b: 0 for b in MAPA_BOOKS}
    if 'seed_eureka' not in st.session_state: st.session_state.seed_eureka = 0
    if 'help_ativo' not in st.session_state: st.session_state.help_ativo = False

    aba_atual = PAGINAS_APP[st.session_state.current_tab_idx]
    
    if aba_atual == "mini": book_em_foco = "temas mini"
    elif aba_atual == "eureka": book_em_foco = "livro vivo"
    else: book_em_foco = st.session_state.book_em_foco
    
    temas_do_livro = carregar_temas(book_
