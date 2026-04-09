import streamlit as st
import extra_streamlit_components as stx
import os
import random
from deep_translator import GoogleTranslator

# CRONOLOGIA ATIVA: X=12 (RECONSTRUÇÃO DA HIERARQUIA VERTICAL)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "base")

def aplicar_estetica_fiel():
    st.markdown("""
        <style>
            header[data-testid="stHeader"], footer { visibility: hidden; height: 0px; }
            [data-testid="stSidebar"] { display: none; }
            .block-container { padding-top: 0.5rem !important; max-width: 95% !important; }
            
            /* Botões de Ação no Topo */
            .stButton > button { 
                border-radius: 50% !important; width: 40px !important; height: 40px !important; 
                border: 1px solid #ddd !important; background: #fff !important; color: #333 !important;
            }
            
            /* Ajuste de espaçamento para as abas abaixo dos botões */
            .stTabs { margin-top: -10px; }

            .poema-box { 
                font-family: 'Georgia', serif; font-size: 1.8em; line-height: 1.6; 
                color: #111; margin-top: 2rem; padding: 10px; text-align: left;
                border-left: 2px solid #eee;
            }
        </style>
    """, unsafe_allow_html=True)

def tradutor_machina(input_text, target_lang='pt'):
    if not input_text or target_lang == 'pt': return input_text
    try:
        output = GoogleTranslator(source='pt', target=target_lang).translate(text=input_text)
        for tag in ["<br>>", "< br>", "<br >", "<br ", " br>", "</br>"]:
            output = output.replace(tag, "<br>")
        return output
    except: return input_text

def main():
    st.set_page_config(layout="wide", page_title="Machina Poética")
    aplicar_estetica_fiel()

    # --- DADOS ---
    arquivos = sorted([f for f in os.listdir(BASE_PATH) if f.startswith("rol_") and f.endswith(".txt")]) if os.path.exists(BASE_PATH) else []
    LIVROS = {f.replace("rol_", "").replace(".txt", ""): f for f in arquivos}
    if not LIVROS: LIVROS = {"todos os temas": "rol_todos os temas.txt"}

    # --- ESTADO ---
    if 'current_tab_idx' not in st.session_state: st.session_state.current_tab_idx = 0 
    if 'book_em_foco' not in st.session_state: st.session_state.book_em_foco = list(LIVROS.keys())[0]
    if 'tema_idx_por_book' not in st.session_state: st.session_state.tema_idx_por_book = {b: 0 for b in LIVROS}
    if 'seed_mutante' not in st.session_state: st.session_state.seed_mutante = 0
    if 'idioma' not in st.session_state: st.session_state.idioma = 'Português'
    if 'talk_audio' not in st.session_state: st.session_state.talk_audio = False

    # 1. TOPO DA TELA: BOTÕES DE NAVEGAÇÃO E AÇÃO
    c_mut, c_prev, c_rand, c_next, c_help, c_talk, c_lang, c_esp = st.columns([0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 1.5, 4])
    
    if c_mut.button("✚"): st.session_state.seed_mutante += 1; st.rerun()
    if c_prev.button("❰"): st.session_state.tema_idx_por_book[st.session_state.book_em_foco] -= 1; st.rerun()
    if c_rand.button("✱"): st.session_state.tema_idx_por_book[st.session_state.book_em_foco] = random.randint(0, 100); st.rerun()
    if c_next.button("❱"): st.session_state.tema_idx_por_book[st.session_state.book_em_foco] += 1; st.rerun()
    c_help.button("?")
    
    label_talk = "🎙️" if st.session_state.talk_audio else "🔇"
    if c_talk.button(label_talk):
        st.session_state.talk_audio = not st.session_state.talk_audio
        st.rerun()

    with c_lang:
        idiomas = {'Português': 'pt', 'English': 'en', 'Español': 'es', 'Français': 'fr', 'Italiano': 'it'}
        st.session_state.idioma = st.selectbox("L", list(idiomas.keys()), 
                                               index=list(idiomas.keys()).index(st.session_state.idioma),
                                               label_visibility="collapsed")

    # 2. PÁGINAS LOGO ABAIXO DOS BOTÕES
    PAGINAS = ["demo", "ypoemas", "eureka", "off-máquina", "books", "about"]
    aba_atual = PAGINAS[st.session_state.current_tab_idx]
    aba_sel = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS], default=aba_atual)
    if aba_sel and aba_sel != aba_atual:
        st.session_state.current_tab_idx = PAGINAS.index(aba_sel)
        st.rerun()

    # 3. DROP_LIST PARA OS TEMAS (Abaixo das abas)
    book_foco = "todos os temas" if aba_atual == "demo" else st.session_state.book_em_foco
    
    @st.cache_data
    def load_temas(arquivo):
        caminho = os.path.join(BASE_PATH, arquivo)
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                return [l.strip() for l in f if l.strip() and not l.startswith("[")]
        return ["Silêncio"]

    lista_temas = load_temas(LIVROS.get(book_foco, "rol_todos os temas.txt"))
    idx_tema = st.session_state.tema_idx_por_book.get(book_foco, 0) % len(lista_temas)
    tema_atual = lista_temas[idx_tema]

    st.selectbox("Tema", lista_temas, index=idx_tema, key=f"sel_{idx_tema}", 
                 on_change=lambda: st.session_state.tema_idx_por_book.update({book_foco: lista_temas.index(st.session_state[f"sel_{idx_tema}"])}),
                 label_visibility="collapsed")

    st.markdown("---")
    
    # 4. PALCO
    try:
        from lay_2_ypo import gera_poema
        res = gera_poema(tema_atual, str(st.session_state.seed_mutante))
        txt = ("".join(res) if isinstance(res, list) else str(res)).strip().replace("\n", "<br>")
        txt_final = tradutor_machina(txt, target_lang=idiomas[st.session_state.idioma])
        st.markdown(f'<div class="poema-box">{txt_final}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Motor: {e}")

if __name__ == "__main__":
    main()
