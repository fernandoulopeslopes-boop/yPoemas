import streamlit as st
import extra_streamlit_components as stx
import os
import random
from deep_translator import GoogleTranslator

# CRONOLOGIA ATIVA: X=26 (SIMETRIA ABSOLUTA: O Eixo Central do Desenho)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "base")

def aplicar_estetica_v26():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap');
            
            /* Reset e Ocultação de Elementos Padrão */
            header[data-testid="stHeader"], footer { visibility: hidden; height: 0px; }
            [data-testid="stSidebar"] { display: none; }
            .stApp { background-color: #ffffff; }

            /* Cockpit Centralizado e Fixo */
            .fixed-top {
                position: fixed; top: 0; left: 0; width: 100%;
                background-color: rgba(255, 255, 255, 0.98);
                z-index: 999; padding: 20px 0 5px 0;
                border-bottom: 1px solid #f2f2f2;
                display: flex; flex-direction: column; align-items: center;
            }
            
            /* Container do Eixo Central (Garante que nada escape para as bordas) */
            .central-axis {
                width: 100%; max-width: 450px; /* Largura controlada para o esmero */
                display: flex; flex-direction: column; align-items: center;
                gap: 15px; margin: 0 auto;
            }

            /* Estilização dos Botões Circulares */
            .stButton > button { 
                border-radius: 50% !important; width: 44px !important; height: 44px !important; 
                border: 1px solid #eee !important; background: white !important; 
                color: #444 !important; transition: 0.2s ease;
            }
            .stButton > button:hover { border-color: #888 !important; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }

            /* Estilização da Selectbox (Temas) - Centralizada e com Width Reduzido */
            div[data-testid="stSelectbox"] {
                width: 300px !important; /* Exatamente o [ temas ] do desenho */
                margin: 0 auto;
            }

            /* Margem do Palco Poético */
            .main-content { margin-top: 260px; display: flex; justify-content: center; padding-bottom: 100px; }

            .poema-box { 
                font-family: 'Libre Baskerville', serif; font-size: 1.9em; line-height: 1.75; 
                color: #111; max-width: 750px; padding: 40px;
                text-align: left; border-left: 5px solid #111;
            }
            
            /* Painel @ (Configurações Ocultas) */
            .config-pane {
                background: #fcfcfc; padding: 25px; border-radius: 4px;
                border: 1px solid #eee; margin-top: 20px; width: 320px;
                text-align: center;
            }
        </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(layout="wide", page_title="Machina Poética")
    aplicar_estetica_v26()

    # --- PERSISTÊNCIA E ESTADOS ---
    if 'current_tab_idx' not in st.session_state: st.session_state.current_tab_idx = 0 
    if 'book_em_foco' not in st.session_state: st.session_state.book_em_foco = "todos os temas"
    if 'memoria_temas' not in st.session_state: st.session_state.memoria_temas = {"todos os temas": 0}
    if 'seed' not in st.session_state: st.session_state.seed = 0
    if 'lang' not in st.session_state: st.session_state.lang = 'Português'
    if 'show_config' not in st.session_state: st.session_state.show_config = False

    # --- COCKPIT (O DESENHO) ---
    st.markdown('<div class="fixed-top">', unsafe_allow_html=True)
    
    # EIXO CENTRAL: Botões e Temas
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        # Linha 1: [ +  <  * >  ?  @ ]
        b1, b2, b3, b4, b5, b6 = st.columns(6)
        if b1.button("✚"): st.session_state.seed += 1; st.rerun()
        if b2.button("❰"): st.session_state.memoria_temas[st.session_state.book_em_foco] -= 1; st.rerun()
        if b3.button("✱"): st.session_state.memoria_temas[st.session_state.book_em_foco] = random.randint(0, 9999); st.rerun()
        if b4.button("❱"): st.session_state.memoria_temas[st.session_state.book_em_foco] += 1; st.rerun()
        b5.button("?")
        if b6.button("@"):
            st.session_state.show_config = not st.session_state.show_config
            st.rerun()

        # Linha 2: [ temas ] - Centralizada e Curta
        arquivos = sorted([f for f in os.listdir(BASE_PATH) if f.startswith("rol_") and f.endswith(".txt")]) if os.path.exists(BASE_PATH) else []
        LIVROS = {f.replace("rol_", "").replace(".txt", ""): f for f in arquivos}
        
        book_foco = "todos os temas" if st.session_state.current_tab_idx == 0 else st.session_state.book_em_foco
        caminho_livro = os.path.join(BASE_PATH, LIVROS.get(book_foco, "rol_todos os temas.txt"))
        
        with open(caminho_livro, "r", encoding="utf-8") as f:
            lista_temas = [l.strip() for l in f if l.strip() and not l.startswith("[")]
        
        idx_tema = st.session_state.memoria_temas.get(book_foco, 0) % len(lista_temas)
        st.selectbox("Temas", lista_temas, index=idx_tema, key=f"sel_{idx_tema}", 
                     on_change=lambda: st.session_state.memoria_temas.update({book_foco: lista_temas.index(st.session_state[f"sel_{idx_tema}"])}),
                     label_visibility="collapsed")

    # Linha 3: PAGINAS (ABAS)
    PAGINAS = ["demo", "ypoemas", "eureka", "off-máquina", "books", "about"]
    aba_atual = PAGINAS[st.session_state.current_tab_idx]
    aba_sel = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS], default=aba_atual)
    if aba_sel and aba_sel != aba_atual:
        st.session_state.current_tab_idx = PAGINAS.index(aba_sel)
        st.rerun()

    # PAINEL @ (SEÇÃO SEPARADA)
    if st.session_state.show_config:
        _, c_cfg, _ = st.columns([1, 1, 1])
        with c_cfg:
            st.markdown('<div class="config-pane">', unsafe_allow_html=True)
            idiomas = {'Português': 'pt', 'English': 'en', 'Español': 'es', 'Français': 'fr', 'Italiano': 'it'}
            st.session_state.lang = st.selectbox("Idioma", list(idiomas.keys()), 
                                                index=list(idiomas.keys()).index(st.session_state.lang))
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # --- PALCO CENTRAL ---
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    try:
        from lay_2_ypo import gera_poema
        res_bruto = gera_poema(lista_temas[idx_tema], str(st.session_state.seed))
        txt_unido = "".join(res_bruto) if isinstance(res_bruto, list) else str(res_bruto)
        txt_limpo = txt_unido.strip().replace("\n", "<br>")
        
        # Tradução apenas se necessário (Configurada no @)
        if st.session_state.lang != 'Português':
            txt_limpo = GoogleTranslator(source='pt', target=idiomas[st.session_state.lang]).translate(text=txt_limpo)
            
        st.markdown(f'<div class="poema-box">{txt_limpo}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Integridade do Motor: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
