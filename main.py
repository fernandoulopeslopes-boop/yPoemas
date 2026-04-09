import streamlit as st
import extra_streamlit_components as stx
import os
import random
from deep_translator import GoogleTranslator

# CRONOLOGIA ATIVA: X=11 (RESTAURAÇÃO TOTAL: Cockpit Completo + Talk/Audio)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "base")

def aplicar_estetica_machina():
    st.markdown("""
        <style>
            header[data-testid="stHeader"], footer { visibility: hidden; height: 0px; }
            [data-testid="stSidebar"] { display: none; }
            .block-container { padding-top: 1rem !important; max-width: 95% !important; }
            
            /* Botões do Cockpit: Estética Industrial Circular */
            .stButton > button { 
                border-radius: 50% !important; width: 42px !important; height: 42px !important; 
                border: 1px solid #eee !important; background: white !important; 
                color: #444 !important; box-shadow: 0px 1px 3px rgba(0,0,0,0.05);
            }
            .stButton > button:hover { border-color: #999 !important; background: #fdfdfd !important; }

            /* O Palco: Onde a poesia respira */
            .poema-box { 
                font-family: 'Georgia', serif; font-size: 1.8em; line-height: 1.6; 
                color: #111; margin-top: 2rem; padding: 10px; text-align: left;
                border-left: 2px solid #efefef;
            }
        </style>
    """, unsafe_allow_html=True)

def tradutor_machina(input_text, target_lang='pt'):
    if not input_text or target_lang == 'pt': return input_text
    try:
        output = GoogleTranslator(source='pt', target=target_lang).translate(text=input_text)
        # Sanitização "na marra" recuperada
        for tag in ["<br>>", "< br>", "<br >", "<br ", " br>", "</br>", " <br>"]:
            output = output.replace(tag, "<br>")
        return output
    except: return input_text

def main():
    st.set_page_config(layout="wide", page_title="Machina Poética")
    aplicar_estetica_machina()

    # --- MAPEAMENTO DE ARQUIVOS ---
    if not os.path.exists(BASE_PATH): os.makedirs(BASE_PATH, exist_ok=True)
    arquivos = sorted([f for f in os.listdir(BASE_PATH) if f.startswith("rol_") and f.endswith(".txt")])
    LIVROS = {f.replace("rol_", "").replace(".txt", ""): f for f in arquivos}
    if not LIVROS: LIVROS = {"todos os temas": "rol_todos os temas.txt"}

    # --- GESTÃO DE ESTADO SOBERANO ---
    if 'current_tab_idx' not in st.session_state: st.session_state.current_tab_idx = 0 
    if 'book_em_foco' not in st.session_state: st.session_state.book_em_foco = list(LIVROS.keys())[0]
    if 'tema_idx_por_book' not in st.session_state: st.session_state.tema_idx_por_book = {b: 0 for b in LIVROS}
    if 'seed_mutante' not in st.session_state: st.session_state.seed_mutante = 0
    if 'idioma_selecionado' not in st.session_state: st.session_state.idioma_selecionado = 'Português'
    if 'talk_audio_ativo' not in st.session_state: st.session_state.talk_audio_ativo = False

    # Tabs Superiores
    PAGINAS = ["demo", "ypoemas", "eureka", "off-máquina", "books", "about"]
    aba_atual = PAGINAS[st.session_state.current_tab_idx]
    
    aba_sel = stx.tab_bar(data=[stx.TabBarItemData(id=p, title=p.upper(), description="") for p in PAGINAS], default=aba_atual)
    if aba_sel and aba_sel != aba_atual:
        st.session_state.current_tab_idx = PAGINAS.index(aba_sel)
        st.rerun()

    book_foco = "todos os temas" if aba_atual == "demo" else st.session_state.book_em_foco
    
    @st.cache_data
    def load_temas(arquivo):
        caminho = os.path.join(BASE_PATH, arquivo)
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                return [l.strip() for l in f if l.strip() and not l.startswith("[")]
        return ["Silêncio"]

    temas = load_temas(LIVROS.get(book_foco, "rol_todos os temas.txt"))
    idx_tema = st.session_state.tema_idx_por_book.get(book_foco, 0) % len(temas)
    tema_atual = temas[idx_tema]

    # --- COCKPIT (A Configuração Completa de Ontem) ---
    st.markdown("<br>", unsafe_allow_html=True)
    # Colunas com espaço para o botão extra de Talk/Audio
    c_mut, c_prev, c_rand, c_next, c_help, c_talk, c_sel_tema, c_lang = st.columns([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 4, 1.5])
    
    if c_mut.button("✚"): st.session_state.seed_mutante += 1; st.rerun()
    if c_prev.button("❰"): st.session_state.tema_idx_por_book[book_foco] = idx_tema - 1; st.rerun()
    if c_rand.button("✱"): st.session_state.tema_idx_por_book[book_foco] = random.randint(0, len(temas)-1); st.rerun()
    if c_next.button("❱"): st.session_state.tema_idx_por_book[book_foco] = idx_tema + 1; st.rerun()
    
    # Botão de Eureka/Help
    c_help.button("?") # Placeholder para a ajuda
    
    # BOTÃO EXTRA: Gerenciador de Talk + Áudio
    label_talk = "🎙️" if st.session_state.talk_audio_ativo else "🔇"
    if c_talk.button(label_talk):
        st.session_state.talk_audio_ativo = not st.session_state.talk_audio_ativo
        st.rerun()

    with c_sel_tema:
        st.selectbox("T", temas, index=idx_tema, key=f"sel_{idx_tema}", 
                     on_change=lambda: st.session_state.tema_idx_por_book.update({book_foco: temas.index(st.session_state[f"sel_{idx_tema}"])}),
                     label_visibility="collapsed")

    with c_lang:
        idiomas = {'Português': 'pt', 'English': 'en', 'Español': 'es', 'Français': 'fr', 'Italiano': 'it', 'Deutsch': 'de'}
        st.session_state.idioma_selecionado = st.selectbox("L", list(idiomas.keys()), 
                                                          index=list(idiomas.keys()).index(st.session_state.idioma_selecionado),
                                                          label_visibility="collapsed")

    st.markdown("---")
    
    # --- PALCO CENTRAL ---
    try:
        from lay_2_ypo import gera_poema
        res = gera_poema(tema_atual, str(st.session_state.seed_mutante))
        txt = ("".join(res) if isinstance(res, list) else str(res)).strip().replace("\n", "<br>")
        
        txt_final = tradutor_machina(txt, target_lang=idiomas[st.session_state.idioma_selecionado])
        st.markdown(f'<div class="poema-box">{txt_final}</div>', unsafe_allow_html=True)
        
        # Lógica de Áudio (se ativo)
        if st.session_state.talk_audio_ativo:
            st.info("O modo Talk + Áudio está monitorando a composição.")
            # Aqui entraria o trigger do gTTS ou similar conforme o projeto original
            
    except Exception as e:
        st.error(f"Conexão com o Motor: {e}")

if __name__ == "__main__":
    main()
    
