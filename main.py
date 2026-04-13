import streamlit as st
import os

# --- 1. CONFIGURAÇÃO DE HARDWARE VIRTUAL ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    layout="wide",
    initial_sidebar_state="expanded",
)

# FUNÇÃO AUXILIAR DE CARREGAMENTO (Busca em md_files ou raiz)
def load_content(file_name):
    paths = [os.path.join(os.path.dirname(__file__), "md_files"), os.path.dirname(__file__)]
    for p in paths:
        full_path = os.path.join(p, file_name)
        if os.path.exists(full_path):
            with open(full_path, "r", encoding="utf-8") as f:
                return f.read()
    return f"⚠️ {file_name} não localizado."

st.markdown("""
    <style>
    /* DESATIVAR HEADER PADRÃO E FIXAR SIDEBAR */
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stSidebar"] { min-width: 320px !important; max-width: 320px !important; }

    /* BOTÕES CIRCULARES DO PALCO (Negrito Profundo) */
    .st-key-palco_btns div.stButton > button {
        background-color: #f0f2f6 !important;
        color: #000000 !important;
        border-radius: 50% !important;
        width: 38px !important;
        height: 38px !important;
        border: 2px solid #000000 !important;
        font-size: 20px !important;
        font-weight: 900 !important;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* INFO BOX: Estética de Dicionário */
    .info-box {
        font-family: 'Georgia', serif;
        font-size: 13px;
        line-height: 1.5;
        color: #222;
        background: #fdfdfd;
        padding: 12px;
        border-left: 4px solid #000;
        margin: 15px 0;
    }

    /* FOOTER REDES: Negrito 900 */
    .social-links { 
        font-size: 11px; 
        font-weight: 900; 
        text-align: center; 
        margin-top: 20px;
        letter-spacing: 1px;
    }
    .social-links a { color: #000; text-decoration: none; margin: 0 8px; }

    /* PALCO: Centralização */
    .main .block-container {
        max-width: 900px !important;
        margin: 0 auto !important;
    }
    
    label { display: none !important; }
    hr { border: 0; height: 1px; background: #ddd; margin: 20px 0 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR: CONSOLE DE COMANDO ---
with st.sidebar:
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    
    # A. IDIOMAS (Elite List no topo)
    elite_langs = ["Português", "Español", "Italiano", "Français", "English", "Català"]
    outros_langs = ["Deutsch", "Nederlands", "Polski", "Svenska", "Dansk", "Suomi"]
    st.selectbox("Idiomas", elite_langs + outros_langs, key="sb_idiomas")
    
    st.markdown("---")

    # B. TOGGLES: Talk, Draw, Vídeo
    st.toggle("TALK (Voz)", key="tg_talk")
    st.toggle("DRAW (Imagem)", key="tg_draw")
    st.toggle("VÍDEO (Motion)", key="tg_video")

    st.markdown("---")

    # C. ARTE DA PÁGINA (Conforme seu Screenshot: img_demo.jpg)
    if os.path.exists("img_demo.jpg"):
        st.image("img_demo.jpg", use_container_width=True)
    
    # D. INFO PÁGINA (Texto do INFO_DEMO.md)
    st.markdown(f"<div class='info-box'>{load_content('INFO_DEMO.md')}</div>", unsafe_allow_html=True)

    st.markdown("---")

    # E. FOOTER: Redes Sociais
    st.markdown("""
    <div class='social-links'>
        <a href='#'>INSTAGRAM</a> • <a href='#'>GITHUB</a> • <a href='#'>LINKEDIN</a>
    </div>
    """, unsafe_allow_html=True)

# --- 3. PALCO: NAVEGAÇÃO SUPERIOR ---
# Espaço para o menu de botões de página (Demo, yPoemas, etc.)
paginas = ["DEMO", "yPoemas", "Eureka", "Off-Machina", "About"]
cols_pg = st.columns(len(paginas))
for i, pg in enumerate(paginas):
    cols_pg[i].button(pg, key=f"btn_nav_{pg}")

st.divider()

# --- 4. BARRA DE COMANDO CENTRALIZADA ---
_, col_barra, _ = st.columns([0.5, 3.0, 0.5])

with col_barra:
    c_btns, c_lista = st.columns([2.0, 1.2])
    
    with c_btns:
        st.markdown("<div class='st-key-palco_btns'>", unsafe_allow_html=True)
        n1, n2, n3, n4, n5 = st.columns(5)
        n1.button("＋", key="p_add")   # Novo texto
        n2.button("＜", key="p_prev")
        n3.button("＊", key="p_star")  # Aleatório
        n4.button("＞", key="p_next")
        n5.button("？", key="p_help")
        st.markdown("</div>", unsafe_allow_html=True)

    with c_lista:
        # Placeholder para o seletor de temas
        st.selectbox("Temas", ["Selecione um Tema", "Amor", "Morte", "Tempo"], key="p_temas")

st.markdown("<hr>", unsafe_allow_html=True)

# --- 5. ÁREA DE EXIBIÇÃO ---
st.markdown("""
<div style='text-align: center; color: #333; font-family: Georgia; margin-top: 50px;'>
    <i>O Palco aguarda o processamento da Máquina.</i>
</div>
""", unsafe_allow_html=True)
