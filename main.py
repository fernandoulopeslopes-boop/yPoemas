import streamlit as st
import extra_streamlit_components as stx
from deep_translator import GoogleTranslator
import os
import random

# --- [PROTOCOL] MOTOR SOBERANO ---
try:
    from lay_2_ypo import gera_poema
except ImportError:
    def gera_poema(t, s=""): return f"Erro: lay_2_ypo.py não encontrado.\nTema: {t}"

def normalizar_e_traduzir(conteudo, idioma_nome):
    if not conteudo: return ""
    texto_unificado = "\n".join(conteudo) if isinstance(conteudo, list) else conteudo
    cod_target = idioma_nome.split(" - ")[0].lower()
    if cod_target == "pt":
        return texto_unificado.replace('\r\n', '\n').replace('\n\n', '\n').strip()
    try:
        texto_final = GoogleTranslator(source='auto', target=cod_target).translate(texto_unificado)
        return texto_final.replace('\r\n', '\n').replace('\n\n', '\n').strip()
    except Exception:
        return texto_unificado

def aplicar_estetica_machina():
    st.markdown("""
        <style>
            header[data-testid="stHeader"] { visibility: hidden; height: 0px; }
            footer { visibility: hidden; }
            [data-testid="stSidebar"] { display: none; }
            
            .block-container { 
                padding-top: 1.5rem !important; 
                padding-left: 10% !important; 
                padding-right: 10% !important; 
                max-width: 100% !important;
            }
            
            /* Centralização e Estilo do Poema */
            .poema-container {
                font-family: 'Courier New', Courier, monospace;
                font-size: 1.1em;
                line-height: 1.6;
                color: #222;
                background-color: #fcfcfc;
                padding: 30px;
                border-left: 1px solid #eee;
                white-space: pre-wrap;
            }

            div.stButton > button {
                border-radius: 50% !important;
                width: 46px !important;
                height: 46px !important;
                border: 1px solid #333 !important;
                background-color: white !important;
                margin: 0 auto !important;
                display: block;
            }
            
            .cockpit-header { 
                font-size: 0.85em; 
                font-weight: bold; 
                color: #666; 
                margin-bottom: 5px;
                font-family: monospace; 
                text-align: center;
                text-transform: lowercase;
            }
        </style>
    """, unsafe_allow_html=True)

MAPA_BOOKS = {
    "livro vivo": "rol_livro_vivo.txt", "poemas": "rol_poemas.txt", "ensaios": "rol_ensaios.txt",
    "jocosos": "rol_jocosos.txt", "variações": "rol_variações.txt", "metalinguagem": "rol_metalinguagem.txt",
    "sociais": "rol_sociais.txt", "outros autores": "rol_outros autores.txt",
    "todos os temas": "rol_poemas.txt", "todos os signos": "rol_todos os signos.txt", "temas mini": "rol_temas_mini.txt"
}

LISTA_IDIOMAS = [
    "PT - Português", "AF - Afrikaans", "SQ - Albanian", "CA - Catalan", "HR - Croatian", 
    "CS - Czech", "DA - Danish", "NL - Dutch", "EN - English", "ET - Estonian", 
    "FI - Finnish", "FR - French", "DE - German", "HU - Hungarian", "IS - Icelandic", 
    "ID - Indonesian", "IT - Italiano", "LV - Latvian", "LT - Lithuanian", "NO - Norwegian", 
    "PL - Polish", "RO - Romanian", "SK - Slovak", "SL - Slovenian", "ES - Español", 
    "SW - Swahili", "SV - Swedish", "TR - Turkish", "VI - Vietnamese"
]

