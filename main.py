import streamlit as st

# 1. CONFIGURAÇÃO DA PÁGINA (NOME OFICIAL)
st.set_page_config(page_title="a Machina de fazer Poesia", layout="wide")

# CSS: LARGURA DA SIDEBAR (300px), ALINHAMENTO E RODAPÉ FIXO
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            width: 300px;
            max-width: 300px;
        }
        .stButton button {
            width: 100%;
        }
        .footer-social {
            position: fixed;
            bottom: 20px;
            width: 260px;
            text-align: center;
            font-size: 20px;
        }
        /* Ajuste para centralizar o slider de som */
        .centered-slider {
            display: flex;
            justify-content: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# 2. ESTADO DA SESSÃO
if 'pagina_ativa' not in st.session_state:
    st.session_state.pagina_ativa = "mini"
if 'som_ativo' not in st.session_state:
    st.session_state.som_ativo = False

# 3. SIDEBAR: CENTRO DE CONTROLE
with st.sidebar:
    # A. Topo: Lista Oficial Completa (incluindo o Russo: ru)
    idiomas_oficiais = [
        "Português : pt", "Espanhol : es", "Italiano : it", "Francês : fr", 
        "Inglês : en", "Catalão : ca", "Córsico : co", "Galego : gl", 
        "Basco : eu", "Esperanto : eo", "Latin : la", "Galês : cy", 
        "Sueco : sv", "Polonês : pl", "Holandês : nl", "Norueguês : no", 
        "Finlandês : fi", "Dinamarquês : da", "Irlandês : ga", "Romeno : ro",
        "Russo : ru"
    ]
    st.selectbox("idiomas disponíveis", idiomas_oficiais, key="lang_selector")
    
    # B. Arte e Som (Alinhados com a largura da lista)
    col_media_1, col_media_2 = st.columns(2)
    with col_media_1:
        st.button("🎨 arte")
    with col_media_2:
        if st.button("🔊 som"):
            st.session_state.som_ativo = not st.session_state.som_ativo

    st.divider()

    # C. Controle Interno (Rádio oculto para sincronia com o palco)
    paginas = ["mini", "yPoemas", "eureka", "off-machina", "livros", "poly", "opiniões", "sobre/about"]
    # Radio mantido no palco para teste estético conforme solicitado
    st.session_state.pagina_ativa = st.radio("navegação interna:", paginas, label_visibility="collapsed")

    st.divider()

    # D. Info e Arte (Traduzidos e em lower)
    st.markdown(f"### info: {st.session_state.pagina_ativa}")
    st.info(f"under construction: {st.session_state.pagina_ativa}")
    
    st.image("https://via.placeholder.com/260x260.png?text=arte+da+pagina", use_column_width=True)

    # E. Rodapé: Redes Sociais
    st.markdown(
        """
        <div class="footer-social">
            <hr>
            🐦 &nbsp; 📸 &nbsp; 🐙 &nbsp; ✉️
        </div>
        """,
        unsafe_allow_html=True
    )

# 4. O PALCO: AVALIAÇÃO VISUAL E ESTÉTICA
st.title(f"a machina / {st.session_state.pagina_ativa}")

# Botões de navegação no palco para avaliação de estética
cols_nav = st.columns(len(paginas))
for idx, nome_pg in enumerate(paginas):
    with cols_nav[idx]:
        if st.button(nome_pg, key=f"btn_{nome_pg}"):
            st.session_state.pagina_ativa = nome_pg
            st.rerun()

# Espaço do Som (Centralizado, entre botões e moldura)
if st.session_state.som_ativo:
    st.markdown("<br>", unsafe_allow_html=True)
    _, col_slider, _ = st.columns([1, 2, 1]) # width = largura_do_palco/2
    with col_slider:
        st.slider("volume", 0, 100, 50, label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)

# Moldura do Palco (Conteúdo Ativo)
with st.container(border=True):
    if st.session_state.pagina_ativa == "yPoemas":
        st.subheader("yPoemas")
        st.warning("⚠️ under construction")
    
    elif st.session_state.pagina_ativa == "poly":
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1: st.button("✔")
        with c2: st.button("⭐") 
        with c3: st.button("?")
        st.warning("⚠️ under construction")
    
    else:
        st.warning(f"⚠️ under construction: {st.session_state.pagina_ativa}")

# Radio no palco apenas para teste estético como solicitado
st.divider()
st.write("teste estético de radio no palco:")
st.radio("", paginas, horizontal=True, key="radio_palco")
