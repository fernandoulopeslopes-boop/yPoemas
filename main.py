import streamlit as st
import streamlit.components.v1 as components
import extra_streamlit_components as stx
import os
import random
from deep_translator import GoogleTranslator

# CRONOLOGIA ATIVA: X=44 (GEOMETRIA DE PRECISÃO + ANCORAGEM ABSOLUTA + PROTOCOLO QUIET)
# REGRA_ZERO: Foco total na restauração da "Pérola" e alinhamento do cockpit.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "base")

DICI_LANG = {
    'Português': 'pt', 'Español': 'es', 'Italiano': 'it', 
    'Français': 'fr', 'English': 'en', 'Català': 'ca',
    'Deutsch': 'de', 'Galego': 'gl', 'Română': 'ro'
}

def aplicar_estetica_v44():
    st.markdown("""
        <style>
            header[data-testid="stHeader"], footer { visibility: hidden; height: 0px; }
            [data-testid="stSidebar"] { display: none; }
            
            /* RESET TOTAL DO PALCO */
            .main .block-container {
                padding-top: 0rem !important;
                padding-bottom: 0rem !important;
                margin-top: -110px !important; 
            }
            
            /* COCKPIT FIXO */
            .fixed-top {
                position: fixed; top: 0; left: 0; width: 100%;
                background-color: white; z-index: 999;
                border-bottom: 1px solid #f2f2f2;
                display: flex; flex-direction: column; align-items: center;
                padding-bottom: 8px;
            }
            
            .stButton > button { 
                border-radius: 50% !important; width: 36px !important; height: 38px !important; 
                background: white !important; border: 1px solid #eee !important;
            }
            
            /* AJUSTE DO SELECTBOX (Tamanho e Invisibilidade do Label) */
            div[data-testid="stSelectbox"] label { display: none !important; }
            div[data-testid="stSelectbox"] { margin-top: -5px !important; }
        </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(layout="wide", page_title="Machina Poética")
    aplicar_estetica_v44()

    # --- ESTADOS ---
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
        # Grade de Botões (1 a 6)
        b_cols = st.columns(6)
        if b_cols[0].button("✚"): 
            st.session_state.seed += 1
            st.rerun()
        if b_cols[1].button("❰"): 
            st.session_state.memoria_temas[st.session_state.book_em_foco] -= 1
            st.rerun()
        if b_cols[2].button("✱"): 
            st.session_state.seed = random.randint(0, 9999)
            st.session_state.do_random = True 
            st.rerun()
        if b_cols[3].button("❱"): 
            st.session_state.memoria_temas[st.session_state.book_em_foco] += 1
            st.rerun()
        b_cols[4].button("?")
        if b_cols[5].button("@"):
            st.session_state.show_config = not st.session_state.show_config
            st.rerun()

        # SUB-GRADE PARA O SELECTBOX (Alinhado sob os botões 2 e 3: ❰ e ✱)
        # 6 colunas espelham a grade de botões acima. Ocupamos da 2 à 3.
        sel_col_1, sel_col_2_3, sel_col_4_6 = st.columns([1, 2, 3])
        
        with sel_col_2_3:
            arquivos = sorted([f for f in os.listdir(BASE_PATH) if f.startswith("rol_") and f.endswith(".txt")]) if os.path.exists(BASE_PATH) else []
            LIVROS = {f.replace("rol_", "").replace(".txt", ""): f for f in arquivos}
            book_foco = "todos os temas" if st.session_state.current_tab == "demo" else st.session_state.book_em_foco
            caminho_livro = os.path.join(BASE_PATH, LIVROS.get(book_foco, "rol_todos os temas.txt"))
            
            try:
                with open(caminho_livro, "r", encoding="utf-8") as f:
                    lista_temas = [l.strip() for l in f if l.strip() and not l.startswith("[")]
            except:
                lista_temas = ["Erro"]

            if st.session_state.get('do_random', False):
                st.session_state.memoria_temas[book_foco] = random.randint(0, len(lista_temas)-1)
                st.session_state.do_random = False

            idx_tema = st.session_state.memoria_temas.get(book_foco, 0) % len(lista_temas)
            st.selectbox("T", lista_temas, index=idx_tema, key=f"v44_{idx_tema}", 
                         on_change=lambda: st.session_state.memoria_temas.update({book_foco: lista_temas.index(st.session_state[f"v44_{idx_tema}"])}),
                         label_visibility="collapsed")

    # Navegação
    PAGINAS = ["demo", "ypoemas", "eureka", "off-máquina", "books", "about"]
    aba_sel = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS], default=st.session_state.current_tab)
    if aba_sel and aba_sel != st.session_state.current_tab:
        st.session_state.current_tab = aba_sel
        st.rerun()

    if st.session_state.show_config:
        _, c_cfg, _ = st.columns([1, 1, 1])
        with c_cfg:
            st.session_state.lang = st.selectbox("L", list(DICI_LANG.keys()), index=list(DICI_LANG.keys()).index(st.session_state.lang))
    st.markdown('</div>', unsafe_allow_html=True)

    # --- PALCO ISOLADO (CORREÇÃO DE ANCORAGEM E FORMATAÇÃO) ---
    st.markdown('<div style="margin-top: 112px;"></div>', unsafe_allow_html=True)
    
    if st.session_state.current_tab in ["demo", "ypoemas"]:
        try:
            from lay_2_ypo import gera_poema
            res = gera_poema(lista_temas[idx_tema], str(st.session_state.seed))
            # Preservação absoluta da string original
            txt = "".join(res) if isinstance(res, list) else str(res)
            
            if st.session_state.lang != 'Português':
                txt = GoogleTranslator(source='pt', target=DICI_LANG[st.session_state.lang]).translate(text=txt)

            # HTML/CSS: Ancoragem Superior Absoluta + Respeito ao Texto
            html_output = f"""
            <link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville&display=swap" rel="stylesheet">
            <style>
                body {{ 
                    margin: 0 !important; padding: 0 !important; 
                    background: white; overflow: hidden;
                    display: flex; justify-content: center;
                }}
                .stage {{
                    width: 780px; text-align: left;
                    margin-top: 0px !important; /* TOPO ABSOLUTO */
                }}
                pre {{
                    font-family: 'Libre Baskerville', serif; 
                    font-size: 21px; line-height: 1.62; color: #1a1a1a;
                    border-left: 2px solid #333;
                    padding: 0px 45px;
                    white-space: pre-wrap; /* MANTÉM QUEBRAS E BLOCOS */
                    margin: 0;
                }}
            </style>
            <div class="stage"><pre>{txt}</pre></div>
            """
            components.html(html_output, height=1500, scrolling=False)
            
        except Exception as e:
            st.error(f"Erro: {e}")

if __name__ == "__main__":
    main()
