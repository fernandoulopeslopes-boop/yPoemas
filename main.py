import streamlit as st
import os
import random
import base64
from gtts import gTTS
from io import BytesIO
from deep_translator import GoogleTranslator

# CRONOLOGIA ATIVA: X=65 (ESTRUTURA LIMPA - DADOS REAIS)
# REGRA: Fidelidade absoluta ao ciclo de arquivos e ao motor original.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "base")
TEMP_PATH = os.path.join(BASE_DIR, "temp")

if not os.path.exists(TEMP_PATH):
    os.makedirs(TEMP_PATH)

def load_typo(user_id):
    path = os.path.join(TEMP_PATH, f"TYPO_{user_id}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_ypoema(text, image=None):
    st.markdown(f"<pre style='font-family: serif; font-size: 20px; white-space: pre;'>{text}</pre>", unsafe_allow_html=True)
    if image:
        st.image(image)

def main():
    st.set_page_config(layout="wide")
    
    if 'seed' not in st.session_state: st.session_state.seed = random.randint(1, 9999)
    if 'lang' not in st.session_state: st.session_state.lang = 'Português'
    if 'last_lang' not in st.session_state: st.session_state.last_lang = 'Português'
    if 'tema_idx' not in st.session_state: st.session_state.tema_idx = 0
    if 'book' not in st.session_state: st.session_state.book = "todos os temas"
    if 'talk' not in st.session_state: st.session_state.talk = False
    if 'draw' not in st.session_state: st.session_state.draw = False

    IPAddress = "SESSION_USER"

    # CARREGAMENTO DO ROL
    arquivos = sorted([f for f in os.listdir(BASE_PATH) if f.startswith("rol_")])
    LIVROS = {f.replace("rol_", "").replace(".txt", ""): f for f in arquivos}
    
    try:
        path_rol = os.path.join(BASE_PATH, LIVROS.get(st.session_state.book, "rol_todos os temas.txt"))
        with open(path_rol, "r", encoding="utf-8") as f:
            temas_list = [l.strip() for l in f if l.strip() and not l.startswith("[")]
        
        # O tema é extraído diretamente da lista real
        st.session_state.tema = temas_list[st.session_state.tema_idx % len(temas_list)]
    except:
        st.stop()

    from lay_2_ypo import gera_poema

    header = f"⚫ {st.session_state.lang} ( {st.session_state.book} )"
    with st.expander(header, expanded=True):
        
        # Execução do Motor
        if st.session_state.lang != st.session_state.last_lang:
            res = gera_poema(st.session_state.tema, str(st.session_state.seed))
            curr_ypoema = "".join(res)
        else:
            res = gera_poema(st.session_state.tema, str(st.session_state.seed))
            curr_ypoema = "".join(res)

        # Tradução com Ciclo de Normalização via HD
        if st.session_state.lang not in ["pt", "Português"]:
            dici = {'Español': 'es', 'Italiano': 'it', 'English': 'en', 'Français': 'fr', 'Català': 'ca', 'Deutsch': 'de'}
            target = dici.get(st.session_state.lang, 'en')
            curr_ypoema = GoogleTranslator(source='pt', target=target).translate(curr_ypoema)
            
            typo_user = "TYPO_" + IPAddress
            with open(os.path.join(TEMP_PATH, typo_user), "w", encoding="utf-8") as save_typo:
                save_typo.write(curr_ypoema)
                save_typo.close()
            curr_ypoema = load_typo(IPAddress)

        write_ypoema(curr_ypoema, None)

        if st.session_state.talk:
            tts = gTTS(text=curr_ypoema, lang='pt')
            fp = BytesIO()
            tts.write_to_fp(fp)
            b64 = base64.b64encode(fp.getvalue()).decode()
            st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}"></audio>', unsafe_allow_html=True)

    st.session_state.last_lang = st.session_state.lang

if __name__ == "__main__":
    main()
