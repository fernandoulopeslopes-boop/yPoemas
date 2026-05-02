import streamlit as st

def main():
    if 'pagina_ativa' not in st.session_state: 
        st.session_state.pagina_ativa = "mini"
    if 'idioma' not in st.session_state:
        st.session_state.idioma = "Português"
    if 'play_audio' not in st.session_state:
        st.session_state.play_audio = False

    st.markdown("""
        <style>
            [data-testid="stAppViewContainer"] {
                display: flex;
                flex-direction: row;
                width: 100vw !important;
            }
            .main {
                flex-grow: 1;
                width: auto !important;
            }
            .main .block-container {
                max-width: 98vw !important;
                width: 98vw !important;
                margin-left: auto !important;
                margin-right: auto !important;
                padding-top: 2rem !important;
                padding-left: 1rem !important;
                padding-right: 1rem !important;
                transition: width 0.3s ease-in-out;
            }
            [data-testid="stSidebar"] {
                min-width: 300px !important;
                width: 300px !important;
            }
            [data-testid="stHeader"] {
                background: transparent !important;
            }
            .stButton > button {
                width: 100%;
                font-size: 22px !important;
                padding: 0px !important;
                border: none !important;
                background: transparent !important;
            }
            /* Alinhamento central do áudio no palco */
            div[data-testid="stAudio"] {
                width: 60% !important;
                margin: 0 auto !important;
            }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        # TÍTULO DA MÁQUINA NO TOPO DA SIDEBAR
        st.markdown("### a Máquina de Fazer Poesia")
        st.caption("yPoema / Machina")
        
        st.divider()

        # TRANSLATOR (22 IDIOMAS)
        idiomas_base = ["Português", "English", "Español", "Français", "Deutsch", "Italiano"]
        extensao = sorted([
            "Català", "Dansk", "Euskara", "Suomi", "Galego", 
            "Islandska", "Lëtzebuergesch", "Magyar", "Nederlands", 
            "Norsk", "Polski", "Portuñol", "Română", "Slovenčina", "Slovenščina"
        ]) + ["Russia", "Suécia"]
        
        lista_completa = idiomas_base + extensao
        st.session_state.idioma = st.selectbox("Translator", lista_completa)
        
        st.divider()

        # BOTÕES ARTE E ÁUDIO (O CLIQUE EM ÁUDIO DISPARA O TALK)
        col_art, col_aud = st.columns(2)
        with col_art:
            st.button("Arte")
        with col_aud:
            if st.button("Áudio"):
                # O botão áudio agora assume a função de disparar o TTS
                st.session_state.play_audio = True
        
        st.divider()

    # PALCO: NAVEGAÇÃO PROPORCIONAL (MOLDURA m -> e)
    paginas = ["mini", "yPoema", "eureka", "off-machina", "livros", "poly", "opinião", "sobre"]
    pesos = [len(pg) for pg in paginas]
    
    cols = st.columns(pesos)
    for i, pg in enumerate(paginas):
        with cols[i]:
            if st.button(pg, key=f"btn_{pg}"):
                st.session_state.pagina_ativa = pg
                st.session_state.play_audio = False 
                st.rerun()

    st.divider()

    # SLIDE DO ÁUDIO: NO PALCO, ABAIXO DAS PÁGINAS, CENTRADO
    if st.session_state.play_audio:
        # MAPEAMENTO DE VOZES MASCULINAS "NOME_NEURAL"
        vozes_neurais = {
            "Português": "antonio_neural", "English": "brian_neural", "Español": "enrique_neural",
            "Français": "mathieu_neural", "Deutsch": "hans_neural", "Italiano": "giorgio_neural",
            "Dansk": "mads_neural", "Suomi": "jari_neural", "Nederlands": "ruben_neural",
            "Norsk": "henrik_neural", "Suécia": "hugo_neural", "Polski": "jacek_neural",
            "Română": "alexandru_neural", "Magyar": "tamas_neural", "Català": "jordi_neural",
            "Islandska": "karl_neural", "Euskara": "jon_neural", "Galego": "roi_neural",
            "Slovenčina": "filip_neural", "Slovenščina": "luka_neural", "Portuñol": "miguel_neural",
            "Lëtzebuergesch": "marc_neural", "Russia": "maxim_neural"
        }
        voz_selecionada = vozes_neurais.get(st.session_state.idioma, "voz_neural")
        
        st.write("") 
        # O player centrado que aparece ao clicar em "Áudio" na sidebar
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3") 
        st.caption(f"<p style='text-align: center;'>Talk/TTS Ativo: {voz_selecionada}</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
