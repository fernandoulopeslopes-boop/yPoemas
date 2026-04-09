import streamlit as st
import extra_streamlit_components as stx
import os
import random
from deep_translator import GoogleTranslator

# CRONOLOGIA ATIVA: X=10 (v2.6 - FOCO EM RESULTADO VISUAL E FUNCIONAMENTO)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "base")

def aplicar_estetica_machina():
    st.markdown("""
        <style>
            header[data-testid="stHeader"], footer { visibility: hidden; height: 0px; }
            [data-testid="stSidebar"] { display: none; }
            .block-container { padding-top: 1.5rem !important; }
            
            /* Cockpit: Botões Circulares Minimalistas */
            .stButton > button { 
                border-radius: 50% !important; width: 44px !important; height: 44px !important; 
                border: 1px solid #ddd !important; background-color: #ffffff !important;
                color: #444 !important; transition: all 0.2s ease-in-out;
            }
            .stButton > button:hover { border-color: #888 !important; transform: scale(1.05); }

            /* Palco: Preservação de Sonoridade e Estética */
            .poema-box { 
                font-family: 'Georgia', serif; font-size: 1.8em; line-height: 1.65; 
                color: #121212; margin-top: 2.5rem; padding: 25px; 
                border-left: 3px solid #f0f0f0; text-align: left;
            }
        </style>
    """, unsafe_allow_html=True)

def sanitizar_na_marra(texto):
    if not texto: return ""
    rep = {"<br>>": "<br>", "< br>": "<br>", "<br >": "<br>", "<br ": "<br>", " br>": "<br>", "</br>": "<br>"}
    for erro, acerto in rep.items():
        texto = texto.replace(erro, acerto)
    return texto

def tradutor_fiel(input_text, target_lang='pt'):
    if not input_text or target_lang == 'pt': return input_text
    try:
        traducao = GoogleTranslator(source='pt', target=target_lang).translate(text=input_text)
        return sanitizar_na_marra(traducao)
    except: return input_text

def listar_livros_reais():
    livros = {}
    if os.path.exists(BASE_PATH):
        arquivos = sorted([f for f in os.listdir(BASE_PATH) if f.startswith("rol_") and f.endswith(".txt")])
        for arq in arquivos:
            nome_display = arq.replace("rol_", "").replace(".txt", "")
            livros[nome_display] = arq
    return livros if livros else {"todos os temas": "rol_todos os temas.txt"}

def main():
    st.set_page_config(layout="wide", page_title="Machina Poética Nova")
    aplicar_estetica_machina()

    LIVROS = listar_livros_reais()
    
    # --- GESTÃO DE ESTADO ---
    if 'current_tab_idx' not in st.session_state: st.session_state.current_tab_idx = 0 
    if 'book_em_foco' not in st.session_state: st.session_state.book_em_foco = list(LIVROS.keys())[0]
    if 'tema_idx_por_book' not in st.session_state: st.session_state.tema_idx_por_book = {b: 0 for b in LIVROS}
    if 'idioma_nome' not in st.session_state: st.session_state.idioma_nome = 'Português'
    if 'seed_mutante' not in st.session_state: st.session_state.seed_mutante = 0

    PAGINAS = ["demo", "ypoemas", "eureka", "off-máquina", "books", "about"]
    aba_atual = PAGINAS[st.session_state.current_tab_idx]
    
    aba_sel = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS], default=aba_atual)
    if aba_sel and aba_sel != aba_atual:
        st.session_state.current_tab_idx = PAGINAS.index(aba_sel)
        st.rerun()

    book_foco = "todos os temas" if aba_atual == "demo" else st.session_state.book_em_foco
    
    @st.cache_data
    def load_temas_do_disco(arquivo):
        caminho = os.path.join(BASE_PATH, arquivo)
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                return [l.strip() for l in f if l.strip() and not l.startswith("[")]
        return ["Silêncio"]

    temas_disponiveis = load_temas_do_disco(LIVROS.get(book_foco, "rol_todos os temas.txt"))
    idx_tema = st.session_state.tema_idx_por_book.get(book_foco, 0) % len(temas_disponiveis)
    tema_atual = temas_disponiveis[idx_tema]

    # --- COCKPIT ---
    st.markdown("<br>", unsafe_allow_html=True)
    c_l, c_p, c_pr, c_ra, c_ne, c_lang, c_r = st.columns([2, 0.5, 0.5, 0.5, 0.5, 2.5, 2])
    
    if c_p.button("✚"): st.session_state.seed_mutante += 1; st.rerun()
    if c_pr.button("❰"): st.session_state.tema_idx_por_book[book_foco] = idx_tema - 1; st.rerun()
    if c_ra.button("✱"): st.session_state.tema_idx_por_book[book_foco] = random.randint(0, len(temas_disponiveis)-1); st.rerun()
    if c_ne.button("❱"): st.session_state.tema_idx_por_book[book_foco] = idx_tema + 1; st.rerun()

    with c_lang:
        idiomas = {'Português': 'pt', 'English': 'en', 'Español': 'es', 'Français': 'fr', 'Italiano': 'it', 'Deutsch': 'de'}
        st.session_state.idioma_nome = st.selectbox("I", list(idiomas.keys()), 
                                                   index=list(idiomas.keys()).index(st.session_state.idioma_nome),
                                                   label_visibility="collapsed")

    def sync_selector():
        st.session_state.tema_idx_por_book[book_foco] = temas_disponiveis.index(st.session_state[f"sel_box_{idx_tema}"])

    st.selectbox("T", temas_disponiveis, index=idx_tema, key=f"sel_box_{idx_tema}", on_change=sync_selector, label_visibility="collapsed")

    st.markdown("---")
    
    # --- PALCO CENTRAL ---
    try:
        from lay_2_ypo import gera_poema
        poema_bruto = gera_poema(tema_atual, str(st.session_state.seed_mutante))
        txt_raw = ("".join(poema_bruto) if isinstance(poema_bruto, list) else str(poema_bruto)).strip()
        
        txt_html_base = txt_raw.replace("\n", "<br>")
        poema_final = tradutor_fiel(txt_html_base, target_lang=idiomas[st.session_state.idioma_nome])

        st.markdown(f'<div class="poema-box">{poema_final}</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Erro no palco: {e}")

if __name__ == "__main__":
    main()
