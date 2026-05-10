import streamlit as st

# =========================
# CONFIG
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
# CORE — EIXO Z REAL
# =========================
def core_generate(theme: str, lang: str, z_variations: int = 3):

    results = []

    for i in range(z_variations):

        # Z ALTERA ESTRUTURA, NÃO TEXTO
        if i == 0:
            content = f"[{lang}] {theme}"
        elif i == 1:
            content = f"[{lang}] {theme}\n\nsilêncio entre camadas"
        else:
            content = f"[{lang}] {theme}\n\nsilêncio entre camadas\n\nderiva sem fechamento\neco residual"

        results.append({
            "z": i,
            "lang": lang,
            "content": content
        })

    return results

# =========================
# STAGE
# =========================
def stage_render(results):

    st.markdown("## 🎭 Palco")

    for r in results:

        st.markdown(f"### Z-{r['z']}")

        st.text_area(
            "yPoema",
            r["content"],
            height=160
        )

        st.divider()

# =========================
# UI
# =========================
st.title("Machina de Fazer Poesia")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Centro de Controle")

    lang = st.selectbox("Idioma (X)", list(voices.keys()))
    theme = st.text_input("Tema (Y)", "Babel")
    z = st.slider("Eixo Z", 1, 3, 3)

    go = st.button("GO")

with col2:
    if go:
        results = core_generate(theme, lang, z_variations=z)
        stage_render(results)
