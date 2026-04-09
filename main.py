import streamlit as st
import os
import random
import base64
from gtts import gTTS
from io import BytesIO
from deep_translator import GoogleTranslator

# CRONOLOGIA ATIVA: X=63 (RETORNO AO BÁSICO - INTEGRIDADE DA GERAÇÃO)
# FOCO: Respeito absoluto ao fluxo de arquivos e diagramação original.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "base")
TEMP_PATH = os.path.join(BASE_DIR, "temp")

if not os.path.exists(TEMP_PATH):
    os.makedirs(TEMP_PATH)

# --- FUNÇÕES DE INFRAESTRUTURA (ORIGINAIS) ---
def load_typo(user_id):
    path = os.path.join(TEMP_PATH, f"TYPO_{user_id}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_ypoema(text, image=None):
    # O uso do <pre> é o que sustenta a diagramação do tema.ypo
    st.markdown(f"<pre style='font-family: serif; font-size: 20px; white-space: pre;'>{text}</pre>", unsafe_allow_html=True)
    if image:
        st.image(image)

def main():
    st.set_page_config(layout="wide")
    
    # Estados de Sessão (Mecanismo de Controle)
    if 'seed' not in st.session_state: st.session_state.seed = random.randint(1, 9999)
    if 'lang' not in st.session_state: st.session_state.lang = 'Português'
    if 'last_lang' not in st.session_state: st.session_state.last_lang = 'Português'
    if 'tema' not in st.session_state: st.session_state.tema = ""
    if 'talk' not in st.session_state: st.session_state.talk = False
    if 'draw' not in st.session_state: st.session_state.draw = False

    IPAddress = "USER_FIX" # Simulação do identificador de arquivo

    # --- EXECUÇÃO DO BLOCO DE CURADORIA ---
    from lay_2_ypo import gera_poema

    # Seletor de temas e controle (Simulado para o teste de geração)
    tema_atual = "exemplo_tema" # Este valor viria do seu seletor
    st.session_state.tema = tema_atual

    header = f"⚫ {st.session_state.lang}"
    ypoemas_expander = st.expander(header, expanded=True)

    with ypoemas_expander:
        # A LÓGICA DE ANOS REINSTALADA:
        if st.session_state.lang != st.session_state.last_lang:
            # Simulando load_lypo() através do gerador
            res = gera_poema(st.session_state.tema, str(st.session_state.seed))
            curr_ypoema = "".join(res)
        else:
            # Simulando load_poema() e load_lypo()
            res = gera_poema(st.session_state.tema, str(st.session_state.seed))
            curr_ypoema = "".join(res)

        # TRADUÇÃO COM CICLO DE HD (O FILTRO DE DIAGRAMAÇÃO)
        if st.session_state.lang != "Português":
            dici = {'Español': 'es', 'Italiano': 'it', 'English': 'en', 'Français': 'fr'}
            target = dici.get(st.session_state.lang, 'en')
            
            curr_ypoema = GoogleTranslator(source='pt', target=target).translate(curr_ypoema)
            
            typo_user = "TYPO_" + IPAddress
            # Escrita Física
            with open(os.path.join(TEMP_PATH, typo_user), "w", encoding="utf-8") as save_typo:
                save_typo.write(curr_ypoema)
                save_typo.close()
            
            # Leitura Física (Normalização de quebras de linha)
            curr_ypoema = load_typo(IPAddress)

        # FINALIZAÇÃO E RENDERIZAÇÃO
        LOGO_TEXT = curr_ypoema
        LOGO_IMAGE = None
        
        if st.session_state.draw:
            # LOGO_IMAGE = load_arts(st.session_state.tema)
            LOGO_IMAGE = None

        # Saída atômica
        write_ypoema(LOGO_TEXT, LOGO_IMAGE)

        # Talk condicional
        if st.session_state.talk:
            tts = gTTS(text=curr_ypoema, lang='pt') # Lang dinâmica na versão final
            fp = BytesIO()
            tts.write_to_fp(fp)
            b64 = base64.b64encode(fp.getvalue()).decode()
            st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}"></audio>', unsafe_allow_html=True)

    st.session_state.last_lang = st.session_state.lang

if __name__ == "__main__":
    main()
