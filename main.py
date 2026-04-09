import streamlit as st
import extra_streamlit_components as stx
import os
import random
from deep_translator import GoogleTranslator

# CRONOLOGIA ATIVA: X=17 (RESTAURAÇÃO CANÔNICA: Ontem 23:24 PM)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "base")

def aplicar_estetica_final_ontem():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap');
            header[data-testid="stHeader"], footer { visibility: hidden; height: 0px; }
            [data-testid="stSidebar"] { display: none; }
            
            .stApp { background-color: #ffffff; }

            /* Cockpit Centralizado e Fixo */
            .fixed-top {
                position: fixed; top: 0; left: 0; width: 100%;
                background-color: rgba(255, 255, 255, 0.98);
                z-index: 999; padding: 10px 0;
                border-bottom: 1px solid #f0f0f0;
                display: flex; flex-direction: column; align-items: center;
            }
            
            .console-inner { width: 92%; max-width: 900px; }
            .main-content { margin-top: 185px; display: flex; justify-content: center; padding-bottom: 80px; }

            /* Botões do Console (Sequência: + < * > ? @) */
            .stButton > button { 
                border-radius: 50% !important; width: 42px !important; height: 42px !important; 
                border: 1px solid #eee !important; background: white !important; 
                color: #444 !important; transition: all 0.2s;
            }
            .stButton > button:hover { border-color: #888 !important; background: #fafafa !important; }

            /* O Palco: Tipografia de Livro */
            .poema-box { 
                font-family: 'Libre Baskerville', serif; font-size: 1.8em; line-height: 1.7; 
                color: #111; max-width: 700px; padding: 30px;
                text-align: left; border-left: 2px solid #111;
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
    aplicar_estetica_final_ontem()

    # --- DADOS ---
    arquivos = sorted([f for f in os.listdir(BASE_PATH) if f.startswith("rol_") and f.endswith(".txt")]) if os.path.exists(BASE_PATH) else []
    LIVROS = {f.replace("rol_", "").replace(".txt", ""): f for f in arquivos}
    if not LIVROS: LIVROS = {"todos os temas": "rol_todos os temas.txt"}

    # --- ESTADOS (Persistent Focus) ---
    if 'current_tab_idx' not in st.session_state: st.session_state.current_tab_idx = 0 
    if 'book_em_foco' not in st.session_state: st.session_state.book_em_foco = list(LIVROS.keys())[0]
    if 'memoria_temas' not in st.session_state: st.session_state.memoria_temas = {b: 0 for b in LIVROS}
    if 'seed' not in st.session_state: st.session_state.seed = 0
    if 'lang' not in st.session_state: st.session_state.lang = 'Português'
    if 'config_ativa' not in st.session_state: st.session_state.config_ativa = False

    # --- COCKPIT ---
    st.markdown('<div class="fixed-top"><div class="console-inner">', unsafe_allow_html=True)
    
    # 1. Navegação de Páginas (Abas)
    PAGINAS = ["demo", "ypoemas", "eureka", "off-máquina", "books", "about"]
    aba_atual = PAGINAS[st.session_state.current_tab_idx]
    aba_sel = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS], default=aba_atual)
    if aba_sel and aba_sel != aba_atual:
        st.session_state.current_tab_idx = PAGINAS.index(aba_sel)
        st.rerun()

    # 2. Console de Comando (+ ❰ ✱ ❱ ? @)
    c_btns, c_lang = st.columns([7, 3])
    with c_btns:
        b1, b2, b3, b4, b5, b6 = st.columns(6)
        if b1.button("✚"): st.session_state.seed += 1; st.rerun() # Mutação
        if b2.button("❰"): st.session_state.memoria_temas[st.session_state.book_em_foco] -= 1; st.rerun()
        if b3.button("✱"): st.session_state.memoria_temas[st.session_state.book_em_foco] = random.randint(0, 5000); st.rerun()
        if b4.button("❱"): st.session_state.memoria_temas[st.session_state.book_em_foco] += 1; st.rerun()
        b5.button("?") # Help
        if b6.button("@"): # Config / Talk Management
            st.session_state.config_ativa = not st.session_state.config_ativa
            st.rerun()

    with c_lang:
        idiomas = {'Português': 'pt', 'English': 'en', 'Español': 'es', 'Français': 'fr', 'Italiano': 'it'}
        st.session_state.lang = st.selectbox("L", list(idiomas.keys()), index=list(idiomas.keys()).index(st.session_state.lang), label_visibility="collapsed")

    # 3. Drop_list de Temas
    book_foco = "todos os temas" if aba_atual == "demo" else st.session_state.book_em_foco
    with open(os.path.join(BASE_PATH, LIVROS.get(book_foco, "rol_todos os temas.txt")), "r", encoding="utf-8") as f:
        lista_temas = [l.strip() for l in f if l.strip() and not l.startswith("[")]

    idx_tema = st.session_state.memoria_temas.get(book_foco, 0) % len(lista_temas)
    st.selectbox("T", lista_temas, index=idx_tema, key=f"drp_{idx_tema}", 
                 on_change=lambda: st.session_state.memoria_temas.update({book_foco: lista_temas.index(st.session_state[f"drp_{idx_tema}"])}),
                 label_visibility="collapsed")
    
    st.markdown('</div></div>', unsafe_allow_html=True)

    # --- PALCO CENTRAL ---
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    try:
        from lay_2_ypo import gera_poema
        # Motor retorna lista de fragmentos -> Unir para manter integridade
        res_bruto = gera_poema(lista_temas[idx_tema], str(st.session_state.seed))
        txt_unido = "".join(res_bruto) if isinstance(res_bruto, list) else str(res_bruto)
        txt_limpo = txt_unido.strip().replace("\n", "<br>")
        
        txt_final = tradutor_estavel(txt_limpo, lang=idiomas[st.session_state.lang])
        st.markdown(f'<div class="poema-box">{txt_final}</div>', unsafe_allow_html=True)
        
        if st.session_state.config_ativa:
            st.toast("Modo de Gerenciamento Ativado", icon="⚙️")
            
    except Exception as e:
        st.error(f"Integridade do Motor: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
