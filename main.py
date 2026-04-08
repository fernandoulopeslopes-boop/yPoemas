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

# Dicionário de Books Reais
MAPA_BOOKS = {
    "livro vivo": "rol_livro_vivo.txt",
    "poemas": "rol_poemas.txt",
    "ensaios": "rol_ensaios.txt",
    "jocosos": "rol_jocosos.txt",
    "variações": "rol_variações.txt",
    "metalinguagem": "rol_metalinguagem.txt",
    "sociais": "rol_sociais.txt",
    "outros autores": "rol_outros autores.txt",
    "temas mini": "rol_temas_mini.txt",
    "todos os signos": "rol_todos os signos.txt"
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
    
    # Determina qual livro está sendo exibido
    # Se estiver na aba 'books', o usuário escolhe o book em foco. 
    # Nas outras abas, o book é fixo ou herdado.
    book_atual = st.session_state.book_em_foco
    if aba_atual == "mini": book_atual = "temas mini"
    elif aba_atual == "eureka": book_atual = "livro vivo"
    
    temas_do_livro = carregar_temas(book_atual)
    idx_atual = st.session_state.tema_idx_por_book.get(book_atual, 0) % len(temas_do_livro)
    tema_selecionado = temas_do_livro[idx_atual]

    # --- 1. CONTROLES TOP ---
    cl, c_plus, c_prev, c_rand, c_next, c_help, cr = st.columns([3, 1, 1, 1, 1, 1, 3])
    
    if c_plus.button("✚"):
        st.session_state.seed_eureka += 1
        st.rerun()
    if c_prev.button("❰"):
        st.session_state.tema_idx_por_book[book_atual] = (idx_atual - 1) % len(temas_do_livro)
        st.rerun()
    if c_rand.button("✱"):
        st.session_state.tema_idx_por_book[book_atual] = random.randint(0, len(temas_do_livro) - 1)
        st.rerun()
    if c_next.button("❱"):
        st.session_state.tema_idx_por_book[book_atual] = (idx_atual + 1) % len(temas_do_livro)
        st.rerun()
    if c_help.button("?"):
        st.session_state.help_ativo = not st.session_state.help_ativo

    aba_clicada = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS_APP], default=aba_atual)

    # --- SIDEBAR ---
    with st.sidebar:
        idioma = st.selectbox("L", ["PT - Português", "ES - Español", "IT - Italiano", "EN - English"], label_visibility="collapsed")
        sigla = idioma[:2].lower()
        
        # Header Dinâmico: pt ( {nome do book em foco} )
        st.markdown(f'<div class="book-header">{sigla} ({book_atual})</div>', unsafe_allow_html=True)
        
        if aba_atual == "books":
            novo_book = st.selectbox("Selecione o Livro", list(MAPA_BOOKS.keys()), index=list(MAPA_BOOKS.keys()).index(book_atual))
            if novo_book != book_atual:
                st.session_state.book_em_foco = novo_book
                st.rerun()
        
        tema_sel = st.selectbox("Temas", temas_do_livro, index=idx_atual, label_visibility="collapsed")
        if tema_sel != tema_selecionado:
            st.session_state.tema_idx_por_book[book_atual] = temas_do_livro.index(tema_sel)
            st.rerun()

    if aba_clicada != aba_atual:
        st.session_state.current_tab_idx = PAGINAS_APP.index(aba_clicada)
        st.rerun()

    st.markdown("---")

    # --- PALCO CENTRAL ---
    if st.session_state.help_ativo or aba_atual == "books":
        nome_doc = f"MANUAL_{aba_atual.upper()}.md"
        path_doc = os.path.join("md_files", nome_doc)
        if os.path.exists(path_doc):
            with open(path_doc, "r", encoding="utf-8") as f:
                st.markdown(normalizar_e_traduzir(f.read(), idioma))
    elif aba_atual in ["mini", "ypoemas", "eureka"]:
        semente = st.session_state.seed_eureka if aba_atual == "eureka" else ""
        poema = gera_poema(tema_selecionado, semente)
        st.text(normalizar_e_traduzir(poema, idioma))

if __name__ == "__main__":
    main()
