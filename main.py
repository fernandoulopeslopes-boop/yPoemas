import streamlit as st
import extra_streamlit_components as stx
import os
import random
from deep_translator import GoogleTranslator

# CRONOLOGIA ATIVA: X=25 (ESTRUTURA PURIFICADA: Temas no Eixo Central + Config Isolada)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "base")

def aplicar_estetica_v25():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap');
            header[data-testid="stHeader"], footer { visibility: hidden; height: 0px; }
            [data-testid="stSidebar"] { display: none; }
            
            .stApp { background-color: #ffffff; }

            /* Cockpit Centralizado e Fixo */
            .fixed-top {
                position: fixed; top: 0; left: 0; width: 100%;
                background-color: rgba(255, 255, 255, 0.98);
                z-index: 999; padding: 15px 0 10px 0;
                border-bottom: 1px solid #f2f2f2;
                display: flex; flex-direction: column; align-items: center;
            }
            
            .console-inner { width: 100%; max-width: 800px; display: flex; flex-direction: column; align-items: center; }

            /* Botões do Console */
            .stButton > button { 
                border-radius: 50% !important; width: 44px !important; height: 44px !important; 
                border: 1px solid #eee !important; background: white !important; 
                color: #444 !important; transition: 0.2s;
            }

            /* Width Reduzido da Drop_list de Temas na Linha de Baixo */
            div[data-testid="stSelectbox"] {
                width: 320px !important; /* Width reduzido conforme solicitado */
                margin-top: -5px;
            }

            .main-content { margin-top: 240px; display: flex; justify-content: center; padding-bottom: 80px; }

            .poema-box { 
                font-family: 'Libre Baskerville', serif; font-size: 1.9em; line-height: 1.7; 
                color: #111; max-width: 750px; padding: 40px;
                text-align: left; border-left: 4px solid #111;
            }
            
            /* Painel de Configurações (Acessado pelo @) */
            .config-pane {
                background: #f9f9f9; padding: 20px; border-radius: 8px;
                border: 1px solid #eee; margin-top: 15px; width: 350px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            }
        </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(layout="wide", page_title="Machina Poética")
    aplicar_estetica_v25()

    # --- DADOS ---
    arquivos = sorted([f for f in os.listdir(BASE_PATH) if f.startswith("rol_") and f.endswith(".txt")]) if os.path.exists(BASE_PATH) else []
    LIVROS = {f.replace("rol_", "").replace(".txt", ""): f for f in arquivos}
    if not LIVROS: LIVROS = {"todos os temas": "rol_todos os temas.txt"}

    # --- ESTADOS ---
    if 'current_tab_idx' not in st.session_state: st.session_state.current_tab_idx = 0 
    if 'book_em_foco' not in st.session_state: st.session_state.book_em_foco = list(LIVROS.keys())[0]
    if 'memoria_temas' not in st.session_state: st.session_state.memoria_temas = {b: 0 for b in LIVROS}
    if 'seed' not in st.session_state: st.session_state.seed = 0
    if 'lang' not in st.session_state: st.session_state.lang = 'Português'
    if 'show_config' not in st.session_state: st.session_state.show_config = False
    if 'talk' not in st.session_state: st.session_state.talk = False

    # --- COCKPIT (A GEOMETRIA SOLICITADA) ---
    st.markdown('<div class="fixed-top"><div class="console-inner">', unsafe_allow_html=True)
    
    # LINHA 1: [ +  <  * >  ?  @ ]
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    if c1.button("✚"): st.session_state.seed += 1; st.rerun()
    if c2.button("❰"): st.session_state.memoria_temas[st.session_state.book_em_foco] -= 1; st.rerun()
    if c3.button("✱"): st.session_state.memoria_temas[st.session_state.book_em_foco] = random.randint(0, 9999); st.rerun()
    if c4.button("❱"): st.session_state.memoria_temas[st.session_state.book_em_foco] += 1; st.rerun()
    c5.button("?")
    if c6.button("@"):
        st.session_state.show_config = not st.session_state.show_config
        st.rerun()

    # LINHA 2: DROP_LIST DE TEMAS (NO LUGAR DOS IDIOMAS)
    book_foco = "todos os temas" if st.session_state.current_tab_idx == 0 else st.session_state.book_em_foco
    with open(os.path.join(BASE_PATH, LIVROS.get(book_foco, "rol_todos os temas.txt")), "r", encoding="utf-8") as f:
        lista_temas = [l.strip() for l in f if l.strip() and not l.startswith("[")]
    
    idx_tema = st.session_state.memoria_temas.get(book_foco, 0) % len(lista_temas)
    
    # Centralização manual da pick-list de temas com width reduzido
    st.selectbox("T", lista_temas, index=idx_tema, key=f"t_v25_{idx_tema}", 
                 on_change=lambda: st.session_state.memoria_temas.update({book_foco: lista_temas.index(st.session_state[f"t_v25_{idx_tema}"])}),
                 label_visibility="collapsed")

    # LINHA 3: ABAS DE PÁGINAS
    PAGINAS = ["demo", "ypoemas", "eureka", "off-máquina", "books", "about"]
    aba_atual = PAGINAS[st.session_state.current_tab_idx]
    aba_sel = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS], default=aba_atual)
    if aba_sel and aba_sel != aba_atual:
        st.session_state.current_tab_idx = PAGINAS.index(aba_sel)
        st.rerun()

    # PAINEL DE CONFIGURAÇÃO (ACIONADO PELO @)
    if st.session_state.show_config:
        st.markdown('<div class="config-pane">', unsafe_allow_html=True)
        idiomas = {'Português': 'pt', 'English': 'en', 'Español': 'es', 'Français': 'fr', 'Italiano': 'it'}
        st.session_state.lang = st.selectbox("Idioma da Tradução", list(idiomas.keys()), 
                                            index=list(idiomas.keys()).index(st.session_state.lang))
        st.session_state.talk = st.toggle("Talk (Audio Mode)", st.session_state.talk)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)

    # --- PALCO CENTRAL ---
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    try:
        from lay_2_ypo import gera_poema
        res = gera_poema(lista_temas[idx_tema], str(st.session_state.seed))
        txt = ("".join(res) if isinstance(res, list) else str(res)).strip().replace("\n", "<br>")
        if st.session_state.lang != 'Português':
            txt = GoogleTranslator(source='pt', target=idiomas[st.session_state.lang]).translate(text=txt)
        st.markdown(f'<div class="poema-box">{txt}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Erro no Motor: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
