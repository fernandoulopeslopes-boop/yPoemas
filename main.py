import streamlit as st
import os

# --- 1. BOOT & CLEANUP ---
st.set_page_config(page_title="yPoemas", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding-top: 1.5rem !important; padding-bottom: 0px !important;}
    div[data-testid="column"] { padding: 0 2px !important; }
    /* Unifica a altura dos botões para evitar a montanha russa */
    .stButton button { height: 38px !important; line-height: 1 !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. ESTADO ---
if 'page' not in st.session_state: st.session_state.page = 'demo'
if 'show_help' not in st.session_state: st.session_state.show_help = False

# --- 3. ESTRUTURA GLOBAL (100% NATIVO) ---
c_cockpit, c_vazio, c_palco = st.columns([2, 0.1, 7.9])

# --- 4. TORRE DE CONTROLE (IMEXÍVEL) ---
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

# --- 5. PALCO E RÉGUA COM PESOS CUSTOM ---
with c_palco:
    # A SEQUÊNCIA DE VALORES INFORMADA (Pares: Botão + Estrela)
    # Aplicando a lógica de pesos para cada par funcional
    menu_labels = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    pesos_user = [0.94, 0.56, 0.60, 0.4, 0.55, 0.75]
    
    # Criamos 12 colunas (6 botões + 6 estrelas)
    # Para as estrelas, usaremos um peso fixo pequeno (ex: 0.25) para manter a proporção
    pesos_finais = []
    for p in pesos_user:
        pesos_finais.extend([p, 0.25])
        
    regua = st.columns(pesos_finais)
    
    for i, item in enumerate(menu_labels):
        col_btn = i * 2
        col_star = col_btn + 1
        
        # Botão da Página
        with regua[col_btn]:
            label = item if item != "yPoemas" else "yPoemas"
            if st.button(label.lower(), key=f"p_{i}", use_container_width=True):
                st.session_state.page = item
                st.session_state.show_help = False
                st.rerun()
        
        # Side-Button (Estrela)
        with regua[col_star]:
            if st.button("⭐", key=f"h_{i}", use_container_width=True):
                st.session_state.page = item
                st.session_state.show_help = True
                st.rerun()

    st.divider()

    # RENDERIZAÇÃO DO CONTEÚDO
    p = st.session_state.page
    if st.session_state.show_help:
        st.info(f"MODO HELP: ABOUT_{p.upper()}.MD")
    else:
        st.markdown(f"<h1 style='text-align: center; font-weight: 200;'>{p.lower()}</h1>", unsafe_allow_html=True)
