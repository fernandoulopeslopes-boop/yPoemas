import streamlit as st
import os
import random
import base64
from gtts import gTTS
from io import BytesIO
from deep_translator import GoogleTranslator

# CRONOLOGIA ATIVA: X=70 (PRECISÃO ABSOLUTA - SEM PRESSA)
# STATUS: Motor e Cockpit integrados com Ciclo de HD para Normalização.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "base")
TEMP_PATH = os.path.join(BASE_DIR, "temp")

# Garantia de infraestrutura
if not os.path.exists(TEMP_PATH):
    os.makedirs(TEMP_PATH)

def load_typo(user_id):
    """Lê o arquivo físico para normalizar line breaks do sistema operacional."""
    path = os.path.join(TEMP_PATH, f"TYPO_{user_id}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_ypoema(text, image=None):
    """Renderiza o texto puro respeitando a mancha gráfica do load_typo."""
    st.text(text)
    if image:
        st.image(image)

def main():
    st.set_page_config(layout="wide", page_title="Machina Poética")
    
    # --- INICIALIZAÇÃO DE ESTADOS ---
    if 'seed' not in st.session_state: st.session_state.seed = random.randint(1, 9999)
    if 'lang' not in st.session_state: st.session_state.lang = 'Português'
    if 'last_lang' not in st.session_state: st.session_state.last_lang = 'Português'
    if 'tema_idx' not in st.session_state: st.session_state.tema_idx = 0
    if 'book' not in st.session_state: st.session_state.book = "todos os temas"
    if 'talk' not in st.session_state: st.session_state.talk = False
    if 'draw' not in st.session_state: st.session_state.draw = False
    if 'tema' not in st.session_state: st.session_state.tema = ""

    IPAddress = "SESSION_USER"

    # --- CARREGAMENTO DO ROL DE TEMAS ---
    arquivos = sorted([f for f in os.listdir(BASE_PATH) if f.startswith("rol_")])
    LIVROS = {f.replace("rol_", "").replace(".txt", ""): f for f in arquivos}
    
    try:
        path_rol = os.path.join(BASE_PATH, LIVROS.get(st.session_state.book, "rol_todos os temas.txt"))
        with open(path_rol, "r", encoding="utf-8") as f:
            temas_list = [l.strip() for l in f if l.strip() and not l.startswith("[")]
        
        # Sincronização segura do tema selecionado
        st.session_state.tema = temas_list[st.session_state.tema_idx % len(temas_list)]
    except Exception as e:
        st.error(f"Erro na base de dados: {e}")
        st.stop()

    # --- COCKPIT (PAINEL DE CONTROLE) ---
    _, col_nav, _ = st.columns([1, 2, 1])
    with col_nav:
        c = st.columns(6)
        if c[0].button("✚"): 
            st.session_state.seed = random.randint(1, 9999)
            st.rerun()
        if c[1].button("❰"): 
            st.session_state.tema_idx = (st.session_state.tema_idx - 1) % len(temas_list)
            st.rerun()
        if c[2].button("✱"): 
            st.session_state.seed = random.randint(1, 9999)
            st.session_state.tema_idx = random.randint(0, len(temas_list)-1)
            st.rerun()
        if c[3].button("❱"): 
            st.session_state.tema_idx = (st.session_state.tema_idx + 1) % len(temas_list)
            st.rerun()
        with c[5]:
            with st.popover("@"):
                langs = ['Português', 'Español', 'Italiano', 'English', 'Français']
                st.session_state.lang = st.selectbox("Idioma", langs, index=langs.index(st.session_state.lang))
                st.session_state.talk = st.checkbox("Talk", value=st.session_state.talk)
                st.session_state.draw = st.checkbox("Arts", value=st.session_state.draw)
        
        # Seletor visual de temas (V)
        tema_sel = st.selectbox("V", temas_list, index=st.session_state.tema_idx % len(temas_list), label_visibility="collapsed")
        if tema_sel != st.session_state.tema:
            st.session_state.tema = tema_sel
            st.session_state.tema_idx = temas_list.index(tema_sel)
            st.rerun()

    st.divider()

    # --- O PALCO (MOTOR E PERSISTÊNCIA) ---
    from lay_2_ypo import gera_poema

    header_text = f"⚫ {st.session_state.lang} ( {st.session_state.book} ) ( {st.session_state.tema_idx + 1} / {len(temas_list)} )"
    ypoemas_expander = st.expander(header_text, expanded=True)

    with ypoemas_expander:
        # 1. Geração pelo Motor Real
        res = gera_poema(st.session_state.tema, str(st.session_state.seed))
        curr_ypoema = "".join(res)

        # 2. Tradução Condicional
        if st.session_state.lang not in ["pt", "Português"]:
            dici = {'Español': 'es', 'Italiano': 'it', 'English': 'en', 'Français': 'fr'}
            target = dici.get(st.session_state.lang, 'en')
            curr_ypoema = GoogleTranslator(source='pt', target=target).translate(curr_ypoema)

        # 3. CICLO DE NORMALIZAÇÃO OBRIGATÓRIO (HD)
        # Este passo garante a diagramação original, independente do idioma.
        typo_user = "TYPO_" + IPAddress
        with open(os.path.join(TEMP_PATH, typo_user), "w", encoding="utf-8") as save_typo:
            save_typo.write(curr_ypoema)
        
        # Recarregamento para "curar" o texto
        curr_ypoema = load_typo(IPAddress)

        # 4. EXIBIÇÃO
        LOGO_TEXT = curr_ypoema
        LOGO_IMAGE = None
        # Espaço reservado para Arts futura
        # if st.session_state.draw: LOGO_IMAGE = load_arts(st.session_state.tema)

        write_ypoema(LOGO_TEXT, LOGO_IMAGE)

        # 5. VOZ (Talk)
        if st.session_state.talk:
            v_lang = 'pt' if st.session_state.lang in ['pt', 'Português'] else {'Español': 'es', 'Italiano': 'it', 'English': 'en', 'Français': 'fr'}.get(st.session_state.lang, 'pt')
            tts = gTTS(text=curr_ypoema, lang=v_lang)
            fp = BytesIO()
            tts.write_to_fp(fp)
            b64 = base64.b64encode(fp.getvalue()).decode()
            st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}"></audio>', unsafe_allow_html=True)

    st.session_state.last_lang = st.session_state.lang

if __name__ == "__main__":
    main()
