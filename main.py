import streamlit as st
import os

# --- 1. BOOT: HARDWARE ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    layout="wide", 
    initial_sidebar_state="expanded"
)

if 'page' not in st.session_state:
    st.session_state.page = 'demo'

# --- 2. MOTOR: RESGATE ---
def get_md(p):
    filename = "yPoemas" if p == "yPoemas" else p.lower()
    path = f"md_files/INFO_{filename}.md"
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except: return ""
    return ""

# --- 3. CSS: SIDEBAR FIXA E ESTÉTICA LOWER ---
st.markdown("""
<style>
    [data-testid="stHeader"] {display: none !important;}
    
    /* SIDEBAR FIXA: REMOVE ANIMAÇÕES E FORÇA EXIBIÇÃO */
    [data-testid="stSidebar"] {
        display: block !important;
        visibility: visible !important;
        background-color: #ffffff !important;
        border-right: 1px solid #f0f0f0 !important;
        transition: none !important; /* Fixa sem deslizar */
    }

    .stButton>button {
        border-radius: 20px !important;
        font-family: 'Georgia', serif !important;
        font-size: 13px !important;
        letter-spacing: 0.5px;
        white-space: nowrap !important;
        width: 100% !important;
        text-transform: none !important;
    }
    
    .st-key-on button {background-color: #000 !important; color: #fff !important; border: none !important;}
    .st-key-off button {background-color: #fff !important; color: #aaa !important; border: 1px solid #eee !important;}
    
    .info-box {
        font-size: 12px;
        font-family: 'Georgia', serif;
        padding: 12px;
        border-left: 3px solid #000;
        background: #fafafa;
    }

    .main .block-container {
        max-width: 1050px !important;
        margin: 0 auto !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR: COCKPIT ---
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    st.selectbox("🌐 idioma", ["português", "español", "english", "français", "italiano", "català"], key="sb_lang")
    st.divider()
    col_a, col_s = st.columns(2)
    with col_a: st.toggle("arte", value=True, key="t_a")
    with col_s: st.toggle("som", key="t_s")
    st.divider()
    img_name = "ypoemas" if st.session_state.page == "yPoemas" else st.session_state.page.lower()
    img_path = f"img_{img_name}.jpg"
    if os.path.exists(img_path): st.image(img_path, use_container_width=True)
    elif os.path.exists("img_demo.jpg"): st.image("img_demo.jpg", use_container_width=True)
    st.divider()
    st.markdown(f"<div class='info-box'>{get_md(st.session_state.page)}</div>", unsafe_allow_html=True)

# --- 5. NAVEGAÇÃO: ANCORAGEM E ESPAÇAMENTO ---
# demo (esq) | yPoemas | Eureka | Off-Machina | comments | sobre (dir)
menu = ["demo", "yPoemas", "eureka", "off-machina", "comments", "sobre"]
# Proporção ajustada para manter as pontas ancoradas e o centro equilibrado
cols_nav = st.columns([1, 1, 1, 1.7, 1.1, 1]) 

for i, item in enumerate(menu):
    with cols_nav[i]:
        tag = 'on' if st.session_state.page == item else 'off'
        st.markdown(f"<div class='st-key-{tag}'>", unsafe_allow_html=True)
        if st.button(item, key=f"nav_{i}"):
            st.session_state.page = item
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# --- 6. RÉGUA E CONTEÚDO ---
p = st.session_state.page

if p == "demo":
    f1, more, rand, auto, f2 = st.columns([4, 1, 1, 1, 4])
    with more: st.button("＋", key="c1")
    with rand: st.button("＊", key="c2")
    with auto: st.button("？", key="c3")

elif p == "comments":
    st.markdown("### comentários e impressões")
    st.info("Espaço dedicado às vozes que atravessam a Machina.")

elif p == "sobre":
    # Conteúdo baseado na Certidão de Gênese 
    st.markdown("## Certidão de Nascimento: A Machina de Fazer Poesia (yPoemas)")
    st.markdown("""
    A Machina é um O.V.N.I. (Objeto Versejador Não Identificado). Não se define pelo hardware, mas pela capacidade de precipitar o acaso em textos de alta coesão. 
    
    ### O Novo Paradigma
    Opera sob uma engenharia onde o código é o vácuo invisível para o movimento da poesia.
    * **Sidebar**: Cockpit de preferências (Artes, Áudio, Vídeo, Idioma).
    * **Efemeridade**: O conteúdo é volátil e existe plenamente no momento da observação.
    
    ### O Ítimo e o Eixo Z
    * **Eixo Z**: Abstração da lógica de escrita onde a substituição semântica é infinita.
    * **Ítimo**: Unidade fundamental da matéria poética que confere vontade própria à Machina.
    """)
    st.divider()
    st.caption("Propriedade Intelectual e Criação: [O Pai da Machina] | Abril de 2026. SARAVÁ. ")

st.divider()
titulo = p if p == "yPoemas" else p.lower()
st.markdown(f"<h1 style='text-align: center; font-family: Georgia; font-weight: 200;'>{titulo}</h1>", unsafe_allow_html=True)
