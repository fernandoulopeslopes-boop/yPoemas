import os
import streamlit as st
import random

### bof: settings

st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="wide",
    initial_sidebar_state="auto",
)

# Inicialização de Estados
if "page" not in st.session_state: st.session_state.page = "mini"
if "poly_name" not in st.session_state: st.session_state.poly_name = "català"

# Regra 0: Look & Feel (Palco Elástico e Blindado)
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    .main .block-container { 
        max-width: 98% !important; 
        padding-top: 1.5rem !important; 
        padding-left: 2rem !important; 
        padding-right: 2rem !important; 
        margin: 0 auto !important;
    }
    [data-testid="stMainViewContainer"] { width: 100% !important; }
    [data-testid="stSidebar"] { width: 240px !important; min-width: 240px !important; background-color: #fafafa; }
    
    /* Navegação 111px */
    [data-testid="stHorizontalBlock"] { display: flex !important; flex-wrap: nowrap !important; gap: 8px !important; }
    [data-testid="column"] { flex: 0 0 auto !important; width: 115px !important; }
    div.stButton > button {
        width: 111px !important; border-radius: 12px; height: 3.2em;
        background-color: #ffffff; border: 1px solid #d1d5db; font-size: 11px;
    }

    /* Limpeza e Centralização Sidebar */
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"], 
    [data-testid="stSidebar"] button[title="View help"] { display: none !important; }
    [data-testid="stSidebarContent"] [data-testid="stHorizontalBlock"] { justify-content: center !important; gap: 15px !important; }

    /* Estética Mini (ypo_old Spirit) */
    .mini-card {
        font-family: 'IBM Plex Serif', serif;
        font-size: 1.7rem;
        line-height: 1.8;
        color: #1a1a1a;
        text-align: center;
        padding: 80px 40px;
        background: #fff;
        border-radius: 30px;
        border: 1px solid #f0f0f0;
        box-shadow: 0 20px 40px rgba(0,0,0,0.02);
        max-width: 700px;
        margin: 40px auto;
    }
    </style> """,
    unsafe_allow_html=True,
)

### bof: logic (O Motor do ypo_old)

def carregar_banco(arquivo="ovny_data.txt"):
    """Puxa a base bruta do projeto de 5 anos"""
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            return [linha.strip() for linha in f.readlines() if linha.strip()]
    return ["a máquina aguarda dados...", "ovny_data.txt não encontrado", "reponha o combustível"]

def gerar_poema_mini():
    """Lógica Mini: 3 linhas, todos os temas, puro sorteio"""
    banco = carregar_banco()
    if len(banco) < 3: return "<br>".join(banco)
    sorteio = random.sample(banco, 3)
    return "<br>".join(sorteio)

### bof: navigation

nav_cols = st.columns(6)
paginas = ["mini", "ypoemas", "eureka", "off-machina", "comments", "sobre"]
labels = ["ツ mini", "ypoemas", "eureka", "off-machina", "comments", "sobre"]

for i, pag in enumerate(paginas):
    with nav_cols[i]:
        if st.button(labels[i], key=f"btn_{pag}"):
            st.session_state.page = pag
            st.rerun()

st.markdown("---")

### bof: sidebar

# Arte Topo
mapeamento_artes = {"mini": "img_mini.jpg", "ypoemas": "img_ypoemas.jpg", "eureka": "img_eureka.jpg", "off-machina": "img_off-machina.jpg", "comments": "img_poly.jpg", "sobre": "img_about.jpg"}
st.sidebar.image(mapeamento_artes.get(st.session_state.page, "img_mini.jpg"), use_container_width=True)

# Idioma e Cookies
st.sidebar.selectbox("idioma", ["Português", "English", "Français", "Español", "Italiano", st.session_state.poly_name], key="sel_lang", label_visibility="collapsed")
st.sidebar.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3 = st.sidebar.columns([1, 1, 1])
with c1: st.session_state.audio_on = st.checkbox("v", value=True, key="v", label_visibility="collapsed")
with c2: st.session_state.draw_on = st.checkbox("a", value=True, key="a", label_visibility="collapsed")
with c3: st.session_state.video_on = st.checkbox("vi", value=False, key="vi", label_visibility="collapsed")

# Contato centralizado
st.sidebar.markdown("<p style='text-align:center; color:#999; font-size:0.8rem; margin-top:20px;'>contato</p>", unsafe_allow_html=True)
st.sidebar.markdown("<div style='text-align:center; font-size:0.9rem;'><a href='#'>📸 instagram</a><br><a href='#'>✉️ email</a></div>", unsafe_allow_html=True)

### bof: pages

if st.session_state.page == "mini":
    st.markdown("<h3 style='text-align: center; font-weight: 300;'>māchina :: mini</h3>", unsafe_allow_html=True)
    
    # O Poema Real (Sorteado do ovny_data.txt)
    st.markdown(f'<div class="mini-card">{gerar_poema_mini()}</div>', unsafe_allow_html=True)
    
    # Botão de Ação
    _, col_btn, _ = st.columns([1, 0.3, 1])
    with col_btn:
        if st.button("gerar novo", use_container_width=True, type="primary"):
            st.rerun()

elif st.session_state.page == "ypoemas":
    st.subheader("ツ ypoemas - O Grande Gerador")

st.sidebar.markdown("---")
st.sidebar.caption(f"Phenix Machina | {st.session_state.page}")
