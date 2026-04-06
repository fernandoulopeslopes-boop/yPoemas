import streamlit as st
import random
import os
import base64
from pathlib import Path
from deep_translator import GoogleTranslator
from gtts import gTTS

# --- [ PROTOCOLO DE SEGURANÇA E DISPARO ] ---
# Condição 1: Alteração de CSS e Lógica de Busca (OK)
# Condição 2: Resposta ao gatilho de extensão de conversa (ATIVO)
# Versão: 1.6.1 - Estável para Teste de Aceitação

st.set_page_config(
    page_title="Machina yPoemas",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS: ESTABILIZAÇÃO DO PALCO & CURA DO ENCAVALAMENTO ---
st.markdown("""
    <style>
    /* Ajuste de Margens para evitar sobreposição da Sidebar */
    .main .block-container {
        padding-top: 2rem;
        padding-right: 5rem;
        padding-left: 5rem;
        max-width: 1000px;
    }
    /* Estilização da Sidebar para clareza visual */
    section[data-testid="stSidebar"] {
        width: 350px !important;
        background-color: #f0f2f6;
    }
    /* Container da Poesia (O Palco) */
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

# --- FUNÇÃO DE BUSCA NORMALIZADA (BLINDAGEM LINUX/DEPLOY) ---
def load_off_content(file_target):
    """
    Busca arquivos na pasta off_machina ignorando case e acentos.
    Garante que o servidor Linux encontre os arquivos .Pip e .md.
    """
    path_off = Path(__file__).parent / "off_machina"
    if not path_off.exists():
        return "Erro: Pasta 'off_machina' não encontrada no servidor."

    def normalize(text):
        # Normaliza strings para comparação cega (ex: Público -> publico)
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
    except Exception as e:
        return None

# --- SIDEBAR: NAVEGAÇÃO DO LABIRINTO ---
with st.sidebar:
    st.title("Machina yPoemas")
    st.markdown("---")
    menu_choice = st.radio(
        "Navegação:",
        ["O Palco (Home)", "O Manual (About)", "Traduttore & Vox"]
    )
    st.markdown("---")
    st.caption("v1.6.1 - Protocolo de Disparo Ativo")
    st.info("Status: Bolo Pronto. Aguardando a Cereja.")

# --- PÁGINA 1: O PALCO (HOME) ---
if menu_choice == "O Palco (Home)":
    st.title("A Machina Poética")
    st.write("---")
    
    # Gatilho de sorteio (Placeholder para integração com os 48 temas)
    if st.button("Girar a Machina (Al'at'zar)"):
        st.session_state.current_poem = "O Si grave ressoa...\nNo baú de jacarandá\nA violinista espera."
    
    if "current_poem" in st.session_state:
        st.markdown(f'<div class="poesia-box">{st.session_state.current_poem}</div>', unsafe_allow_html=True)
    else:
        st.info("Toque o 'Si' grave para iniciar o sorteio e revelar a poesia.")

# --- PÁGINA 2: O MANUAL (ABOUT & MANDALA) ---
elif menu_choice == "O Manual (About)":
    st.title("Sobre a Machina")
    
    aba1, aba2, aba3 = st.tabs(["Inventário de Achados", "Mandala Linguafiada", "Acessar o Baú"])
    
    with aba1:
        st.markdown("""
        ### **Linguafiada: O Inventário de Achados**
        * **O Baú de Jacarandá:** Repositório físico e metafísico do que é raro.
        * **A Nota Si:** A tensão necessária; a sensível que não resolve, mas atrai.
        * **O Vinho e o Veludo:** A preparação do espírito para o encontro com a arte.
        * **A Violinista:** O leitor ideal, atraído pelo som contínuo.
        """)

    with aba2:
        st.subheader("Arquitetura do Labirinto")
        st.table([
            {"Círculo": "NÚCLEO", "Elemento": "O Drope (17s)", "Função": "Átomo da poesia."},
            {"Círculo": "INTERMEDIÁRIO", "Elemento": "Temas (48)", "Função": "Paredes do labirinto."},
            {"Círculo": "EXTERIOR", "Elemento": "Off-Machina (.Pip)", "Função": "Onde o Si grave reside."},
            {"Círculo": "AUREOLA", "Elemento": "Al'at'zar (Lâmpada)", "Função": "O acesso ao desconhecido."}
        ])

    with aba3:
        st.write("Acesso direto aos arquivos .Pip e .md guardados no baú.")
        file_query = st.text_input("O que busca?", placeholder="Ex: violino.Pip")
        if st.button("Abrir"):
            resultado = load_off_content(file_query)
            st.code(resultado, language="text")

# --- PÁGINA 3: TRADUTTORE & VOX ---
elif menu_choice == "Traduttore & Vox":
    st.title("Tradução e Voz")
    
    if "current_poem" in st.session_state:
        texto_base = st.session_state.current_poem
        st.markdown(f"**Texto Original:**\n{texto_base}")
        
        target_lang = st.selectbox("Escolha o Idioma Destino:", ["en", "es", "it", "fr", "de"])
        
        if st.button("Processar Tradução e Voz"):
            with st.spinner("Traduzindo..."):
                translation = GoogleTranslator(source='pt', target=target_lang).translate(texto_base)
                st.success(f"**Tradução:**\n{translation}")
                
                audio_b64 = gerar_audio(translation, lang=target_lang)
                if audio_b64:
                    audio_html = f'<audio controls src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3"></audio>'
                    st.markdown(audio_html, unsafe_allow_html=True)
    else:
        st.warning("É necessário gerar uma poesia no 'Palco' antes de traduzir.")

# --- FIM DO ARQUIVO ---
