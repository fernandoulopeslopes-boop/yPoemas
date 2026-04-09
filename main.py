import streamlit as st
import extra_streamlit_components as stx
from deep_translator import GoogleTranslator
from gtts import gTTS
import io
import os
import random

# --- DIRETÓRIO RAIZ ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- [PROTOCOL] MOTOR SOBERANO ---
try:
    from lay_2_ypo import gera_poema
except ImportError:
    def gera_poema(t, s=""): return f"Erro: lay_2_ypo.py não localizado.\nTema: {t}"

# --- CACHE DE SISTEMA (PERFORMANCE & FLUIDEZ) ---
@st.cache_data
def load_images_list_cached():
    caminho = os.path.join(BASE_DIR, "base", "images.txt")
    if os.path.exists(caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return f.readlines()
        except: pass
    return []

@st.cache_data
def carregar_temas_cached(arquivo_nome):
    caminho = os.path.join(BASE_DIR, "base", arquivo_nome)
    if os.path.exists(caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return [l.strip() for l in f if l.strip() and not l.startswith("[")]
        except: pass
    return ["Fatos"]

def load_arts(nome_tema):
    path = "./images/machina/"
    path_list = load_images_list_cached()
    for line in path_list:
        if line.startswith(nome_tema):
            this_line = line.strip("\n")
            part_line = this_line.partition(" : ")
            if nome_tema == part_line[0]:
                path = "./images/" + part_line[2] + "/"
                break
    if not os.path.exists(path): return None
    arts_list = [f for f in os.listdir(path) if f.lower().endswith((".jpg", ".png", ".jpeg"))]
    if not arts_list: return None
    
    if 'arts' not in st.session_state: st.session_state.arts = []
    image = random.choice(arts_list)
    
    intentos = 0
    while image in st.session_state.arts and intentos < 10:
        image = random.choice(arts_list)
        intentos += 1
        
    st.session_state.arts.append(image)
    if len(st.session_state.arts) > 36: del st.session_state.arts[0]
    return path + image

def normalizar_e_traduzir(conteudo, idioma_nome):
    if not conteudo: return ""
    texto_bruto = "\n".join(conteudo) if isinstance(conteudo, list) else conteudo
    cod_target = idioma_nome.split(" - ")[0].lower()
    if cod_target == "pt": return texto_bruto.strip()
    try:
        return GoogleTranslator(source='auto', target=cod_target).translate(texto_bruto).replace('\r\n', '\n').strip()
    except: return texto_bruto.strip()

def aplicar_estetica_machina():
    st.markdown("""
        <style>
            header[data-testid="stHeader"] { visibility: hidden; height: 0px; }
            footer { visibility: hidden; }
            [data-testid="stSidebar"] { display: none; }
            .block-container { padding-top: 1.5rem !important; padding-left: 5% !important; padding-right: 5% !important; max-width: 100% !important; }
            .titulo-poema { font-family: serif; font-size: 2.2em; font-weight: bold; color: #333; margin-bottom: 1.5rem; text-align: center; }
            .poema-box { font-family: serif; font-size: 1.4em; line-height: 1.6; color: #1a1a1a; white-space: pre-wrap; }
            div.stButton > button { border-radius: 50% !important; width: 48px !important; height: 48px !important; border: 1px solid #ddd !important; background-color: white !important; margin: 0 auto !important; display: block; }
            .stSelectbox div[data-baseweb="select"] { cursor: pointer; }
            [data-testid="column"] { display: flex; align-items: center; justify-content: center; }
            hr { margin: 1em 0 !important; }
        </style>
    """, unsafe_allow_html=True)

def limpar_para_audio(t):
    ruidos = ['"', '*', '_', '[', ']', '(', ')', '«', '»', '—']
    for r in ruidos: t = t.replace(r, '')
    return t.strip()

def executar_som(texto, idioma_nome):
    try:
        texto_limpo = limpar_para_audio(texto)
        tts = gTTS(text=texto_limpo, lang=idioma_nome.split(" - ")[0].lower())
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        return fp
    except: return None

# --- MAPA DE LIVROS ---
MAPA_BOOKS = {
    "todos os temas": "rol_todos os temas.txt", 
    "livro vivo": "rol_livro_vivo.txt", 
    "ensaios": "rol_ensaios.txt", 
    "jocosos": "rol_jocosos.txt", 
    "variações": "rol_variações.txt", 
    "metalinguagem": "rol_metalinguagem.txt",
    "sociais": "rol_sociais.txt", 
    "outros autores": "rol_outros autores.txt",
    "todos os signos": "rol_todos os signos.txt", 
    "temas mini": "rol_temas_mini.txt"
}

LISTA_IDIOMAS = [
    "PT - Português", "ES - Español", "IT - Italiano", "FR - French", "EN - English", "CA - Catalan",
    "AF - Afrikaans", "SQ - Albanian", "DE - German", "HR - Croatian", "DA - Danish", 
    "SK - Slovak", "SL - Slovenian", "ET - Estonian", "FI - Finnish", "HU - Hungarian", 
    "IS - Icelandic", "ID - Indonesian", "LV - Latvian", "LT - Lithuanian", "NO - Norwegian", 
    "NL - Dutch", "PL - Polish", "RO - Romanian", "SW - Swahili", "SV - Swedish", 
    "TR - Turkish", "VI - Vietnamese"
]

def main():
    st.set_page_config(layout="wide", page_title="yPoemas")
    aplicar_estetica_machina()

    # --- INITIAL STATE ---
    if 'current_tab_idx' not in st.session_state: st.session_state.current_tab_idx = 1 # Inicia agora em yPoemas
    if 'book_em_foco' not in st.session_state: st.session_state.book_em_foco = 'todos os temas'
    if 'com_imagem' not in st.session_state: st.session_state.com_imagem = True
    if 'com_som' not in st.session_state: st.session_state.com_som = False
    if 'seed_eureka' not in st.session_state: st.session_state.seed_eureka = 0
    if 'help_ativo' not in st.session_state: st.session_state.help_ativo = False
    if 'tema_idx_por_book' not in st.session_state: st.session_state.tema_idx_por_book = {b: 0 for b in MAPA_BOOKS}

    PAGINAS_APP = ["demo", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
    aba_atual = PAGINAS_APP[st.session_state.current_tab_idx]

    # --- ABAS ---
    aba_clicada = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS_APP], default=aba_atual)
    if aba_clicada and aba_clicada != aba_atual:
        st.session_state.current_tab_idx = PAGINAS_APP.index(aba_clicada)
        st.rerun()

    # --- LÓGICA DE CONTEXTO ---
    # Na yPoemas, respeitamos o st.session_state.book_em_foco. Na Demo, forçamos.
    book_em_foco = "todos os temas" if aba_atual == "demo" else st.session_state.book_em_foco
    
    arquivo_alvo = MAPA_BOOKS.get(book_em_foco, "rol_todos os temas.txt")
    temas_do_livro = carregar_temas_cached(arquivo_alvo)
    
    idx_atual = st.session_state.tema_idx_por_book.get(book_em_foco, 0) % len(temas_do_livro)
    tema_selecionado = temas_do_livro[idx_atual]

    # --- NAVEGAÇÃO ---
    _, c_plus, c_prev, c_rand, c_next, c_help, _ = st.columns([2, 1, 1, 1, 1, 1, 2])
    if c_plus.button("✚", help="Novo yPoema"): st.session_state.seed_eureka += 1; st.rerun()
    if c_prev.button("❰", help="Anterior"): st.session_state.tema_idx_por_book[book_em_foco] = (idx_atual - 1); st.rerun()
    if c_rand.button("✱", help="Aleatório"): st.session_state.tema_idx_por_book[book_em_foco] = random.randint(0, len(temas_do_livro)-1); st.rerun()
    if c_next.button("❱", help="Próximo"): st.session_state.tema_idx_por_book[book_em_foco] = (idx_atual + 1); st.rerun()
    if c_help.button("?", help="Ajuda"): st.session_state.help_ativo = not st.session_state.help_ativo; st.rerun()

    # --- COCKPIT ---
    _, col_arte, col_idioma, col_livro, col_tema, col_som, _ = st.columns([0.5, 1, 2, 2, 2, 1, 0.5])
    with col_arte: st.session_state.com_imagem = st.toggle("Arte", value=st.session_state.com_imagem)
    with col_idioma: idioma = st.selectbox("Idioma", LISTA_IDIOMAS, label_visibility="collapsed")
    with col_livro:
        def m_livro(): st.session_state.book_em_foco = st.session_state.bk_tmp
        st.selectbox("Livro", list(MAPA_BOOKS.keys()), index=list(MAPA_BOOKS.keys()).index(book_em_foco), 
                     key="bk_tmp", on_change=m_livro, label_visibility="collapsed", disabled=(aba_atual=="demo"))
    with col_tema:
        def m_tema(): st.session_state.tema_idx_por_book[book_em_foco] = temas_do_livro.index(st.session_state.tm_tmp)
        st.selectbox("Tema", temas_do_livro, index=idx_atual, key="tm_tmp", on_change=m_tema, label_visibility="collapsed")
    with col_som: st.session_state.com_som = st.toggle("Som", value=st.session_state.com_som)

    st.markdown("---")

    # --- PALCO CENTRAL ---
    if not st.session_state.help_ativo:
        try:
            semente = st.session_state.seed_eureka if aba_atual == "eureka" else ""
            poema = gera_poema(tema_selecionado, semente)
            txt = normalizar_e_traduzir(poema, idioma)
            
            if st.session_state.com_som:
                audio_fp = executar_som(txt, idioma)
                if audio_fp: st.audio(audio_fp, format='audio/mp3')

            if st.session_state.com_imagem:
                col_img, col_txt = st.columns([1, 2])
                with col_txt:
                    st.markdown(f'<div class="titulo-poema">{tema_selecionado}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="poema-box">{txt}</div>', unsafe_allow_html=True)
                with col_img:
                    c_arte = load_arts(tema_selecionado)
                    if c_arte: st.image(c_arte, use_container_width=True)
            else:
                _, col_c, _ = st.columns([1, 4, 1])
                with col_c:
                    st.markdown(f'<div class="titulo-poema">{tema_selecionado}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="poema-box">{txt}</div>', unsafe_allow_html=True)
        except Exception:
            st.error(f"Erro no motor ao processar o tema: {tema_selecionado}")
    else:
        p_doc = os.path.join(BASE_DIR, "md_files", f"MANUAL_{aba_atual.upper()}.md")
        if os.path.exists(p_doc):
            with open(p_doc, "r", encoding="utf-8") as f:
                st.markdown(normalizar_e_traduzir(f.read(), idioma))

if __name__ == "__main__":
    main()
