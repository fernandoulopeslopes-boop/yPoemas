import os
import random
import json
import streamlit as st
from deep_translator import GoogleTranslator

# ==============================================================================
# 1. CONFIGURAÇÕES & ESTADO GLOBAL
# ==============================================================================
st.set_page_config(layout="wide")

if "arts" not in st.session_state:
    st.session_state.arts = [] # Histórico de 36 imagens [cite: 12]

# Listas Oficiais [cite: 1, 2, 3, 4, 5, 6, 7, 8, 9]
IDIOMAS = {
    'Português': 'pt', 'Espanhol': 'es', 'Italiano': 'it', 'Francês': 'fr',
    'Inglês': 'en', 'Esperanto': 'eo', 'Latin': 'la', 'Basco': 'eu',
    'Catalão': 'ca', 'Córsico': 'co', 'Galego': 'gl', 'Galês': 'cy',
    'Polonês': 'pl', 'Holandês': 'nl', 'Irlandês': 'ga', 'Norueguês': 'no',
    'Finlandês': 'fi', 'Dinamarquês': 'da', 'Romeno': 'ro', 'Russo': 'ru', 'Sueco': 'sv'
}

TEMAS_ATIVOS = {
    'Ais': 'ensaio', 'Amaré': 'poesia', 'Anjos': 'author', 'Aolero': 'ensaio',
    'Arerir': 'ensaio', 'Astros': 'ensaio', 'Atido': 'poesia', 'Augusto': 'author',
    'Avevida': 'poesia', 'Babel': 'ensaio', 'Batismo': 'metalinguagem', 'Beaba': 'metalinguagem',
    'Becos': 'poesia', 'Blablabla': 'metalinguagem', 'Bolero': 'poesia', 'Brado': 'joco',
    'Bula': 'joco', 'Cadência': 'metalinguagem', 'Cartaz': 'joco', 'Circular': 'poesia',
    'Ciuminho': 'poesia', 'Clandestino': 'author', 'Clarice': 'poesia', 'Conto': 'poesia',
    'Cordel': 'metalinguagem', 'Críticas': 'joco', 'Critico': 'author', 'Cromossomo': 'joco',
    'Cuores': 'poesia', 'Destinos': 'poesia', 'Distintos': 'poesia', 'Dolores': 'poesia',
    'Duralex': 'joco', 'Elogio': 'poesia', 'Enfrente': 'ensaio', 'Epitafiando': 'poesia',
    'Escriba': 'author', 'Essa': 'metalinguagem', 'Essas': 'ensaio', 'Esses': 'ensaio',
    'Estudo': 'joco', 'Fatos': 'poesia', 'Feiras': 'metalinguagem', 'Festim': 'poesia',
    'Finalmentes': 'joco', 'Frases': 'joco', 'Fugaz': 'poesia', 'Gula': 'joco',
    'HaiKai': 'poesia', 'i-Mundo': 'poesia', 'Impar': 'ensaio', 'Indolor': 'poesia',
    'Inhos': 'poesia', 'Insano': 'joco', 'Joker': 'joco', 'Lato': 'author',
    'Leituras': 'metalinguagem', 'Liberta': 'poesia', 'Loremipsum': 'ensaio', 'Machbeth': 'poesia',
    'Machbrait': 'author', 'Manifesto': 'machina', 'Manusgrite': 'metalinguagem', 'Manusgrito': 'metalinguagem',
    'Meteoro': 'joco', 'Minuto': 'joco', 'Mirante': 'poesia', 'Nonono': 'ensaio',
    'Nós': 'poesia', 'Oca': 'poesia', 'Ocio': 'joco', 'Oco': 'poesia',
    'Oficia': 'joco', 'Oficio': 'author', 'Ogiva': 'poesia', 'Olhares': 'poesia',
    'Palyndro': 'ensaio', 'Papilio': 'poesia', 'Paroles': 'metalinguagem', 'Passagens': 'poesia',
    'Pedidos': 'poesia', 'Perfil': 'beauty', 'Pessoa': 'author', 'Portal': 'poesia',
    'Posfácio': 'poesia', 'Preciso': 'poesia', 'Prefácil': 'poesia', 'Psiu': 'poesia',
    'Reger': 'poesia', 'Reinos': 'joco', 'Remedeio': 'joco', 'Restos': 'joco',
    'Rever': 'poesia', 'Rito': 'joco', 'Salute': 'joco', 'Saudades': 'poesia',
    'Seguro': 'joco', 'Sentença': 'joco', 'Ser': 'poesia', 'Silente': 'poesia',
    'Sinais': 'poesia', 'Sinas': 'ensaio', 'Sn6=ball': 'ensaio', 'Sn8=ball': 'ensaio',
    'SnowBall': 'ensaio', 'Sonoro': 'poesia', 'Sopros': 'poesia', 'Sos': 'joco',
    'Tempo': 'poesia', 'Tiro': 'metalinguagem', 'Tolero': 'poesia', 'Usinas': 'poesia',
    'Veio': 'poesia', 'Victor': 'author', 'Vozes': 'joco', 'Zelo': 'poesia',
    'Zodiacaos': 'zodíaco', 'Zoia': 'poesia', 'Aquarius=f': 'zodíaco', 'Aquarius=m': 'zodíaco',
    'Aries=f': 'zodíaco', 'Aries=m': 'zodíaco', 'Cancer=f': 'zodíaco', 'Cancer=m': 'zodíaco',
    'Caprico=f': 'zodíaco', 'Caprico=m': 'zodíaco', 'Escorpio=f': 'zodíaco', 'Escorpio=m': 'zodíaco',
    'Gemeos=f': 'zodíaco', 'Gemeos=m': 'zodíaco', 'Leao=f': 'zodíaco', 'Leao=m': 'zodíaco',
    'Libra=f': 'zodíaco', 'Libra=m': 'zodíaco', 'Peixes=f': 'zodíaco', 'Peixes=m': 'zodíaco',
    'Sagitari=f': 'zodíaco', 'Sagitari=m': 'zodíaco', 'Touro=f': 'zodíaco', 'Touro=m': 'zodíaco',
    'Virgem=f': 'zodíaco', 'Virgem=m': 'zodíaco'
}

