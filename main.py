import streamlit as st
import extra_streamlit_components as stx
import os
import random
from deep_translator import GoogleTranslator

# CRONOLOGIA ATIVA: RESTAURAÇÃO DE ONTEM (Pré-Pausa / Ponto de Estabilidade)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "base")

def aplicar_estetica():
    st.markdown("""
        <style>
            header[data-testid="stHeader"], footer { visibility: hidden; height: 0px; }
            [data-testid="stSidebar"] { display: none; }
            .block-container { padding-top: 2rem !important; max-width: 90% !important; }
            
            /* Cockpit de Comando */
            .stButton > button { 
                border-radius: 50% !important; width: 42px !important; height: 42px !important; 
                border: 1px solid #eee !important; background: white !important; color: #555 !important;
                box-shadow: 0px 2px 4px rgba(0,0,0,0.05);
            }
            
            /* O Palco Central da Poesia */
            .poema-box { 
                font-family: 'Georgia', serif; font-size: 1.8em; line-height: 1.6; 
                color: #1a1a1a; margin-top: 3rem; padding: 10px; text-align: left;
                border-left: 2px solid #f0f0f0;
            }
        </style>
    """, unsafe_allow_html=True)

def tradutor_na_marra(input_text, target_lang='pt'):
    if not input_text or target_lang == 'pt': return input_text
    try:
        output = GoogleTranslator(source='pt', target=target_lang).translate(text=input_text)
        # Sanitização de quebras para manter a sonoridade
        for tag in ["<br>>", "< br>", "<br >", "<br ", " br>", "</br>", " <br>"]:
            output = output.replace(tag, "<br>")
        return output
    except: return input_text

def listar_livros_reais():
    livros = {}
    if os.path.exists(BASE_PATH):
        arquivos = sorted([f for f in os.listdir(BASE_PATH) if f.startswith("rol_") and f.endswith(".txt")])
        for arq in arquivos:
            nome = arq.replace("rol_", "").replace(".txt", "")
            livros[nome] = arq
    return livros if livros else {"todos os temas": "rol_todos os temas.txt"}

def main():
    st.set_page_config(layout="wide", page_title="Machina Poética")
    aplicar_estetica()

    LIVROS = listar_livros_reais()

    # --- ESTADOS (O Coração da Permanência) ---
    if 'current_tab_idx' not in st.session_state: st.session_state.current_tab_idx = 0 
    if 'book_em_foco' not in st.session_state: st.session_state.book_em_foco = list(LIVROS.keys())[0]
    if 'tema_idx_por_book' not in st.session_state: st.session_state.tema_idx_por_book = {b: 0 for b in LIVROS}
    if 'seed_mutante' not in st.session_state: st.session_state.seed_mutante = 0
    if 'idioma_idx' not in st.session_state: st.session_state.idioma_idx = 0

    PAGINAS = ["demo", "ypoemas", "eureka", "off-máquina", "books", "about"]
    aba_atual = PAGINAS[st.session_state.current_tab_idx]

    aba_sel = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS], default=aba_atual)
    if aba_sel and aba_sel != aba_atual:
        st.session_state.current_tab_idx = PAGINAS.index(aba_sel)
        st.rerun()

    book_foco = "todos os temas" if aba_atual == "demo" else st.session_state.book_em_foco
    
    @st.cache_data
    def get_temas(arquivo):
        caminho = os.path.join(BASE_PATH, arquivo)
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                return [l.strip() for l in f if l.strip() and not l.startswith("[")]
        return ["Silêncio"]

    temas = get_temas(LIVROS.get(book_foco, "rol_todos os temas.txt"))
    idx_tema = st.session_state.tema_idx_por_book.get(book_foco, 0) % len(temas)
    tema_atual = temas[idx_tema]

    # --- COCKPIT (Distribuição de Ontem) ---
    st.markdown("<br>", unsafe_allow_html=True)
    c_p, c_pr, c_ra, c_ne, c_lang, c_esp = st.columns([1, 1, 1, 1, 3, 5])
    
    if c_p.button("✚"): st.session_state.seed_mutante += 1; st.rerun()
    if c_pr.button("❰"): st.session_state.tema_idx_por_book[book_foco] = idx_tema - 1; st.rerun()
    if c_ra.button("✱"): st.session_state.tema_idx_por_book[book_foco] = random.randint(0, len(temas)-1); st.rerun()
    if c_ne.button("❱"): st.session_state.tema_idx_por_book[book_foco] = idx_tema + 1; st.rerun()

    langs = {"Português": "pt", "English": "en", "Español": "es", "Français": "fr", "Italiano": "it"}
    with c_lang:
        st.session_state.idioma_idx = list(langs.keys()).index(
            st.radio("Idiomas", list(langs.keys()), index=st.session_state.idioma_idx, 
                     horizontal=True, label_visibility="collapsed")
        )

    st.selectbox("Tema", temas, index=idx_tema, key=f"sel_{idx_tema}", label_visibility="collapsed")

    st.markdown("---")
    
    # --- PALCO ---
    try:
        from lay_2_ypo import gera_poema
        res = gera_poema(tema_atual, str(st.session_state.seed_mutante))
        txt = ("".join(res) if isinstance(res, list) else str(res)).strip().replace("\n", "<br>")
        
        target = list(langs.values())[st.session_state.idioma_idx]
        txt_final = tradutor_na_marra(txt, target_lang=target)

        st.markdown(f'<div class="poema-box">{txt_final}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Integridade preservada. Erro técnico: {e}")

if __name__ == "__main__":
    main()
    
