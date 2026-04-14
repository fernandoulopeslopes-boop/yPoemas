import streamlit as st
import os

# --- 1. CONFIGURAÇÃO SOBERANA ---
st.set_page_config(page_title="a máquina de fazer Poesia", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS DE TRAVAMENTO ESTRUTURAL ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding-top: 1.2rem !important; padding-bottom: 0px !important;}
    div[data-testid="column"] { padding: 0 1px !important; }
    .stButton button { height: 38px !important; font-family: 'Georgia', serif !important; }
    .palco { padding: 20px; border-radius: 10px; background-color: #ffffff; min-height: 80vh; }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS POPULADOS (ESTRUTURA DE LISTAS) ---
BIBLIOTECA = {
    "Livro de Amaré": ["Geral", "Variações Éticas", "Cantares"],
    "Anjos de Vidro": ["Serafins", "Querubins", "Tronos"],
    "O Tempo e a Máquina": ["Passado", "Presente", "Infinito"],
    "A Outra Margem": ["Rio", "Neblina", "Travessia"]
}
IDIOMAS = ["Português", "Español", "English", "Français", "Italiano", "Català"]

# --- 4. ESTADO GLOBAL ---
if 'page' not in st.session_state: st.session_state.page = 'demo'
if 'show_help' not in st.session_state: st.session_state.show_help = False

# --- 5. MOLDURA: COCKPIT (2) | PALCO (8) ---
c_cockpit, c_vazio, c_palco = st.columns([2, 0.1, 7.9])

# --- 6. TORRE DE CONTROLE (IMEXÍVEL) ---
with c_cockpit:
    st.markdown("### ⚙️ cockpit")
    i_cols = st.columns(3)
    i_cols[0].button("🔈", key="s_on", use_container_width=True)
    i_cols[1].button("🎨", key="a_on", use_container_width=True)
    i_cols[2].button("🎬", key="v_on", use_container_width=True)
    
    st.divider()
    livro_sel = st.selectbox("biblioteca", list(BIBLIOTECA.keys()), key="sel_b")
    st.selectbox("temas", BIBLIOTECA[livro_sel], key="sel_t")
    
    st.divider()
    st.selectbox("idioma", IDIOMAS, key="sel_l")
    
    st.divider()
    st.button("🎲 RANDOM", use_container_width=True)

# --- 7. PALCO CENTRAL E RÉGUA DE PRECISÃO ---
with c_palco:
    # A SEQUÊNCIA DE PESOS CALIBRADA
    pesos_user = [0.94, 0.1, 0.56, 0.1, 0.60, 0.1, 0.4, 0.1, 0.55, 0.1, 0.75, 0.1]
    regua = st.columns(pesos_user)
    paginas = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    
    for i, item in enumerate(paginas):
        col_btn, col_star = i * 2, (i * 2) + 1
        with regua[col_btn]:
            if st.button(item.lower() if item != "yPoemas" else "yPoemas", key=f"p_{i}", use_container_width=True):
                st.session_state.page, st.session_state.show_help = item, False
                st.rerun()
        with regua[col_star]:
            if st.button("⭐", key=f"h_{i}", use_container_width=True):
                st.session_state.page, st.session_state.show_help = item, True
                st.rerun()

    st.divider()

    # ÁREA DE CONTEÚDO (POPULADA)
    st.markdown('<div class="palco">', unsafe_allow_html=True)
    p, h = st.session_state.page, st.session_state.show_help
    
    if h:
        st.info(f"### ⭐ AJUDA: {p.upper()}\nCarregando ABOUT_{p.upper()}.MD...")
    else:
        if p == "opinião":
            st.markdown("### ✍️ Opinião/Comments\n*(Conteúdo do arquivo comments.md será renderizado aqui)*")
        elif p == "sobre":
            st.markdown("### 📖 Sobre a Máquina\n*(Conteúdo do arquivo sobre.md será renderizado aqui)*")
        else:
            st.subheader(f"Executando rotina: {p.upper()}")
            st.write("Aguardando acoplagem do motor de geração...")
    st.markdown('</div>', unsafe_allow_html=True)
