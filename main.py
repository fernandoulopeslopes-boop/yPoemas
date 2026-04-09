import streamlit as st
import extra_streamlit_components as stx
import os
import random
from deep_translator import GoogleTranslator

# CRONOLOGIA ATIVA: X=41 (A PÉROLA DA MACHINA: Formatação Áurea e Início Automático)
# REGRA_ZERO: Protocolo ptc mantido sob vigilância rigorosa da IA.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "base")

DICI_LANG = {
    'Português': 'pt', 'Español': 'es', 'Italiano': 'it', 
    'Français': 'fr', 'English': 'en', 'Català': 'ca',
    'Deutsch': 'de', 'Galego': 'gl', 'Română': 'ro'
}

def aplicar_estetica_v41():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap');
            
            /* RESET E OCULTAÇÃO AGRESSIVA */
            header[data-testid="stHeader"], footer { visibility: hidden; height: 0px; }
            [data-testid="stSidebar"] { display: none; }
            
            /* REMOÇÃO DO RETÂNGULO EM BRANCO E AJUSTE DE TOPO */
            .main .block-container {
                padding-top: 0rem !important;
                padding-bottom: 0rem !important;
                margin-top: -85px !important; 
            }
            div[data-testid="stSelectbox"] label { display: none !important; }
            div[data-testid="stSelectbox"] div[data-baseweb="select"] { margin-top: -10px !important; }

            .stApp { background-color: #ffffff; }

            /* COCKPIT FIXO */
            .fixed-top {
                position: fixed; top: 0; left: 0; width: 100%;
                background-color: rgba(255, 255, 255, 0.98);
                z-index: 999; padding: 5px 0 2px 0;
                border-bottom: 1px solid #f2f2f2;
                display: flex; flex-direction: column; align-items: center;
            }
            
            .stButton > button { 
                border-radius: 50% !important; width: 36px !important; height: 38px !important; 
                border: 1px solid #eee !important; background: white !important; 
            }

            div[data-testid="stSelectbox"] { width: 180px !important; margin: 0 auto !important; }

            /* PALCO: A PÉROLA DA FORMATAÇÃO */
            .main-content { 
                margin-top: 105px; 
                display: block; 
                width: 100%;
                max-width: 800px;
                margin-left: auto;
                margin-right: auto;
            }

            .poema-box { 
                font-family: 'Libre Baskerville', serif; 
                font-size: 1.25em !important; 
                line-height: 1.65 !important; 
                color: #1a1a1a; 
                padding: 5px 45px; 
                border-left: 2px solid #333;
                margin-top: 0px !important;
                white-space: pre-wrap !important; /* PRESERVA ENDENTAÇÃO E LINHAS DUPLAS ORIGINAIS */
                word-wrap: break-word;
            }
            
            .cfg-head { font-size: 0.7em; font-weight: bold; color: #bbb; text-transform: uppercase; margin-bottom: 3px; }
        </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(layout="wide", page_title="Machina Poética")
    aplicar_estetica_v41()

    # --- INICIALIZAÇÃO E PERSISTÊNCIA ---
    PAGINAS = ["demo", "ypoemas", "eureka", "off-máquina", "books", "about"]
    if 'current_tab' not in st.session_state: st.session_state.current_tab = "demo"
    if 'book_em_foco' not in st.session_state: st.session_state.book_em_foco = "todos os temas"
    if 'memoria_temas' not in st.session_state: st.session_state.memoria_temas = {"todos os temas": 0}
    if 'seed' not in st.session_state: st.session_state.seed = random.randint(0, 99999) 
    if 'lang' not in st.session_state: st.session_state.lang = 'Português'
    if 'show_config' not in st.session_state: st.session_state.show_config = False

    # --- COCKPIT ---
    st.markdown('<div class="fixed-top">', unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        b1, b2, b3, b4, b5, b6 = st.columns(6)
        if b1.button("✚"): st.session_state.seed += 1; st.rerun()
        if b2.button("❰"): st.session_state.memoria_temas[st.session_state.book_em_foco] -= 1; st.rerun()
        if b3.button("✱"): st.session_state.seed = random.randint(0, 99999); st.rerun()
        if b4.button("❱"): st.session_state.memoria_temas[st.session_state.book_em_foco] += 1; st.rerun()
        b5.button("?")
        if b6.button("@"):
            st.session_state.show_config = not st.session_state.show_config
            st.rerun()

        # Carregamento de Temas
        arquivos = sorted([f for f in os.listdir(BASE_PATH) if f.startswith("rol_") and f.endswith(".txt")]) if os.path.exists(BASE_PATH) else []
        LIVROS = {f.replace("rol_", "").replace(".txt", ""): f for f in arquivos}
        book_foco = "todos os temas" if st.session_state.current_tab == "demo" else st.session_state.book_em_foco
        caminho_livro = os.path.join(BASE_PATH, LIVROS.get(book_foco, "rol_todos os temas.txt"))
        
        with open(caminho_livro, "r", encoding="utf-8") as f:
            lista_temas = [l.strip() for l in f if l.strip() and not l.startswith("[")]
        
        idx_tema = st.session_state.memoria_temas.get(book_foco, 0) % len(lista_temas)
        st.selectbox("T", lista_temas, index=idx_tema, key=f"v41_{idx_tema}", 
                     on_change=lambda: st.session_state.memoria_temas.update({book_foco: lista_temas.index(st.session_state[f"v41_{idx_tema}"])}),
                     label_visibility="collapsed")

    # Navegação de Abas
    aba_sel = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS], default=st.session_state.current_tab)
    if aba_sel and aba_sel != st.session_state.current_tab:
        st.session_state.current_tab = aba_sel
        st.rerun()

    if st.session_state.show_config:
        _, c_cfg, _ = st.columns([1, 1, 1])
        with c_cfg:
            st.markdown('<div style="background:#fdfdfd; padding:12px; border:1px solid #eee; margin-top:2px; text-align:center;">', unsafe_allow_html=True)
            st.markdown('<p class="cfg-head">idiomas disponíveis</p>', unsafe_allow_html=True)
            st.session_state.lang = st.selectbox("L", list(DICI_LANG.keys()), index=list(DICI_LANG.keys()).index(st.session_state.lang), label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- PALCO (A PÉROLA) ---
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    if st.session_state.current_tab in ["demo", "ypoemas"]:
        try:
            from lay_2_ypo import gera_poema
            res = gera_poema(lista_temas[idx_tema], str(st.session_state.seed))
            
            txt_final = "".join(res) if isinstance(res, list) else str(res)
            
            if st.session_state.lang != 'Português':
                txt_final = GoogleTranslator(source='pt', target=DICI_LANG[st.session_state.lang]).translate(text=txt_final)
            
            st.markdown(f'<div class="poema-box">{txt_final}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Erro no motor: {e}")
    elif st.session_state.current_tab == "about":
        st.markdown('<div class="poema-box"><b>a Máquina de Fazer Poesia</b><br>Geometria restaurada.</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
