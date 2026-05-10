import streamlit as st

# =========================
# CONFIG BASE
# =========================
st.set_page_config(
    page_title="Machina de Fazer Poesia",
    layout="wide"
)

# =========================
# VOZES (placeholder futuro)
# =========================
voices = {
    "pt": "pt-BR-FranciscaNeural",
    "en": "en-US-AvaNeural",
    "es": "es-ES-ElviraNeural",
    "fr": "fr-FR-DeniseNeural",
    "it": "it-IT-ElsaNeural"
}

# =========================
# CORE (simulado por enquanto)
# =========================
def core_generate(theme: str, lang: str):
    """
    Núcleo lógico da Machina (placeholder limpo)
    Aqui depois entra Eixo X/Y/Z real.
    """
    return {
        "theme": theme,
        "lang": lang,
        "content": f"[{lang}] yPoema sobre {theme}",
        "meta": {
            "z_state": "neutral"
        }
    }

# =========================
# STAGE (apenas render)
# =========================
def stage_render(result: dict):
    st.markdown("## 🎭 Palco")

    st.text_area(
        "yPoema",
        result["content"],
        height=300
    )

    st.caption(f"Tema: {result['theme']} | Idioma: {result['lang']}")

# =========================
# UI — CENTRO DE CONTROLE
# =========================
st.title("Machina de Fazer Poesia")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Centro de Controle")

    lang = st.selectbox("Idioma (X)", list(voices.keys()))
    theme = st.text_input("Tema (Y)", "Babel")

    go = st.button("GO")

with col2:
    if go:
        result = core_generate(theme, lang)
        stage_render(result)
