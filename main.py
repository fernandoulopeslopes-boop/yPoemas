import streamlit as st

# --- 1. LISTA DE IDIOMAS OBRIGATÓRIA (PCP) ---
IDIOMAS_MACHINA = {
    "Português": "pt", "Espanhol": "es", "Italiano": "it", "Francês": "fr",
    "Inglês": "en", "Catalão": "ca", "Córsico": "co", "Galego": "gl",
    "Basco": "eu", "Esperanto": "eo", "Latin": "la", "Galês": "cy",
    "Sueco": "sv", "Polonês": "pl", "Holandês": "nl", "Norueguês": "no",
    "Finlandês": "fi", "Dinamarquês": "da", "Irlandês": "ga", "Romeno": "ro", "Russo": "ru"
}

def configurar_estetica():
    st.set_page_config(layout="wide", initial_sidebar_state="expanded")
    st.markdown("""
        <style>
        [data-testid="stSidebarNav"] {padding-top: 0rem;}
        /* Palco sem bordas inúteis - 100% de aproveitamento */
        .main .block-container { max-width: 100%; padding-top: 1rem; padding-left: 1rem; padding-right: 1rem; }
        /* Botões do Navegador Central */
        .stButton > button { width: 100%; border-radius: 5px; font-weight: bold; height: 3rem; }
        /* Alinhamento das listas laterais */
        div[data-testid="stSelectbox"] { margin-top: -10px; }
        /* LINHA FINA: Encostada nas laterais do palco */
        .separador-palco {
            width: 100%; 
            margin: 10px 0px 20px 0px; 
            border: 0;
            border-top: 1px solid #ccc;
        }
        </style>
        """, unsafe_allow_html=True)

def carregar_sidebar():
    with st.sidebar:
        st.write("---")
        idioma_exibido = st.selectbox("idioma", list(IDIOMAS_MACHINA.keys()))
        sigla_traducao = IDIOMAS_MACHINA[idioma_exibido]
        st.write("---")
        col_v1, col_v2 = st.columns(2)
        with col_v1: st.button("Arts")
        with col_v2: st.button("Voice")
    return sigla_traducao

