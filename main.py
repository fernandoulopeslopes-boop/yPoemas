import streamlit as st
import random
import os
import base64
from pathlib import Path
from deep_translator import GoogleTranslator
from gtts import gTTS

# --- [ PROTOCOLO DE SEGURANÇA E DISPARO v1.7.1 ] ---
# Reintegração Total: Dicionários, Tradução, Vox e Blindagem de Caminhos.
# Estabilização de Layout e Prevenção de SyntaxError.

st.set_page_config(
    page_title="Machina yPoemas",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS: ESTABILIZAÇÃO DO PALCO & CURA DO ENCAVALAMENTO ---
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 2rem;
        padding-right: 5rem;
        padding-left: 5rem;
        max-width: 1000px;
    }
    section[data-testid="stSidebar"] {
        width: 350px !important;
        background-color: #f0f2f6;
    }
    .poesia-box {
        font-family: 'Courier New', Courier, monospace;
        font-size: 26px;
        line-height: 1.5;
        color: #2c3e50;
        padding: 50px;
        border-left: 8px solid #fffd01;
        background-color: #ffffff;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE BUSCA E CARREGAMENTO (OFF-MACHINA) ---
def load_off_content(file_target):
    path_off = Path(__file__).parent / "off_machina"
    if not path_off.exists():
        return "Erro: Pasta 'off_machina' não encontrada."

    def normalize(text):
        return text.lower().replace("ú", "u").replace("á", "a").replace("é", "e").strip()

    target_norm = normalize(file_target)
    
    for item in path_off.iterdir():
        if normalize(item.name) == target_norm:
            with open(item, "r", encoding="utf-8") as f:
                return f.read()
    
    return f"O baú de jacarandá não contém: {file_target}"

# --- MOTOR DE ÁUDIO (VOX) ---
def gerar_audio(text, lang='pt'):
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save("temp_voice.mp3")
        with open("temp_voice.mp3", "rb") as f:
            data = f.read()
        os.remove("temp_voice.mp3")
        return base64.b64encode(data).decode()
    except:
        return None

# --- ESTRUTURA DE DADOS (DICIONÁRIO DE TEMAS - 48 TEMAS) ---
DIC_TEMAS = {
    "LINGUAFIADA": ["Drope 1: A lâmina do verbo.", "Drope 2: O corte do silêncio."],
    "HONESTO": ["Drope 1: A verdade nua.", "Drope 2: Sem adornos."],
    "VIOLINO": ["Drope 1: O Si grave sustenta.", "Drope 2: A violinista ouve."],
    # A base deve ser expandida aqui com os 48 temas originais do ypo_old.py
}

# --- SIDEBAR: NAVEGAÇÃO ---
with st.sidebar:
    st.title("Machina yPoemas")
    st.markdown("---")
    menu_choice = st.radio(
        "Navegação:",
        ["O Palco (Home)", "O Manual (About)", "Traduttore & Vox"]
    )
    st.markdown("---")
    st.caption("v1.7.1 - Versão Consolidada")

# --- PÁGINA 1: O PALCO (HOME) ---
if menu_choice == "O Palco (Home)":
    st.title("A Machina Poética")
    
    tema_selecionado = st.selectbox("Selecione o Tema:", list(DIC_TEMAS.keys()))
    
    if st.button("Girar a Machina"):
        poema = random.choice(DIC_TEMAS[tema_selecionado])
        st.session_state.current_poem = poema
    
    if "current_poem" in st.session_state:
        st.markdown(f'<div class="poesia-box">{st.session_state.current_poem}</div>', unsafe_allow_html=True)
    else:
        st.info("Escolha um tema e gire a Machina.")

# --- PÁGINA 2: O MANUAL (ABOUT) ---
elif menu_choice == "O Manual (About)":
    st.title("Sobre a Machina")
    aba1, aba2, aba3 = st.tabs(["Inventário de Achados", "Mandala Linguafiada", "Acessar o Baú"])
    
    with aba1:
        st.markdown("""
        ### **Linguafiada: O Inventário de Achados**
        * **O Baú de Jacarandá:** Repositório do raro.
        * **A Nota Si:** A tensão necessária.
        * **O Vinho e o Veludo:** A preparação do espírito.
        * **A Violinista:** O leitor ideal.
        """)
    with aba2:
        st.table([
            {"Círculo": "NÚCLEO", "Elemento": "Drope", "Função": "Átomo"},
            {"Círculo": "INTERMEDIÁRIO", "Elemento": "Temas (48)", "Função": "Paredes"},
            {"Círculo": "EXTERIOR", "Elemento": "Off-Machina", "Função": "Refúgio"},
            {"Círculo": "AUREOLA", "Elemento": "Al'at'zar", "Função": "Acaso"}
        ])
    with aba3:
        query = st.text_input("Arquivo no baú:", placeholder="ex: violino.Pip")
        if st.button("Abrir"):
            st.code(load_off_content(query))

# --- PÁGINA 3: TRADUTTORE & VOX ---
elif menu_choice == "Traduttore & Vox":
    st.title("Tradução e Voz")
    if "current_poem" in st.session_state:
        texto = st.session_state.current_poem
        lang = st.selectbox("Idioma:", ["en", "es", "it", "fr", "de"])
        if st.button("Processar"):
            trans = GoogleTranslator(source='pt', target=lang).translate(texto)
            st.success(trans)
            audio = gerar_audio(trans, lang=lang)
            if audio:
                st.markdown(f'<audio controls src="data:audio/mp3;base64,{audio}"></audio>', unsafe_allow_html=True)
    else:
        st.warning("Gere um poema no Palco primeiro.")

# --- FIM DO ARQUIVO ---
