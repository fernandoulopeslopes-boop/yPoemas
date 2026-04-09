import streamlit as st
import streamlit.components.v1 as components
import extra_streamlit_components as stx
import os
import random
from deep_translator import GoogleTranslator

# CRONOLOGIA ATIVA: X=43 (ESTABILIZAÇÃO: Palco Isolado + Lógica de Sorteio + REGRA_ZERO)
# Este código restaura a dignidade visual e a funcionalidade dos botões.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "base")

DICI_LANG = {
    'Português': 'pt', 'Español': 'es', 'Italiano': 'it', 
    'Français': 'fr', 'English': 'en', 'Català': 'ca',
    'Deutsch': 'de', 'Galego': 'gl', 'Română': 'ro'
}

def aplicar_estetica_v43():
    st.markdown("""
        <style>
            header[data-testid="stHeader"], footer { visibility: hidden; height: 0px; }
            [data-testid="stSidebar"] { display: none; }
            
            /* Ajuste de Topo do Streamlit */
            .main .block-container {
                padding-top: 0rem !important;
                padding-bottom: 0rem !important;
                margin-top: -100px !important; 
            }
            
            /* Cockpit Fixo */
            .fixed-top {
                position: fixed; top: 0; left: 0; width: 100%;
                background-color: white; z-index: 999;
                border-bottom: 1px solid #f2f2f2;
                display: flex; flex-direction: column; align-items: center;
            }
            
            .stButton > button { 
                border-radius: 50% !important; width: 36px !important; height: 38px !important; 
                background: white !important; border: 1px solid #eee !important;
                display: flex; align-items: center; justify-content: center;
            }
            
            div[data-testid="stSelectbox"] label { display: none !important; }
        </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(layout="wide", page_title="Machina Poética")
    aplicar_estetica_v43()

    # --- PERSISTÊNCIA E ESTADOS ---
    if 'current_tab' not in st.session_state: st.session_state.current_tab = "demo"
    if 'book_em_foco' not in st.session_state: st.session_state.book_em_foco = "todos os temas"
    if 'memoria_temas' not in st.session_state: st.session_state.memoria_temas = {"todos os temas": 0}
    if 'seed' not in st.session_state: st.session_state.seed = random.randint(0, 9999)
    if 'lang' not in st.session_state: st.session_state.lang = 'Português'
    if 'show_config' not in st.session_state: st.session_state.show_config = False

    # --- COCKPIT ---
    st.markdown('<div class="fixed-top">', unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        # Linha de Comandos
        b1, b2, b3, b4, b5, b6 = st.columns(6)
        if b1.button("✚"): 
            st.session_state.seed += 1
            st.rerun()
        if b2.button("❰"): 
            st.session_state.memoria_temas[st.session_state.book_em_foco] -= 1
            st.rerun()
        if b3.button("✱"): 
            # Lógica Random: Nova variação + Novo Tema
            st.session_state.seed = random.randint(0, 9999)
            st.session_state.do_random = True 
            st.rerun()
        if b4.button("❱"): 
            st.session_state.memoria_temas[st.session_state.book_em_foco] += 1
            st.rerun()
        b5.button("?")
        if b6.button("@"):
            st.session_state.show_config = not st.session_state.show_config
            st.rerun()

        # Gestão de Temas
        arquivos = sorted([f for f in os.listdir(BASE_PATH) if f.startswith("rol_") and f.endswith(".txt")]) if os.path.exists(BASE_PATH) else []
        LIVROS = {f.replace("rol_", "").replace(".txt", ""): f for f in arquivos}
        book_foco = "todos os temas" if st.session_state.current_tab == "demo" else st.session_state.book_em_foco
        caminho_livro = os.path.join(BASE_PATH, LIVROS.get(book_foco, "rol_todos os temas.txt"))
        
        try:
            with open(caminho_livro, "r", encoding="utf-8") as f:
                lista_temas = [l.strip() for l in f if l.strip() and not l.startswith("[")]
        except:
            lista_temas = ["Erro no carregamento"]

        if st.session_state.get('do_random', False):
            st.session_state.memoria_temas[book_foco] = random.randint(0, len(lista_temas)-1)
            st.session_state.do_random = False

        idx_tema = st.session_state.memoria_temas.get(book_foco, 0) % len(lista_temas)
        st.selectbox("T", lista_temas, index=idx_tema, key=f"v43_{idx_tema}", 
                     on_change=lambda: st.session_state.memoria_temas.update({book_foco: lista_temas.index(st.session_state[f"v43_{idx_tema}"])}),
                     label_visibility="collapsed")

    # Navegação de Abas
    PAGINAS = ["demo", "ypoemas", "eureka", "off-máquina", "books", "about"]
    aba_sel = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS], default=st.session_state.current_tab)
    if aba_sel and aba_sel != st.session_state.current_tab:
        st.session_state.current_tab = aba_sel
        st.rerun()

    if st.session_state.show_config:
        _, c_cfg, _ = st.columns([1, 1, 1])
        with c_cfg:
            st.markdown('<div style="text-align:center; padding:10px;">', unsafe_allow_html=True)
            st.session_state.lang = st.selectbox("Idioma", list(DICI_LANG.keys()), index=list(DICI_LANG.keys()).index(st.session_state.lang))
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- PALCO ISOLADO ---
    # Espaçamento para o cockpit não cobrir o início do texto
    st.markdown('<div style="margin-top: 105px;"></div>', unsafe_allow_html=True)
    
    if st.session_state.current_tab in ["demo", "ypoemas"]:
        try:
            from lay_2_ypo import gera_poema
            res = gera_poema(lista_temas[idx_tema], str(st.session_state.seed))
            txt = "".join(res) if isinstance(res, list) else str(res)
            
            if st.session_state.lang != 'Português':
                txt = GoogleTranslator(source='pt', target=DICI_LANG[st.session_state.lang]).translate(text=txt)

            # HTML/CSS Protegido (Dever de Casa)
            html_poema = f"""
            <link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville&display=swap" rel="stylesheet">
            <style>
                body {{ 
                    margin: 0; padding: 0; background: white; 
                    display: flex; justify-content: center; 
                }}
                .poema-container {{ 
                    font-family: 'Libre Baskerville', serif; 
                    font-size: 21px; line-height: 1.6; color: #1a1a1a;
                    width: 780px; border-left: 2px solid #333;
                    padding: 5px 45px; white-space: pre-wrap;
                    text-align: left;
                }}
            </style>
            <div class="poema-container">{txt}</div>
            """
            components.html(html_poema, height=1500, scrolling=False)
            
        except Exception as e:
            st.error(f"Erro no motor: {e}")
    else:
        st.info(f"Página {st.session_state.current_tab.upper()} carregada.")

if __name__ == "__main__":
    main()