def main():
    configurar_estetica()
    sigla = carregar_sidebar()

    # --- 2. BASE DE DADOS (ROLS) ---
    dicionario_dados = {
        "livro vivo": ["Prefácil", "Fatos", "Manifesto", "Manusgrite", "Beaba", "Paroles", "Essa", "Tiro", "Aolero", "Atido", "Lato", "Avevida", "Joker", "Feiras", "Cartaz", "Conto", "Festim", "I-Mundo", "Sos", "Meteoro", "Brado", "Inhos", "Astros", "Cromossomo", "Clandestino", "Pessoa", "Minuto", "Reger", "Preciso", "Pedidos", "Seguro", "Fugaz", "Nós", "Enfrente", "Leituras", "Rever", "Ocio", "Essas", "Mirante", "Indolor", "Elogio", "Distintos", "Gula", "Dolores", "Clarice", "Cuores", "Zoia", "Amaré", "Ciuminho", "Saudades", "Sentença", "Finalmentes", "Ser", "Rito", "Sonoro", "Anjos", "Epitafiando", "Tempo", "Usinas", "Veio", "Sopros", "Silente", "Oficio", "Posfácio"],
        "poemas": ["Amaré", "Atido", "Becos", "Ciuminho", "Clandestino", "Clarice", "Conto", "Cuores", "Elogio", "Festim", "Indolor", "Lato", "Machbeth", "Machbrait", "Mirante", "Oca", "Oco", "Ogiva", "Olhares", "Papilio", "Psiu", "Reger", "Rever", "Saudades", "Ser", "Silente", "Sinais", "Sonoro", "Sopros", "Tempo", "Usinas", "Veio", "Victor", "Zelo", "Zoia"],
        "variações": ["Destinos", "Distintos", "Dolores", "Indolor", "Essas", "Esses", "Sinais", "Sinas", "Fugaz", "Haikai", "Tempo", "Olhares", "Mirante", "Ogiva", "Zoia", "Manusgrito", "Manusgrite", "Aolero", "Bolero", "Tolero", "Ciuminho", "Psiu", "Zelo", "Bula", "Salute", "Sn8=ball", "Sn6=ball", "Snowball", "Blablabla", "Nonono", "Paroles", "Epitafiando", "Portal"],
        "ensaios": ["Ais", "Astros", "Arerir", "Babel", "Demo", "Essas", "Esses", "Loremipsum", "Palyndro", "Sinais", "Ss1", "Ss2", "Sn6=ball", "Sn8=ball", "SnowBall", "Nós"],
        "metalinguagem": ["Babel", "Batismo", "Beaba", "Blablabla", "Cadência", "Cartaz", "Cordel", "Essa", "Feiras", "Leituras", "Manusgrite", "Manusgrito", "Nonono", "Paroles", "Prefácil", "Snowball", "Tiro"],
        "sociais": ["Becos", "Brado", "Cromossomo", "Duralex", "Feiras", "i-Mundo", "Impar", "Inhos", "Insano", "Joker", "Nós", "Perfil", "Preciso", "Seguro"],
        "jocosos": ["Brado", "Cartaz", "Cromossomo", "Destinos", "Distintos", "Estudo", "Frases", "Gula", "Joker", "Meteoro", "Ocio", "Oficio", "Reinos", "Remedeio", "Rito", "Sos", "Perfil", "Seguro", "Zodiacaos"],
        "outros autores": ["Anjos", "Augusto", "Clandestino", "Clarice", "Elogio", "Escriba", "Finalmentes", "HayKay", "Jealousy", "MachBeth", "MachBrait", "Papilio", "Perfil", "Pessoa", "Victor"],
        "signos femininos": ["Aquarius=f", "Aries=f", "Cancer=f", "Caprico=f", "Escorpio=f", "Gemeos=f", "Leao=f", "Libra=f", "Peixes=f", "Sagitari=f", "Touro=f", "Virgem=f"],
        "signos masculinos": ["Aquarius=m", "Aries=m", "Cancer=m", "Caprico=m", "Escorpio=m", "Gemeos=m", "Leao=m", "Libra=m", "Peixes=m", "Sagitari=m", "Touro=m", "Virgem=m"],
        "todos os temas": ["Ais", "Amaré", "Anjos", "Aolero", "Arerir", "Astros", "Atido", "Augusto", "Avevida", "Babel", "Batismo", "Beaba", "Becos", "Blablabla", "Bolero", "Brado", "Bula", "Cadência", "Cartaz", "Circular", "Ciuminho", "Clandestino", "Clarice", "Conto", "Cordel", "Críticas", "Crítico", "Cromossomo", "Cuores", "Destinos", "Distintos", "Dolores", "Duralex", "Elogio", "Enfrente", "Epitafiando", "Escriba", "Essa", "Essas", "Esses", "Estudo", "Fatos", "Feiras", "Festim", "Finalmentes", "Frases", "Fugaz", "Gula", "Haikai", "i-Mundo", "Impar", "Indolor", "Inhos", "Insano", "Joker", "Lato", "Leituras", "Liberta", "Loremipsum", "Machbeth", "Machbrait", "Manifesto", "Manusgrite", "Manusgrito", "Meteoro", "Minuto", "Mirante", "Nonono", "Nós", "Oca", "Ocio", "Oco", "Oficio", "Ogiva", "Olhares", "Palyndro", "Papilio", "Paroles", "Passagens", "Pedidos", "Perfil", "Pessoa", "Portal", "Posfácio", "Preciso", "Prefácil", "Psiu", "Reger", "Reinos", "Remedeio", "Rever", "Rito", "Salute", "Saudades", "Seguro", "Sentença", "Ser", "Silente", "Sinais", "Sinas", "Sn6=ball", "Sn8=ball", "SnowBall", "Sonoro", "Sopros", "Sos", "Tempo", "Time", "Tiro", "Tolero", "Usinas", "Veio", "Victor", "Zelo", "Zodiacaos", "Zoia", "Aquarius=f", "Aquarius=m", "Aries=f", "Aries=m", "Cancer=f", "Cancer=m", "Caprico=f", "Caprico=m", "Escorpio=f", "Escorpio=m", "Gemeos=f", "Gemeos=m", "Leao=f", "Leao=m", "Libra=f", "Libra=m", "Peixes=f", "Peixes=m", "Sagitari=f", "Sagitari=m", "Touro=f", "Touro=m", "Virgem=f", "Virgem=m"]
    }

    # --- 3. PALCO: LISTAS LARGAS E NAVEGADOR ---
    # Proporções expandidas nas laterais para evitar nomes truncados
    col_l, col_nav, col_t = st.columns([2.0, 3.0, 2.0])

    with col_l:
        livro_sel = st.selectbox("livros", list(dicionario_dados.keys()), label_visibility="collapsed")
    
    with col_nav:
        n1, n2, n3, n4, n5, n6 = st.columns(6)
        with n1: st.button("+") 
        with n2: st.button("<") 
        with n3: st.button("*") # aleatório
        with n4: st.button(">") 
        with n5: st.button("?") 
        with n6: st.button("i") # portal About

    with col_t:
        temas_disponiveis = dicionario_dados.get(livro_sel, ["..."])
        tema_sel = st.selectbox("temas", temas_disponiveis, label_visibility="collapsed")

    # Linha separadora sincronizada de ponta a ponta
    st.markdown('<div class="separador-palco"></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
