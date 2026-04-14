import streamlit as st
import os

# --- 1. CONFIGURAÇÃO (O DNA DO SEGURO) ---
st.set_page_config(
    page_title="yPoemas",
    layout="centered", # Mantendo seu padrão
    initial_sidebar_state="expanded" # Forçando a abertura
)

# Inicialização do Estado
if 'page' not in st.session_state:
    st.session_state.page = 'demo'

# --- 2. MOTOR DE CARGA (SEM INDIREÇÃO) ---
def resgate_texto(pagina):
    # Pasta md_files conforme sua instrução
    # Mapeamento literal para evitar erros de minúscula/maiúscula
    arquivos = {
        "opinião": "ABOUT_COMMENTS.MD",
        "sobre": "ABOUT_SOBRE.MD",
        "off-mach": "ABOUT_OFF-MACHINA.MD",
        "eureka": "ABOUT_EUREKA.MD",
        "ypoemas": "ABOUT_YPOEMAS.MD",
        "demo": "ABOUT_DEMO.MD"
    }
    
    nome_arquivo = arquivos.get(pagina.lower(), f"ABOUT_{pagina.upper()}.MD")
    caminho = os.path.join("md_files", nome_arquivo)
    
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    return f"Busca falhou: {caminho}"

# --- 3. CSS MÍNIMO (SÓ O VERNIZ DOS BOTÕES) ---
st.markdown("""
<style>
    [data-testid="stHeader"] {display: none !important;}
    
    /* Botões Superiores */
    .stButton>button {
        border-radius: 20px !important;
        width: 100px !important;
        height: 35px !important;
        font-family: 'Georgia', serif !important;
    }
    
    /* Botões de Navegação do Palco (60% menores) */
    .nav-symbol button {
        width: 40px !important; 
        height: 40px !important;
        font-size: 18px !important;
        border-radius: 50% !important;
    }

    .st-key-on button {background-color: #000 !important; color: #fff !important;}
    .st-key-off button {background-color: #fff !important; color: #aaa !important; border: 1px solid #eee !important;}
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR (O COCKPIT) ---
# Se a sidebar não aparecer aqui, o problema é o Host/Cache
with st.sidebar:
    st.title("Cockpit")
    
    # Seletor de Idiomas
    st.selectbox("🌐 idioma", ["português", "español", "english", "italiano"], key="lang_final")
    
    st.divider()
    
    # Navegação Interna (<< e >>)
    cl, cr = st.columns(2)
    with cl: st.button("<<", key="nav_prev_sidebar")
    with cr: st.button(">>", key="nav_next_sidebar")
    
    st.divider()
    
    # Imagem Lateral
    p_atual = st.session_state.page.lower()
    img_path = f"img_{'off-machina' if p_atual == 'off-mach' else p_atual}.jpg"
    if os.path.exists(img_path):
        st.image(img_path)
    
    # Texto de apoio na Sidebar
    st.info(f"Página: {st.session_state.page}")

# --- 5. NAVEGAÇÃO SUPERIOR (MENU 6) ---
menu = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
cols = st.columns(len(menu))

for i, item in enumerate(menu):
    with cols[i]:
        # Estilo ativo/inativo
        tag = 'on' if st.session_state.page == item else 'off'
        st.markdown(f"<div class='st-key-{tag}'>", unsafe_allow_html=True)
        if st.button(item.lower() if item != "yPoemas" else "yPoemas", key=f"bt_nav_{i}"):
            st.session_state.page = item
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# --- 6. RÉGUA DO PALCO (MATEMÁTICA DO 10) ---
p = st.session_state.page
if p == "demo":
    f1, b1, b2, b3, f2 = st.columns([3.5, 1, 1, 1, 3.5])
    with b1: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("＋", key="ctrl_d1")
    with b2: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("＊", key="ctrl_d2")
    with b3: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("？", key="ctrl_d3")

elif p == "yPoemas":
    f1, b1, b2, b3, b4, b5, f2 = st.columns([2.5, 1, 1, 1, 1, 1, 2.5])
    with b1: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("＋", key="ctrl_y1")
    with b2: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("＜", key="ctrl_y2")
    with b3: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("＊", key="ctrl_y3")
    with b4: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("＞", key="ctrl_y4")
    with b5: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("？", key="ctrl_y5")

# --- 7. PALCO CENTRAL (OPINIÃO E SOBRE) ---
# Renderiza o conteúdo das páginas
conteudo_palco = resgate_texto(p)
st.markdown(conteudo_palco)

st.divider()
st.markdown(f"<h3 style='text-align: center;'>{p.lower()}</h3>", unsafe_allow_html=True)