# ==============================================================================
# 2. MOTOR DE ARTES (Fiel à sua lógica [cite: 10, 11, 12])
# ==============================================================================
def load_arts(seed_tema):
    path = "./images/machina/"
    # Identifica categoria baseada no TEMAS_ATIVOS [cite: 10]
    if seed_tema in TEMAS_ATIVOS:
        path = f"./images/{TEMAS_ATIVOS[seed_tema]}/"
    
    if not os.path.exists(path):
        return None

    arts_list = [f for f in os.listdir(path) if f.endswith(".jpg")]
    if not arts_list:
        return None

    # Sorteio com proteção contra repetição [cite: 11, 12]
    image = random.choice(arts_list)
    while image in st.session_state.arts and len(st.session_state.arts) < len(arts_list):
        image = random.choice(arts_list)

    st.session_state.arts.append(image)
    if len(st.session_state.arts) > 36: # Limite seguro [cite: 12]
        del st.session_state.arts[0]

    return os.path.join(path, image)

# ==============================================================================
# 3. INTERFACE PRINCIPAL
# ==============================================================================
# Botões de Navegação Acima do Palco
cols_nav = st.columns(5)
with cols_nav[0]: st.button("yPoemas", use_container_width=True)
with cols_nav[1]: st.button("Sobre", use_container_width=True)
with cols_nav[2]: st.button("Manual", use_container_width=True)
# ... demais botões conforme funcional no ypo_seguro.py

st.divider()

# Sidebar Original (Fiel ao Padrão )
with st.sidebar:
    # 1. Seleção de Idioma
    idioma_escolhido = st.selectbox("Idiomas:", list(IDIOMAS.keys()))
    
    # 2. Alinhamento Horizontal Arte/Áudio
    col_a, col_b = st.columns(2)
    with col_a:
        btn_arte = st.button("arte", use_container_width=True)
    with col_b:
        btn_audio = st.button("audio", use_container_width=True)

    st.divider()

    # 3. Informações da Página (Rigor de Case )
    nome_pagina = "yPoemas" # Exemplo dinâmico
    info_path = f"md_files/INFO_{nome_pagina}.md" # Nome da página em foco 
    if os.path.exists(info_path):
        with open(info_path, "r", encoding="utf-8") as f:
            st.markdown(f.read())

    # 4. Exibição da Arte sorteada
    if btn_arte:
        # Exemplo de semente de tema, integraria com o seletor da página
        current_art = load_arts("Amaré") 
        if current_art:
            st.image(current_art, use_container_width=True)

    # 5. Redes Sociais no final da Sidebar
    st.markdown("<br>"*5, unsafe_allow_html=True)
    st.markdown("""
        <div style='display: flex; justify-content: space-between;'>
            <img src='app/static/btn_face.jpg' width='25'>
            <img src='app/static/btn_insta.jpg' width='25'>
            <img src='app/static/btn_zap.jpg' width='25'>
            <img src='app/static/btn_mail.jpg' width='25'>
        </div>
    """, unsafe_allow_html=True)
