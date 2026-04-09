import streamlit as st
import os
import random
import base64
from gtts import gTTS
from io import BytesIO
from deep_translator import GoogleTranslator

# CRONOLOGIA ATIVA: X=61 (FIX DE DIAGRAMAÇÃO - WHITE-SPACE PRE)
# FOCO: Manter o formato exato do tema.ypo sem achatar linhas.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "base")

DICI_LANG = {
    'Português': 'pt', 'Español': 'es', 'Italiano': 'it', 
    'Français': 'fr', 'English': 'en', 'Català': 'ca',
    'Deutsch': 'de', 'Galego': 'gl', 'Română': 'ro'
}

def configurar_basico():
    st.markdown("""
        <style>
            header, footer { visibility: hidden; }
            .stButton > button { border-radius: 50% !important; width: 40px; height: 40px; }
            /* PRE PURO: RESPEITA QUEBRAS DE LINHA DO ARQUIVO ORIGINAL */
            pre { 
                font-family: 'serif'; 
                font-size: 20px; 
                line-height: 1.6; 
                white-space: pre !important; 
                word-wrap: normal !important;
                overflow-x: auto;
            }
        </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(layout="wide")
    configurar_basico()

    if 'seed' not in st.session_state: st.session_state.seed = random.randint(1, 9999)
    if 'lang' not in st.session_state: st.session_state.lang = 'Português'
    if 'book' not in st.session_state: st.session_state.book = "todos os temas"
    if 'tema_idx' not in st.session_state: st.session_state.tema_idx = 0
    if 'talk' not in st.session_state: st.session_state.talk = False
    if 'draw' not in st.session_state: st.session_state.draw = False

    arquivos = sorted([f for f in os.listdir(BASE_PATH) if f.startswith("rol_")])
    LIVROS = {f.replace("rol_", "").replace(".txt", ""): f for f in arquivos}
    
    try:
        with open(os.path.join(BASE_PATH, LIVROS.get(st.session_state.book, "rol_todos os temas.txt")), "r", encoding="utf-8") as f:
            temas_list = [l.strip() for l in f if l.strip() and not l.startswith("[")]
    except:
        temas_list = ["Erro"]

    _, col_nav, _ = st.columns([1, 2, 1])
    with col_nav:
        c = st.columns(6)
        if c[0].button("✚"): st.session_state.seed = random.randint(1, 9999); st.rerun()
        if c[1].button("❰"): st.session_state.tema_idx -= 1; st.rerun()
        if c[2].button("✱"): st.session_state.seed = random.randint(1, 9999); st.session_state.tema_idx = random.randint(0, len(temas_list)-1); st.rerun()
        if c[3].button("❱"): st.session_state.tema_idx += 1; st.rerun()
        with c[5]:
            with st.popover("@"):
                st.session_state.lang = st.selectbox("Idioma", list(DICI_LANG.keys()), index=list(DICI_LANG.keys()).index(st.session_state.lang))
                st.session_state.talk = st.checkbox("Talk", value=st.session_state.talk)
                st.session_state.draw = st.checkbox("Arts", value=st.session_state.draw)
        st.session_state.tema_idx = temas_list.index(st.selectbox("V", temas_list, index=st.session_state.tema_idx % len(temas_list), label_visibility="collapsed"))

    st.divider()
    
    header = f"⚫ {st.session_state.lang} ( {st.session_state.book} ) ( {st.session_state.tema_idx + 1} / {len(temas_list)} )"
    
    with st.expander(header, expanded=True):
        try:
            from lay_2_ypo import gera_poema
            tema_atual = temas_list[st.session_state.tema_idx % len(temas_list)]
            
            # GERAÇÃO PURA
            res = gera_poema(tema_atual, str(st.session_state.seed))
            curr_ypoema = "".join(res) if isinstance(res, list) else str(res)

            # TRADUÇÃO (Mantendo a estrutura de strings se possível)
            if st.session_state.lang != "Português":
                curr_ypoema = GoogleTranslator(source='pt', target=DICI_LANG[st.session_state.lang]).translate(curr_ypoema)

            # EXIBIÇÃO EM BLOCO PRÉ-FORMATADO
            st.markdown(f"<pre>{curr_ypoema}</pre>", unsafe_allow_html=True)

            if st.session_state.draw:
                st.image("https://via.placeholder.com/500", caption=tema_atual)

            if st.session_state.talk:
                tts = gTTS(text=curr_ypoema, lang=DICI_LANG[st.session_state.lang])
                fp = BytesIO()
                tts.write_to_fp(fp)
                b64 = base64.b64encode(fp.getvalue()).decode()
                st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}"></audio>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Erro: {e}")

if __name__ == "__main__":
    main()
