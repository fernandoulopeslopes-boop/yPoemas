import streamlit as st
import extra_streamlit_components as stx
import os
import random
from deep_translator import GoogleTranslator

# CRONOLOGIA ATIVA: X=28 (EXPANSÃO: Idiomas + Navegação de Páginas)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "base")

def aplicar_estetica_v28():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap');
            
            header[data-testid="stHeader"], footer { visibility: hidden; height: 0px; }
            [data-testid="stSidebar"] { display: none; }
            .stApp { background-color: #ffffff; }

            .fixed-top {
                position: fixed; top: 0; left: 0; width: 100%;
                background-color: rgba(255, 255, 255, 0.98);
                z-index: 999; padding: 5px 0 2px 0;
                border-bottom: 1px solid #f2f2f2;
                display: flex; flex-direction: column; align-items: center;
            }
            
            .stButton > button { 
                border-radius: 50% !important; width: 40px !important; height: 40px !important; 
                border: 1px solid #eee !important; background: white !important; 
            }

            /* Width da Pick-list de Temas */
            div[data-testid="stSelectbox"] { width: 180px !important; margin: 0 auto; }

            .main-content { margin-top: 160px; display: flex; flex-direction: column; align-items: center; padding-bottom: 80px; }

            .poema-box { 
                font-family: 'Libre Baskerville', serif; font-size: 1.9em; line-height: 1.7; 
                color: #111; max-width: 750px; padding: 30px; border-left: 5px solid #111;
            }
            
            /* Heading do Painel @ */
            .cfg-head { font-size: 0.8em; font-weight: bold; color: #888; text-transform: uppercase; margin-bottom: 5px; }
        </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(layout="wide", page_title="Machina Poética")
    aplicar_estetica_v28()

    # --- ESTADOS ---
    if 'current_tab_idx' not in st.session_state: st.session_state.current_tab_idx = 0 
    if 'book_em_foco' not in st.session_state: st.session_state.book_em_foco = "todos os temas"
    if 'memoria_temas' not in st.session_state: st.session_state.memoria_temas = {"todos os temas": 0}
    if 'seed' not in st.session_state: st.session_state.seed = 0
    if 'lang' not in st.session_state: st.session_state.lang = 'Português'
    if 'show_config' not in st.session_state: st.session_state.show_config = False

    # --- COCKPIT ---
    st.markdown('<div class="fixed-top">', unsafe_allow_html=True)
    
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        # Navegação
        b1, b2, b3, b4, b5, b6 = st.columns(6)
        if b1.button("✚"): st.session_state.seed += 1; st.rerun()
        if b2.button("❰"): st.session_state.memoria_temas[st.session_state.book_em_foco] -= 1; st.rerun()
        if b3.button("✱"): st.session_state.memoria_temas[st.session_state.book_em_foco] = random.randint(0, 9999); st.rerun()
        if b4.button("❱"): st.session_state.memoria_temas[st.session_state.book_em_foco] += 1; st.rerun()
        b5.button("?")
        if b6.button("@"):
            st.session_state.show_config = not st.session_state.show_config
            st.rerun()

        # Temas
        arquivos = sorted([f for f in os.listdir(BASE_PATH) if f.startswith("rol_") and f.endswith(".txt")]) if os.path.exists(BASE_PATH) else []
        LIVROS = {f.replace("rol_", "").replace(".txt", ""): f for f in arquivos}
        PAGINAS = ["demo", "ypoemas", "eureka", "off-máquina", "books", "about"]
        aba_atual = PAGINAS[st.session_state.current_tab_idx]
        
        book_foco = "todos os temas" if aba_atual == "demo" else st.session_state.book_em_foco
        caminho_livro = os.path.join(BASE_PATH, LIVROS.get(book_foco, "rol_todos os temas.txt"))
        
        with open(caminho_livro, "r", encoding="utf-8") as f:
            lista_temas = [l.strip() for l in f if l.strip() and not l.startswith("[")]
        
        idx_tema = st.session_state.memoria_temas.get(book_foco, 0) % len(lista_temas)
        st.selectbox("T", lista_temas, index=idx_tema, key=f"v28_{idx_tema}", 
                     on_change=lambda: st.session_state.memoria_temas.update({book_foco: lista_temas.index(st.session_state[f"v28_{idx_tema}"])}),
                     label_visibility="collapsed")

    # Abas
    aba_sel = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS], default=aba_atual)
    if aba_sel and aba_sel != aba_atual:
        st.session_state.current_tab_idx = PAGINAS.index(aba_sel)
        st.rerun()

    # Painel @ (Idioma Expandido)
    if st.session_state.show_config:
        _, c_cfg, _ = st.columns([1, 1, 1])
        with c_cfg:
            st.markdown('<div style="background:#fcfcfc; padding:15px; border:1px solid #eee; margin-top:5px;">', unsafe_allow_html=True)
            st.markdown('<p class="cfg-head">idiomas disponíveis</p>', unsafe_allow_html=True)
            
            # Lista Expandida
            DICI_LANG = {
                'Português': 'pt', 'English': 'en', 'Español': 'es', 'Français': 'fr', 
                'Italiano': 'it', 'Deutsch': 'de', '日本語': 'ja', '中文': 'zh-CN', 
                'Русский': 'ru', 'العربية': 'ar', 'हिन्दी': 'hi', 'Ελληνικά': 'el'
            }
            st.session_state.lang = st.selectbox("L", list(DICI_LANG.keys()), index=list(DICI_LANG.keys()).index(st.session_state.lang), label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # --- PALCO DINÂMICO ---
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    if aba_atual == "demo" or aba_atual == "ypoemas":
        try:
            from lay_2_ypo import gera_poema
            res = gera_poema(lista_temas[idx_tema], str(st.session_state.seed))
            txt = ("".join(res) if isinstance(res, list) else str(res)).strip().replace("\n", "<br>")
            if st.session_state.lang != 'Português':
                txt = GoogleTranslator(source='pt', target=DICI_LANG[st.session_state.lang]).translate(text=txt)
            st.markdown(f'<div class="poema-box">{txt}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Motor Offline: {e}")
            
    elif aba_atual == "eureka":
        st.info("Espaço para Insight e Descobertas: Motor Eureka em desenvolvimento.")
    elif aba_atual == "off-máquina":
        st.info("Arquivos e Rascunhos Externos.")
    elif aba_atual == "books":
        st.info("Biblioteca de Róis e Coleções.")
    elif aba_atual == "about":
        st.markdown("### a Máquina de Fazer Poesia\nVersão 2026.04 - Esmero & Rigor.")

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
