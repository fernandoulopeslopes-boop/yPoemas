import streamlit as st
import os
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(layout="wide", page_title="a máquina de fazer poesia")

# --- DICIONÁRIOS OFICIAIS (FONTE: listas_oficiais.doc) ---
IDIOMAS = {
    'português': 'pt', 'espanhol': 'es', 'italiano': 'it', 'francês': 'fr', 
    'inglês': 'en', 'esperanto': 'eo', 'latin': 'la', 'basco': 'eu', 
    'catalão': 'ca', 'córsico': 'co', 'galego': 'gl', 'galês': 'cy', 
    'polonês': 'pl', 'holandês': 'nl', 'irlandês': 'ga', 'norueguês': 'no', 
    'finlandês': 'fi', 'dinamarquês': 'da', 'romeno': 'ro', 'russo': 'ru', 'sueco': 'sv'
}

TEMAS_ATIVOS = {
    'ais': 'ensaio', 'amaré': 'poesia', 'anjos': 'author', 'aolero': 'ensaio',
    'aquário=f': 'zodíaco', 'aquário=m': 'zodíaco', 'aries=f': 'zodíaco', 'aries=m': 'zodíaco',
    'cancer=f': 'zodíaco', 'cancer=m': 'zodíaco', 'capricor=f': 'zodíaco', 'capricor=m': 'zodíaco',
    'escorpia=f': 'zodíaco', 'escorpia=m': 'zodíaco', 'gemeos=f': 'zodíaco', 'gemeos=m': 'zodíaco',
    'leao=f': 'zodíaco', 'leao=m': 'zodíaco', 'libra=f': 'zodíaco', 'libra=m': 'zodíaco',
    'peixes=f': 'zodíaco', 'peixes=m': 'zodíaco', 'sagitari=f': 'zodíaco', 'sagitari=m': 'zodíaco',
    'touro=f': 'zodíaco', 'touro=m': 'zodíaco', 'virgem=f': 'zodíaco', 'virgem=m': 'zodíaco'
}

# --- MOTOR DE GOVERNANÇA DIRECIONADA ---
def inject_governance():
    font = st.session_state.get('main_font', 'Source Serif 4')
    font_url = font.replace(" ", "+")
    
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family={font_url}:wght@300;400;700&display=swap');
        
        /* Aplicação Seletiva: Apenas textos de interface e conteúdo */
        [data-testid="stMarkdownContainer"] p, 
        [data-testid="stMarkdownContainer"] h1, 
        [data-testid="stSidebar"] span,
        .stSelectbox label, 
        .stButton button,
        div[data-baseweb="select"] {{
            font-family: '{font}', serif !important;
            text-transform: lowercase !important;
        }}
        
        /* Proteção de elementos técnicos */
        code, pre {{ text-transform: none !important; }}

        [data-testid="stSidebar"] {{ background-color: #f8f9fa; }}
        .footer-logo {{ position: fixed; bottom: 20px; width: 260px; text-align: center; }}
        </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO DE ARTES ---
def load_arts(seed_tema):
    path = "./images/machina/"
    if seed_tema.lower() in TEMAS_ATIVOS:
        categoria = TEMAS_ATIVOS[seed_tema.lower()]
        path = f"./images/{categoria}/"
    
    try:
        arts_list = [f for f in os.listdir(path) if f.endswith(".jpg")]
        if arts_list:
            return os.path.join(path, random.choice(arts_list))
    except:
        pass
    return None

# --- INICIALIZAÇÃO ---
if 'main_font' not in st.session_state: st.session_state.main_font = 'Source Serif 4'
if 'show_panel' not in st.session_state: st.session_state.show_panel = False

inject_governance()

# --- SIDEBAR ---
with st.sidebar:
    st.selectbox("idioma", options=list(IDIOMAS.keys()))
    st.selectbox("tema", options=list(TEMAS_ATIVOS.keys()), key="seed_tema")

    st.write("---")
    
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("arte"): st.rerun()
    with c2:
        if st.button("⚙"): st.session_state.show_panel = not st.session_state.show_panel
    with c3:
        st.button("áudio")

    if st.session_state.show_panel:
        st.write("---")
        st.session_state.main_font = st.radio(
            "tipografia", 
            ["Source Serif 4", "OpenDyslexic", "Playfair Display", "Inter", "JetBrains Mono", "Nunito"]
        )
        st.info("fontes disponíveis na machina...")

    # Identidade no Rodapé usando o parâmetro 'fatos' como solicitado
    logo = load_arts(st.session_state.get('seed_tema', 'fatos'))
    if logo:
        st.markdown('<div class="footer-logo">', unsafe_allow_html=True)
        st.image(logo, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- CONTEÚDO ---
st.title("palco principal")
