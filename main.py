import streamlit as st
import os

# --- 1. BOOT: HARDWARE VIRTUAL (SIMETRIA ABSOLUTA) ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    layout="wide",
    initial_sidebar_state="expanded",
)

if 'page' not in st.session_state:
    st.session_state.page = 'Demo'

def get_md_content(page_name):
    """Resgate fiel do conteúdo dos arquivos INFO_ na pasta md_files"""
    try:
        path = f"md_files/INFO_{page_name.upper()}.md"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
    except: pass
    return "Aguardando pulso da Machina..."

# --- 2. CSS: BLINDAGEM DO CHASSI (320px) E IDENTIDADE VISUAL ---
st.markdown("""
    <style>
    /* REMOVER LIXO NATIVO */
    [data-testid="stHeader"] { display: none !important; }
    
    /* SIDEBAR: CHASSI DE PRECISÃO */
    section[data-testid="stSidebar"] {
        min-width: 320px !important;
        max-width: 320px !important;
        background-color: #fcfcfc !important;
        border-right: 1px solid #e0e0e0 !important;
    }

    /* BOTÕES DE NAVEGAÇÃO: SIMETRIA DE GRID (TAMANHOS IGUAIS) */
    .stButton > button {
        width: 100% !important;
        height: 45px !important;
        border-radius: 20px !important;
        font-weight: 900 !important;
        font-size: 11px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .st-key-nav_on button {
        background-color: #000 !important;
        color: #fff !important;
        border: 2px solid #000 !important;
    }
    .st-key-nav_off button {
        background-color: #f8f9fa !important;
        color: #888 !important;
        border: 1px solid #ddd !important;
    }

    /* RÉGUA DE COMANDO: OS 5 QUADRADOS DO PAINEL */
    .st-key-cmd_btn button {
        border-radius: 8px !important;
        border: 1px solid #bbb !important;
        background-color: #fff !important;
        width: 52px !important;
        height: 52px !important;
        font-size: 26px !important;
        font-weight: 900 !important;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05) !important;
    }

    /* INFO BOX (GEORGIA CLASSIC) */
    .info-box {
        font-family: 'Georgia', serif; font-size: 14px; line-height: 1.6;
        color: #1a1a1a; background: #fff; padding: 18px; 
        border-left: 6px solid #000; box-shadow: inset 0 0 10px rgba(0,0,0,0.02);
    }

    /* CENTRALIZAÇÃO DO PALCO PRINCIPAL */
    .main .block-container { max-width: 1100px !important; padding-top: 2rem !important; }
    div[data-testid="stHorizontalBlock"] { align-items: center !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR: O COCKPIT ---
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # IDIOMAS: Radical Western ABC
    idiomas_elite = ["Português", "Español", "English", "Français", "Italiano", "Català", "German", "Latin"]
    st.selectbox("🌐 IDIOMA", idiomas_elite, key="sb_lang")
    
    st.divider()

    # ARTE DA PÁGINA (CAPA)
    if os.path.exists("img_demo.jpg"):
        st.image("img_demo.jpg", use_container_width=True)
    
    st.divider()

    # INFO BOX (CONTEÚDO DINÂMICO DOS .MD)
    st.markdown(f"<div class='info-box'>{get_md_content(st.session_state.page)}</div>", unsafe_allow_html=True)

# --- 4. PALCO CENTRAL: NAVEGAÇÃO SUPERIOR (6 ABAS) ---
menu = ["Demo", "yPoemas", "Eureka", "Off-Machina", "Comments", "About"]
cols_nav = st.columns(len(menu))

for i, item in enumerate(menu):
    active = st.session_state.page == item
    tag = "nav_on" if active else "nav_off"
    with cols_nav[i]:
        st.markdown(f"<div class='st-key-{tag}'>", unsafe_allow_html=True)
        if st.button(item, key=f"nav_{item}", use_container_width=True):
            st.session_state.page = item
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# --- 5. A RÉGUA DE COMANDO (FIM DA PREGUIÇA DE DADOS) ---

# Linha 1: Os 5 Botões de Ação
c_cmd = st.columns([1, 1, 1, 1, 1, 7.5])
icons = ["＋", "＜", "＊", "＞", "？"]
for i, col in enumerate(c_cmd[:5]):
    with col:
        st.markdown("<div class='st-key-cmd_btn'>", unsafe_allow_html=True)
        st.button(icons[i], key=f"cmd_{i}")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)

# Linha 2: Seletores (Varredura Automática da pasta \base)
row_sel = st.columns([1.1, 1.4, 1.8, 2, 1.1])

# ARTE
with row_sel[0]:
    c_t, c_l = st.columns([1, 2])
    c_t.toggle("Toggle_Arte", value=True, key="t_arte", label_visibility="collapsed")
    c_l.markdown("<span style='font-size:13px; font-weight:900;'>ARTE</span>", unsafe_allow_html=True)

# IDIOMA DA RÉGUA
with row_sel[1]:
    st.selectbox("Regua_Lang", idiomas_elite[:3], key="s_lang", label_visibility="collapsed")

# GRUPO: Varredura dos arquivos rol_*.txt enviados
with row_sel[2]:
    try:
        # Pega a lista real de grupos (ensaios, poemas, sociais, etc)
        grupos_disponiveis = [f.replace("rol_", "").replace(".txt", "") for f in os.listdir("base") if f.startswith("rol_")]
        grupo_selecionado = st.selectbox("Regua_Grupo", sorted(grupos_disponiveis), key="s_group", label_visibility="collapsed")
    except:
        grupo_selecionado = "todos os temas"
        st.selectbox("Regua_Grupo", ["todos os temas"], key="s_group_err", label_visibility="collapsed")

# TEMA: Leitura dinâmica do arquivo de grupo selecionado
with row_sel[3]:
    try:
        path_txt = f"base/rol_{grupo_selecionado}.txt"
        with open(path_txt, "r", encoding="utf-8") as f:
            lista_temas = [linha.strip() for linha in f.readlines() if linha.strip()]
        st.selectbox("Regua_Tema", lista_temas, key="s_tema", label_visibility="collapsed")
    except:
        st.selectbox("Regua_Tema", ["Amaré"], key="s_tema_err", label_visibility="collapsed")

# SOM
with row_sel[4]:
    c_t_s, c_l_s = st.columns([1, 2])
    c_t_s.toggle("Toggle_Som", value=False, key="t_som", label_visibility="collapsed")
    c_l_s.markdown("<span style='font-size:13px; font-weight:900;'>SOM</span>", unsafe_allow_html=True)

st.divider()

# --- 6. DISPLAY CENTRAL ---
st.markdown(f"<h1 style='text-align: center; font-family: Georgia;'>{st.session_state.page}</h1>", unsafe_allow_html=True)
