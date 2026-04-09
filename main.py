import streamlit as st
import extra_streamlit_components as stx
import os
import random
from deep_translator import GoogleTranslator

# CRONOLOGIA ATIVA: X=09 (RESTAURAÇÃO: Versão Estável de Ontem)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "base")

# --- MOTOR DE TRADUÇÃO COM SANITIZAÇÃO "NA MARRA" ---
def tradutor_na_marra(input_text, target_lang='pt'):
    if not input_text or target_lang == 'pt':
        return input_text
    
    try:
        # Tradução direta
        output_text = GoogleTranslator(source='pt', target=target_lang).translate(text=input_text)
        
        # Limpeza cirúrgica de alucinações de tags HTML
        output_text = output_text.replace("<br>>", "<br>")
        output_text = output_text.replace("< br>", "<br>")
        output_text = output_text.replace("<br >", "<br>")
        output_text = output_text.replace("<br ", "<br>")
        output_text = output_text.replace(" br>", "<br>")
        output_text = output_text.replace("</br>", "<br>")
        
        return output_text
    except:
        return input_text

# --- MAPEAMENTO DINÂMICO DE LIVROS ---
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
            .block-container { padding-top: 1rem !important; max-width: 100% !important; }
            
            .stButton > button { 
                border-radius: 50% !important; width: 42px !important; height: 42px !important; 
                border: 1px solid #eee !important; background: white !important; color: #555 !important;
            }
            
            .poema-box { 
                font-family: 'Georgia', serif; font-size: 1.7em; line-height: 1.6; 
                color: #1a1a1a; margin-top: 2rem; padding: 15px; text-align: left;
            }
        </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(layout="wide", page_title="yPoemas")
    aplicar_estetica()

    # --- CARREGAMENTO DA ESTRUTURA ---
    LIVROS_DISPONIVEIS = listar_livros_reais()

    # --- ESTADOS ---
    if 'current_tab_idx' not in st.session_state: st.session_state.current_tab_idx = 0 
    if 'book_em_foco' not in st.session_state: st.session_state.book_em_foco = list(LIVROS_DISPONIVEIS.keys())[0]
    if 'tema_idx_por_book' not in st.session_state: st.session_state.tema_idx_por_book = {b: 0 for b in LIVROS_DISPONIVEIS}
    if 'seed_mutante' not in st.session_state: st.session_state.seed_mutante = 0
    if 'idioma_selecionado' not in st.session_state: st.session_state.idioma_selecionado = 'PT'

    PAGINAS_APP = ["demo", "ypoemas", "eureka", "off-máquina", "books", "about"]
    aba_atual = PAGINAS_APP[st.session_state.current_tab_idx]

    # Tabs
    aba_clicada = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS_APP], default=aba_atual)
    if aba_clicada and aba_clicada != aba_atual:
        st.session_state.current_tab_idx = PAGINAS_APP.index(aba_clicada)
        st.rerun()

    book_foco = "todos os temas" if aba_atual == "demo" else st.session_state.book_em_foco
    
    @st.cache_data
    def get_temas(arquivo):
        caminho = os.path.join(BASE_PATH, arquivo)
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                return [l.strip() for l in f if l.strip() and not l.startswith("[")]
        return ["Silêncio"]

    lista_temas = get_temas(LIVROS_DISPONIVEIS.get(book_foco, "rol_todos os temas.txt"))
    idx_tema = st.session_state.tema_idx_por_book.get(book_foco, 0) % len(lista_temas)
    tema_atual = lista_temas[idx_tema]

    # --- COCKPIT ---
    st.markdown("<br>", unsafe_allow_html=True)
    c_l, c_p, c_pr, c_ra, c_ne, c_he, c_cf, c_r = st.columns([3, 1, 1, 1, 1, 1, 1, 3])
    
    if c_p.button("✚"): st.session_state.seed_mutante += 1; st.rerun()
    if c_pr.button("❰"): st.session_state.tema_idx_por_book[book_foco] = idx_tema - 1; st.rerun()
    if c_ra.button("✱"): st.session_state.tema_idx_por_book[book_foco] = random.randint(0, len(lista_temas)-1); st.rerun()
    if c_ne.button("❱"): st.session_state.tema_idx_por_book[book_foco] = idx_tema + 1; st.rerun()

    st.selectbox("Tema", lista_temas, index=idx_tema, key=f"sel_{idx_tema}", label_visibility="collapsed")

    # --- PALCO CENTRAL ---
    st.markdown("---")
    
    try:
        from lay_2_ypo import gera_poema
        res_bruto = gera_poema(tema_atual, str(st.session_state.seed_mutante))
        txt_original = "".join(res_bruto) if isinstance(res_bruto, list) else str(res_bruto)
        
        txt_com_breaks = txt_original.strip().replace("\n", "<br>")
        
        # Idiomas Simplificados (Modo Estável)
        idiomas_map = {"PT": "pt", "EN": "en", "ES": "es", "FR": "fr"}
        target = idiomas_map.get(st.session_state.idioma_selecionado, "pt")
        
        txt_final = tradutor_na_marra(txt_com_breaks, target_lang=target)

        st.markdown(f'<div class="poema-box">{txt_final}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Erro na Machina: {e}")

if __name__ == "__main__":
    main()
