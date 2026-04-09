import streamlit as st
import extra_streamlit_components as stx
import os
import random
from deep_translator import GoogleTranslator

# CRONOLOGIA ATIVA: X=20 (PRECISÃO GEOMÉTRICA: Console -> Pick-list -> Páginas)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "base")

def aplicar_estetica_v20():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap');
            header[data-testid="stHeader"], footer { visibility: hidden; height: 0px; }
            [data-testid="stSidebar"] { display: none; }
            
            .stApp { background-color: #ffffff; }

            /* Cockpit Unificado e Centralizado */
            .fixed-top {
                position: fixed; top: 0; left: 0; width: 100%;
                background-color: rgba(255, 255, 255, 0.98);
                z-index: 999; padding: 15px 0 10px 0;
                border-bottom: 1px solid #f2f2f2;
                display: flex; flex-direction: column; align-items: center;
            }
            
            .console-inner { width: 92%; max-width: 800px; margin: 0 auto; text-align: center; }
            
            /* Ajuste de Margem do Palco para o novo cockpit triplo */
            .main-content { margin-top: 230px; display: flex; justify-content: center; padding-bottom: 80px; }

            /* Botões do Console: Simetria Total */
            .stButton > button { 
                border-radius: 50% !important; width: 42px !important; height: 42px !important; 
                border: 1px solid #eee !important; background: white !important; 
                color: #444 !important; transition: 0.2s;
            }

            /* Espaçamento vertical entre os elementos do Cockpit */
            .spacer-mini { margin-bottom: 10px; }

            .poema-box { 
                font-family: 'Libre Baskerville', serif; font-size: 1.85em; line-height: 1.7; 
                color: #111; max-width: 720px; padding: 35px;
                text-align: left; border-left: 3px solid #111;
            }
        </style>
    """, unsafe_allow_html=True)

def tradutor_estavel(txt, lang='pt'):
    if not txt or lang == 'pt': return txt
    try:
        res = GoogleTranslator(source='pt', target=lang).translate(text=txt)
        for t in ["<br>>", "< br>", "<br >", "<br ", " br>", "</br>", " <br>"]:
            res = res.replace(t, "<br>")
        return res
    except: return txt

def main():
    st.set_page_config(layout="wide", page_title="Machina Poética")
    aplicar_estetica_v20()

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

    # --- COCKPIT (A GEOMETRIA DESENHADA) ---
    st.markdown('<div class="fixed-top"><div class="console-inner">', unsafe_allow_html=True)
    
    # 1. TOPO: OS BOTÕES [+ < * > ?] + Idioma
    c_btns, c_lang = st.columns([7, 3])
    with c_btns:
        # Criando o alinhamento centralizado dos botões
        b_mut, b_prev, b_rand, b_next, b_help, b_cfg = st.columns(6)
        if b_mut.button("✚"): st.session_state.seed += 1; st.rerun()
        if b_prev.button("❰"): st.session_state.memoria_temas[st.session_state.book_em_foco] -= 1; st.rerun()
        if b_rand.button("✱"): st.session_state.memoria_temas[st.session_state.book_em_foco] = random.randint(0, 8000); st.rerun()
        if b_next.button("❱"): st.session_state.memoria_temas[st.session_state.book_em_foco] += 1; st.rerun()
        b_help.button("?")
        b_cfg.button("@")

    with c_lang:
        idiomas = {'Português': 'pt', 'English': 'en', 'Español': 'es', 'Français': 'fr', 'Italiano': 'it'}
        st.session_state.lang = st.selectbox("L", list(idiomas.keys()), index=list(idiomas.keys()).index(st.session_state.lang), label_visibility="collapsed")

    st.markdown('<div class="spacer-mini"></div>', unsafe_allow_html=True)

    # 2. LOGO ABAIXO: PICK_LIST DE TEMAS (O SEU DESENHO)
    book_foco = "todos os temas" if st.session_state.current_tab_idx == 0 else st.session_state.book_em_foco
    caminho_livro = os.path.join(BASE_PATH, LIVROS.get(book_foco, "rol_todos os temas.txt"))
    with open(caminho_livro, "r", encoding="utf-8") as f:
        lista_temas = [l.strip() for l in f if l.strip() and not l.startswith("[")]

    idx_tema = st.session_state.memoria_temas.get(book_foco, 0) % len(lista_temas)
    
    # Selectbox centralizado com atualização reativa
    st.selectbox("Tema", lista_temas, index=idx_tema, key=f"p_{book_foco}_{idx_tema}", 
                 on_change=lambda: st.session_state.memoria_temas.update({book_foco: lista_temas.index(st.session_state[f"p_{book_foco}_{idx_tema}"])}),
                 label_visibility="collapsed")

    # 3. BASE DO COCKPIT: PÁGINAS (ABAS)
    PAGINAS = ["demo", "ypoemas", "eureka", "off-máquina", "books", "about"]
    aba_atual = PAGINAS[st.session_state.current_tab_idx]
    aba_sel = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS], default=aba_atual)
    if aba_sel and aba_sel != aba_atual:
        st.session_state.current_tab_idx = PAGINAS.index(aba_sel)
        st.rerun()
    
    st.markdown('</div></div>', unsafe_allow_html=True)

    # --- PALCO CENTRAL ---
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    try:
        from lay_2_ypo import gera_poema
        res_bruto = gera_poema(lista_temas[idx_tema], str(st.session_state.seed))
        txt_unido = "".join(res_bruto) if isinstance(res_bruto, list) else str(res_bruto)
        txt_final = tradutor_estavel(txt_unido.strip().replace("\n", "<br>"), lang=idiomas[st.session_state.lang])
        st.markdown(f'<div class="poema-box">{txt_final}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Erro no Motor: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
