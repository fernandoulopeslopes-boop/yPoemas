import streamlit as st
import os

# --- 1. CONFIGURAÇÃO SOBERANA ---
st.set_page_config(
    page_title="a máquina de fazer Poesia", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. CSS DE PRECISÃO (ESTRUTURAL E ESTÉTICO) ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding-top: 1rem !important;}
    
    /* Alinhamento vertical absoluto da régua */
    div[data-testid="stHorizontalBlock"] { align-items: center !important; }

    /* Botões: Altura travada para eliminar a 'Montanha Russa' */
    .stButton button {
        height: 35px !important;
        margin: 0px !important;
        padding: 0px 5px !important;
        line-height: 1 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* Estilo específico para as Estrelas Amarelas */
    .stButton button p {
        color: #FFD700 !important; /* Gold / Amarelo */
        font-size: 20px !important;
    }

    div[data-testid="column"] { padding: 0 1px !important; }
    
    .md-render { font-family: 'Georgia', serif; line-height: 1.6; font-size: 1.1rem; }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS REAIS DA MACHINA (CONSISTENTES) ---
LIVROS_REAIS = [
    "Livro de Amaré", 
    "Anjos de Vidro", 
    "O Tempo e a Máquina", 
    "A Outra Margem", 
    "Labirintos", 
    "Eros", 
    "Cosmos"
]
IDIOMAS_REAIS = ["Português", "Español", "English", "Français", "Italiano", "Català"]

# --- 4. ENGINE DE CARREGAMENTO DE CONTEÚDO ---
def load_md_file(name):
    path = f"{name}.md"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return f"*Conteúdo de {path} ainda não disponível no diretório.*"

# --- 5. ESTADO GLOBAL ---
if 'page' not in st.session_state: st.session_state.page = 'demo'
if 'show_help' not in st.session_state: st.session_state.show_help = False

# --- 6. ARQUITETURA (PAINEL 2 | PALCO 8) ---
c_painel, c_vazio, c_palco = st.columns([2, 0.1, 7.9])

# --- 7. PAINEL DE CONTROLE (IMEXÍVEL) ---
with c_painel:
    st.write("### controles")
    
    # Interruptores (Som, Arts, Talk)
    i1, i2, i3 = st.columns(3)
    i1.button("🔈", key="btn_som", use_container_width=True)
    i2.button("🎨", key="btn_arts", use_container_width=True)
    i3.button("💬", key="btn_talk", use_container_width=True)
    
    st.divider()
    
    # Seletores com Listas Reais
    st.selectbox("livros", LIVROS_REAIS, key="sel_livro")
    st.selectbox("idioma", IDIOMAS_REAIS, key="sel_lang")

# --- 8. PALCO CENTRAL E RÉGUA DE PRECISÃO ---
with c_palco:
    # Pesos decimais exatos para diagramação
    pesos_user = [0.94, 0.1, 0.56, 0.1, 0.60, 0.1, 0.4, 0.1, 0.55, 0.1, 0.75, 0.1]
    regua = st.columns(pesos_user)
    
    paginas = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
    
    for i, item in enumerate(paginas):
        col_btn = i * 2
        col_star = col_btn + 1
        
        # Botão de Navegação
        with regua[col_btn]:
            label = item if item != "yPoemas" else "yPoemas"
            if st.button(label.lower(), key=f"p_{i}", use_container_width=True):
                st.session_state.page = item
                st.session_state.show_help = False
                st.rerun()
        
        # Side-Button (Estrela Amarela solicitada)
        with regua[col_star]:
            if st.button("★", key=f"h_{i}", use_container_width=True):
                st.session_state.page = item
                st.session_state.show_help = True
                st.rerun()

    st.divider()

    # --- 9. RENDERIZAÇÃO DO PALCO ---
    p, h = st.session_state.page, st.session_state.show_help
    
    st.markdown('<div class="md-render">', unsafe_allow_html=True)
    if h:
        st.markdown(load_md_file(f"ABOUT_{p.upper()}"))
    else:
        if p == "opinião":
            st.markdown(load_md_file("comments"))
        elif p == "sobre":
            st.markdown(load_md_file("sobre"))
        else:
            st.subheader(f"Página: {p.lower()}")
            st.info(f"O esqueleto está pronto. Aguardando o acoplamento da rotina '{p}'.")
    st.markdown('</div>', unsafe_allow_html=True)
