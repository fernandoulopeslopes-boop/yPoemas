import streamlit as st

def main():
    # Inicialização de estados
    if 'pagina_ativa' not in st.session_state: 
        st.session_state.pagina_ativa = "mini"
    if 'idioma' not in st.session_state:
        st.session_state.idioma = "Português"
    if 'trigger_tts' not in st.session_state:
        st.session_state.trigger_tts = False

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
            }
            [data-testid="stSidebar"] {
                min-width: 300px !important;
                width: 300px !important;
            }
            .stButton > button {
                width: 100%;
                font-size: 22px !important;
                padding: 0px !important;
                border: none !important;
                background: transparent !important;
            }
            div[data-testid="stAudio"] {
                width: 60% !important;
                margin: 0 auto !important;
            }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### a Máquina de Fazer Poesia")
        st.caption("yPoema / Machina")
        
        st.divider()

        # LISTA COMPLETA DE IDIOMAS
        idiomas_base = ["Português", "English", "Español", "Français", "Deutsch", "Italiano"]
        extensao = sorted([
            "Català", "Dansk", "Euskara", "Suomi", "Galego", 
            "Islandska", "Lëtzebuergesch", "Magyar", "Nederlands", 
            "Norsk", "Polski", "Portuñol", "Română", "Slovenčina", "Slovenščina"
        ]) + ["Russia", "Suécia"]
        
        lista_completa = idiomas_base + extensao
        st.session_state.idioma = st.selectbox("Translator", lista_completa)
        
        st.divider()

        col_art, col_aud = st.columns(2)
        with col_art:
            st.button("Arte")
        with col_aud:
            # DISPARA O TALK/TTS
            if st.button("Áudio"):
                st.session_state.trigger_tts = True
        
        st.divider()

    # PALCO: NAVEGAÇÃO PROPORCIONAL
    paginas = ["mini", "yPoema", "eureka", "off-machina", "livros", "poly", "opinião", "sobre"]
    pesos = [len(pg) for pg in paginas]
    
    cols = st.columns(pesos)
    for i, pg in enumerate(paginas):
        with cols[i]:
            if st.button(pg, key=f"btn_{pg}"):
                st.session_state.pagina_ativa = pg
                st.session_state.trigger_tts = False 
                st.rerun()

    st.divider()

    # LÓGICA DO TALK/TTS NO PALCO
    if st.session_state.trigger_tts:
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
        voz = vozes_neurais.get(st.session_state.idioma, "voz_neural")
        texto_para_falar = st.session_state.pagina_ativa

        st.write("") 
        # O player agora "fala" o nome da página
        st.audio(f"https://translate.google.com/translate_tts?ie=UTF-8&q={texto_para_falar}&tl=pt&client=tw-ob") 
        st.caption(f"<p style='text-align: center;'>Talk/TTS: <b>{texto_para_falar}</b> (Voz: {voz})</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
