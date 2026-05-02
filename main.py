import streamlit as st

def main():
    # Garantindo que a página ativa e o idioma existam no estado
    if 'pagina_ativa' not in st.session_state: 
        st.session_state.pagina_ativa = None  # Começa zerado
    if 'idioma' not in st.session_state:
        st.session_state.idioma = "Português"
    if 'trigger_tts' not in st.session_state:
        st.session_state.trigger_tts = False

    st.markdown("""
        <style>
            [data-testid="stAppViewContainer"] { display: flex; flex-direction: row; width: 100vw !important; }
            .main { flex-grow: 1; width: auto !important; }
            .main .block-container { max-width: 98vw !important; padding-top: 2rem !important; }
            [data-testid="stSidebar"] { min-width: 300px !important; }
            .stButton > button { width: 100%; font-size: 22px !important; background: transparent !important; border: none !important; }
            div[data-testid="stAudio"] { width: 60% !important; margin: 0 auto !important; }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### a Máquina de Fazer Poesia")
        st.caption("yPoema / Machina")
        
        st.divider()

        # Lista de 22 Idiomas (Filtro Ocidental)
        idiomas_base = ["Português", "English", "Español", "Français", "Deutsch", "Italiano"]
        extensao = sorted(["Català", "Dansk", "Euskara", "Suomi", "Galego", "Islandska", "Lëtzebuergesch", "Magyar", "Nederlands", "Norsk", "Polski", "Portuñol", "Română", "Slovenčina", "Slovenščina"]) + ["Russia", "Suécia"]
        
        st.session_state.idioma = st.selectbox("Translator", idiomas_base + extensao)
        
        st.divider()

        col_art, col_aud = st.columns(2)
        with col_art:
            st.button("Arte")
        with col_aud:
            # Só permite o gatilho se houver uma página selecionada
            if st.button("Áudio"):
                if st.session_state.pagina_ativa:
                    st.session_state.trigger_tts = True
                else:
                    st.sidebar.warning("Selecione uma página primeiro.")

    # PALCO: Navegação Proporcional
    paginas = ["mini", "yPoema", "eureka", "off-machina", "livros", "poly", "opinião", "sobre"]
    pesos = [len(pg) for pg in paginas]
    
    cols = st.columns(pesos)
    for i, pg in enumerate(paginas):
        with cols[i]:
            if st.button(pg, key=f"btn_{pg}"):
                st.session_state.pagina_ativa = pg
                st.session_state.trigger_tts = False # Reseta para aguardar novo clique em áudio
                st.rerun()

    st.divider()

    # LOGICA TTS (NOMES NEURAIS MASCULINOS)
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
    
    audio_source = None
    # Se houver página e o botão Áudio foi clicado, gera a URL
    if st.session_state.trigger_tts and st.session_state.pagina_ativa:
        texto = st.session_state.pagina_ativa
        audio_source = f"https://translate.google.com/translate_tts?ie=UTF-8&q={texto}&tl=pt&client=tw-ob"

    # Player aparece zerado se audio_source for None
    st.audio(audio_source) 
    st.caption(f"<p style='text-align: center;'>Status: <b>{voz}</b> | Página: <b>{st.session_state.pagina_ativa or 'Nenhuma'}</b></p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
