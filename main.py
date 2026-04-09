import streamlit as st
import extra_streamlit_components as stx
import os
import random
from deep_translator import GoogleTranslator

# CRONOLOGIA ATIVA: X=13 (EVOLUÇÃO: Hierarquia Vertical + Memória de Foco por Livro)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "base")

def aplicar_estetica_v13():
    st.markdown("""
        <style>
            header[data-testid="stHeader"], footer { visibility: hidden; height: 0px; }
            [data-testid="stSidebar"] { display: none; }
            .block-container { padding-top: 0.5rem !important; max-width: 95% !important; }
            
            /* Botões de Ação Superiores: O console de comando */
            .stButton > button { 
                border-radius: 50% !important; width: 42px !important; height: 42px !important; 
                border: 1px solid #ddd !important; background: #fff !important; 
                transition: all 0.3s ease;
            }
            .stButton > button:hover { border-color: #888 !important; transform: scale(1.1); }
            
            /* Estilo da Drop_list de Temas */
            .stSelectbox [data-testid="stMarkdownContainer"] { font-size: 1.1em; color: #555; }

            /* O Palco Central */
            .poema-box { 
                font-family: 'Georgia', serif; font-size: 1.85em; line-height: 1.6; 
                color: #121212; margin-top: 1.5rem; padding: 20px; text-align: left;
                border-left: 3px solid #f9f9f9;
            }
        </style>
    """, unsafe_allow_html=True)

def sanitizar_sonoridade(texto):
    if not texto: return ""
    tags = ["<br>>", "< br>", "<br >", "<br ", " br>", "</br>", " <br>", "<Br>", "<BR>"]
    for tag in tags:
        texto = texto.replace(tag, "<br>")
    return texto

def tradutor_especialista(txt, lang_target='pt'):
    if not txt or lang_target == 'pt': return txt
    try:
        traducao = GoogleTranslator(source='pt', target=lang_target).translate(text=txt)
        return sanitizar_sonoridade(traducao)
    except: return txt

def main():
    st.set_page_config(layout="wide", page_title="Machina Poética - Console")
    aplicar_estetica_v13()

    # --- MAPEAMENTO DE ARQUIVOS (Auto-discovery) ---
    arquivos = sorted([f for f in os.listdir(BASE_PATH) if f.startswith("rol_") and f.endswith(".txt")]) if os.path.exists(BASE_PATH) else []
    LIVROS = {f.replace("rol_", "").replace(".txt", ""): f for f in arquivos}
    if not LIVROS: LIVROS = {"todos os temas": "rol_todos os temas.txt"}

    # --- ESTADOS DE PERSISTÊNCIA ---
    if 'current_tab_idx' not in st.session_state: st.session_state.current_tab_idx = 0 
    if 'book_em_foco' not in st.session_state: st.session_state.book_em_foco = list(LIVROS.keys())[0]
    if 'temas_memoria' not in st.session_state: st.session_state.temas_memoria = {b: 0 for b in LIVROS}
    if 'seed_mutante' not in st.session_state: st.session_state.seed_mutante = 0
    if 'idioma_atual' not in st.session_state: st.session_state.idioma_atual = 'Português'
    if 'talk_audio_on' not in st.session_state: st.session_state.talk_audio_on = False

    # 1. TOPO: O CONSOLE DE BOTÕES
    c_mut, c_prev, c_rand, c_next, c_help, c_talk, c_lang, c_esp = st.columns([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 2, 4])
    
    if c_mut.button("✚"): st.session_state.seed_mutante += 1; st.rerun()
    if c_prev.button("❰"): st.session_state.temas_memoria[st.session_state.book_em_foco] -= 1; st.rerun()
    if c_rand.button("✱"): st.session_state.temas_memoria[st.session_state.book_em_foco] = random.randint(0, 999); st.rerun()
    if c_next.button("❱"): st.session_state.temas_memoria[st.session_state.book_em_foco] += 1; st.rerun()
    
    c_help.button("?")
    
    btn_talk = "🎙️" if st.session_state.talk_audio_on else "🔇"
    if c_talk.button(btn_talk):
        st.session_state.talk_audio_on = not st.session_state.talk_audio_on
        st.rerun()

    with c_lang:
        langs = {'Português': 'pt', 'English': 'en', 'Español': 'es', 'Français': 'fr', 'Italiano': 'it', 'Deutsch': 'de'}
        st.session_state.idioma_atual = st.selectbox("L", list(langs.keys()), 
                                                   index=list(langs.keys()).index(st.session_state.idioma_atual),
                                                   label_visibility="collapsed")

    # 2. SUB-TOPO: AS PÁGINAS (ABAS)
    PAGINAS = ["demo", "ypoemas", "eureka", "off-máquina", "books", "about"]
    aba_atual = PAGINAS[st.session_state.current_tab_idx]
    aba_sel = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS], default=aba_atual)
    
    if aba_sel and aba_sel != aba_atual:
        st.session_state.current_tab_idx = PAGINAS.index(aba_sel)
        # Sincroniza o livro em foco com a aba se necessário
        if aba_sel in LIVROS: st.session_state.book_em_foco = aba_sel
        st.rerun()

    # 3. CONTROLE: DROP_LIST DE TEMAS
    book_foco = "todos os temas" if aba_atual == "demo" else st.session_state.book_em_foco
    
    @st.cache_data
    def carregar_temas_disco(arquivo):
        caminho = os.path.join(BASE_PATH, arquivo)
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                return [l.strip() for l in f if l.strip() and not l.startswith("[")]
        return ["Silêncio"]

    temas_lista = carregar_temas_disco(LIVROS.get(book_foco, "rol_todos os temas.txt"))
    idx_tema = st.session_state.temas_memoria.get(book_foco, 0) % len(temas_lista)
    tema_ativo = temas_lista[idx_tema]

    # A Drop_list que você mencionou
    st.selectbox("Seletor de Temas", temas_lista, index=idx_tema, key=f"drop_{idx_tema}", 
                 on_change=lambda: st.session_state.temas_memoria.update({book_foco: temas_lista.index(st.session_state[f"drop_{idx_tema}"])}),
                 label_visibility="collapsed")

    st.markdown("---")
    
    # 4. PALCO
    try:
        from lay_2_ypo import gera_poema
        bruto = gera_poema(tema_ativo, str(st.session_state.seed_mutante))
        base_html = ("".join(bruto) if isinstance(bruto, list) else str(bruto)).strip().replace("\n", "<br>")
        
        final = tradutor_especialista(base_html, lang_target=langs[st.session_state.idioma_atual])
        st.markdown(f'<div class="poema-box">{final}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Erro de Execução: {e}")

if __name__ == "__main__":
    main()
