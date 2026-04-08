import streamlit as st
import extra_streamlit_components as stx
from deep_translator import GoogleTranslator
from gtts import gTTS # Adicionado para o som
import io
import os
import random

# --- DIRETÓRIO RAIZ (BLINDAGEM APENAS PARA VERIFICAÇÃO DE EXISTÊNCIA) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- [PROTOCOL] MOTOR SOBERANO ---
try:
    from lay_2_ypo import gera_poema
except ImportError:
    def gera_poema(t, s=""): return f"Erro: lay_2_ypo.py não localizado.\nTema: {t}"

def carregar_mapa_imagens():
    mapa = {}
    caminho = os.path.join(BASE_DIR, "base", "images.txt")
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
            .poema-box {
                font-family: serif; 
                font-size: 1.4em;
                line-height: 1.6;
                color: #1a1a1a;
                background-color: transparent;
                padding: 20px;
                white-space: pre-wrap;
            }
            div.stButton > button {
                border-radius: 50% !important;
                width: 48px !important;
                height: 48px !important;
                border: 1px solid #ddd !important;
                background-color: white !important;
                margin: 0 auto !important;
                display: block;
            }
            /* Centralização e ajuste dos widgets do cockpit */
            [data-testid="column"] {
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
            }
            .stSelectbox, .stToggle {
                width: 100% !important;
            }
            hr { margin: 1em 0 !important; }
        </style>
    """, unsafe_allow_html=True)

# --- LÓGICA RESTAURADA DO SALVADOR (Try #1 que funcionava) ---
def buscar_arte_curada(tema, mapa_fotos):
    grupo = mapa_fotos.get(tema, "maquina")
    # Tenta o grupo mapeado, depois tenta 'maquina'
    for g in [grupo, "maquina"]:
        # Verificação física do caminho (BASE_DIR)
        path_fisico = os.path.join(BASE_DIR, "img", g)
        if os.path.exists(path_fisico):
            arquivos = [f for f in os.listdir(path_fisico) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if arquivos:
                # RETORNA APENAS O CAMINHO RELATIVO (A string pura que o Cloud entende)
                return f"img/{g}/{random.choice(arquivos)}"
    return None

def executar_som(texto, idioma_nome):
    try:
        cod_lang = idioma_nome.split(" - ")[0].lower()
        tts = gTTS(text=texto, lang=cod_lang)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        return fp
    except: return None

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
    caminho = os.path.join(BASE_DIR, "base", arquivo)
    if os.path.exists(caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return [l.strip() for l in f if l.strip() and not l.startswith("[")]
        except Exception: pass
    return ["Fatos"]

def main():
    st.set_page_config(layout="wide", page_title="yPoemas")
    aplicar_estetica_machina()

    # Inicialização do Estado
    for key, val in {'current_tab_idx': 1, 'book_em_foco': 'poemas', 'com_imagem': True, 'com_som': False, 'seed_eureka': 0, 'help_ativo': False}.items():
        if key not in st.session_state: st.session_state[key] = val
    if 'tema_idx_por_book' not in st.session_state: st.session_state.tema_idx_por_book = {b: 0 for b in MAPA_BOOKS}

    PAGINAS_APP = ["mini", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
    aba_atual = PAGINAS_APP[st.session_state.current_tab_idx]
    book_em_foco = st.session_state.book_em_foco
    
    temas_do_livro = carregar_temas(book_em_foco)
    idx_atual = st.session_state.tema_idx_por_book.get(book_em_foco, 0) % len(temas_do_livro)
    tema_selecionado = temas_do_livro[idx_atual]
    
    mapa_fotos = carregar_mapa_imagens()

    # --- NAVEGAÇÃO ---
    _, c_plus, c_prev, c_rand, c_next, c_help, _ = st.columns([2, 1, 1, 1, 1, 1, 2])
    
    if c_plus.button("✚", help="gera novo yPoema"): 
        st.session_state.seed_eureka += 1; st.rerun()
    if c_prev.button("❰", help="Página anterior"): 
        st.session_state.tema_idx_por_book[book_em_foco] = (idx_atual - 1); st.rerun()
    if c_rand.button("✱", help="Tema aleatório"): 
        st.session_state.tema_idx_por_book[book_em_foco] = random.randint(0, len(temas_do_livro)-1); st.rerun()
    if c_next.button("❱", help="Próxima página"): 
        st.session_state.tema_idx_por_book[book_em_foco] = (idx_atual + 1); st.rerun()
    if c_help.button("?", help="menu de ajuda"): 
        st.session_state.help_ativo = not st.session_state.help_ativo; st.rerun()

    aba_clicada = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS_APP], default=aba_atual)
    if aba_clicada != aba_atual:
        st.session_state.current_tab_idx = PAGINAS_APP.index(aba_clicada); st.rerun()

    # --- COCKPIT CENTRALIZADO ---
    _, col_idioma, col_livro, col_tema, col_arte, col_som, _ = st.columns([1, 2, 2, 2, 1, 1, 1])
    
    with col_idioma:
        idioma = st.selectbox("Idioma", LISTA_IDIOMAS, label_visibility="collapsed")
    
    with col_livro:
        novo_book = st.selectbox("Livro", list(MAPA_BOOKS.keys()), index=list(MAPA_BOOKS.keys()).index(book_em_foco), label_visibility="collapsed")
        if novo_book != book_em_foco: 
            st.session_state.book_em_foco = novo_book
            st.rerun()
    
    with col_tema:
        tema_sel = st.selectbox("Tema", temas_do_livro, index=idx_atual, label_visibility="collapsed")
        if tema_sel != tema_selecionado: 
            st.session_state.tema_idx_por_book[book_em_foco] = temas_do_livro.index(tema_sel)
            st.rerun()
    
    with col_arte:
        st.session_state.com_imagem = st.toggle("Arte", value=st.session_state.com_imagem)

    with col_som:
        st.session_state.com_som = st.toggle("Som", value=st.session_state.com_som)

    st.markdown("---")

    # --- PALCO CENTRAL ---
    if st.session_state.help_ativo:
        path_doc = os.path.join(BASE_DIR, "md_files", f"MANUAL_{aba_atual.upper()}.md")
        if os.path.exists(path_doc):
            with open(path_doc, "r", encoding="utf-8") as f:
                st.markdown(normalizar_e_traduzir(f.read(), idioma))
    else:
        semente = st.session_state.seed_eureka if aba_atual == "eureka" else ""
        poema = gera_poema(tema_selecionado, semente)
        txt = normalizar_e_traduzir(poema, idioma)

        # Execução do som (se ativo)
        if st.session_state.com_som:
            audio_fp = executar_som(txt, idioma)
            if audio_fp:
                st.audio(audio_fp, format='audio/mp3')

        if st.session_state.com_imagem:
            col_img, col_txt = st.columns([1, 2])
            arte = buscar_arte_curada(tema_selecionado, mapa_fotos)
            if arte: 
                # Lógica restaurada: st.image usando o caminho relativo (string)
                col_img.image(arte, use_container_width=True)
            col_txt.markdown(f'<div class="poema-box">{txt}</div>', unsafe_allow_html=True)
        else:
            _, col_central, _ = st.columns([1, 4, 1])
            col_central.markdown(f'<div class="poema-box" style="text-align: center;">{txt}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
