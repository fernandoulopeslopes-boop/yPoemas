import streamlit as st
import os

# --- 1. CONFIGURAÇÃO DE HARDWARE (RESTAURO RIGOROSO) ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Bússola de Estado
if 'page' not in st.session_state:
    st.session_state.page = 'DEMO'

def get_md_safe(page_name):
    """Leitura direta do acervo INFO_*.md em md_files"""
    try:
        path = f"md_files/INFO_{page_name.upper()}.md"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
    except:
        pass
    return "Aguardando pulso da Machina..."

# --- 2. CSS: ARQUITETURA DE SIMETRIA (LAST_SCREENSHOT) ---
st.markdown("""
    <style>
    /* ELIMINA LIXO NATIVO */
    [data-testid="stHeader"] { display: none !important; }
    
    /* SIDEBAR BLINDADA (310px - 320px) */
    section[data-testid="stSidebar"] {
        min-width: 310px !important;
        max-width: 310px !important;
        background-color: #fcfcfc !important;
        border-right: 1px solid #eee !important;
    }

    /* NAV TOGGLES: ABAS CENTRALIZADAS */
    .st-key-nav_on button {
        background-color: #000 !important;
        color: #fff !important;
        border-radius: 20px !important;
        font-weight: 900 !important;
        height: 40px !important;
    }
    .st-key-nav_off button {
        background-color: #f8f9fa !important;
        color: #888 !important;
        border: 1px solid #ddd !important;
        border-radius: 20px !important;
        font-weight: 900 !important;
        height: 40px !important;
    }

    /* A RÉGUA: OS 5 BOTÕES QUADRADOS DA IMAGEM */
    .st-key-cmd_btn button {
        border-radius: 8px !important;
        border: 1px solid #ccc !important;
        background-color: #fff !important;
        width: 52px !important;
        height: 52px !important;
        font-size: 26px !important;
        font-weight: 900 !important;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.1) !important;
    }

    /* INFO BOX: ESTÉTICA DICIONÁRIO GEORGIA */
    .info-box {
        font-family: 'Georgia', serif;
        font-size: 13px;
        line-height: 1.6;
        color: #1a1a1a;
        background: #fff;
        padding: 15px;
        border-left: 5px solid #000;
        margin-top: 10px;
    }

    /* CONTAINER DO PALCO */
    .main .block-container { 
        max-width: 950px !important; 
        margin: 0 auto !important; 
        padding-top: 2rem !important; 
    }
    
    /* ALINHAMENTO DAS SELECTBOXES E TOGGLES */
    div[data-testid="stHorizontalBlock"] { align-items: center !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR: O COCKPIT ---
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # IDIOMA: Radical Western ABC
    langs = ["Português", "Español", "English", "Français", "Italiano", "Català", "Latin"]
    st.selectbox("🌐 IDIOMA", langs, key="sb_lang")
    
    st.divider()

    # ARTE DA PÁGINA (CAPA)
    if os.path.exists("img_demo.jpg"):
        st.image("img_demo.jpg", use_container_width=True)
    
    st.divider()

    # INFO BOX (CONTEÚDO REAL DOS .md)
    content = get_md_safe(st.session_state.page)
    st.markdown(f"<div class='info-box'>{content}</div>", unsafe_allow_html=True)

# --- 4. PALCO CENTRAL: NAVEGAÇÃO SUPERIOR ---
menu = ["Demo", "yPoemas", "Eureka", "Off-Machina", "About"]
cols_nav = st.columns(len(menu))

for i, item in enumerate(menu):
    is_active = st.session_state.page == item
    style = "nav_on" if is_active else "nav_off"
    with cols_nav[i]:
        st.markdown(f"<div class='st-key-{style}'>", unsafe_allow_html=True)
        if st.button(item.upper(), key=f"nav_{item}"):
            st.session_state.page = item
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# --- 5. A RÉGUA DE COMANDO (SIMETRIA ABSOLUTA) ---

# Linha 1: Comandos (Os 5 Quadrados)
c1, c2, c3, c4, c5, _ = st.columns([1, 1, 1, 1, 1, 6])
icons = ["＋", "＜", "＊", "＞", "？"]
for i, col in enumerate([c1, c2, c3, c4, c5]):
    with col:
        st.markdown("<div class='st-key-cmd_btn'>", unsafe_allow_html=True)
        st.button(icons[i], key=f"cmd_{i}")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

# Linha 2: Seletores (Alinhamento Horizontal como na Last Screenshot)
row_sel = st.columns([1, 1.5, 1.5, 2, 1])

# Arte
with row_sel[0]:
    c_t, c_l = st.columns([1, 2])
    c_t.toggle("", value=True, key="t_arte", label_visibility="collapsed")
    c_l.markdown("<span style='font-size:12px; font-weight:900;'>ARTE</span>", unsafe_allow_html=True)

# Idioma
with row_sel[1]:
    st.selectbox("Idioma", ["Português", "English", "Español"], key="s_lang", label_visibility="collapsed")

# Grupo
with row_sel[2]:
    st.selectbox("Grupo", ["todos os temas", "livros"], key="s_group", label_visibility="collapsed")

# Tema (Varredura do acervo real)
with row_sel[3]:
    try:
        acervo = [f.replace(".ypo", "") for f in os.listdir("data") if f.endswith(".ypo")]
        st.selectbox("Tema", sorted(acervo) if acervo else ["Geral"], key="s_tema", label_visibility="collapsed")
    except:
        st.selectbox("Tema", ["Check data/"], key="s_tema_err", label_visibility="collapsed")

# Som
with row_sel[4]:
    c_t_s, c_l_s = st.columns([1, 2])
    c_t_s.toggle("", value=False, key="t_som", label_visibility="collapsed")
    c_l_s.markdown("<span style='font-size:12px; font-weight:900;'>SOM</span>", unsafe_allow_html=True)

st.divider()

# --- 6. DISPLAY ---
st.markdown(f"<h1 style='text-align: center; font-family: Georgia;'>{st.session_state.page}</h1>", unsafe_allow_html=True)
