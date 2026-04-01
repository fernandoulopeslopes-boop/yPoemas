import streamlit as st
import os, random, subprocess, sys

# =================================================================
# 0º SETOR: INFRAESTRUTURA (AUTO-INSTALAÇÃO)
# =================================================================
try:
    import extra_stylable_components as stx
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "extra-stylable-components"])
    import extra_stylable_components as stx

# =================================================================
# 1º SETOR: LENTE (DNA VISUAL E PRUMO DA SIDEBAR)
# =================================================================
st.set_page_config(page_title="yPoemas - Layout Consolidado", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* FORÇA A SIDEBAR A FICAR NO CANTO (310px) */
    [data-testid="stSidebar"] {
        min-width: 310px !important;
        max-width: 310px !important;
    }

    /* FORÇA O PALCO A OCUPAR O RESTANTE DA TELA */
    [data-testid="stAppViewBlockContainer"] {
        max-width: 100% !important;
        padding-top: 1rem !important;
        padding-right: 2rem !important;
        padding-left: 2rem !important;
        padding-bottom: 1rem !important;
        margin: 0 !important;
    }

    /* LIMPEZA DE INTERFACE */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}

    /* ESTILO DO POEMA (32px Georgia) */
    .poesia-viva {
        font-family: 'Georgia', serif !important;
        font-size: 32px !important; 
        line-height: 1.6 !important;
        color: #1a1a1a !important;
        white-space: pre-wrap;
        padding: 40px;
        background-color: #fdfdfd;
        border-radius: 8px;
        border: 1px solid #eee;
        margin-top: 10px;
    }
    mark { background-color: powderblue; color: black; }
    </style>
""", unsafe_allow_html=True)

# =================================================================
# 2º SETOR: PAIOL (LOGÍSTICA DE ESTADO)
# =================================================================
if 'take' not in st.session_state: st.session_state.take = random.randint(1000, 9999)
if 'lang' not in st.session_state: st.session_state.lang = "pt"
if 'last_lang' not in st.session_state: st.session_state.last_lang = "pt"

# =================================================================
# 5º SETOR: FAROL E NAVEGAÇÃO (TABS)
# =================================================================
# Barra de Abas Superior (Original do Projeto)
chosen_id = stx.tab_bar(data=[
    stx.TabBarItemData(id="1", title="mini", description=""),
    stx.TabBarItemData(id="2", title="yPoemas", description=""),
    stx.TabBarItemData(id="3", title="eureka", description=""),
    stx.TabBarItemData(id="4", title="off-machina", description=""),
    stx.TabBarItemData(id="5", title="books", description=""),
    stx.TabBarItemData(id="6", title="poly", description=""),
    stx.TabBarItemData(id="7", title="about", description=""),
], default="2")

mapa_tabs = {"1":"mini", "2":"yPoemas", "3":"eureka", "4":"off-machina", "5":"books", "6":"poly", "7":"about"}
sala_atual = mapa_tabs.get(chosen_id, "yPoemas")

# Controles de ID (Semente Temporal)
st.write("")
c1, c2, c3, c4, c_id = st.columns([1, 1, 1, 1, 2])
if c1.button("✚", key="btn_new"): st.session_state.take = random.randint(1000, 9999); st.rerun()
if c2.button("◀", key="btn_prev"): st.session_state.take -= 1; st.rerun()
if c3.button("✻", key="btn_rand"): st.session_state.take = random.randint(1000, 9999); st.rerun()
if c4.button("▶", key="btn_next"): st.session_state.take += 1; st.rerun()
c_id.code(f"SALA: {sala_atual.upper()} | ID: {st.session_state.take}")

# =================================================================
# 3º SETOR: PALCO (EXIBIÇÃO DO TRABALHO)
# =================================================================
st.divider()
msg_teste = f"A MACHINA ESTÁ DE PÉ\nSALA: {sala_atual.upper()}\nIDIOMA: {st.session_state.lang.upper()}\n\n[O prédio está no prumo? Sidebar à esquerda, Palco ao centro.]"
st.markdown(f'<div class="poesia-viva">{msg_teste}</div>', unsafe_allow_html=True)

# =================================================================
# 6º SETOR: METAS (SIDEBAR)
# =================================================================
with st.sidebar:
    st.title("A Machina")
    st.divider()
    
    # Seletor de Idiomas (Colunas Originais)
    st.write("🌍 **IDIOMA**")
    b1, b2, b3, b4, b5, b6 = st.columns([1.1, 1.13, 1.04, 1.04, 1.17, 1.25])
    if b1.button("pt", key="p_pt"): st.session_state.lang = "pt"; st.rerun()
    if b2.button("es", key="p_es"): st.session_state.lang = "es"; st.rerun()
    if b3.button("it", key="p_it"): st.session_state.lang = "it"; st.rerun()
    if b4.button("fr", key="p_fr"): st.session_state.lang = "fr"; st.rerun()
    if b5.button("en", key="p_en"): st.session_state.lang = "en"; st.rerun()
    if b6.button("⚒️", key="p_xy"): st.session_state.lang = "poly"; st.rerun()
    
    st.divider()
    st.checkbox("🖼️ Arte", key="chk_arte")
    st.checkbox("🔊 Voz", key="chk_voz")
    st.divider()
    
    # Placeholder Visual
    st.info(f"Câmera na sala: {sala_atual}")
    st.caption(f"Arquivo esperado: img_{sala_atual}.jpg")
