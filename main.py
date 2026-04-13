import streamlit as st
import os

# 1. HARDWARE: BOOT SEM INTERFERÊNCIA
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

if 'page' not in st.session_state:
    st.session_state.page = 'Demo'

# 2. CSS: FORÇANDO A PRESENÇA FÍSICA DA SIDEBAR
st.markdown("""<style>
    /* Esconde o Header nativo */
    [data-testid="stHeader"] {display: none !important;}
    
    /* FORÇA A SIDEBAR A APARECER E MANTER 300PX */
    [data-testid="stSidebar"] {
        min-width: 300px !important;
        max-width: 300px !important;
        visibility: visible !important;
        display: block !important;
    }

    /* NAV: BOTÕES ARREDONDADOS */
    .stButton>button {
        width: 100%; height: 42px; border-radius: 20px; 
        font-weight: 900; font-size: 11px; text-transform: uppercase;
    }
    .st-key-on button {background-color: #000 !important; color: #fff !important;}
    .st-key-off button {background-color: #f8f9fa !important; color: #888 !important; border: 1px solid #eee !important;}
    
    /* RÉGUA: QUADRADOS */
    .st-key-cmd button {
        border-radius: 8px !important; width: 52px !important; height: 52px !important; 
        font-size: 24px !important; font-weight: 900; background: #fff !important; border: 1px solid #ccc !important;
    }

    /* INFO BOX */
    .info-box {
        font-family: 'Georgia', serif; font-size: 13px; line-height: 1.6; 
        padding: 15px; border-left: 5px solid #000; background: #fff;
    }

    .main .block-container {max-width: 1100px !important; margin: 0 auto !important;}
</style>""", unsafe_allow_html=True)

# 3. SIDEBAR (CONTEÚDO)
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    langs = ["Português", "Español", "English", "Français", "Italiano", "Català", "German", "Latin"]
    st.selectbox("🌐 IDIOMA", langs, key="sb_lang")
    st.divider()
    if os.path.exists("img_demo.jpg"): 
        st.image("img_demo.jpg", use_container_width=True)
    st.divider()
    path_md = f"md_files/INFO_{st.session_state.page.upper()}.md"
    info = open(path_md, "r", encoding="utf-8").read() if os.path.exists(path_md) else ""
    st.markdown(f"<div class='info-box'>{info}</div>", unsafe_allow_html=True)

# 4. NAVEGAÇÃO
menu = ["Demo", "yPoemas", "Eureka", "Off-Machina", "Comments", "About"]
c_nav = st.columns(6)
for i, item in enumerate(menu):
    with c_nav[i]:
        tag = 'on' if st.session_state.page == item else 'off'
        st.markdown(f"<div class='st-key-{tag}'>", unsafe_allow_html=True)
        if st.button(item, key=f"n_{i}"):
            st.session_state.page = item
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# 5. RÉGUA
c_cmd = st.columns([1, 1, 1, 1, 1, 7.5])
icons = ["＋", "＜", "＊", "＞", "？"]
for i, icon in enumerate(icons):
    with c_cmd[i]:
        st.markdown("<div class='st-key-cmd'>", unsafe_allow_html=True)
        st.button(icon, key=f"c_{i}")
        st.markdown("</div>", unsafe_allow_html=True)

st.write("")

# SELETORES
c_sel = st.columns([1.1, 1.4, 1.8, 2, 1.1])
with c_sel[0]:
    t1, t2 = st.columns([1, 2])
    t1.toggle("A", value=True, key="t_a", label_visibility="collapsed")
    t2.markdown("**ARTE**")
with c_sel[1]:
    st.selectbox("L", langs[:3], key="s_l", label_visibility="collapsed")
with c_sel[2]:
    grupos = sorted([f[4:-4] for f in os.listdir("base") if f.startswith("rol_")])
    g_sel = st.selectbox("G", grupos, key="s_g", label_visibility="collapsed")
with c_sel[3]:
    temas = open(f"base/rol_{g_sel}.txt", "r", encoding="utf-8").read().splitlines()
    st.selectbox("T", temas, key="s_t", label_visibility="collapsed")
with c_sel[4]:
    t3, t4 = st.columns([1, 2])
    t3.toggle("S", key="t_s", label_visibility="collapsed")
    t4.markdown("**SOM**")

st.divider()

# 6. DISPLAY
st.markdown(f"<h1 style='text-align: center; font-family: Georgia;'>{st.session_state.page}</h1>", unsafe_allow_html=True)
