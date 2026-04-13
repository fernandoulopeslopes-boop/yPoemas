import streamlit as st
import os

# --- 1. BOOT: HARDWARE VIRTUAL (RESTAURO 13/ABRIL) ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    layout="wide",
    initial_sidebar_state="expanded",
)

if 'page' not in st.session_state:
    st.session_state.page = 'DEMO'

def get_md(page_name):
    """Resgate fiel do conteúdo dos arquivos INFO_*.md"""
    path = f"md_files/INFO_{page_name.upper()}.md"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "Aguardando pulso da Machina..."

# --- 2. CSS: TRADUÇÃO DA RÉGUA (SIMETRIA PERFEITA) ---
st.markdown("""
    <style>
    [data-testid="stHeader"] { display: none !important; }
    section[data-testid="stSidebar"] { min-width: 320px !important; max-width: 320px !important; }

    /* OS 5 BOTÕES QUADRADOS DA RÉGUA */
    .st-key-cmd_btn button {
        border-radius: 8px !important;
        border: 1px solid #ccc !important;
        background-color: #fff !important;
        width: 52px !important;
        height: 52px !important;
        font-size: 26px !important;
        font-weight: bold !important;
        color: #000 !important;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
    }

    /* NAV TOGGLES (ABAS DO TOPO) */
    .st-key-nav_on button { background-color: #000 !important; color: #fff !important; border-radius: 20px !important; font-weight: 900 !important; }
    .st-key-nav_off button { background-color: #f8f9fa !important; color: #888 !important; border-radius: 20px !important; font-weight: 900 !important; }

    /* SELECTBOXES DA RÉGUA (REDUÇÃO DE ALTURA PARA ALINHAMENTO) */
    div[data-testid="stSelectbox"] > div { min-height: 32px !important; }
    
    /* INFO BOX SIDEBAR */
    .info-box {
        font-family: 'Georgia', serif; font-size: 13px; line-height: 1.5;
        background: #fff; padding: 15px; border-left: 5px solid #000;
    }

    .main .block-container { max-width: 1000px !important; margin: 0 auto !important; padding-top: 2rem !important; }
    label { font-size: 10px !important; font-weight: 900 !important; text-transform: uppercase; color: #666; margin-bottom: 2px !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR: O COCKPIT ---
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    # Identidade Visual
    if os.path.exists("img_demo.jpg"):
        st.image("img_demo.jpg", use_container_width=True)
    
    st.divider()
    # Carregamento Real dos MDs (Sem lixo)
    st.markdown(f"<div class='info-box'>{get_md(st.session_state.page)}</div>", unsafe_allow_html=True)

# --- 4. PALCO CENTRAL ---

# A. NAVEGAÇÃO SUPERIOR (TOGGLE)
menu = ["Demo", "yPoemas", "Eureka", "Off-Machina", "About"]
cols_nav = st.columns(len(menu))
for i, item in enumerate(menu):
    is_active = st.session_state.page.upper() == item.upper()
    with cols_nav[i]:
        st.markdown(f"<div class='st-key-nav_{'on' if is_active else 'off'}'>", unsafe_allow_html=True)
        if st.button(item.upper(), key=f"nav_{item}"):
            st.session_state.page = item
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

# B. A RÉGUA DE COMANDO (ESPELHO DA IMAGEM)
# Bloco Superior: Os 5 Comandos
c_regua = st.columns([1, 1, 1, 1, 1, 5]) # Mantém os botões à esquerda como na foto
icons = ["＋", "＜", "＊", "＞", "？"]
for i, col in enumerate(c_regua[:5]):
    with col:
        st.markdown("<div class='st-key-cmd_btn'>", unsafe_allow_html=True)
        st.button(icons[i], key=f"cmd_{i}")
        st.markdown("</div>", unsafe_allow_html=True)

# Bloco Inferior: Seletores em Linha
st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
row_sel = st.columns([0.7, 1.5, 1.5, 2, 0.7])

with row_sel[0]: st.toggle("Arte", value=True, key="t_arte")
with row_sel[1]: 
    # Varredura real de idiomas Western ABC
    st.selectbox("Idioma", ["Português", "English", "Español", "Français", "Català"], key="s_lang")
with row_sel[2]: 
    st.selectbox("Grupo", ["Todos os Temas", "Livros"], key="s_group")
with row_sel[3]: 
    # Varredura real do acervo .ypo
    try:
        acervo = [f.replace(".ypo", "") for f in os.listdir("data") if f.endswith(".ypo")]
        st.selectbox("Tema / Livro", sorted(acervo) if acervo else ["Vazio"], key="s_tema")
    except:
        st.selectbox("Tema", ["Geral"], key="s_tema_err")
with row_sel[4]: st.toggle("Som", value=False, key="t_som")

st.divider()

# --- 5. ÁREA DE EXIBIÇÃO ---
st.markdown(f"<h1 style='text-align:center; font-family: Georgia;'>{st.session_state.page}</h1>", unsafe_allow_html=True)
