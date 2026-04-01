import streamlit as st
import random
import extra_stylable_components as stx

# 1. CONFIGURAÇÃO DE LENTE (SEM SUBPROCESS!)
st.set_page_config(page_title="yPoemas v2", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    [data-testid="stSidebar"] { min-width: 310px !important; max-width: 310px !important; }
    [data-testid="stAppViewBlockContainer"] { max-width: 100% !important; padding: 1rem 2rem !important; }
    footer {visibility: hidden;} #MainMenu {visibility: hidden;} header {visibility: hidden;}
    .poesia-viva {
        font-family: 'Georgia', serif !important;
        font-size: 32px !important; 
        line-height: 1.6 !important;
        padding: 40px;
        background-color: #fdfdfd;
        border-radius: 8px;
        border: 1px solid #eee;
    }
    </style>
""", unsafe_allow_html=True)

# 2. ESTADOS
if 'take' not in st.session_state: st.session_state.take = random.randint(1000, 9999)
if 'lang' not in st.session_state: st.session_state.lang = "pt"

# 3. NAVEGAÇÃO (TABS)
chosen_id = stx.tab_bar(data=[
    stx.TabBarItemData(id="1", title="mini", description=""),
    stx.TabBarItemData(id="2", title="yPoemas", description=""),
    stx.TabBarItemData(id="3", title="eureka", description=""),
    stx.TabBarItemData(id="4", title="off-machina", description=""),
    stx.TabBarItemData(id="5", title="books", description=""),
    stx.TabBarItemData(id="6", title="poly", description=""),
    stx.TabBarItemData(id="7", title="about", description=""),
], default="2")

mapa = {"1":"mini", "2":"yPoemas", "3":"eureka", "4":"off-machina", "5":"books", "6":"poly", "7":"about"}
sala = mapa.get(chosen_id, "yPoemas")

# 4. PALCO
st.write("")
c1, c2, c3, c4, c_id = st.columns([1, 1, 1, 1, 2])
if c1.button("✚"): st.session_state.take = random.randint(1000, 9999); st.rerun()
if c2.button("◀"): st.session_state.take -= 1; st.rerun()
if c3.button("✻"): st.session_state.take = random.randint(1000, 9999); st.rerun()
if c4.button("▶"): st.session_state.take += 1; st.rerun()
c_id.code(f"SALA: {sala.upper()} | ID: {st.session_state.take}")

st.divider()
st.markdown(f'<div class="poesia-viva">SALA: {sala.upper()}\n[Se você vê este texto, o erro da linha 10 sumiu!]</div>', unsafe_allow_html=True)

# 5. SIDEBAR
with st.sidebar:
    st.title("A Machina")
    st.divider()
    st.write("🌍 **IDIOMA**")
    col1, col2 = st.columns(2)
    if col1.button("pt"): st.session_state.lang = "pt"; st.rerun()
    if col2.button("es"): st.session_state.lang = "es"; st.rerun()
