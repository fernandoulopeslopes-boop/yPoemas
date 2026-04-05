import streamlit as st
import os
import random
from gtts import gTTS
from deep_translator import GoogleTranslator

# --- 1. SETUP DO PALCO ---
st.set_page_config(page_title="Machina de Fazer Poesia", layout="wide", initial_sidebar_state="expanded")

# --- 2. O DNA ESTÉTICO (ZERO INTERFERÊNCIA) ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    
    /* A MANCHA GRÁFICA DO yPoema */
    .ypo_text {
        font-family: 'Courier New', Courier, monospace;
        font-size: 1.35rem;
        font-weight: 600;
        line-height: 1.4;
        color: #1A1A1A;
        padding: 40px;
        background-color: #FAFAFA;
        border: 1px solid #EEE;
        white-space: pre-wrap;
        margin-top: 10px;
    }

    /* BOTÕES EM LINHA: Respeito à varredura do olho */
    div.stButton > button {
        display: inline-block;
        width: auto !important;
        min-width: 45px;
        border-radius: 0px !important;
        border: 1px solid #000 !important;
        background-color: #FFF !important;
        color: #000 !important;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        text-transform: uppercase;
        margin-right: 2px;
        padding: 2px 8px;
    }
    div.stButton > button:hover {
        background-color: #000 !important;
        color: #FFF !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #F0F0F0;
        border-right: 2px solid #000;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #000 !important;
        color: #FFF !important;
    }
    
    /* Remove labels automáticas do Streamlit que poluem o visual */
    label { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ESTADOS ---
if 'lang' not in st.session_state: st.session_state.lang = 'pt'
if 'current_text' not in st.session_state: st.session_state.current_text = ""

# --- 4. SIDEBAR: COCKPIT PURA LINHA ---
with st.sidebar:
    # Apenas os botões de idioma, lado a lado, sem títulos/labels
    cols = st.columns([1,1,1,1,1,1])
    l_codes = [("PT", "pt"), ("EN", "en"), ("ES", "es"), ("FR", "fr"), ("IT", "it"), ("DE", "de")]
    for i, (lab, cod) in enumerate(l_codes):
        if cols[i].button(lab): st.session_state.lang = cod
    
    st.divider()
    
    # Toggles sem labels (O olho já sabe o que são pelos nomes Talk/Arts/Vídeo)
    t_talk = st.toggle("Talk", value=False)
    t_arts = st.toggle("Arts", value=True)
    t_vyde = st.toggle("Vídeo", value=False)

# --- 5. O PALCO ---
# Nomes das abas oriundos do seu sistema
paginas = ["Mini", "yPoemas", "Eureka", "Biblioteca", "Livro Vivo", "Ensaios", "Sobre"]
tabs = st.tabs([p.upper() for p in paginas])

for nome, tab in zip(paginas, tabs):
    slug = nome.lower().replace(" ", "_")
    with tab:
        col_main, col_aux = st.columns([2, 1])
        
        with col_main:
            # O botão de disparo usa apenas o nome da aba, sem prefixos "Executar"
            if st.button(nome.upper(), key=f"cmd_{slug}"):
                f_path = f"base/{slug}.txt"
                if os.path.exists(f_path):
                    with open(f_path, "r", encoding="utf-8") as f:
                        lines = f.read().splitlines()
                    
                    # O Ítimo no Eixo Z
                    raw_text = "\n".join(random.sample(lines, min(len(lines), 6)))
                    
                    # Tradução
                    if st.session_state.lang != 'pt':
                        raw_text = GoogleTranslator(source='pt', target=st.session_state.lang).translate(raw_text)
                    st.session_state.current_text = raw_text
                else:
                    st.session_state.current_text = "VÁCUO DETECTADO."

            if st.session_state.current_text:
                st.markdown(f'<div class="ypo_text">{st.session_state.current_text}</div>', unsafe_allow_html=True)
                
                if t_talk:
                    tts = gTTS(text=st.session_state.current_text, lang=st.session_state.lang)
                    tts.save("voice.mp3")
                    st.audio("voice.mp3")

        with col_aux:
            if t_arts:
                img = f"base/{slug}.jpg"
                if os.path.exists(img): st.image(img, use_column_width=True)
            if t_vyde:
                vid = f"base/video_{slug}.webm"
                if os.path.exists(vid): st.video(vid)import streamlit as st
import os
import random
from gtts import gTTS
from deep_translator import GoogleTranslator

# --- 1. SETUP DO PALCO ---
st.set_page_config(page_title="Machina de Fazer Poesia", layout="wide", initial_sidebar_state="expanded")

# --- 2. O DNA ESTÉTICO (ZERO INTERFERÊNCIA) ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    
    /* A MANCHA GRÁFICA DO yPoema */
    .ypo_text {
        font-family: 'Courier New', Courier, monospace;
        font-size: 1.35rem;
        font-weight: 600;
        line-height: 1.4;
        color: #1A1A1A;
        padding: 40px;
        background-color: #FAFAFA;
        border: 1px solid #EEE;
        white-space: pre-wrap;
        margin-top: 10px;
    }

    /* BOTÕES EM LINHA: Respeito à varredura do olho */
    div.stButton > button {
        display: inline-block;
        width: auto !important;
        min-width: 45px;
        border-radius: 0px !important;
        border: 1px solid #000 !important;
        background-color: #FFF !important;
        color: #000 !important;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        text-transform: uppercase;
        margin-right: 2px;
        padding: 2px 8px;
    }
    div.stButton > button:hover {
        background-color: #000 !important;
        color: #FFF !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #F0F0F0;
        border-right: 2px solid #000;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #000 !important;
        color: #FFF !important;
    }
    
    /* Remove labels automáticas do Streamlit que poluem o visual */
    label { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ESTADOS ---
if 'lang' not in st.session_state: st.session_state.lang = 'pt'
if 'current_text' not in st.session_state: st.session_state.current_text = ""

# --- 4. SIDEBAR: COCKPIT PURA LINHA ---
with st.sidebar:
    # Apenas os botões de idioma, lado a lado, sem títulos/labels
    cols = st.columns([1,1,1,1,1,1])
    l_codes = [("PT", "pt"), ("EN", "en"), ("ES", "es"), ("FR", "fr"), ("IT", "it"), ("DE", "de")]
    for i, (lab, cod) in enumerate(l_codes):
        if cols[i].button(lab): st.session_state.lang = cod
    
    st.divider()
    
    # Toggles sem labels (O olho já sabe o que são pelos nomes Talk/Arts/Vídeo)
    t_talk = st.toggle("Talk", value=False)
    t_arts = st.toggle("Arts", value=True)
    t_vyde = st.toggle("Vídeo", value=False)

# --- 5. O PALCO ---
# Nomes das abas oriundos do seu sistema
paginas = ["Mini", "yPoemas", "Eureka", "Biblioteca", "Livro Vivo", "Ensaios", "Sobre"]
tabs = st.tabs([p.upper() for p in paginas])

for nome, tab in zip(paginas, tabs):
    slug = nome.lower().replace(" ", "_")
    with tab:
        col_main, col_aux = st.columns([2, 1])
        
        with col_main:
            # O botão de disparo usa apenas o nome da aba, sem prefixos "Executar"
            if st.button(nome.upper(), key=f"cmd_{slug}"):
                f_path = f"base/{slug}.txt"
                if os.path.exists(f_path):
                    with open(f_path, "r", encoding="utf-8") as f:
                        lines = f.read().splitlines()
                    
                    # O Ítimo no Eixo Z
                    raw_text = "\n".join(random.sample(lines, min(len(lines), 6)))
                    
                    # Tradução
                    if st.session_state.lang != 'pt':
                        raw_text = GoogleTranslator(source='pt', target=st.session_state.lang).translate(raw_text)
                    st.session_state.current_text = raw_text
                else:
                    st.session_state.current_text = "VÁCUO DETECTADO."

            if st.session_state.current_text:
                st.markdown(f'<div class="ypo_text">{st.session_state.current_text}</div>', unsafe_allow_html=True)
                
                if t_talk:
                    tts = gTTS(text=st.session_state.current_text, lang=st.session_state.lang)
                    tts.save("voice.mp3")
                    st.audio("voice.mp3")

        with col_aux:
            if t_arts:
                img = f"base/{slug}.jpg"
                if os.path.exists(img): st.image(img, use_column_width=True)
            if t_vyde:
                vid = f"base/video_{slug}.webm"
                if os.path.exists(vid): st.video(vid)
