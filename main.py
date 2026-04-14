import streamlit as st
import os

# --- 1. BOOT & CLEANUP ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding-top: 1.5rem !important;}
    div[data-testid="column"] { padding: 0 1px !important; }
    .stButton button { height: 36px !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. ESTADO ---
if 'page' not in st.session_state: st.session_state.page = 'demo'

# --- 3. ESTRUTURA GLOBAL ---
c_cockpit, c_vazio, c_palco = st.columns([2, 0.1, 7.9])

# --- 4. COCKPIT (IMEXÍVEL) ---
with c_cockpit:
    st.write("### ⚙️ cockpit")
    i_cols = st.columns(3)
    i_cols[0].button("🔈", key="s_on", use_container_width=True)
    i_cols[1].button("🎨", key="a_on", use_container_width=True)
    i_cols[2].button("🎬", key="v_on", use_container_width=True)
    st.divider()
    st.selectbox("biblioteca", ["Livro 01", "Livro 02"], key="sel_b")
    st.selectbox("temas", ["Tema A", "Tema B"], key="sel_t")
    st.divider()
    st.selectbox("idioma", ["português", "español", "english"], key="sel_l")

# --- 5. PALCO E RÉGUA COM ESPAÇADORES ---
with c_palco:
    # A SEQUÊNCIA SOLICITADA (Botão + Espaçador .1)
    pesos_user = [0.94, 0.1, 0.56, 0.1, 0.60, 0.1, 0.4, 0.1, 0.55, 0.1, 0.75, 0.1]
    regua = st.columns(pesos_user)
    
    menu_labels = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    
    # Percorremos apenas os índices pares (onde ficam os botões)
    for i, item in enumerate(menu_labels):
        col_idx = i * 2
        with regua[col_idx]:
            label = item if item != "yPoemas" else "yPoemas"
            if st.button(label.lower(), key=f"p_{i}", use_container_width=True):
                st.session_state.page = item
                st.rerun()
        
        # As colunas ímpares (col_idx + 1) permanecem como o espaçador .1 (vazias)

    st.divider()

    # RENDERIZAÇÃO
    p = st.session_state.page
    st.markdown(f"<h1 style='text-align: center; font-weight: 200;'>{p.lower()}</h1>", unsafe_allow_html=True)
