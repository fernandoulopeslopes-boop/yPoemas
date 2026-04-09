import streamlit as st
import extra_streamlit_components as stx
import os
import random
from deep_translator import GoogleTranslator

# CRONOLOGIA ATIVA: X=10 (v2.0 - Sincronia de Idiomas & Sanitização Obsessiva)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- MOTOR DE TRADUÇÃO (MODO SEGURO) ---
def tradutor_na_marra(input_text, target_lang='pt'):
    # Mapeamento para o deep-translator
    lang_map = {"PT": "pt", "EN": "en", "ES": "es"}
    target = lang_map.get(target_lang, "pt")
    
    if not input_text or target == 'pt':
        return input_text
    
    try:
        # Tradução mantendo as tags <br>
        output_text = GoogleTranslator(source='pt', target=target).translate(text=input_text)
        
        # O "Vício" da Sanitização: Limpeza de alucinações do tradutor
        rep = {
            "<br>>": "<br>", "< br>": "<br>", "<br >": "<br>", 
            "<br ": "<br>", " br>": "<br>", "</br>": "<br>", 
            "<Br>": "<br>", "<BR>": "<br>"
        }
        for old, new in rep.items():
            output_text = output_text.replace(old, new)
        
        return output_text
    except:
        return input_text

# --- MOTOR DE POESIA ---
try:
    from lay_2_ypo import gera_poema
except ImportError:
    def gera_poema(t, s=""): return f"Erro: Motor não localizado.\nTema: {t}"

# --- DADOS ---
@st.cache_data
def carregar_temas_cached(arquivo_nome):
    caminho = os.path.join(BASE_DIR, "base", arquivo_nome)
    if os.path.exists(caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return [l.strip() for l in f if l.strip() and not l.startswith("[")]
        except: pass
    return ["Fatos"]

# --- INTERFACE ---
def aplicar_estetica_machina():
    st.markdown("""
        <style>
            header[data-testid="stHeader"], footer { visibility: hidden; height: 0px; }
            [data-testid="stSidebar"] { display: none; }
            .block-container { padding-top: 1rem !important; max-width: 100% !important; }
            .stButton > button { 
                border-radius: 50% !important; width: 42px !important; height: 42px !important; 
                border: 1px solid #eee !important; background: white !important; color: #555 !important;
            }
            .poema-box { 
                font-family: 'Georgia', serif; font-size: 1.7em; line-height: 1.6; 
                color: #1a1a1a; margin-top: 2rem; padding: 15px; text-align: left;
            }
            .lang-text { font-family: sans-serif; font-size: 0.8em; color: #888; margin-bottom: 5px; }
        </style>
    """, unsafe_allow_html=True)

MAPA_BOOKS = {
    "todos os temas": "rol_todos os temas.txt", "livro vivo": "rol_livro_vivo.txt", 
    "ensaios": "rol_ensaios.txt", "jocosos": "rol_jocosos.txt", "variações": "rol_variações.txt", 
    "metalinguagem": "rol_metalinguagem.txt", "sociais": "rol_sociais.txt", 
    "outros autores": "rol_outros autores.txt", "todos os signos": "rol_todos os signos.txt", 
    "temas mini": "rol_temas_mini.txt"
}

def main():
    st.set_page_config(layout="wide", page_title="yPoemas")
    aplicar_estetica_machina()

    # --- ESTADOS ---
    if 'current_tab_idx' not in st.session_state: st.session_state.current_tab_idx = 0 
    if 'book_em_foco' not in st.session_state: st.session_state.book_em_foco = 'todos os temas'
    if 'tema_idx_por_book' not in st.session_state: st.session_state.tema_idx_por_book = {b: 0 for b in MAPA_BOOKS}
    if 'idioma' not in st.session_state: st.session_state.idioma = 'PT'
    if 'seed_mutante' not in st.session_state: st.session_state.seed_mutante = 0

    PAGINAS_APP = ["demo", "ypoemas", "eureka", "off-máquina", "books", "comments", "about"]
    aba_atual = PAGINAS_APP[st.session_state.current_tab_idx]

    # Barra de abas
    aba_clicada = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS_APP], default=aba_atual)
    if aba_clicada and aba_clicada != aba_atual:
        st.session_state.current_tab_idx = PAGINAS_APP.index(aba_clicada)
        st.rerun()

    book_foco = "todos os temas" if aba_atual == "demo" else st.session_state.book_em_foco
    lista_temas = carregar_temas_cached(MAPA_BOOKS.get(book_foco, "rol_todos os temas.txt"))
    idx_tema = st.session_state.tema_idx_por_book.get(book_foco, 0) % len(lista_temas)
    tema_atual = lista_temas[idx_tema]

    # --- COCKPIT ---
    st.markdown("<br>", unsafe_allow_html=True)
    c_l, c_p, c_pr, c_ra, c_ne, c_lang, c_r = st.columns([2, 0.5, 0.5, 0.5, 0.5, 2, 2])
    
    if c_p.button("✚"): st.session_state.seed_mutante += 1; st.rerun()
    if c_pr.button("❰"): st.session_state.tema_idx_por_book[book_foco] = idx_tema - 1; st.rerun()
    if c_ra.button("✱"): st.session_state.tema_idx_por_book[book_foco] = random.randint(0, len(lista_temas)-1); st.rerun()
    if c_ne.button("❱"): st.session_state.tema_idx_por_book[book_foco] = idx_tema + 1; st.rerun()

    with c_lang:
        # Seletor de Idioma Obsessivo
        opcoes_idioma = ["PT", "EN", "ES"]
        st.session_state.idioma = st.radio(
            "Idioma", opcoes_idioma, 
            index=opcoes_idioma.index(st.session_state.idioma),
            horizontal=True, label_visibility="collapsed"
        )

    st.selectbox("Tema", lista_temas, index=idx_tema, key=f"sel_{idx_tema}", label_visibility="collapsed")

    # --- PALCO CENTRAL ---
    st.markdown("---")
    
    try:
        # 1. Geração Original
        res_bruto = gera_poema(tema_atual, str(st.session_state.seed_mutante))
        txt_raw = "".join(res_bruto) if isinstance(res_bruto, list) else str(res_bruto)
        
        # 2. Preparação Estrutural (Linhas -> HTML)
        txt_com_breaks = txt_raw.strip().replace("\n", "<br>")
        
        # 3. Tradução com Sanitização de "Segredinhos"
        txt_final = tradutor_na_marra(txt_com_breaks, target_lang=st.session_state.idioma)

        st.markdown(f'<div class="poema-box">{txt_final}</div>', unsafe_allow_html=True)
    except:
        st.error("A Machina exige silêncio para processar.")

if __name__ == "__main__":
    main()
