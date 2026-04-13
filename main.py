import streamlit as st
import os

# --- 1. BOOT: FORÇANDO A EXISTÊNCIA DA SIDEBAR ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    layout="wide",
    initial_sidebar_state="expanded", # FORÇA ABERTURA
)

if 'page' not in st.session_state:
    st.session_state.page = 'Demo'

def get_md_content(page_name):
    """Resgate real do conteúdo dos arquivos INFO_*.md"""
    path = f"md_files/INFO_{page_name.upper()}.md"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "Aguardando pulso da Machina..."

# --- 2. CSS: BLINDAGEM E SIMETRIA (LAST_SCREENSHOT) ---
st.markdown("""
    <style>
    /* REMOVER HEADER E AJUSTAR MARGENS */
    [data-testid="stHeader"] { display: none !important; }
    
    /* SIDEBAR: FORÇA A LARGURA DE 320PX E A VISIBILIDADE */
    section[data-testid="stSidebar"] {
        min-width: 320px !important;
        max-width: 320px !important;
        border-right: 1px solid #ddd !important;
    }

    /* NAV BUTTONS: TODOS COM A MESMA LARGURA (GRID 1/6) */
    .stButton > button {
        width: 100% !important;
        height: 42px !important;
        border-radius: 20px !important;
        font-weight: 900 !important;
        font-size: 11px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* RÉGUA: BOTÕES QUADRADOS */
    .st-key-cmd_btn button {
        border-radius: 8px !important;
        border: 1px solid #ccc !important;
        background-color: #fff !important;
        width: 52px !important;
        height: 52px !important;
        font-size: 24px !important;
        font-weight: 900 !important;
    }

    /* INFO BOX: GEORGIA */
    .info-box {
        font-family: 'Georgia', serif; font-size: 13px; line-height: 1.6;
        background: #fff; padding: 15px; border-left: 5px solid #000;
    }

    /* ALINHAMENTO GERAL */
    div[data-testid="stHorizontalBlock"] { align-items: center !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR: O COCKPIT ---
with st.sidebar:
    st.write(" ") # Espaçador para evitar colapso
    
    idiomas = ["Português", "Español", "English", "Français", "Italiano", "Català", "German", "Latin"]
    st.selectbox("🌐 IDIOMA", idiomas, key="sb_lang")
    
    st.divider()
    
    if os.path.exists("img_demo.jpg"):
        st.image("img_demo.jpg", use_container_width=True)
    
    st.divider()
    
    st.markdown(f"<div class='info-box'>{get_md_content(st.session_state.page)}</div>", unsafe_allow_html=True)

# --- 4. NAV: BOTÕES ALINHADOS À ESQUERDA (GRID SIMÉTRICO) ---
menu = ["Demo", "yPoemas", "Eureka", "Off-Machina", "Comments", "About"]
cols_nav = st.columns(len(menu))

for i, item in enumerate(menu):
    is_active = st.session_state.page == item
    # Estilo via key para o CSS capturar
    tag = "nav_on" if is_active else "nav_off"
    with cols_nav[i]:
        st.markdown(f"<div class='st-key-{tag}'>", unsafe_allow_html=True)
        if st.button(item, key=f"nav_{item}", use_container_width=True):
            st.session_state.page = item
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# --- 5. RÉGUA DE COMANDO (FIM DA PREGUIÇA DE LISTAS) ---

# Linha 1: 5 Quadrados
c_cmd = st.columns([1, 1, 1, 1, 1, 8])
icons = ["＋", "＜", "＊", "＞", "？"]
for i, col in enumerate(c_cmd[:5]):
    with col:
        st.markdown("<div class='st-key-cmd_btn'>", unsafe_allow_html=True)
        st.button(icons[i], key=f"cmd_{i}")
        st.markdown("</div>", unsafe_allow_html=True)

st.write("") # Espaçador horizontal

# Linha 2: Os Seletores
row_sel = st.columns([1, 1.5, 1.8, 2, 1])

with row_sel[0]:
    c_t, c_l = st.columns([1, 2])
    c_t.toggle("A", value=True, key="t_arte", label_visibility="collapsed")
    c_l.markdown("<b style='font-size:12px;'>ARTE</b>", unsafe_allow_html=True)

with row_sel[1]:
    st.selectbox("L", idiomas[:3], key="s_lang", label_visibility="collapsed")

with row_sel[2]:
    # VARREDURA REAL DA PASTA \BASE
    try:
        grupos = [f.replace("rol_", "").replace(".txt", "") for f in os.listdir("base") if f.startswith("rol_")]
        st.selectbox("G", sorted(grupos), key="s_group", label_visibility="collapsed")
    except:
        st.selectbox("G", ["base/ error"], key="s_group_err", label_visibility="collapsed")

with row_sel[3]:
    # LEITURA DO ARQUIVO SELECIONADO
    try:
        with open(f"base/rol_{st.session_state.s_group}.txt", "r", encoding="utf-8") as f:
            temas = [l.strip() for l in f.readlines() if l.strip()]
        st.selectbox("T", temas, key="s_tema", label_visibility="collapsed")
    except:
        st.selectbox("T", ["..."], key="s_tema_err", label_visibility="collapsed")

with row_sel[4]:
    c_t_s, c_l_s = st.columns([1, 2])
    c_t_s.toggle("S", value=False, key="t_som", label_visibility="collapsed")
    c_l_s.markdown("<b style='font-size:12px;'>SOM</b>", unsafe_allow_html=True)

st.divider()

# --- 6. DISPLAY ---
st.markdown(f"<h1 style='text-align:center; font-family:Georgia;'>{st.session_state.page}</h1>", unsafe_allow_html=True)import streamlit as st
import os

# --- 1. BOOT: FORÇANDO A EXISTÊNCIA DA SIDEBAR ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    layout="wide",
    initial_sidebar_state="expanded", # FORÇA ABERTURA
)

if 'page' not in st.session_state:
    st.session_state.page = 'Demo'

def get_md_content(page_name):
    """Resgate real do conteúdo dos arquivos INFO_*.md"""
    path = f"md_files/INFO_{page_name.upper()}.md"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "Aguardando pulso da Machina..."

# --- 2. CSS: BLINDAGEM E SIMETRIA (LAST_SCREENSHOT) ---
st.markdown("""
    <style>
    /* REMOVER HEADER E AJUSTAR MARGENS */
    [data-testid="stHeader"] { display: none !important; }
    
    /* SIDEBAR: FORÇA A LARGURA DE 320PX E A VISIBILIDADE */
    section[data-testid="stSidebar"] {
        min-width: 320px !important;
        max-width: 320px !important;
        border-right: 1px solid #ddd !important;
    }

    /* NAV BUTTONS: TODOS COM A MESMA LARGURA (GRID 1/6) */
    .stButton > button {
        width: 100% !important;
        height: 42px !important;
        border-radius: 20px !important;
        font-weight: 900 !important;
        font-size: 11px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* RÉGUA: BOTÕES QUADRADOS */
    .st-key-cmd_btn button {
        border-radius: 8px !important;
        border: 1px solid #ccc !important;
        background-color: #fff !important;
        width: 52px !important;
        height: 52px !important;
        font-size: 24px !important;
        font-weight: 900 !important;
    }

    /* INFO BOX: GEORGIA */
    .info-box {
        font-family: 'Georgia', serif; font-size: 13px; line-height: 1.6;
        background: #fff; padding: 15px; border-left: 5px solid #000;
    }

    /* ALINHAMENTO GERAL */
    div[data-testid="stHorizontalBlock"] { align-items: center !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR: O COCKPIT ---
with st.sidebar:
    st.write(" ") # Espaçador para evitar colapso
    
    idiomas = ["Português", "Español", "English", "Français", "Italiano", "Català", "German", "Latin"]
    st.selectbox("🌐 IDIOMA", idiomas, key="sb_lang")
    
    st.divider()
    
    if os.path.exists("img_demo.jpg"):
        st.image("img_demo.jpg", use_container_width=True)
    
    st.divider()
    
    st.markdown(f"<div class='info-box'>{get_md_content(st.session_state.page)}</div>", unsafe_allow_html=True)

# --- 4. NAV: BOTÕES ALINHADOS À ESQUERDA (GRID SIMÉTRICO) ---
menu = ["Demo", "yPoemas", "Eureka", "Off-Machina", "Comments", "About"]
cols_nav = st.columns(len(menu))

for i, item in enumerate(menu):
    is_active = st.session_state.page == item
    # Estilo via key para o CSS capturar
    tag = "nav_on" if is_active else "nav_off"
    with cols_nav[i]:
        st.markdown(f"<div class='st-key-{tag}'>", unsafe_allow_html=True)
        if st.button(item, key=f"nav_{item}", use_container_width=True):
            st.session_state.page = item
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# --- 5. RÉGUA DE COMANDO (FIM DA PREGUIÇA DE LISTAS) ---

# Linha 1: 5 Quadrados
c_cmd = st.columns([1, 1, 1, 1, 1, 8])
icons = ["＋", "＜", "＊", "＞", "？"]
for i, col in enumerate(c_cmd[:5]):
    with col:
        st.markdown("<div class='st-key-cmd_btn'>", unsafe_allow_html=True)
        st.button(icons[i], key=f"cmd_{i}")
        st.markdown("</div>", unsafe_allow_html=True)

st.write("") # Espaçador horizontal

# Linha 2: Os Seletores
row_sel = st.columns([1, 1.5, 1.8, 2, 1])

with row_sel[0]:
    c_t, c_l = st.columns([1, 2])
    c_t.toggle("A", value=True, key="t_arte", label_visibility="collapsed")
    c_l.markdown("<b style='font-size:12px;'>ARTE</b>", unsafe_allow_html=True)

with row_sel[1]:
    st.selectbox("L", idiomas[:3], key="s_lang", label_visibility="collapsed")

with row_sel[2]:
    # VARREDURA REAL DA PASTA \BASE
    try:
        grupos = [f.replace("rol_", "").replace(".txt", "") for f in os.listdir("base") if f.startswith("rol_")]
        st.selectbox("G", sorted(grupos), key="s_group", label_visibility="collapsed")
    except:
        st.selectbox("G", ["base/ error"], key="s_group_err", label_visibility="collapsed")

with row_sel[3]:
    # LEITURA DO ARQUIVO SELECIONADO
    try:
        with open(f"base/rol_{st.session_state.s_group}.txt", "r", encoding="utf-8") as f:
            temas = [l.strip() for l in f.readlines() if l.strip()]
        st.selectbox("T", temas, key="s_tema", label_visibility="collapsed")
    except:
        st.selectbox("T", ["..."], key="s_tema_err", label_visibility="collapsed")

with row_sel[4]:
    c_t_s, c_l_s = st.columns([1, 2])
    c_t_s.toggle("S", value=False, key="t_som", label_visibility="collapsed")
    c_l_s.markdown("<b style='font-size:12px;'>SOM</b>", unsafe_allow_html=True)

st.divider()

# --- 6. DISPLAY ---
st.markdown(f"<h1 style='text-align:center; font-family:Georgia;'>{st.session_state.page}</h1>", unsafe_allow_html=True)
