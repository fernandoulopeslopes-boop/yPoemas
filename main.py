import streamlit as st
import os

# --- 1. BOOT: DEFINIÇÃO DO HARDWARE ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Estado inicial do sistema
if 'page' not in st.session_state:
    st.session_state.page = 'Demo'

# --- 2. BASTIDORES: A FUNÇÃO DE RESGATE (CLEAN) ---
def get_md(p):
    """
    Entendi: esta função é o pulso que sincroniza a sidebar com o palco.
    Busca na pasta md_files o arquivo INFO_ correspondente à página.
    """
    path = f"md_files/INFO_{p.upper()}.md"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# --- 3. CSS: O FIRMWARE VISUAL (SEM VÍRGULA FORA DO LUGAR) ---
st.markdown("""<style>
    [data-testid="stHeader"] {display: none !important;}
    
    /* SIDEBAR: BLINDAGEM DE 300PX */
    section[data-testid="stSidebar"] {
        min-width: 300px !important;
        max-width: 300px !important;
    }

    /* NAV: BOTÕES ARREDONDADOS SIMÉTRICOS */
    .stButton>button {
        width: 100% !important;
        height: 42px !important;
        border-radius: 20px !important;
        font-weight: 900 !important;
        font-size: 11px !important;
        text-transform: uppercase;
    }
    .st-key-on button {background-color: #000 !important; color: #fff !important;}
    .st-key-off button {background-color: #f8f9fa !important; color: #888 !important; border: 1px solid #eee !important;}
    
    /* RÉGUA: OS 5 QUADRADOS DO PAINEL */
    .st-key-cmd button {
        border-radius: 8px !important;
        width: 52px !important;
        height: 52px !important;
        font-size: 24px !important;
        font-weight: 900 !important;
        background: #fff !important;
        border: 1px solid #ccc !important;
    }

    /* INFO BOX (GEORGIA) */
    .info-box {
        font-family: 'Georgia', serif;
        font-size: 13px;
        line-height: 1.6;
        padding: 15px;
        border-left: 5px solid #000;
        background: #fff;
    }

    .main .block-container {max-width: 1100px !important; margin: 0 auto !important;}
</style>""", unsafe_allow_html=True)

# --- 4. SIDEBAR: O COCKPIT ---
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    langs = ["Português", "Español", "English", "Français", "Italiano", "Català", "German", "Latin"]
    st.selectbox("🌐 IDIOMA", langs, key="sb_lang")
    
    st.divider()
    
    if os.path.exists("img_demo.jpg"):
        st.image("img_demo.jpg", use_container_width=True)
    
    st.divider()
    
    # Injeção direta do conteúdo MD sem filtros desnecessários
    st.markdown(f"<div class='info-box'>{get_md(st.session_state.page)}</div>", unsafe_allow_html=True)

# --- 5. PALCO: NAVEGAÇÃO (6 COLUNAS IGUAIS) ---
menu = ["Demo", "yPoemas", "Eureka", "Off-Machina", "Comments", "About"]
cols_nav = st.columns(6)

for i, item in enumerate(menu):
    with cols_nav[i]:
        tag = 'on' if st.session_state.page == item else 'off'
        st.markdown(f"<div class='st-key-{tag}'>", unsafe_allow_html=True)
        if st.button(item, key=f"nav_{i}"):
            st.session_state.page = item
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# --- 6. RÉGUA DE COMANDO (A GEOMETRIA DO YPO_SEGURO) ---
c1 = st.columns([1, 1, 1, 1, 1, 7.5])
icones = ["＋", "＜", "＊", "＞", "？"]
for i, icone in enumerate(icones):
    with c1[i]:
        st.markdown("<div class='st-key-cmd'>", unsafe_allow_html=True)
        st.button(icone, key=f"cmd_{i}")
        st.markdown("</div>", unsafe_allow_html=True)

st.write("") # Espaço rítmico

# SELETORES (ESTRUTURA DE COLUNAS DO DESENHO ORIGINAL)
c2 = st.columns([1.1, 1.4, 1.8, 2, 1.1])

with c2[0]: # ARTE
    t1, t2 = st.columns([1, 2])
    t1.toggle("A", value=True, key="t_a", label_visibility="collapsed")
    t2.markdown("**ARTE**")

with c2[1]: # IDIOMA RÉGUA
    st.selectbox("L", langs[:3], key="s_l", label_visibility="collapsed")

with c2[2]: # GRUPO
    # Varredura direta da pasta base
    grupos = sorted([f[4:-4] for f in os.listdir("base") if f.startswith("rol_")])
    g_sel = st.selectbox("G", grupos, key="s_g", label_visibility="collapsed")

with c2[3]: # TEMA
    # Leitura direta do arquivo correspondente
    path_txt = f"base/rol_{g_sel}.txt"
    temas = open(path_txt, "r", encoding="utf-8").read().splitlines()
    st.selectbox("T", temas, key="s_t", label_visibility="collapsed")

with c2[4]: # SOM
    t3, t4 = st.columns([1, 2])
    t3.toggle("S", key="t_s", label_visibility="collapsed")
    t4.markdown("**SOM**")

st.divider()

# --- 7. DISPLAY: IDENTIDADE DA PÁGINA ---
st.markdown(f"<h1 style='text-align: center; font-family: Georgia;'>{st.session_state.page}</h1>", unsafe_allow_html=True)
