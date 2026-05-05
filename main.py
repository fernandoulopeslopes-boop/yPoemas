import streamlit as st
import os
import glob
import base64

# ============================================================
# ⚙️ CONFIGURAÇÃO DE AMBIENTE & ESTILO
# ============================================================
# Dicionário Estático conforme Guia Machina 2026
IDIOMAS = {
    "Português": "pt",
    "English": "en",
    "Español": "es",
    "Français": "fr",
    "Deutsch": "de",
    "Italiano": "it"
}

# CSS: Sidebar fixa em 300px e remoção de redundâncias visuais
st.markdown(
    "<style>"
    "section[data-testid='stSidebar'] {width: 300px !important; max-width: 300px !important; min-width: 300px !important;}"
    ".linkey-container {display: flex; justify-content: flex-end; padding-right: 5px; margin-top: -30px;}"
    ".linkey-button {background: none; border: none; padding: 0; cursor: pointer;}"
    "div.stButton > button:first-child {width: 100%;}"
    ".stSelectbox label {display: none;}"
    "</style>",
    unsafe_allow_html=True
)

# Inicialização do State
if "focus_page" not in st.session_state:
    st.session_state.focus_page = "livros"
if "lang_selector" not in st.session_state:
    st.session_state.lang_selector = "Português"

# ============================================================
# 📥 FUNÇÕES DE PROTOCOLO (PTC)
# ============================================================
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def ler_md(nome_arquivo):
    caminho = f"md_files/{nome_arquivo}"
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# ============================================================
# ⚙️ SIDEBAR: CENTRO DE CONTROLE
# ============================================================
def render_sidebar():
    with st.sidebar:
        # 1. LINKEY (Topo Direito)
        chave_base64 = get_base64_image("images/chave_dourada.png")
        if chave_base64:
            html_linkey = (
                f"<div class='linkey-container'>"
                f"<button class='linkey-button' title='Linkey'>"
                f"<img src='data:image/png;base64,{chave_base64}' width='20' height='20' style='image-rendering: pixelated;'/>"
                f"</button></div>"
            )
            st.markdown(html_linkey, unsafe_allow_html=True)
        
        # 2. SELETOR DE PÁGINA (A alma da navegação)
        paginas = ["mini", "yPoemas", "eureka", "livros", "poly", "Sobre"]
        st.session_state.focus_page = st.selectbox(
            "Página em Foco", paginas, 
            index=paginas.index(st.session_state.focus_page),
            key="page_nav"
        )
        st.markdown("---")

        # 3. IDIOMAS (Dropdown oficial)
        st.markdown("*idiomas disponíveis...*")
        st.selectbox("Idiomas", list(IDIOMAS.keys()), key="lang_selector")

        # 4. BOTÕES [ARTE] E [ÁUDIO]
        col_art, col_aud = st.columns(2)
        with col_art:
            st.button("🎨 [arte]", key="btn_arte")
        with col_aud:
            st.button("🔊 [audio]", key="btn_audio")
        
        st.markdown("---")

        # 5. TEXTO INFO_PAGINA.MD
        pg = st.session_state.focus_page
        info_text = ler_md(f"INFO_{pg}.MD")
        if info_text:
            st.markdown(info_text)
            st.markdown("---")

        # 6. IMAGEM img_PAGINA.JPG
        img_path = f"images/img_{pg}.JPG"
        if os.path.exists(img_path):
            st.image(img_path, use_column_width=True)

# ============================================================
# 🎭 O PALCO: COMPONENTES ESPECÍFICOS
# ============================================================
def render_palco():
    pg = st.session_state.focus_page

    # 1. MINI
    if pg == "mini":
        c1, c2, c3, c4, _ = st.columns([1, 1, 1, 1, 8])
        c1.button("<-", key="m_prev")
        c2.button("⭐", key="m_star")
        c3.button("->", key="m_next")
        c4.button("?", key="m_help", help=ler_md("help_ypoemas.md"))
        st.write("---")

    # 2. YPOEMAS
    elif pg == "yPoemas":
        c1, c2, c3, c4, _ = st.columns([1, 1, 1, 1, 8])
        c1.button("<-", key="y_prev")
        c2.button("⭐", key="y_star")
        c3.button("->", key="y_next")
        c4.button("?", key="y_help", help=ler_md("HELP_YPOEMAS.MD"))
        st.write("---")

    # 3. EUREKA
    elif pg == "eureka":
        find_what = st.text_input("find_what", placeholder="O que busca?", label_visibility="collapsed")
        c1, c2, c3, _ = st.columns([1, 1, 1, 9])
        c1.button("+", key="e_plus")
        c2.button("⭐", key="e_star")
        c3.button("?", key="e_help", help=ler_md("HELP_EUREKA.MD"))
        st.write("---")

    # 4. LIVROS
    elif pg == "livros":
        pasta = "md_files"
        arquivos = [f for f in os.listdir(pasta) if f.endswith(".MD") and "_" not in f]
        if arquivos:
            livro_sel = st.selectbox("Livros", arquivos, key="sel_livros")
            c1, c2, c3, c4, c5, _ = st.columns([1, 1, 1, 1, 1, 7])
            c1.button("<-", key="l_prev")
            c2.button("⭐", key="l_star")
            c3.button("->", key="l_next")
            c4.button("❤️", key="l_heart")
            c5.button("?", key="l_help", help=ler_md("HELP_OFF-MACHINA.MD"))
            st.write("---")
            st.markdown(ler_md(livro_sel))

    # 5. POLY
    elif pg == "poly":
        c1, c2, _ = st.columns([1, 1, 10])
        c1.button("❤️", key="p_heart", help="temas mais lidos")
        c2.button("?", key="p_help", help=ler_md("HELP_POLY.MD"))
        st.write("---")

    # 6. SOBRE
    elif pg == "Sobre":
        abouts = glob.glob("md_files/ABOUT_*.MD")
        if abouts:
            mapa = {os.path.basename(a)[6:-3]: os.path.basename(a) for a in abouts}
            sub_sel = st.selectbox("Sobre", list(mapa.keys()), key="sel_about")
            st.write("---")
            st.markdown(ler_md(mapa[sub_sel]))

# ============================================================
# EXECUÇÃO
# ============================================================
render_sidebar()
render_palco()