def carregar_temas(nome_book):
    arquivo = MAPA_BOOKS.get(nome_book, "rol_poemas.txt")
    caminho = os.path.join("base", arquivo)
    if os.path.exists(caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return [l.strip() for l in f if l.strip() and not l.startswith("[")]
        except Exception: pass
    return ["Fatos"]

def main():
    st.set_page_config(layout="wide", page_title="yPoemas", initial_sidebar_state="collapsed")
    aplicar_estetica_machina()

    # Session State
    if 'current_tab_idx' not in st.session_state: st.session_state.current_tab_idx = 1
    if 'book_em_foco' not in st.session_state: st.session_state.book_em_foco = "poemas"
    if 'tema_idx_por_book' not in st.session_state: st.session_state.tema_idx_por_book = {b: 0 for b in MAPA_BOOKS}
    if 'seed_eureka' not in st.session_state: st.session_state.seed_eureka = 0
    if 'help_ativo' not in st.session_state: st.session_state.help_ativo = False
    if 'com_imagem' not in st.session_state: st.session_state.com_imagem = True

    aba_atual = PAGINAS_APP = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
    aba_atual = PAGINAS_APP[st.session_state.current_tab_idx]
    
    book_em_foco = "temas mini" if aba_atual == "mini" else ("livro vivo" if aba_atual == "eureka" else st.session_state.book_em_foco)
    temas_do_livro = carregar_temas(book_em_foco)
    total_paginas = len(temas_do_livro)
    idx_atual = st.session_state.tema_idx_por_book.get(book_em_foco, 0) % total_paginas
    tema_selecionado = temas_do_livro[idx_atual]

    # --- NAVEGAÇÃO SUPERIOR ---
    _, c_plus, c_prev, c_rand, c_next, c_help, _ = st.columns([2, 1, 1, 1, 1, 1, 2])
    if c_plus.button("✚"): st.session_state.seed_eureka += 1; st.rerun()
    if c_prev.button("❰"): st.session_state.tema_idx_por_book[book_em_foco] = (idx_atual - 1) % total_paginas; st.rerun()
    if c_rand.button("✱"): st.session_state.tema_idx_por_book[book_em_foco] = random.randint(0, total_paginas - 1); st.rerun()
    if c_next.button("❱"): st.session_state.tema_idx_por_book[book_em_foco] = (idx_atual + 1) % total_paginas; st.rerun()
    if c_help.button("?"): st.session_state.help_ativo = not st.session_state.help_ativo; st.rerun()

    aba_clicada = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS_APP], default=aba_atual)

    # --- COCKPIT (Sempre visível, centralizado) ---
    st.markdown(f'<div class="cockpit-header">página {idx_atual + 1} de {total_paginas}</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([1, 1.5, 2.5, 1])
    
    idioma = c1.selectbox("L", LISTA_IDIOMAS, label_visibility="collapsed")
    sigla = idioma.split(" - ")[0].lower()
    
    lista_livros = list(MAPA_BOOKS.keys())
    novo_book = c2.selectbox("Livro", lista_livros, index=lista_livros.index(book_em_foco), label_visibility="collapsed")
    if novo_book != book_em_foco:
        st.session_state.book_em_foco = novo_book; st.rerun()

    tema_sel = c3.selectbox("Tema", temas_do_livro, index=idx_atual, label_visibility="collapsed")
    if tema_sel != tema_selecionado:
        st.session_state.tema_idx_por_book[book_em_foco] = temas_do_livro.index(tema_sel); st.rerun()

    st.session_state.com_imagem = c4.toggle("Imagem", value=st.session_state.com_imagem)

    if aba_clicada != aba_atual:
        st.session_state.current_tab_idx = PAGINAS_APP.index(aba_clicada); st.rerun()

    st.markdown("---")

    # --- PALCO CENTRAL (COM ARTE) ---
    if st.session_state.help_ativo or aba_atual == "books":
        path_doc = os.path.join("md_files", f"MANUAL_{aba_atual.upper()}.md")
        if os.path.exists(path_doc):
            with open(path_doc, "r", encoding="utf-8") as f:
                st.markdown(normalizar_e_traduzir(f.read(), idioma))
    elif aba_atual in ["mini", "ypoemas", "eureka"]:
        semente = st.session_state.seed_eureka if aba_atual == "eureka" else ""
        poema = gera_poema(tema_selecionado, semente)
        conteudo_traduzido = normalizar_e_traduzir(poema, idioma)

        if st.session_state.com_imagem:
            col_img, col_txt = st.columns([1, 1.2])
            # Lógica de imagem baseada na aba e no tema selecionado
            img_path = os.path.join("img", aba_atual, f"{tema_selecionado}.png")
            if not os.path.exists(img_path):
                img_path = os.path.join("img", "default.png") # Fallback
            
            if os.path.exists(img_path):
                col_img.image(img_path, use_container_width=True)
            else:
                col_img.info("Arte em processamento...")
            
            col_txt.markdown(f'<div class="poema-container">{conteudo_traduzido}</div>', unsafe_allow_html=True)
        else:
            # Texto centralizado sem imagem
            _, col_central, _ = st.columns([1, 2, 1])
            col_central.markdown(f'<div class="poema-container">{conteudo_traduzido}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

# --- FIM DO ARQUIVO: MÓDULO DE IMAGEM REESTABELECIDO ---
