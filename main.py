import streamlit as st
import extra_streamlit_components as stx
import os
import random
from deep_translator import GoogleTranslator

# CRONOLOGIA ATIVA: X=14 (CONSOLIDAÇÃO: Cockpit Fixo + Scroll de Palco)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "base")

def aplicar_estetica_fixed_cockpit():
    st.markdown("""
        <style>
            header[data-testid="stHeader"], footer { visibility: hidden; height: 0px; }
            [data-testid="stSidebar"] { display: none; }
            
            /* FIXANDO O COCKPIT NO TOPO */
            .fixed-top {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                background-color: white;
                z-index: 999;
                padding: 10px 2.5% 0 2.5%;
                border-bottom: 1px solid #f0f0f0;
            }
            
            /* ESPAÇAMENTO PARA O PALCO NÃO SUMIR SOB O COCKPIT */
            .main-content { margin-top: 180px; }

            .stButton > button { 
                border-radius: 50% !important; width: 42px !important; height: 42px !important; 
                border: 1px solid #ddd !important; background: #fff;
            }
            
            .poema-box { 
                font-family: 'Georgia', serif; font-size: 1.85em; line-height: 1.6; 
                color: #111; padding: 20px; text-align: left;
                border-left: 3px solid #f5f5f5;
            }
        </style>
    """, unsafe_allow_html=True)

def tradutor_machina(txt, lang='pt'):
    if not txt or lang == 'pt': return txt
    try:
        trad = GoogleTranslator(source='pt', target=lang).translate(text=txt)
        for tag in ["<br>>", "< br>", "<br >", "<br ", " br>", "</br>", " <br>"]:
            trad = trad.replace(tag, "<br>")
        return trad
    except: return txt

def main():
    st.set_page_config(layout="wide", page_title="Machina Poética - Cockpit Fixo")
    aplicar_estetica_fixed_cockpit()

    # --- DADOS ---
    arquivos = sorted([f for f in os.listdir(BASE_PATH) if f.startswith("rol_") and f.endswith(".txt")]) if os.path.exists(BASE_PATH) else []
    LIVROS = {f.replace("rol_", "").replace(".txt", ""): f for f in arquivos}
    if not LIVROS: LIVROS = {"todos os temas": "rol_todos os temas.txt"}

    # --- ESTADO ---
    if 'current_tab_idx' not in st.session_state: st.session_state.current_tab_idx = 0 
    if 'book_em_foco' not in st.session_state: st.session_state.book_em_foco = list(LIVROS.keys())[0]
    if 'temas_memoria' not in st.session_state: st.session_state.temas_memoria = {b: 0 for b in LIVROS}
    if 'seed_mutante' not in st.session_state: st.session_state.seed_mutante = 0
    if 'idioma' not in st.session_state: st.session_state.idioma = 'Português'
    if 'talk' not in st.session_state: st.session_state.talk = False

    # --- CONTAINER FIXO (COCKPIT) ---
    st.markdown('<div class="fixed-top">', unsafe_allow_html=True)
    
    # Linha 1: Botões e Idioma
    c_mut, c_prev, c_rand, c_next, c_help, c_talk, c_lang, c_esp = st.columns([0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 2, 4])
    if c_mut.button("✚"): st.session_state.seed_mutante += 1; st.rerun()
    if c_prev.button("❰"): st.session_state.temas_memoria[st.session_state.book_em_foco] -= 1; st.rerun()
    if c_rand.button("✱"): st.session_state.temas_memoria[st.session_state.book_em_foco] = random.randint(0, 999); st.rerun()
    if c_next.button("❱"): st.session_state.temas_memoria[st.session_state.book_em_foco] += 1; st.rerun()
    c_help.button("?")
    t_icon = "🎙️" if st.session_state.talk else "🔇"
    if c_talk.button(t_icon): st.session_state.talk = not st.session_state.talk; st.rerun()
    
    with c_lang:
        langs = {'Português': 'pt', 'English': 'en', 'Español': 'es', 'Français': 'fr', 'Italiano': 'it'}
        st.session_state.idioma = st.selectbox("L", list(langs.keys()), index=list(langs.keys()).index(st.session_state.idioma), label_visibility="collapsed")

    # Linha 2: Abas de Navegação
    PAGINAS = ["demo", "ypoemas", "eureka", "off-máquina", "books", "about"]
    aba_atual = PAGINAS[st.session_state.current_tab_idx]
    aba_sel = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS], default=aba_atual)
    if aba_sel and aba_sel != aba_atual:
        st.session_state.current_tab_idx = PAGINAS.index(aba_sel)
        st.rerun()

    # Linha 3: Drop_list de Temas
    book_foco = "todos os temas" if aba_atual == "demo" else st.session_state.book_em_foco
    lista_temas = ["Silêncio"]
    caminho_livro = os.path.join(BASE_PATH, LIVROS.get(book_foco, "rol_todos os temas.txt"))
    if os.path.exists(caminho_livro):
        with open(caminho_livro, "r", encoding="utf-8") as f:
            lista_temas = [l.strip() for l in f if l.strip() and not l.startswith("[")]

    idx_tema = st.session_state.temas_memoria.get(book_foco, 0) % len(lista_temas)
    st.selectbox("Tema", lista_temas, index=idx_tema, key=f"drop_{idx_tema}", 
                 on_change=lambda: st.session_state.temas_memoria.update({book_foco: lista_temas.index(st.session_state[f"drop_{idx_tema}"])}),
                 label_visibility="collapsed")
    
    st.markdown('</div>', unsafe_allow_html=True) # FIM DO FIXED-TOP

    # --- PALCO (CONTEÚDO) ---
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    try:
        from lay_2_ypo import gera_poema
        res = gera_poema(lista_temas[idx_tema], str(st.session_state.seed_mutante))
        txt = ("".join(res) if isinstance(res, list) else str(res)).strip().replace("\n", "<br>")
        txt_final = tradutor_machina(txt, lang=langs[st.session_state.idioma])
        st.markdown(f'<div class="poema-box">{txt_final}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Integridade do Motor: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
