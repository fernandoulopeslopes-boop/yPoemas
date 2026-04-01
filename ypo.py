import streamlit as st
import os, random, subprocess, sys

# --- BLOCO DE INSTALAÇÃO AUTOMÁTICA ---
try:
    import extra_stylable_components as stx
except ImportError:
    # Se não achar o pacote, ele instala agora "na marra"
    subprocess.check_call([sys.executable, "-m", "pip", "install", "extra-stylable-components"])
    import extra_stylable_components as stx
# --------------------------------------

# 1º SETOR: LENTE (CONFIGURAÇÃO VISUAL)
st.set_page_config(page_title="yPoemas - Layout Final", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child { width: 310px; }
    .block-container { padding-top: 0rem; padding-right: 1rem; padding-left: 1rem; padding-bottom: 0rem; }
    
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
        margin-top: 20px;
    }
    mark { background-color: powderblue; color: black; }
    </style>
""", unsafe_allow_html=True)

# 2º SETOR: PAIOL (ESTADOS)
if 'take' not in st.session_state: st.session_state.take = random.randint(1000, 9999)
if 'lang' not in st.session_state: st.session_state.lang = "pt"

# 5º SETOR: NAVEGAÇÃO (A TAB BAR REAL)
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

# O FAROL (CONTROLES)
st.write("")
c1, c2, c3, c4, c_id = st.columns([1, 1, 1, 1, 2])
if c1.button("✚"): st.session_state.take = random.randint(1000, 9999); st.rerun()
if c2.button("◀"): st.session_state.take -= 1; st.rerun()
if c3.button("✻"): st.session_state.take = random.randint(1000, 9999); st.rerun()
if c4.button("▶"): st.session_state.take += 1; st.rerun()
c_id.code(f"SALA: {sala_atual.upper()} | ID: {st.session_state.take}")

# 3º SETOR: PALCO (EXIBIÇÃO)
st.divider()
st.markdown(f'<div class="poesia-viva">A MÁQUINA ESTÁ DE PÉ\nSALA: {sala_atual.upper()}\nIDIOMA: {st.session_state.lang.upper()}\n\n[O texto aparecerá aqui com 32px e fonte Georgia]</div>', unsafe_allow_html=True)

# 6º SETOR: SIDEBAR (O REVESTIMENTO)
with st.sidebar:
    st.title("A Machina")
    st.divider()
    st.write("🌍 **IDIOMA**")
    b1, b2, b3, b4, b5, b6 = st.columns([1.1, 1.13, 1.04, 1.04, 1.17, 1.25])
    if b1.button("pt"): st.session_state.lang = "pt"; st.rerun()
    if b2.button("es"): st.session_state.lang = "es"; st.rerun()
    if b3.button("it"): st.session_state.lang = "it"; st.rerun()
    if b4.button("fr"): st.session_state.lang = "fr"; st.rerun()
    if b5.button("en"): st.session_state.lang = "en"; st.rerun()
    if b6.button("⚒️"): st.session_state.lang = "poly"; st.rerun()
    
    st.divider()
    st.checkbox("🖼️ Arte")
    st.checkbox("🔊 Voz")
    st.divider()
    st.info(f"Espaço para imagem: img_{sala_atual}.jpg")
    
