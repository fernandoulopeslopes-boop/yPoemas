import streamlit as st
import os

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="a máquina de fazer Poesia", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS DE PRECISÃO (FIM DA MONTANHA RUSSA) ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding-top: 1rem !important;}
    
    /* Força o alinhamento vertical absoluto no chassi da régua */
    div[data-testid="stHorizontalBlock"] {
        align-items: center !important;
    }

    /* Botões: altura travada e remoção de margens que causam o desnível */
    .stButton button {
        height: 35px !important;
        padding: 0px 5px !important;
        margin: 0px !important;
        line-height: 1 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* Ajuste de colunas para não haver respiro interno */
    div[data-testid="column"] { padding: 0 1px !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS REAIS (A MÁQUINA) ---
# Listas baseadas nos seus arquivos e definições de projeto
TEMAS_REAIS = ["Amaré", "Anjos", "Tempo", "A Outra Margem", "Labirintos", "Eros", "Cosmos"]
IDIOMAS_REAIS = ["Português", "Español", "English", "Français", "Italiano", "Català"]

# --- 4. ESTADO GLOBAL ---
if 'page' not in st.session_state: st.session_state.page = 'demo'
if 'show_help' not in st.session_state: st.session_state.show_help = False

# --- 5. ESTRUTURA ( PAINEL 2 | PALCO 8 ) ---
c_painel, c_vazio, c_palco = st.columns([2, 0.1, 7.9])

# --- 6. PAINEL DE CONTROLE (IMEXÍVEL) ---
with c_painel:
    st.write("### controles")
    
    # Interruptores (Som, Arts, Talk)
    i1, i2, i3 = st.columns(3)
    i1.button("🔈", key="btn_som", use_container_width=True)
    i2.button("🎨", key="btn_arts", use_container_width=True)
    i3.button("💬", key="btn_talk", use_container_width=True)
    
    st.divider()
    
    # Listas Consistentes
    st.selectbox("temas", TEMAS_REAIS, key="sel_tema")
    st.selectbox("idioma", IDIOMAS_REAIS, key="sel_lang")
    
    st.divider()
    st.button("RANDOM", key="btn_rnd", use_container_width=True)

# --- 7. PALCO E RÉGUA DE PRECISÃO ---
with c_palco:
    # A sequência de pesos decimais informada por você
    pesos_user = [0.94, 0.1, 0.56, 0.1, 0.60, 0.1, 0.4, 0.1, 0.55, 0.1, 0.75, 0.1]
    regua = st.columns(pesos_user)
    
    paginas = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    
    for i, item in enumerate(paginas):
        col_btn = i * 2
        col_star = col_btn + 1
        
        with regua[col_btn]:
            label = item if item != "yPoemas" else "yPoemas"
            if st.button(label.lower(), key=f"p_{i}", use_container_width=True):
                st.session_state.page = item
                st.session_state.show_help = False
                st.rerun()
        
        with regua[col_star]:
            if st.button("⭐", key=f"h_{i}", use_container_width=True):
                st.session_state.page = item
                st.session_state.show_help = True
                st.rerun()

    st.divider()

    # ÁREA DE RENDERIZAÇÃO
    p, h = st.session_state.page, st.session_state.show_help
    
    if h:
        st.markdown(f"### contextualização: {p.lower()}")
        # Aqui entra a chamada real dos arquivos ABOUT_...
    else:
        if p == "opinião":
            # Aqui entra a rotina do comments.md
            st.write("### comentários e opiniões")
        elif p == "sobre":
            # Aqui entra a rotina do sobre.md
            st.write("### sobre a máquina")
        else:
            st.write(f"### {p.lower()}")
