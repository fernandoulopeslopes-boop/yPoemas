import streamlit as st

# 1. CONFIGURAÇÃO DA PÁGINA (NOME OFICIAL)
st.set_page_config(page_title="a Machina de fazer Poesia", layout="wide")

# CSS para fixar a sidebar em 300px e garantir o equilíbrio estético
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            width: 300px;
            max-width: 300px;
        }
        .footer-social {
            position: fixed;
            bottom: 20px;
            width: 260px;
            text-align: center;
            font-size: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# 2. ESTADO DA SESSÃO (DEFAULT = MINI)
if 'pagina_ativa' not in st.session_state:
    st.session_state.pagina_ativa = "mini"

# 3. SIDEBAR: O CENTRO DE CONTROLE
with st.sidebar:
    # A. Topo: Lista Oficial de Idiomas (Sequência pt a ro)
    idiomas_oficiais = [
        "Português : pt", "Espanhol : es", "Italiano : it", "Francês : fr", 
        "Inglês : en", "Catalão : ca", "Córsico : co", "Galego : gl", 
        "Basco : eu", "Esperanto : eo", "Latin : la", "Galês : cy", 
        "Sueco : sv", "Polonês : pl", "Holandês : nl", "Norueguês : no", 
        "Finlandês : fi", "Dinamarquês : da", "Irlandês : ga", "Romeno : ro", "Russo : ru"
    ]
    st.selectbox("Idiomas disponíveis", idiomas_oficiais, key="lang_selector")
    
    # B. Controles de Mídia: conforme o manual oficial
    col_media_1, col_media_2 = st.columns(2)
    with col_media_1:
        st.button("🎨 arte")
    with col_media_2:
        st.button("🔊 som")

    st.divider()

    # C. Navegação (Lista em lower, sem rótulo intruso)
    paginas = ["mini", "ypoemas", "eureka", "off-machina", "poly", "opiniões", "sobre/about"]
    st.session_state.pagina_ativa = st.radio("", paginas)

    st.divider()

    # D. Info_About & Arte da Página Ativa
    st.markdown(f"### info: {st.session_state.pagina_ativa}")
    
    # Exibição do contexto (under construction)
    st.info(f"under construction: {st.session_state.pagina_ativa}")
    
    # Arte da página ativa
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

# 4. O PALCO: AVALIAÇÃO VISUAL
st.title(f"{st.session_state.pagina_ativa}")

if st.session_state.pagina_ativa == "mini":
    st.warning("⚠️ under construction")

elif st.session_state.pagina_ativa == "yPoemas":
    st.warning("⚠️ under construction")

elif st.session_state.pagina_ativa == "eureka":
    st.warning("⚠️ under construction")

elif st.session_state.pagina_ativa == "off-machina":
    st.warning("⚠️ under construction")

elif st.session_state.pagina_ativa == "poly":
    # A trindade de botões na Poly: Confirmar, Estrela Guia e Help Técnico
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1: st.button("✔")
    with c2: st.button("⭐")
    with c3: st.button("?")
    st.warning("⚠️ under construction")

elif st.session_state.pagina_ativa == "opiniões":
    st.warning("⚠️ under construction")

elif st.session_state.pagina_ativa == "sobre":
    st.warning("⚠️ under construction")
