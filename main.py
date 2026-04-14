import streamlit as st
import os

# --- 1. BOOT: IGUAL AO SEGURO (MÁXIMA PRIORIDADE) ---
st.set_page_config(
    page_title="yPoemas",
    layout="centered",
    initial_sidebar_state="expanded" # Forçamos a expansão aqui
)

# Garantia de Estado
if 'page' not in st.session_state:
    st.session_state.page = 'demo'

# --- 2. MOTOR: CARGA SEM SUPOSIÇÕES ---
def load_md_final(p):
    # Mapeamento exato dos seus arquivos testados
    mapping = {
        "opinião": "COMMENTS",
        "sobre": "SOBRE",
        "off-mach": "OFF-MACHINA",
        "eureka": "EUREKA",
        "ypoemas": "YPOEMAS",
        "demo": "DEMO"
    }
    file_key = mapping.get(p.lower(), p.upper())
    path = f"md_files/ABOUT_{file_key}.MD"
    
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# --- 3. CSS: APENAS O QUE NÃO MATA A SIDEBAR ---
st.markdown("""
<style>
    [data-testid="stHeader"] {display: none !important;}
    
    /* Botões Superiores */
    .stButton>button {
        border-radius: 20px !important;
        font-family: 'Georgia', serif !important;
        text-transform: none !important;
        width: 100px !important;
        height: 35px !important;
    }

    /* Redução de 60% nos botões de controle (Símbolos) */
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

# --- 4. SIDEBAR: COCKPIT (NATIVO E SEGURO) ---
with st.sidebar:
    st.markdown("### 🌐 idioma")
    # Simplificado para garantir que nada trave a renderização
    idioma = st.selectbox("", ["português", "español", "english", "italiano"], label_visibility="collapsed")
    
    st.divider()
    
    # Controles de Direção (<< e >>)
    c_l, c_r = st.columns(2)
    with c_l: st.button("<<", key="s_prev")
    with c_r: st.button(">>", key="s_next")
    
    st.divider()
    
    # Imagem Lateral
    img_name = "off-machina" if st.session_state.page == "off-mach" else st.session_state.page.lower()
    img_path = f"img_{img_name}.jpg"
    if os.path.exists(img_path):
        st.image(img_path)
    
    # Resumo da Página na Sidebar
    st.markdown(f"<div style='font-size:12px;'>{load_md_final(st.session_state.page)}</div>", unsafe_allow_html=True)

# --- 5. NAVEGAÇÃO SUPERIOR ---
menu = ["demo", "yPoemas", "eureka", "off-mach", "opinião", "sobre"]
cols = st.columns(6)

for i, item in enumerate(menu):
    with cols[i]:
        tag = 'on' if st.session_state.page == item else 'off'
        if st.button(item.lower() if item != "yPoemas" else "yPoemas", key=f"m_{i}"):
            st.session_state.page = item
            st.rerun()

st.divider()

# --- 6. RÉGUA DO PALCO (MATEMÁTICA DO 10) ---
p = st.session_state.page
if p == "demo":
    f1, b1, b2, b3, f2 = st.columns([3.5, 1, 1, 1, 3.5])
    with b1: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("＋", key="d1")
    with b2: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("＊", key="d2")
    with b3: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("？", key="d3")

elif p == "yPoemas":
    f1, b1, b2, b3, b4, b5, f2 = st.columns([2.5, 1, 1, 1, 1, 1, 2.5])
    with b1: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("＋", key="y1")
    with b2: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("＜", key="y2")
    with b3: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("＊", key="y3")
    with b4: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("＞", key="y4")
    with b5: st.markdown("<div class='nav-symbol'>", unsafe_allow_html=True); st.button("？", key="y5")

# --- 7. PALCO CENTRAL (OPINIÃO / SOBRE) ---
# Aqui o conteúdo das páginas deve aparecer por inteiro
st.markdown(load_md_final(p))

st.divider()
st.markdown(f"<h1 style='text-align: center; font-family: Georgia; font-weight: 200;'>{p.lower()}</h1>", unsafe_allow_html=True)
