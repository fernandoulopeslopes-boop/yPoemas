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

# 2. INJEÇÃO DE CSS (Versão compatível com Python 3.14)
# Evitando as aspas triplas dentro do st.markdown para prevenir o erro de metrics_util
css_style = "<style>section[data-testid='stSidebar'] {width: 300px !important; max-width: 300px !important; min-width: 300px !important;} .linkey-container {display: flex; justify-content: flex-end; padding-right: 5px;} .linkey-button {background: none; border: none; padding: 0; cursor: pointer;}</style>"
st.write(css_style, unsafe_with_html=True)

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
        # Linkey
        chave_base64 = get_base64_image("images/chave_dourada.png")
        if chave_base64:
            html_linkey = f"<div class='linkey-container'><button class='linkey-button'><img src='data:image/png;base64,{chave_base64}' width='20' height='20' style='image-rendering: pixelated;'/></button></div>"
            st.write(html_linkey, unsafe_with_html=True)
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
        # Help conforme Guia: help_ypoemas.md (minúsculo nesta página)
        if c4.button("?", key="m_h"):
            st.help("md_files/help_ypoemas.md")

    elif p == "yPoemas":
        st.subheader("yPoemas")
        c1, c2, c3, c4, _ = st.columns([1, 1, 1, 1, 8])
        c1.button("<-", key="y_prev")
        c2.button("⭐", key="y_star")
        c3.button("->", key="y_next")
        if c4.button("?", key="y_h"):
            st.help("md_files/HELP_YPOEMAS.MD")

    elif p == "eureka":
        st.subheader("Eureka")
        st.text_input("Find what:", key="find_what", label_visibility="collapsed")
        c1, c2, c3, _ = st.columns([1, 1, 1, 9])
        c1.button("+", key="e_plus")
        c2.button("⭐", key="e_star")
        if c3.button("?", key="e_h"):
            st.help("md_files/HELP_EUREKA.MD")

    elif p == "livros":
        st.subheader("Biblioteca Off-Machina")
        files = [f for f in os.listdir("md_files") if f.endswith(".MD") and "_" not in f] if os.path.exists("md_files") else []
        if files:
            sel = st.selectbox("Livro:", files, label_visibility="collapsed", key="s_liv")
            c1, c2, c3, c4, c5, _ = st.columns([1, 1, 1, 1, 1, 7])
            c1.button("<-", key="l_prev")
            c2.button("⭐", key="l_star")
            c3.button("->", key="l_next")
            c4.button("❤️", key="l_heart")
            if c5.button("?", key="l_h"):
                st.help("md_files/HELP_OFF-MACHINA.MD")
            st.markdown("---")
            with open(f"md_files/{sel}", "r", encoding="utf-8") as f:
                st.markdown(f.read())

    elif p == "poly":
        st.subheader("Modo Poliglota")
        files = [f for f in os.listdir("md_files") if f.endswith(".MD") and "_" not in f]
        if files:
            sel = st.selectbox("Texto:", files, label_visibility="collapsed", key="s_poly")
            c1, c2, _ = st.columns([1, 1, 10])
            c1.button("❤️", key="p_heart", help="temas mais lidos")
            if c2.button("?", key="p_h"):
                st.help("md_files/HELP_POLY.MD")
            st.markdown("---")
            with open(f"md_files/{sel}", "r", encoding="utf-8") as f:
                st.markdown(f.read())

    elif p == "Sobre":
        st.subheader("Sobre a Machina")
        abouts = glob.glob("md_files/ABOUT_*.MD")
        if abouts:
            mapa = {os.path.basename(a)[6:-3]: a for a in abouts}
            sel = st.selectbox("Sessão:", list(mapa.keys()), label_visibility="collapsed", key="s_ab")
            st.markdown("---")
            with open(mapa[sel], "r", encoding="utf-8") as f:
                st.markdown(f.read())

render_sidebar()
render_palco()
