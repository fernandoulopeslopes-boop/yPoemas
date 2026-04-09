import streamlit as st
import extra_streamlit_components as stx
import os
import random
from deep_translator import GoogleTranslator

# CRONOLOGIA ATIVA: X=22 (ESTADO ATUAL: Simetria Central e Cockpit de Comando)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "base")

def aplicar_estetica_v22():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap');
            header[data-testid="stHeader"], footer { visibility: hidden; height: 0px; }
            [data-testid="stSidebar"] { display: none; }
            
            .stApp { background-color: #ffffff; }

            /* Cockpit Unificado e Fixo */
            .fixed-top {
                position: fixed; top: 0; left: 0; width: 100%;
                background-color: rgba(255, 255, 255, 0.98);
                z-index: 999; padding: 15px 0 10px 0;
                border-bottom: 1px solid #f2f2f2;
                display: flex; flex-direction: column; align-items: center;
            }
            
            /* Container da Pick_list de Idiomas (O desenho __________) */
            .lang-wrapper {
                width: 320px; /* Width igual à linha desenhada */
                margin: 5px auto 15px auto;
            }

            /* Botões do Console */
            .stButton > button { 
                border-radius: 50% !important; width: 44px !important; height: 44px !important; 
                border: 1px solid #eee !important; background: white !important; 
                color: #444 !important; transition: 0.2s;
            }

            .main-content { margin-top: 250px; display: flex; justify-content: center; padding-bottom: 80px; }

            .poema-box { 
                font-family: 'Libre Baskerville', serif; font-size: 1.85em; line-height: 1.7; 
                color: #111; max-width: 720px; padding: 35px;
                text-align: left; border-left: 3px solid #111;
            }
        </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(layout="wide", page_title="Machina Poética")
    aplicar_estetica_v22()

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

    # --- COCKPIT ---
    st.markdown('<div class="fixed-top">', unsafe_allow_html=True)
    
    # 1. BOTÕES NO TOPO CENTRO
    col_btns = st.columns([1, 1, 1, 1, 1, 1, 6, 1, 1, 1, 1, 1, 1])[1:7]
    with col_btns[0]: 
        if st.button("✚"): st.session_state.seed += 1; st.rerun()
    with col_btns[1]: 
        if st.button("❰"): st.session_state.memoria_temas[st.session_state.book_em_foco] -= 1; st.rerun()
    with col_btns[2]: 
        if st.button("✱"): st.session_state.memoria_temas[st.session_state.book_em_foco] = random.randint(0, 9999); st.rerun()
    with col_btns[3]: 
        if st.button("❱"): st.session_state.memoria_temas[st.session_state.book_em_foco] += 1; st.rerun()
    with col_btns[4]: st.button("?")
    with col_btns[5]: st.button("@")

    # 2. PICK_LIST IDIOMAS (ABAIXO DOS BOTÕES, CENTRALIZADA)
    idiomas = {'Português': 'pt', 'English': 'en', 'Español': 'es', 'Français': 'fr', 'Italiano': 'it'}
    
    # Criando o efeito do width fixo (__________)
    _, central_col, _ = st.columns([1, 0.6, 1]) 
    with central_col:
        st.session_state.lang = st.selectbox("L", list(idiomas.keys()), 
                                            index=list(idiomas.keys()).index(st.session_state.lang), 
                                            label_visibility="collapsed")

    # 3. PÁGINAS (ABAS)
    PAGINAS = ["demo", "ypoemas", "eureka", "off-máquina", "books", "about"]
    aba_atual = PAGINAS[st.session_state.current_tab_idx]
    aba_sel = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS], default=aba_atual)
    if aba_sel and aba_sel != aba_atual:
        st.session_state.current_tab_idx = PAGINAS.index(aba_sel)
        st.rerun()

    # 4. TEMAS
    book_foco = "todos os temas" if st.session_state.current_tab_idx == 0 else st.session_state.book_em_foco
    with open(os.path.join(BASE_PATH, LIVROS.get(book_foco, "rol_todos os temas.txt")), "r", encoding="utf-8") as f:
        lista_temas = [l.strip() for l in f if l.strip() and not l.startswith("[")]

    idx_tema = st.session_state.memoria_temas.get(book_foco, 0) % len(lista_temas)
    st.selectbox("T", lista_temas, index=idx_tema, key=f"t_v22_{idx_tema}", 
                 on_change=lambda: st.session_state.memoria_temas.update({book_foco: lista_temas.index(st.session_state[f"t_v22_{idx_tema}"])}),
                 label_visibility="collapsed")

    st.markdown('</div>', unsafe_allow_html=True) 

    # --- PALCO ---
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    try:
        from lay_2_ypo import gera_poema
        res = gera_poema(lista_temas[idx_tema], str(st.session_state.seed))
        txt = ("".join(res) if isinstance(res, list) else str(res)).strip().replace("\n", "<br>")
        txt_final = GoogleTranslator(source='pt', target=idiomas[st.session_state.lang]).translate(text=txt) if st.session_state.lang != 'Português' else txt
        st.markdown(f'<div class="poema-box">{txt_final}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Erro: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
