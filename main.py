# ... (manter o bloco inicial de settings e navegação)

### bof: sidebar (O Novo Painel Minimalista)

# 1. Arte da Página (Sem controles de imagem)
mapeamento_artes = {
    "mini": "img_mini.jpg",
    "ypoemas": "img_ypoemas.jpg",
    "eureka": "img_eureka.jpg",
    "off-machina": "img_off-machina.jpg",
    "comments": "img_poly.jpg",
    "sobre": "img_about.jpg"
}

arte_atual = mapeamento_artes.get(st.session_state.page)
if arte_atual and os.path.exists(arte_atual):
    st.sidebar.image(arte_atual, use_container_width=True)

st.sidebar.markdown("<br>", unsafe_allow_html=True) # Espaçamento leve

# 2. Seção: Idiomas
st.sidebar.markdown("### idiomas")
st.selectbox(
    "Escolha a tradução:",
    ["Português", "English", "Français", "Español", "Italiano"],
    label_visibility="collapsed", # Esconde o label interno para ficar mais clean
    key="sel_lang"
)

# 3. Seção: Recursos
st.sidebar.markdown("### recursos")
# Usando checkbox ou um multiselect para "Talk" e "Draw"
st.session_state.audio_on = st.sidebar.checkbox("🎙️ voz (talk)", value=True)
st.session_state.draw_on = st.sidebar.checkbox("🎨 arte (draw)", value=True)

st.sidebar.markdown("---")

# 4. Redes Sociais & Info (Onde os botões viram links)
st.sidebar.markdown("### conexões")
st.sidebar.markdown("""
<div style="display: flex; gap: 15px; font-size: 20px;">
    <a href="https://github.com/seu-perfil" target="_blank">🐙</a>
    <a href="https://instagram.com/seu-perfil" target="_blank">📸</a>
    <a href="mailto:seu-email@link.com">✉️</a>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.caption("Phenix Machina v2026")
