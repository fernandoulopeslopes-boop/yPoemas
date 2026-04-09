import streamlit as st
import extra_streamlit_components as stx
import os
import random
from deep_translator import GoogleTranslator

# CRONOLOGIA ATIVA: X=08 (RESTAURAÇÃO PROFUNDA: Versão de Equilíbrio Cockpit/Palco)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "base")

# --- SANITIZAÇÃO "NA MARRA" (RECUPERADA) ---
def tradutor_na_marra(input_text, target_lang='pt'):
    if not input_text or target_lang == 'pt': return input_text
    try:
        output_text = GoogleTranslator(source='pt', target=target_lang).translate(text=input_text)
        # Limpeza essencial de tags para manter a sonoridade
        rep = {"<br>>": "<br>", "< br>": "<br>", "<br >": "<br>", "<br ": "<br>", " br>": "<br>", "</br>": "<br>"}
        for old, new in rep.items():
            output_text = output_text.replace(old, new)
        return output_text
    except: return input_text

# --- NAVEGAÇÃO DE ARQUIVOS ROL_ ---
def listar_livros_reais():
    livros = {}
    if os.path.exists(BASE_PATH):
        arquivos = sorted([f for f in os.listdir(BASE_PATH) if f.startswith("rol_") and f.endswith(".txt")])
        for arq in arquivos:
            nome_limpo = arq.replace("rol_", "").replace(".txt", "")
            livros[nome_limpo] = arq
    return livros if livros else {"todos os temas": "rol_todos os temas.txt"}

def aplicar_estetica():
    st.markdown("""
        <style>
            header[data-testid="stHeader"], footer { visibility: hidden; height: 0px; }
            [data-testid="stSidebar"] { display: none; }
            .block-container { padding-top: 1rem !important; }
            
            /* Botões do Cockpit */
            .stButton > button { 
                border-radius: 50% !important; width: 42px !important; height: 42px !important; 
                border: 1px solid #eee !important; background: white !important; color: #555 !important;
            }
            
            /* O Palco Central */
            .poema-box { 
                font-family: 'Georgia', serif; font-size: 1.7em; line-height: 1.6; 
                color: #1a1a1a; margin-top: 2rem; padding: 10px; text-align: left;
            }
        </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(layout="wide", page_title="yPoemas")
    aplicar_estetica()

    LIVROS_DISPONIVEIS = listar_livros_reais()

    # --- ESTADOS SOBERANOS ---
    if 'current_tab_idx' not in st.session_state: st.session_state.current_tab_idx = 0 
    if 'book_em_foco' not in st.session_state: st.session_state.book_em_foco = list(LIVROS_DISPONIVEIS.keys())[0]
    if 'tema_idx_por_book' not in st.session_state: st.session_state.tema_idx_por_book = {b: 0 for b in LIVROS_DISPONIVEIS}
    if 'seed_mutante' not in st.session_state: st.session_state.seed_mutante = 0

    PAGINAS = ["demo", "ypoemas", "eureka", "off-máquina", "books", "about"]
    aba_atual = PAGINAS[st.session_state.current_tab_idx]

    aba_sel = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS], default=aba_atual)
    if aba_sel and aba_sel != aba_atual:
        st.session_state.current_tab_idx = PAGINAS.index(aba_sel)
        st.rerun()

    book_foco = "todos os temas" if aba_atual == "demo" else st.session_state.book_em_foco
    
    @st.cache_data
    def load_temas(arquivo):
        caminho = os.path.join(BASE_PATH, arquivo)
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                return [l.strip() for l in f if l.strip() and not l.startswith("[")]
        return ["Silêncio"]

    lista_temas = load_temas(LIVROS_DISPONIVEIS.get(book_foco, "rol_todos os temas.txt"))
    idx_tema = st.session_state.tema_idx_por_book.get(book_foco, 0) % len(lista_temas)
    tema_atual = lista_temas[idx_tema]

    # --- COCKPIT CENTRALIZADO ---
    st.markdown("<br>", unsafe_allow_html=True)
    # Colunas para centralizar os controles
    c1, c2, c3, c4, c5, c6, c7, c8, c9 = st.columns([2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 2])
    
    if c3.button("✚"): st.session_state.seed_mutante += 1; st.rerun()
    if c4.button("❰"): st.session_state.tema_idx_por_book[book_foco] = idx_tema - 1; st.rerun()
    if c5.button("✱"): st.session_state.tema_idx_por_book[book_foco] = random.randint(0, len(lista_temas)-1); st.rerun()
    if c6.button("❱"): st.session_state.tema_idx_por_book[book_foco] = idx_tema + 1; st.rerun()

    st.selectbox("Tema", lista_temas, index=idx_tema, key=f"sel_{idx_tema}", label_visibility="collapsed")

    st.markdown("---")
    
    # --- PALCO ---
    try:
        from lay_2_ypo import gera_poema
        res = gera_poema(tema_atual, str(st.session_state.seed_mutante))
        txt = ("".join(res) if isinstance(res, list) else str(res)).strip().replace("\n", "<br>")
        
        # Exibição limpa (PT por padrão nesta restauração)
        st.markdown(f'<div class="poema-box">{txt}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Integridade: {e}")

if __name__ == "__main__":
    main()
    
