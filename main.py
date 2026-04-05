import streamlit as st
import os
import random
from gtts import gTTS
from deep_translator import GoogleTranslator

# --- 1. SETUP DO PALCO (SEM MARGENS DESNECESSÁRIAS) ---
st.set_page_config(page_title="Machina de Fazer Poesia", layout="wide", initial_sidebar_state="expanded")

# --- 2. A ALMA VISUAL (CSS INJETADO PARA MATAR O PADRÃO) ---
st.markdown("""
    <style>
    /* Fundo e Fonte Base */
    .stApp { background-color: #FFFFFF; }
    
    /* A Mancha Gráfica do yPoema */
    .yPoema {
        font-family: 'Courier New', Courier, monospace;
        font-size: 1.4rem;
        font-weight: 500;
        line-height: 1.6;
        color: #000000;
        padding: 40px;
        border-left: 3px solid #EEE;
        margin-top: 20px;
        white-space: pre-wrap;
    }

    /* Botões: O Padrão de Comando */
    .stButton>button {
        width: 100%;
        border-radius: 0px;
        border: 1px solid #333;
        background-color: #F8F8F8;
        color: #000;
        font-weight: bold;
        transition: 0.3s;
        height: 3em;
    }
    .stButton>button:hover {
        background-color: #000;
        color: #FFF;
    }

    /* Sidebar e Abas */
    [data-testid="stSidebar"] { background-color: #F0F2F6; border-right: 1px solid #CCC; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #F0F0F0;
        border: 1px solid #CCC;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] { background-color: #000 !important; color: #FFF !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGICA DE ESTADO (PERSISTÊNCIA) ---
if 'idioma' not in st.session_state: st.session_state.idioma = 'pt'
if 'poema_atual' not in st.session_state: st.session_state.poema_atual = ""

# --- 4. SIDEBAR: HIERARQUIA DO PROTOCOLO ---
with st.sidebar:
    st.markdown("### 🌐 SELEÇÃO DE IDIOMA")
    # Grade de Botões para Idiomas (Sem preguiça de Dropdown)
    c1, c2 = st.columns(2)
    langs = {"PORTUGUÊS": "pt", "ENGLISH": "en", "ESPAÑOL": "es", 
             "FRANÇAIS": "fr", "ITALIANO": "it", "DEUTSCH": "de"}
    
    for i, (label, code) in enumerate(langs.items()):
        target_col = c1 if i % 2 == 0 else c2
        if target_col.button(label):
            st.session_state.idioma = code

    st.markdown(f"**Ativo:** `{st.session_state.idioma.upper()}`")
    st.divider()

    st.markdown("### 🕹️ COMMANDS")
    v_talk = st.toggle("Talk (Voz)", value=False)
    v_arts = st.toggle("Arts (Imagem)", value=True)
    v_video = st.toggle("Vídeo (Instrução)", value=False)
    
    st.divider()
    st.caption("O.V.N.I. Command | Protocolo 1983-2026")

# --- 5. O PALCO: TODAS AS PÁGINAS DO ESQUELETO ---
abas_nomes = ["Mini", "yPoemas", "Eureka", "Biblioteca", "Livro Vivo", "Ensaios", "Sobre"]
tabs = st.tabs([a.upper() for a in abas_nomes])

for nome, tab in zip(abas_nomes, tabs):
    tag = nome.lower().replace(" ", "_")
    with tab:
        col_main, col_aux = st.columns([2, 1])
        
        with col_main:
            if st.button(f"DISPARAR FRANCO-ATIRADOR: {nome.upper()}", key=f"btn_{tag}"):
                # Busca na base
                path = f"base/{tag}.txt"
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f:
                        linhas = f.read().splitlines()
                    
                    # O ÍTIMO (Simulação fiel à estrutura de 6 linhas)
                    selecao = random.sample(linhas, min(len(linhas), 6))
                    texto = "\n".join(selecao)
                    
                    # Tradução Seletiva
                    if st.session_state.idioma != 'pt':
                        texto = GoogleTranslator(source='pt', target=st.session_state.idioma).translate(texto)
                    
                    st.session_state.poema_atual = texto
                else:
                    st.session_state.poema_atual = "Vácuo detectado."

            # Exibição da Mancha Gráfica
            if st.session_state.poema_atual:
                st.markdown(f'<div class="yPoema">{st.session_state.poema_atual}</div>', unsafe_allow_html=True)
                
                if v_talk:
                    tts = gTTS(text=st.session_state.poema_atual, lang=st.session_state.idioma)
                    tts.save("temp_voice.mp3")
                    st.audio("temp_voice.mp3")

        with col_aux:
            if v_arts:
                # Tenta carregar imagem do tema
                img_p = f"base/{tag}.jpg"
                if os.path.exists(img_p): st.image(img_p, use_column_width=True)
            
            if v_video:
                # Tenta carregar vídeo de instrução
                vid_p = f"base/video_{tag}.webm"
                if os.path.exists(vid_p): st.video(vid_p)
