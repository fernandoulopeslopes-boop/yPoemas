import streamlit as st

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 320px !important;
        }
        [data-testid="stMarkdownContainer"] img {
            border-radius: 5px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

IDIOMAS_OFFICIAL = {
    "Português": "pt", "Espanhol": "es", "Italiano": "it", "Francês": "fr",
    "Inglês": "en", "Catalão": "ca", "Córsico": "co", "Galego": "gl",
    "Basco": "eu", "Esperanto": "eo", "Latim": "la", "Galês": "cy",
    "Sueco": "sv", "Polonês": "pl", "Holandês": "nl", "Norueguês": "no",
    "Finlandês": "fi", "Dinamarquês": "da", "Irlandês": "ga", "Romeno": "ro",
    "Russo": "ru"
}

with st.sidebar:
    nome_idioma = st.segmented_control(
        label="Idiomas",
        options=list(IDIOMAS_OFFICIAL.keys()),
        default="Português",
        label_visibility="collapsed"
    )
    sigla_idioma = IDIOMAS_OFFICIAL[nome_idioma]

    st.markdown(info_pagina)
    st.image(imagem_pagina, use_container_width=True)

    c_som, c_arte = st.columns(2)
    with c_som:
        if st.button("Som", use_container_width=True):
            st.session_state['som'] = sigla_idioma
    with c_arte:
        if st.button("Arte", use_container_width=True):
            st.session_state['arte'] = sigla_idioma

    st.divider()

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f"[![Zap](app/static/btn_zap.jpg)](https://wa.me/5512991368181)")
    with c2: st.markdown(f"[![Mail](app/static/btn_mail.jpg)](mailto:lopes.fernando@hotmail.com)")
    with c3: st.markdown(f"[![Face](app/static/btn_face.jpg)](https://www.facebook.com/fernando.lopes.942)")
    with c4: st.markdown(f"[![Insta](app/static/btn_insta.jpg)](https://www.instagram.com/fernandoulopes)")

if __name__ == "__main__":
    pass
