import streamlit as st
import os

# --- 1. CONFIGURAÇÃO DE HARDWARE VIRTUAL ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    layout="wide",
    initial_sidebar_state="expanded",
)

def load_content(file_name):
    base_path = os.path.dirname(__file__)
    search_paths = [os.path.join(base_path, "md_files"), base_path]
    target = file_name.upper()
    for folder in search_paths:
        if os.path.exists(folder):
            try:
                for arquivo in os.listdir(folder):
                    if arquivo.upper() == target:
                        with open(os.path.join(folder, arquivo), "r", encoding="utf-8") as f:
                            return f.read()
            except Exception: continue
    return f"⚠️ {target} não localizado."

st.markdown("""
    <style>
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stSidebar"] { min-width: 320px !important; max-width: 320px !important; }
    
    .st-key-palco_btns div.stButton > button {
        background-color: #f0f2f6 !important;
        color: #000 !important;
        border-radius: 50% !important;
        width: 38px !important;
        height: 38px !important;
        border: 2px solid #000 !important;
        font-size: 20px !important;
        font-weight: 900 !important;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0px !important;
    }

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

    .social-links { 
        font-size: 11px; 
        font-weight: 900; 
        text-align: center; 
        margin-top: 20px;
        letter-spacing: 1px;
    }
    .social-links a { color: #000; text-decoration: none; margin: 0 8px; }

    .main .block-container { max-width: 900px !important; margin: 0 auto !important; }
    label { display: none !important; }
    hr { border: 0; height: 1px; background: #ddd; margin: 15px 0 !important; }
    </style>
""", unsafe_allow_html=True)

if "active_page" not in st.session_state:
    st.session_state.active_page = "Demo"

img_map = {
    "Demo": "img_demo.jpg",
    "yPoemas": "img_ypoemas.jpg",
    "Eureka": "img_eureka.jpg",
    "Off-Machina": "img_off-machina.jpg",
    "About": "img_about.jpg"
}

# --- 2. SIDEBAR: CONSOLE DE COMANDO ---
with st.sidebar:
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    
    elite_langs = ["Português", "Español", "Italiano", "Français", "English", "Català"]
    st.selectbox("Idiomas", elite_langs, key="sb_idiomas")
    
    st.markdown("---")

    st.toggle("TALK (Voz)", key="tg_talk")
    st.toggle("DRAW (Imagem)", key="tg_draw")
    st.toggle("VÍDEO (Motion)", key="tg_video")

    st.markdown("---")

    # ATUALIZAÇÃO SINTÁTICA: width='stretch'
    current = st.session_state.active_page
    target_img = img_map.get(current, "img_demo.jpg")
    if os.path.exists(target_img):
        st.image(target_img, width='stretch')
    
    info_text = load_content(f"INFO_{current.upper()}.MD")
    st.markdown(f<div class='info-box'>{info_text}</div>, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div class='social-links'>
        <a href='#'>INSTAGRAM</a> • <a href='#'>GITHUB</a> • <a href='#'>LINKEDIN</a>
    </div>
    """, unsafe_allow_html=True)

# --- 3. PALCO ---
paginas = ["Demo", "yPoemas", "Eureka", "Off-Machina", "About"]
cols_nav = st.columns(len(paginas))
for i, pg in enumerate(paginas):
    if cols_nav[i].button(pg.upper(), key=f"nav_{pg}"):
        st.session_state.active_page = pg
        st.rerun()

st.divider()

_, col_barra, _ = st.columns([0.5, 3.0, 0.5])
with col_barra:
    c_btns, c_lista = st.columns([2.0, 1.2])
    with c_btns:
        st.markdown("<div class='st-key-palco_btns'>", unsafe_allow_html=True)
        n1, n2, n3, n4, n5 = st.columns(5)
        n1.button("＋") 
        n2.button("＜") 
        n3.button("＊") 
        n4.button("＞") 
        n5.button("？") 
        st.markdown("</div>", unsafe_allow_html=True)

    with c_lista:
        try:
            temas = [f.replace(".ypo", "") for f in os.listdir("data") if f.endswith(".ypo")]
            st.selectbox("Temas", temas if temas else ["Geral"], key="sel_temas")
        except:
            st.selectbox("Temas", ["Padrão"], key="sel_temas")

st.markdown("<hr>", unsafe_allow_html=True)

if current == "Demo":
    st.markdown("""
    <div style='text-align: center; color: #444; font-family: Georgia; margin-top: 50px;'>
        <i>O Palco processa a matriz rítmica...</i>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(load_content(f"MANUAL_{current.upper()}.MD"))
