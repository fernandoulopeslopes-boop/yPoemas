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
# CORE (EIXO X + Y + Z)
# =========================
def core_generate(theme: str, lang: str, z_variations: int = 3):
    """
    Núcleo da Machina com Eixo Z:
    gera múltiplas variações do mesmo poema-base
    """

    base = f"[{lang}] yPoema sobre {theme}"

    results = []

    for i in range(z_variations):
        # pequena variação estrutural simulando deriva do Z
        if i == 0:
            content = base
        elif i == 1:
            content = base + " :: deriva silenciosa"
        else:
            content = base + " :: expansão residual da linguagem"

        results.append({
            "version": i,
            "theme": theme,
            "lang": lang,
            "content": content,
            "meta": {
                "z_index": i
            }
        })

    return results

# =========================
# STAGE (RENDER PURA)
# =========================
def stage_render(results: list):
    st.markdown("## 🎭 Palco")

    for r in results:
        st.text_area(
            f"yPoema Z-{r['meta']['z_index']}",
            r["content"],
            height=140
        )

        st.divider()

# =========================
# UI — CENTRO DE CONTROLE
# =========================
st.title("Machina de Fazer Poesia")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Centro de Controle")

    lang = st.selectbox("Idioma (X)", list(voices.keys()))
    theme = st.text_input("Tema (Y)", "Babel")
    z = st.slider("Eixo Z (variações)", 1, 5, 3)

    go = st.button("GO")

with col2:
    if go:
        results = core_generate(theme, lang, z_variations=z)
        stage_render(results)
