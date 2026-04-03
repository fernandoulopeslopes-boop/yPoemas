import os
import streamlit as st

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

# Regra 0: Look & Feel (A Blindagem Estética)
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    .main .block-container { max-width: 95% !important; padding-top: 1.5rem; margin: 0 auto; }
    
    /* SIDEBAR: Largura e Fundo */
    [data-testid="stSidebar"] { width: 240px !important; min-width: 240px !important; background-color: #fafafa; }
    
    /* NAVEGAÇÃO SUPERIOR: Botões de 111px */
    [data-testid="stHorizontalBlock"] { display: flex !important; flex-wrap: nowrap !important; gap: 8px !important; }
    [data-testid="column"] { flex: 0 0 auto !important; width: 115px !important; }
    div.stButton > button {
        width: 111px !important; border-radius: 12px; height: 3.2em;
        background-color: #ffffff; border: 1px solid #d1d5db; font-size: 11px;
    }

    /* LIMPEZA DE LABELS E HELPS */
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"], 
    [data-testid="stSidebar"] button[title="View help"] { 
        display: none !important; 
    }

    /* CENTRALIZAÇÃO DOS CHECKBOXES (Os Cookies) */
    /* Este seletor ataca o container interno das colunas na sidebar */
    [data-testid="stSidebarContent"] [data-testid="stHorizontalBlock"] {
        justify-content: center !important;
        gap: 20px !important;
        margin-top: 10px !important;
    }

    /* Estilo do Poema na Página Mini */
    .poema-box {
        font-family: 'IBM Plex Serif', serif;
        font-size: 1.3rem;
        font-style: italic;
        line-height: 1.8;
        color: #2c3e50;
        padding: 40px;
        background-color: #ffffff;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        margin: 20px 0;
        border-left: 3px solid #eee;
    }

    .sidebar-header {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 0.8rem;
        color: #aaa;
        text-transform: lowercase;
        text-align: center;
        margin-top: 30px;
    }
    </style> """,
    unsafe_allow_html=True,
)

### bof: navigation (O Trilho)

nav_cols = st.columns(6)
paginas = ["mini", "ypoemas", "eureka", "off-machina", "comments", "sobre"]
labels = ["ツ mini", "ypoemas", "eureka", "off-machina", "comments", "sobre"]

for i in range(6):
    with nav_cols[i]:
        if st.button(labels[i], key=f"btn_nav_{paginas[i]}"):
            st.session_state.page = paginas[i]
            st.rerun()

st.markdown("---")

### bof: sidebar (O Cockpit)

# Artes
mapeamento_artes = {
    "mini": "img_mini.jpg", "ypoemas": "img_ypoemas.jpg", "eureka": "img_eureka.jpg",
    "off-machina": "img_off-machina.jpg", "comments": "img_poly.jpg", "sobre": "img_about.jpg"
}
arte_atual = mapeamento_artes.get(st.session_state.page)
if arte_atual and os.path.exists(arte_atual):
    st.sidebar.image(arte_atual, use_container_width=True)

# 1. Idioma
lista_idiomas = ["Português", "English", "Français", "Español", "Italiano", st.session_state.poly_name]
sel_idioma = st.sidebar.selectbox("idioma", lista_idiomas, key="sel_lang", label_visibility="collapsed")

# 2. Recursos (Centralizados e Equidistantes)
st.sidebar.markdown("<br>", unsafe_allow_html=True)
# Usamos colunas 1:1:1 para garantir a equidistância interna, 
# e o CSS [justify-content: center] cuida da centralização na largura total.
c1, c2, c3 = st.sidebar.columns([1, 1, 1])
with c1:
    st.session_state.audio_on = st.checkbox("v", value=True, key="chk_v", label_visibility="collapsed")
with c2:
    st.session_state.draw_on = st.checkbox("a", value=True, key="chk_a", label_visibility="collapsed")
with c3:
    st.session_state.video_on = st.checkbox("vi", value=False, key="chk_vi", label_visibility="collapsed")

# 3. Contato
st.sidebar.markdown("<div class='sidebar-header'>contato</div>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style="text-align: center; display: flex; flex-direction: column; gap: 8px; font-family: 'IBM Plex Sans', sans-serif; font-size: 0.9rem; margin-top:10px;">
    <a href="#" style="text-decoration: none; color: #444;">📸 instagram</a>
    <a href="#" style="text-decoration: none; color: #444;">✉️ email</a>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption(f"Phenix Machina | {st.session_state.page}")

### bof: pages (O Palco)

if st.session_state.page == "mini":
    # Layout da Página Mini: Equilíbrio entre branco e texto
    st.markdown("## ツ mini-maquina")
    st.caption(f"idioma atual: {sel_idioma}")
    
    col_p1, col_p2 = st.columns([3, 1])
    
    with col_p1:
        # Placeholder do Poema
        st.markdown("""
        <div class="poema-box">
            o silêncio da máquina<br>
            ecoalha no papel digital<br>
            breve como um clique.
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("gerar novo verso", type="primary"):
            st.toast("A Phenix está processando seus arquivos...")

    with col_p2:
        st.markdown("---")
        st.write("### log")
        st.caption("v.2026.04")

elif st.session_state.page == "ypoemas":
    st.subheader("ツ ypoemas")

st.write("")
