import streamlit as st
import os

# --- 1. SETUP DO PALCO ---
st.set_page_config(
    page_title="yPoemas - a Máquina",
    layout="wide",
    initial_sidebar_state="collapsed", # Esconde a sidebar nativa
)

# CSS para fixar o layout do Retrato
st.markdown("""
    <style>
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    
    /* Centralização do Bloco Principal */
    .block-container {
        max-width: 950px !important;
        margin: 0 auto !important;
        padding-top: 2rem !important;
    }

    /* Botões de Navegação (Menu Superior) */
    .st-key-nav_btns div.stButton > button {
        border-radius: 20px;
        font-weight: 900;
        background-color: #f8f9fa;
        border: 1px solid #ddd;
    }

    /* Botões de Comando (Círculos Pretos do Retrato) */
    .st-key-cmd_btns div.stButton > button {
        background-color: #f0f2f6 !important;
        color: #000 !important;
        border-radius: 50% !important;
        width: 42px !important;
        height: 42px !important;
        border: 2px solid #000 !important;
        font-size: 22px !important;
        font-weight: 900 !important;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0px !important;
    }

    /* Estilo da Poesia (Georgia) */
    .poesia-text {
        font-family: 'Georgia', serif;
        font-size: 18px;
        line-height: 1.7;
        color: #1a1a1a;
        padding: 20px;
    }

    hr { border: 0; height: 1px; background: #eee; margin: 10px 0 !important; }
    label { font-weight: 900 !important; font-size: 12px !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. NAVEGAÇÃO SUPERIOR ---
if "active_page" not in st.session_state:
    st.session_state.active_page = "Demo"

cols_nav = st.columns(6)
menu = ["Demo", "yPoemas", "Eureka", "Off-Machina", "Comments", "About"]

st.markdown("<div class='st-key-nav_btns'>", unsafe_allow_html=True)
for i, item in enumerate(menu):
    if cols_nav[i].button(item.upper(), key=f"nav_{item}"):
        st.session_state.active_page = item
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# --- 3. CONSOLE DE COMANDO (CENTRALIZADO NO PALCO) ---
# Seguindo o layout: [Botões + * []] [Idioma] [Tema] [Som]
c_btns, c_idio, c_tema, c_som = st.columns([1.5, 1.2, 1.2, 0.8])

with c_btns:
    st.markdown("<div class='st-key-cmd_btns'>", unsafe_allow_html=True)
    b1, b2, b3 = st.columns(3)
    b1.button("＋", key="cmd_add")
    b2.button("✻", key="cmd_star")
    b3.button("☐", key="cmd_auto")
    st.markdown("</div>", unsafe_allow_html=True)

with c_idio:
    st.selectbox("Idioma", ["Português", "Español", "English", "Italiano", "Français"], key="sel_lang")

with c_tema:
    # Simulação de temas
    st.selectbox("Tema", ["Selecione...", "Proust", "Metafísica", "Urbano"], key="sel_tema")

with c_som:
    st.selectbox("Som", ["Voz 1", "Voz 2", "Mudo"], key="sel_voice")

st.markdown("<hr>", unsafe_allow_html=True)

# --- 4. ÁREA DE EXIBIÇÃO (O RETRATO) ---
current = st.session_state.active_page

if current == "Demo":
    # Layout Lado a Lado como no print
    col_img, col_txt = st.columns([1, 1.2])
    
    with col_img:
        if os.path.exists("img_demo.jpg"):
            st.image("img_demo.jpg", width='stretch')
        else:
            st.rect(height=400) # Placeholder caso a imagem falhe
            
    with col_txt:
        st.markdown("""
        <div class='poesia-text'>
            <b>O TEMPO RECOBRADO</b><br><br>
            A máquina não pensa,<br>
            ela apenas recorda<br>
            o que o silêncio dita<br>
            e a memória transborda.<br><br>
            <i>... processando rima ...</i>
        </div>
        """, unsafe_allow_html=True)
else:
    # Carregamento dos Manuais para as outras páginas
    st.markdown(f"### {current}")
    st.info(f"Conteúdo de MANUAL_{current.upper()}.MD será renderizado aqui.")

# --- 5. FOOTER ---
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; font-weight: 900; font-size: 11px; letter-spacing: 2px;'>INSTAGRAM • GITHUB • LINKEDIN</div>", unsafe_allow_html=True)
