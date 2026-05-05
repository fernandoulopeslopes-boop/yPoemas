import streamlit as st
import os
import glob
import base64

# 1. IDIOMAS - Dicionário Estático (Protocolo Machina)
IDIOMAS = {
    "Português": "pt",
    "English": "en",
    "Español": "es",
    "Français": "fr",
    "Deutsch": "de",
    "Italiano": "it"
}

# 2. INJEÇÃO DE CSS (Parâmetro corrigido para unsafe_allow_html)
css_style = "<style>section[data-testid='stSidebar'] {width: 300px !important; max-width: 300px !important; min-width: 300px !important;} .linkey-container {display: flex; justify-content: flex-end; padding-right: 5px;} .linkey-button {background: none; border: none; padding: 0; cursor: pointer;}</style>"
st.markdown(css_style, unsafe_allow_html=True)

# 3. ESTADO DA SESSÃO
if "focus_page" not in st.session_state:
    st.session_state.focus_page = "livros"
if "lang_selector" not in st.session_state:
    st.session_state.lang_selector = list(IDIOMAS.keys())[0]

# 4. AUXILIARES
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# ============================================================
# ⚙️ SIDEBAR (300px)
# ============================================================
def render_sidebar():
    with st.sidebar:
        # Linkey com injeção HTML corrigida
        chave_base64 = get_base64_image("images/chave_dourada.png")
        if chave_base64:
            html_linkey = f"<div class='linkey-container'><button class='linkey-button'><img src='data:image/png;base64,{chave_base64}' width='20' height='20' style='image-rendering: pixelated;'/></button></div>"
            st.markdown(html_linkey, unsafe_allow_html=True)
        else:
            st.button("🔗", key="btn_linkey")

        # Imagem e Info (Padrão: img_[PAGINA].JPG / INFO_[PAGINA].MD)
        pg = str(st.session_state.focus_page)
        
        # Render Imagem
        img_path = f"images/img_{pg}.JPG"
        if os.path.exists(img_path):
            st.image(img_path, use_column_width=True)
        
        # Render Info
        info_path = f"md_files/INFO_{pg}.MD"
        if os.path.exists(info_path):
            with open(info_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())
            st.markdown("---")

        # Controles
        st.markdown("*idiomas disponíveis...*")
        col_l, col_ar, col_au = st.columns([6, 2, 2])
        with col_l:
            st.selectbox("lang", list(IDIOMAS.keys()), label_visibility="collapsed", key="lang_selector")
        with col_ar:
            st.session_state.draw = st.checkbox("🎨", key="chk_draw")
        with col_au:
            st.session_state.talk = st.checkbox("🔊", key="chk_talk")
        
        st.markdown("---")
        st.session_state.auto = st.checkbox("auto", key="chk_auto")
        
        st.markdown("---")
        c1, c2, c3, c4 = st.columns(4)
        c1.button("📘", key="sb_fb")
        c2.button("📸", key="sb_ig")
        c3.button("📺", key="sb_yt")
        c4.button("🐦", key="sb_tw")

# ============================================================
# 🎭 PALCO
# ============================================================
def render_palco():
    paginas = ["mini", "yPoemas", "eureka", "livros", "poly", "Sobre"]
    st.session_state.focus_page = st.radio("Foco:", paginas, index=paginas.index(st.session_state.focus_page), horizontal=True)
    st.markdown("---")

    p = st.session_state.focus_page

    if p == "mini":
        st.subheader("Mini-Machina")
        c1, c2, c3, c4, _ = st.columns([1, 1, 1, 1, 8])
        c1.button("<-", key="m_prev")
        c2.button("⭐", key="m_star")
        c3.button("->", key="m_next")
        # Help
