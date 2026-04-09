import streamlit as st
import extra_streamlit_components as stx
import os
import random
from deep_translator import GoogleTranslator

# CRONOLOGIA ATIVA: X=23 (PURIFICAÇÃO: Navegação vs. Configuração)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "base")

def aplicar_estetica_v23():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap');
            header[data-testid="stHeader"], footer { visibility: hidden; height: 0px; }
            [data-testid="stSidebar"] { display: none; }
            
            .stApp { background-color: #ffffff; }

            /* Cockpit Fixo e Minimalista */
            .fixed-top {
                position: fixed; top: 0; left: 0; width: 100%;
                background-color: rgba(255, 255, 255, 0.98);
                z-index: 999; padding: 15px 0 10px 0;
                border-bottom: 1px solid #f2f2f2;
                display: flex; flex-direction: column; align-items: center;
            }
            
            .console-inner { width: 95%; max-width: 900px; margin: 0 auto; }

            /* Botões de Navegação Circulares */
            .stButton > button { 
                border-radius: 50% !important; width: 44px !important; height: 44px !important; 
                border: 1px solid #eee !important; background: white !important; 
                color: #444 !important; transition: 0.2s;
            }
            .stButton > button:hover { border-color: #888 !important; }

            /* Palco */
            .main-content { margin-top: 200px; display: flex; justify-content: center; padding-bottom: 80px; }
            .poema-box { 
                font-family: 'Libre Baskerville', serif; font-size: 1.85em; line-height: 1.7; 
                color: #111; max-width: 720px; padding: 35px;
                text-align: left; border-left: 3px solid #111;
            }
            
            /* Overlay para Configuração */
            .config-pane {
                background: #fdfdfd; padding: 20px; border-radius: 10px;
                border: 1px solid #eee; margin-top: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(layout="wide", page_title="Machina Poética")
    aplicar_estetica_v23()

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
    if 'draw' not in st.session_state: st.session_state.draw = False

    # --- COCKPIT (TOP-CENTER) ---
    st.markdown('<div class="fixed-top"><div class="console-inner">', unsafe_allow_html=True)
    
    # 1. LINHA DE NAVEGAÇÃO E TEMAS
    # Colunas para centralizar botões e a drop_list ao lado do @
    c_nav, c_tema, c_cfg = st.columns([4, 5, 1])
    
    with c_nav:
        n1, n2, n3, n4, n5 = st.columns(5)
        if n1.button("✚"): st.session_state.seed += 1; st.rerun()
        if n2.button("❰"): st.session_state.memoria_temas[st.session_state.book_em_foco] -= 1; st.rerun()
        if n3.button("✱"): st.session_state.memoria_temas[st.session_state.book_em_foco] = random.randint(0, 5000); st.rerun()
        if n4.button("❱"): st.session_state.memoria_temas[st.session_state.book_em_foco] += 1; st.rerun()
        n5.button("?")

    with c_tema:
        book_foco = "todos os temas" if st.session_state.current_tab_idx == 0 else st.session_state.book_em_foco
        with open(os.path.join(BASE_PATH, LIVROS.get(book_foco, "rol_todos os temas.txt")), "r", encoding="utf-8") as f:
            lista_temas = [l.strip() for l in f if l.strip() and not l.startswith("[")]
        
        idx_tema = st.session_state.memoria_temas.get(book_foco, 0) % len(lista_temas)
        st.selectbox("Tema", lista_temas, index=idx_tema, key=f"t_{idx_tema}", 
                     on_change=lambda: st.session_state.memoria_temas.update({book_foco: lista_temas.index(st.session_state[f"t_{idx_tema}"])}),
                     label_visibility="collapsed")

    with c_cfg:
        if st.button("@"):
            st.session_state.show_config = not st.session_state.show_config
            st.rerun()

    # 2. SEÇÃO DE PÁGINAS (ABAS)
    PAGINAS = ["demo", "ypoemas", "eureka", "off-máquina", "books", "about"]
    aba_atual = PAGINAS[st.session_state.current_tab_idx]
    aba_sel = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS], default=aba_atual)
    if aba_sel and aba_sel != aba_atual:
        st.session_state.current_tab_idx = PAGINAS.index(aba_sel)
        st.rerun()

    # 3. PEQUENA PÁGINA SEPARADA (OVERLAY DE CONFIG)
    if st.session_state.show_config:
        st.markdown('<div class="config-pane">', unsafe_allow_html=True)
        col_l, col_t, col_d = st.columns(3)
        with col_l:
            idiomas = {'Português': 'pt', 'English': 'en', 'Español': 'es', 'Français': 'fr', 'Italiano': 'it'}
            st.session_state.lang = st.selectbox("Idioma", list(idiomas.keys()), 
                                                index=list(idiomas.keys()).index(st.session_state.lang))
        with col_t:
            st.session_state.talk = st.toggle("Talk (Audio)", st.session_state.talk)
        with col_d:
            st.session_state.draw = st.toggle("Draw (Arts)", st.session_state.draw)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)

    # --- PALCO ---
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    try:
        from lay_2_ypo import gera_poema
        res_bruto = gera_poema(lista_temas[idx_tema], str(st.session_state.seed))
        txt_unido = "".join(res_bruto) if isinstance(res_bruto, list) else str(res_bruto)
        txt_final = txt_unido.strip().replace("\n", "<br>")
        
        if st.session_state.lang != 'Português':
            txt_final = GoogleTranslator(source='pt', target=idiomas[st.session_state.lang]).translate(text=txt_final)
            
        st.markdown(f'<div class="poema-box">{txt_final}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Erro no Motor: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
