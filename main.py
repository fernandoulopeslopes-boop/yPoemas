import streamlit as st

def main():
    if 'pagina_ativa' not in st.session_state: 
        st.session_state.pagina_ativa = "mini"
    if 'idioma' not in st.session_state:
        st.session_state.idioma = "Português"

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
            [data-testid="stSidebar"][aria-expanded="false"] {
                min-width: 0px !important;
                width: 0px !important;
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
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.button("Talk")
        
        st.divider()

        # LISTA DE IDIOMAS: OCIDENTAIS + EXTENSÃO (RUSSIA + SUÉCIA NO FINAL)
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
            # MAPEAMENTO DE VOZES (NOMES PRÓPRIOS MASCULINOS)
            vozes_neurais = {
                "Português": "António", "English": "Brian", "Español": "Enrique",
                "Français": "Mathieu", "Deutsch": "Hans", "Italiano": "Giorgio",
                "Dansk": "Mads", "Suomi": "Jari", "Nederlands": "Ruben",
                "Norsk": "Henrik", "Suécia": "Hugo", "Polski": "Jacek",
                "Română": "Alexandru", "Magyar": "Tamás", "Català": "Jordi",
                "Islandska": "Karl", "Euskara": "Jon", "Galego": "Roi",
                "Slovenčina": "Filip", "Slovenščina": "Luka", "Portuñol": "Miguel",
                "Lëtzebuergesch": "Marc", "Russia": "Maxim"
            }
            voz_ativa = vozes_neurais.get(st.session_state.idioma, "Voz Masculina")
            if st.button("Áudio"):
                st.toast(f"Voz: {voz_ativa}")

        st.divider()

        st.markdown("### a Máquina de Fazer Poesia")
        st.caption("yPoema / Machina")

    # PALCO: NAVEGAÇÃO PROPORCIONAL POR CARACTERES
    paginas = ["mini", "yPoema", "eureka", "off-machina", "livros", "poly", "opiniões", "sobre"]
    pesos = [len(pg) for pg in paginas]
    
    cols = st.columns(pesos)
    for i, pg in enumerate(paginas):
        with cols[i]:
            if st.button(pg, key=f"btn_{pg}"):
                st.session_state.pagina_ativa = pg
                st.rerun()

    st.divider()

if __name__ == "__main__":
    main()
