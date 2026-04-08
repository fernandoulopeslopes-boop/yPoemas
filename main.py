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

def carregar_mapa_imagens():
    """Lê a curadoria exata de base/images.txt"""
    mapa = {}
    caminho = os.path.join("base", "images.txt")
    if os.path.exists(caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                for linha in f:
                    if "=" in linha:
                        tema, grupo = linha.split("=")
                        mapa[tema.strip()] = grupo.strip()
        except Exception: pass
    return mapa

def normalizar_e_traduzir(conteudo, idioma_nome):
    if not conteudo: return ""
    texto_unificado = "\n".join(conteudo) if isinstance(conteudo, list) else conteudo
    cod_target = idioma_nome.split(" - ")[0].lower()
    if cod_target == "pt":
        return texto_unificado.replace('\r\n', '\n').replace('\n\n', '\n').strip()
    try:
        texto_final = GoogleTranslator(source='auto', target=cod_target).translate(texto_unificado)
        return texto_final.replace('\r\n', '\n').replace('\n\n', '\n').strip()
    except Exception: return texto_unificado

def aplicar_estetica_machina():
    st.markdown("""
        <style>
            header[data-testid="stHeader"] { visibility: hidden; height: 0px; }
            footer { visibility: hidden; }
            [data-testid="stSidebar"] { display: none; }
            
            .block-container { 
                padding-top: 1.5rem !important; 
                padding-left: 5% !important; 
                padding-right: 5% !important; 
                max-width: 100% !important;
            }
            
            /* Container do Poema - Esmero na Legibilidade */
            .poema-box {
                font-family: serif; /* Sob análise: serifado para teste de leitura */
                font-size: 1.35em;
                line-height: 1.6;
                color: #1a1a1a;
                background-color: transparent;
                padding: 20px;
                white-space: pre-wrap;
                word-wrap: break-word;
            }

            /* Estilo dos Botões da Navegação */
            div.stButton > button {
                border-radius: 50% !important;
                width: 48px !important;
                height: 48px !important;
                border: 1px solid #ddd !important;
                background-color: white !important;
                margin: 0 auto !important;
                display: block;
                font-size: 1.2em !important;
            }
            
            .cockpit-info { 
                font-size: 0.8em; 
                font-weight: bold; 
                color: #999; 
                text-align: center;
                font-family: monospace; 
                text-transform: lowercase;
                margin-bottom: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

def buscar_arte_curada(tema, mapa_fotos):
    grupo = mapa_fotos.get(tema, "maquina")
    for g in [grupo, "maquina"]:
        path_pasta = os.path.join("img", g)
        if os.path.exists(path_pasta):
            arquivos = [f for f in os.listdir(path_pasta) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if arquivos: return os.path.join(path_pasta, random.choice(arquivos))
    return None

MAPA_BOOKS = {
    "livro vivo": "rol_livro_vivo.txt", "poemas": "rol_poemas.txt", "ensaios": "rol_ensaios.txt",
    "jocosos": "rol_jocosos.txt", "variações": "rol_variações.txt", "metalinguagem": "rol_metalinguagem.txt",
    "sociais": "rol_sociais.txt", "outros autores": "rol_outros autores.txt",
    "todos os temas": "rol_poemas.txt", "todos os signos": "rol_todos os signos.txt", "temas mini": "rol_temas_mini.txt"
}

LISTA_IDIOMAS = ["PT - Português", "EN - English", "ES - Español", "IT - Italiano", "FR - French", "DE - German"]

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
    st.set_page_config(layout="wide", page_title="yPoemas")
    aplicar_estetica_machina()

    # Session State
    if 'current_tab_idx' not in st.session_state: st.session_state.current_tab_idx = 1
    if 'book_em_foco' not in st.session_state: st.session_state.book_em_foco = "poemas"
    if 'tema_idx_por_book' not in st.session_state: st.session_state.tema_idx_por_book = {b: 0 for b in MAPA_BOOKS}
    if 'com_imagem' not in st.session_state: st.session_state.com_imagem = True
    if 'seed_eureka' not in st.session_state: st.session_state.seed_eureka = 0
    if 'help_ativo' not in st.session_state: st.session_state.help_ativo = False

    PAGINAS_APP = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
    aba_atual = PAGINAS_APP[st.session_state.current_tab_idx]
    book_em_foco = st.session_state.book_em_foco
    
    temas_do_livro = carregar_temas(book_em_foco)
    idx_atual = st.session_state.tema_idx_por_book.get(book_em_foco, 0) % len(temas_do_livro)
    tema_selecionado = temas_do_livro[idx_atual]
    
    mapa_fotos = carregar_mapa_imagens()

    # --- NAVEGAÇÃO ---
    _, c_plus, c_prev, c_rand, c_next, c_help, _ = st.columns([2, 1, 1, 1, 1, 1, 2])
    if c_plus.button("✚", help="Nova semente"): st.session_state.seed_eureka += 1; st.rerun()
    if c_prev.button("❰", help="Anterior"): st.session_state.tema_idx_por_book[book_em_foco] = (idx_atual - 1); st.rerun()
    if c_rand.button("✱", help="Aleatório"): st.session_state.tema_idx_por_book[book_em_foco] = random.randint(0, len(temas_do_livro)-1); st.rerun()
    if c_next.button("❱", help="Próximo"): st.session_state.tema_idx_por_book[book_em_foco] = (idx_atual + 1); st.rerun()
    if c_help.button("?", help="Manual"): st.session_state.help_ativo = not st.session_state.help_ativo; st.rerun()

    aba_clicada = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS_APP], default=aba_atual)
    if aba_clicada != aba_atual:
        st.session_state.current_tab_idx = PAGINAS_APP.index(aba_clicada); st.rerun()

    # --- COCKPIT ---
    c1, c2, c3, c4 = st.columns([1, 1.5, 2.5, 1])
    idioma = c1.selectbox("L", LISTA_IDIOMAS, label_visibility="collapsed")
    novo_book = c2.selectbox("B", list(MAPA_BOOKS.keys()), index=list(MAPA_BOOKS.keys()).index(book_em_foco), label_visibility="collapsed")
    if novo_book != book_em_foco: st.session_state.book_em_foco = novo_book; st.rerun()
    
    tema_sel = c3.selectbox("T", temas_do_livro, index=idx_atual, label_visibility="collapsed")
    if tema_sel != tema_selecionado: st.session_state.tema_idx_por_book[book_em_foco] = temas_do_livro.index(tema_sel); st.rerun()
    
    st.session_state.com_imagem = c4.toggle("Arte", value=st.session_state.com_imagem)

    st.markdown(f'<div class="cockpit-info">{book_em_foco} | {tema_selecionado} ({idx_atual+1}/{len(temas_do_livro)})</div>', unsafe_allow_html=True)
    st.markdown("---")

    # --- PALCO CENTRAL DINÂMICO ---
    if st.session_state.help_ativo:
        path_doc = os.path.join("md_files", f"MANUAL_{aba_atual.upper()}.md")
        if os.path.exists(path_doc):
            with open(path_doc, "r", encoding="utf-8") as f:
                st.markdown(normalizar_e_traduzir(f.read(), idioma))
    else:
        semente = st.session_state.seed_eureka if aba_atual == "eureka" else ""
        poema = gera_poema(tema_selecionado, semente)
        txt = normalizar_e_traduzir(poema, idioma)

        if st.session_state.com_imagem:
            # Layout Proporcional 1/3 (Imagem) e 2/3 (Texto)
            col_img, col_txt = st.columns([1, 2])
            arte = buscar_arte_curada(tema_selecionado, mapa_fotos)
            if arte: col_img.image(arte, use_container_width=True)
            col_txt.markdown(f'<div class="poema-box">{txt}</div>', unsafe_allow_html=True)
        else:
            # Layout Centralizado (Else) - Container Único
            _, col_central, _ = st.columns([1, 4, 1])
            col_central.markdown(f'<div class="poema-box" style="text-align: center;">{txt}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
