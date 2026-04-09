import streamlit as st
import os
import random
import base64
from gtts import gTTS
from io import BytesIO
from deep_translator import GoogleTranslator

# CRONOLOGIA ATIVA: X=59 (SANEAMENTO NATIVO & LÓGICA DE ANOS)
# FOCO: Estabilidade, Cockpit Fixo e Funções Atômicas.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "base")
MD_PATH = os.path.join(BASE_DIR, "md_files")

DICI_LANG = {
    'Português': 'pt', 'Español': 'es', 'Italiano': 'it', 
    'Français': 'fr', 'English': 'en', 'Català': 'ca',
    'Deutsch': 'de', 'Galego': 'gl', 'Română': 'ro'
}

def aplicar_estetica_v59():
    st.markdown("""
        <style>
            header, footer { visibility: hidden; height: 0px; }
            .block-container { padding-top: 2rem !important; }
            .stButton > button { 
                border-radius: 50% !important; width: 42px !important; height: 42px !important; 
                background: white !important; border: 1px solid #ddd !important;
            }
            /* REMOVE LABELS DOS SELECTS PARA LIMPEZA VISUAL */
            div[data-testid="stSelectbox"] label { display: none !important; }
            pre { 
                font-family: 'serif'; font-size: 20px; line-height: 1.6; 
                color: #1a1a1a; white-space: pre-wrap; word-wrap: break-word;
            }
        </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(layout="wide", page_title="Machina Poética")
    aplicar_estetica_v59()

    # --- 1. ESTADOS (LÓGICA DE ANOS) ---
    if 'seed' not in st.session_state: st.session_state.seed = random.randint(1, 99999)
    if 'lang' not in st.session_state: st.session_state.lang = 'Português'
    if 'book' not in st.session_state: st.session_state.book = "todos os temas"
    if 'tema_idx' not in st.session_state: st.session_state.tema_idx = 0
    if 'talk' not in st.session_state: st.session_state.talk = False
    if 'draw' not in st.session_state: st.session_state.draw = False
    if 'current_tab' not in st.session_state: st.session_state.current_tab = "DEMO"

    # --- 2. CARREGAMENTO DOS TEMAS ---
    arquivos = sorted([f for f in os.listdir(BASE_PATH) if f.startswith("rol_")]) if os.path.exists(BASE_PATH) else []
    LIVROS = {f.replace("rol_", "").replace(".txt", ""): f for f in arquivos}
    
    try:
        path_rol = os.path.join(BASE_PATH, LIVROS.get(st.session_state.book, "rol_todos os temas.txt"))
        with open(path_rol, "r", encoding="utf-8") as f:
            temas_list = [l.strip() for l in f if l.strip() and not l.startswith("[")]
    except:
        temas_list = ["Erro: Base não encontrada"]

    # --- 3. COCKPIT (NATIVO & CENTRALIZADO) ---
    _, col_centro, _ = st.columns([1, 2, 1])
    
    with col_centro:
        # BOTÕES ATÔMICOS
        b = st.columns(6)
        if b[0].button("✚", help="Nova variação (Seed)"): 
            st.session_state.seed = random.randint(1, 99999)
            st.rerun()
        if b[1].button("❰", help="Tema Anterior"): 
            st.session_state.tema_idx = (st.session_state.tema_idx - 1) % len(temas_list)
            st.rerun()
        if b[2].button("✱", help="Tudo Aleatório"): 
            st.session_state.seed = random.randint(1, 99999)
            st.session_state.tema_idx = random.randint(0, len(temas_list)-1)
            st.rerun()
        if b[3].button("❱", help="Próximo Tema"): 
            st.session_state.tema_idx = (st.session_state.tema_idx + 1) % len(temas_list)
            st.rerun()
        
        # HELP (?) NATIVO
        with b[4]:
            with st.popover("?"):
                h_file = os.path.join(MD_PATH, f"ABOUT_{st.session_state.current_tab}.md")
                if os.path.exists(h_file):
                    st.markdown(open(h_file, "r", encoding="utf-8").read())
                else:
                    st.info(f"Aguardando manual: {st.session_state.current_tab}")

        # CONFIG (@) NATIVO
        with b[5]:
            with st.popover("@"):
                st.session_state.lang = st.selectbox("L", list(DICI_LANG.keys()), 
                                                   index=list(DICI_LANG.keys()).index(st.session_state.lang))
                st.session_state.talk = st.checkbox("Talk", value=st.session_state.talk)
                st.session_state.draw = st.checkbox("Arts", value=st.session_state.draw)

        # VISOR (SELECTBOX SINCRONIZADO)
        tema_selecionado = st.selectbox("V", temas_list, index=st.session_state.tema_idx % len(temas_list))
        if tema_selecionado != temas_list[st.session_state.tema_idx % len(temas_list)]:
            st.session_state.tema_idx = temas_list.index(tema_selecionado)
            st.rerun()

    # ABAS (DEMO / YPOEMAS / ETC)
    aba_titulos = ["DEMO", "YPOEMAS", "EUREKA", "OFF-MÁQUINA", "BOOKS", "ABOUT"]
    tabs = st.tabs(aba_titulos)
    # Identifica aba ativa (Simulado para manter o cockpit fixo)
    # Nota: Em versões futuras, usaremos o retorno de st.tabs para mudar st.session_state.current_tab

    # --- 4. O PALCO (A LÓGICA DE ANOS) ---
    st.divider()
    
    # Cabeçalho do Expander (Status Dinâmico)
    status_header = (
        f"⚫ {st.session_state.lang} ( {st.session_state.book} ) "
        f"( {st.session_state.tema_idx + 1} / {len(temas_list)} )"
    )

    with st.expander(status_header, expanded=True):
        try:
            from lay_2_ypo import gera_poema
            tema_atual = temas_list[st.session_state.tema_idx % len(temas_list)]
            
            # Geração do Poema
            res = gera_poema(tema_atual, str(st.session_state.seed))
            curr_ypoema = "".join(res) if isinstance(res, list) else str(res)

            # Tradução se Lang != PT
            if st.session_state.lang != "Português":
                curr_ypoema = GoogleTranslator(source='pt', target=DICI_LANG[st.session_state.lang]).translate(curr_ypoema)

            # CONTAINER DE ALTURA FIXA (PALCO NOBRE)
            with st.container(height=550, border=False):
                st.markdown(f"<pre>{curr_ypoema}</pre>", unsafe_allow_html=True)

            # DISPARO DO TALK
            if st.session_state.talk:
                tts = gTTS(text=curr_ypoema, lang=DICI_LANG[st.session_state.lang])
                fp = BytesIO()
                tts.write_to_fp(fp)
                b64 = base64.b64encode(fp.getvalue()).decode()
                st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}"></audio>', unsafe_allow_html=True)

            # DISPARO DO ARTS (Simulado conforme sua lógica)
            if st.session_state.draw:
                st.image("https://via.placeholder.com/600x300?text=ARTS+ACTIVE", use_column_width=True)

        except Exception as e:
            st.error(f"Integridade da Machina: {e}")

if __name__ == "__main__":
    main()
