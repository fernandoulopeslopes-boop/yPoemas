import streamlit as st

# 1. CONFIGURAÇÃO DA PÁGINA (NOME OFICIAL)
st.set_page_config(page_title=t("a Machina de fazer Poesia"), layout="wide")

# 2. CSS PARA EXPANSÃO TOTAL E ESTÉTICA DA SIDEBAR
st.markdown(
    """
    <style>
        /* Expansão total do palco quando a sidebar é recolhida */
        .main .block-container {
            max-width: 100%;
            padding-left: 2rem;
            padding-right: 2rem;
        }
        
        /* Largura fixa da sidebar de 300px */
        [data-testid="stSidebar"] {
            width: 300px;
            max-width: 300px;
        }
        
        /* Botões ocupando toda a largura da sidebar */
        .stButton button {
            width: 100%;
        }

        /* Rodapé Fixo nas redes sociais */
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

# 3. SISTEMA DE TRADUÇÃO (MANDATÓRIO)
def t(texto):
    # Regra: yPoemas sempre preservado (exceção à regra lower)
    if "yPoemas" in texto:
        return texto
    return texto.lower() # Todos os outros nomes traduzidos e em lower

# 4. ESTADO DA SESSÃO
if 'pagina_ativa' not in st.session_state:
    st.session_state.pagina_ativa = "mini" # Default = mini
if 'som_ativo' not in st.session_state:
    st.session_state.som_ativo = False

# 5. SIDEBAR: CENTRO DE CONTROLE
with st.sidebar:
    # A. Topo: Lista Oficial Completa (incluindo Russo)
    idiomas_oficiais = [
        "Português : pt", "Espanhol : es", "Italiano : it", "Francês : fr", 
        "Inglês : en", "Catalão : ca", "Córsico : co", "Galego : gl", 
        "Basco : eu", "Esperanto : eo", "Latin : la", "Galês : cy", 
        "Sueco : sv", "Polonês : pl", "Holandês : nl", "Norueguês : no", 
        "Finlandês : fi", "Dinamarquês : da", "Irlandês : ga", "Romeno : ro",
        "Russo : ru"
    ]
    
    idioma_selecionado = st.selectbox(
        t("idiomas disponíveis"), # Texto oficial: idiomas disponíveis
        idiomas_oficiais, 
        key="lang_selector", 
        help=t("selecione o idioma da machina")
    )
    
    # B. arte e som (alinhados horizontalmente)
    col_media_1, col_media_2 = st.columns(2)
    with col_media_1:
        st.button(t("🎨 arte"), help=t("visualizar mandalas e artes"))
    with col_media_2:
        # Help tip dinâmico conforme regra específica
        help_som = t(f"ouvir o yPoemas em {idioma_selecionado}")
        if st.button(t("🔊 som"), help=help_som):
            st.session_state.som_ativo = not st.session_state.som_ativo

    st.divider()

    # C. Info e Arte da Página Ativa na Sidebar
    st.markdown(f"### {t('info')}: {st.session_state.pagina_ativa if st.session_state.pagina_ativa != 'yPoemas' else 'yPoemas'}")
    st.info(t(f"under construction: {st.session_state.pagina_ativa}"))
    st.image("https://via.placeholder.com/260x260.png?text=arte+da+pagina", use_column_width=True)

    # D. Rodapé: Redes Sociais
    st.markdown(
        """
        <div class="footer-social">
            <hr>
            🐦 &nbsp; 📸 &nbsp; 🐙 &nbsp; ✉️
        </div>
        """,
        unsafe_allow_html=True
    )

# 6. O PALCO: EXPANSÃO E TESTE ESTÉTICO
st.title(f"{t('a machina')} / {st.session_state.pagina_ativa if st.session_state.pagina_ativa != 'yPoemas' else 'yPoemas'}")

# Navegação por Botões no Palco para avaliação estética
paginas = ["mini", "yPoemas", "eureka", "off-machina", "livros", "poly", "opiniões", "sobre/about"]
cols_nav = st.columns(len(paginas))
for idx, nome_pg in enumerate(paginas):
    with cols_nav[idx]:
        nome_exibicao = "yPoemas" if nome_pg == "yPoemas" else t(nome_pg)
        if st.button(nome_exibicao, key=f"palco_{nome_pg}"):
            st.session_state.pagina_ativa = nome_pg
            st.rerun()

# Controle de Som (Centralizado acima da moldura)
if st.session_state.som_ativo:
    st.markdown("<br>", unsafe_allow_html=True)
    _, col_slider, _ = st.columns([1, 2, 1]) # width = largura_do_palco/2
    with col_slider:
        st.slider(t("volume"), 0, 100, 50, label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)

# Teste Estético: Radio movido para o Palco conforme pedido
st.write(t("teste estético de radio no palco:"))
st.radio(
    "", 
    [("yPoemas" if p == "yPoemas" else t(p)) for p in paginas], 
    horizontal=True, 
    key="radio_palco_teste"
)

# Moldura do Palco (Conteúdo Ativo)
with st.container(border=True):
    if st.session_state.pagina_ativa == "yPoemas":
        st.subheader("yPoemas")
        st.warning(t("⚠️ under construction"))
    
    elif st.session_state.pagina_ativa == "poly":
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1: st.button("✔")
        with c2: st.button("⭐") 
        with c3: st.button("?", help=t("informações sobre os idiomas")) # Help específico solicitado
        st.warning(t("⚠️ under construction"))
    
    else:
        st.warning(t(f"⚠️ under construction: {st.session_state.pagina_ativa}"))
