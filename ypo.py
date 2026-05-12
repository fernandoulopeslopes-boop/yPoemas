import streamlit as st

st.set_page_config(
    page_title="Machina Sidebar Preview",
    page_icon="✶",
    layout="wide",
    initial_sidebar_state="expanded",
)

IDIOMAS = [
    "Português", "Español", "Italiano", "Français", "English",
    "Català", "Deutsch", "Dansk", "Esperanto", "Galego", "Latin",
    "Íslenska", "Nederlands", "Norsk", "Polski", "Portuñol",
    "Română", "Русский", "Svenska", "Suomi", "Magyar",
]

PAGINAS = ["mini", "yPoemas", "eureka", "off-machina", "livros", "poly", "sobre"]
ICON_COLOR = "#c1bad8"

st.markdown(
    f"""
    <style>
    [data-testid="stSidebar"] {{
        min-width: 310px !important;
        width: 310px !important;
        max-width: 310px !important;
        background-color: #09090b;
        font-family: 'IBM Plex Sans', Arial, sans-serif !important;
        overflow-x: hidden !important;
    }}
    [data-testid="stSidebar"] * {{
        font-family: 'IBM Plex Sans', Arial, sans-serif !important;
        font-size: 12px !important;
        line-height: 1.25 !important;
    }}
    [data-testid="stSidebar"] section {{
        padding-top: 0.6rem !important;
    }}
    div[data-testid="stSelectbox"] {{
        width: 80% !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }}
    div[data-testid="stSelectbox"] label {{
        display: none !important;
    }}
    div[data-testid="stSelectbox"] div {{
        font-family: 'IBM Plex Sans', Arial, sans-serif !important;
        font-size: 12px !important;
    }}
    .sb-row {{
        width: 80%;
        margin: 0 auto 0.65rem auto;
        display: grid;
        grid-template-columns: 1fr 1.35fr 1fr;
        gap: 6px;
    }}
    .sb-row-4 {{
        width: 80%;
        margin: 0 auto 0.65rem auto;
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 6px;
    }}
    .sb-btn {{
        height: 28px;
        border: 1px solid #27272a;
        border-radius: 6px;
        background: rgba(24,24,27,.65);
        color: {ICON_COLOR};
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        white-space: nowrap;
    }}
    .sb-info {{
        width: 80%;
        margin: 0 auto 0.65rem auto;
        border: 1px solid #27272a;
        border-radius: 7px;
        background: rgba(24,24,27,.45);
        color: #d4d4d8;
        padding: 8px 9px;
    }}
    .sb-info-title {{
        color: {ICON_COLOR};
        margin-bottom: 4px;
    }}
    .mini-palco {{
        margin: 0 8px 0.65rem 8px;
        min-height: 180px;
        border: 1px solid #27272a;
        border-radius: 7px;
        background: rgba(24,24,27,.25);
        color: #a1a1aa;
        padding: 10px;
    }}
    .mini-palco-title {{
        color: {ICON_COLOR};
        font-size: 11px !important;
        margin-bottom: 8px;
    }}
    .sb-footer-art {{
        width: 300px;
        height: 96px;
        margin: 0 auto;
        border: 1px solid #27272a;
        border-radius: 7px;
        background: linear-gradient(135deg, #18181b, #2e1065, #09090b);
        color: {ICON_COLOR};
        display: flex;
        align-items: center;
        justify-content: center;
        letter-spacing: .04em;
    }}
    .main .block-container {{
        padding-top: 1rem !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

if "pagina_preview" not in st.session_state:
    st.session_state.pagina_preview = "yPoemas"

with st.sidebar:
    st.selectbox("idiomas", IDIOMAS, index=0, key="idioma_preview")

    st.markdown(
        """
        <div class="sb-row">
            <div class="sb-btn" title="arte">◉</div>
            <div class="sb-btn" title="fonte">⟐</div>
            <div class="sb-btn" title="audio">◌</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="sb-info">
            <div class="sb-info-title">{st.session_state.pagina_preview}</div>
            <div>info da página em foco</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sb-row-4">
            <div class="sb-btn" title="anterior">←</div>
            <div class="sb-btn" title="aleatório">※</div>
            <div class="sb-btn" title="novo">↻</div>
            <div class="sb-btn" title="próximo">→</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="mini-palco">
            <div class="mini-palco-title">mini-palco</div>
            <div>área reservada</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sb-footer-art">
            arte da página • 300 px
        </div>
        """,
        unsafe_allow_html=True,
    )

cols = st.columns([1, 1, 1, 1, 1, 1, 1])
for col, pagina in zip(cols, PAGINAS):
    with col:
        if st.button(pagina, key=f"page_{pagina}"):
            st.session_state.pagina_preview = pagina
            st.rerun()

st.markdown("### Palco principal vazio")
st.write("Use este arquivo apenas para testar a presença visual da sidebar.")
