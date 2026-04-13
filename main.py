import streamlit as st
import os

# --- 1. CONFIGURAÇÃO DE HARDWARE VIRTUAL ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
    <style>
    /* DESATIVAR HEADER PADRÃO E FIXAR SIDEBAR */
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stSidebar"] { min-width: 320px !important; max-width: 320px !important; }

    /* BOTÕES CIRCULARES DO PALCO (Console de 6 Unidades) */
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
        padding: 0px !important;
    }

    /* INFO BOX: Estética de Dicionário na Sidebar */
    .info-box {
        font-family: 'Georgia', serif;
        font-size: 13px;
        line-height: 1.5;
        color: #222;
        background: #fdfdfd;
        padding: 12px;
        border-left: 4px solid #000;
        margin: 15px 0;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }

    /* REDES SOCIAIS */
    .social-links { 
        font-size: 11px; 
        font-weight: 900; 
        text-align: center; 
        margin-top: 20px;
        letter-spacing: 1px;
    }
    .social-links a { color: #000; text-decoration: none; margin: 0 8px; }

    /* PALCO: Centralização dinâmica */
    .main .block-container {
        max-width: 850px !important;
        margin: 0 auto !important;
        padding-top: 1.5rem !important;
    }
    
    hr { border: 0; height: 1px; background: #ddd; margin: 15px 0 !important; }
    label { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR: CONSOLE DE COMANDO ---
with st.sidebar:
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    
    # A. IDIOMAS: Elite + Western
    elite = ["Português", "Español", "Italiano", "Français", "English", "Català"]
    western = ["Deutsch", "Nederlands", "Polski", "Svenska", "Latin", "Română"]
    st.selectbox("Idiomas", elite + western, key="sb_idiomas")
    
    st.markdown("---")

    # B. TOGGLES
    st.toggle("TALK (Voz)", key="tg_talk")
    st.toggle("DRAW (Imagem)", key="tg_draw")
    st.toggle("VÍDEO (Motion)", key="tg_video")

    st.markdown("---")

    # C. INFO PÁGINA
    st.markdown("""
    <div class='info-box'>
        <b>Status da Página:</b><br>
        Processando matriz rítmica. Sincronia de tradução ativa para os idiomas de elite.
    </div>
    """, unsafe_allow_html=True)
    
    # D. ARTE DA PÁGINA (Sintaxe 2026: width='stretch')
    if os.path.exists("img_demo.jpg"):
        st.image("img_demo.jpg", width='stretch')
    else:
        st.image("https://via.placeholder.com/300x200.png?text=ARTE+DA+PÁGINA", width='stretch')

    st.markdown("---")

    # E. FOOTER
    st.markdown("""
    <div class='social-links'>
        <a href='#'>INSTAGRAM</a> • <a href='#'>GITHUB</a> • <a href='#'>LINKEDIN</a>
    </div>
    """, unsafe_allow_html=True)

# --- 3. PALCO: BARRA DE COMANDO CENTRALIZADA ---
_, col_barra, _ = st.columns([0.4, 3.2, 0.4])

with col_barra:
    c_btns, c_lista = st.columns([2.2, 1.0])
    
    with c_btns:
        st.markdown("<div class='st-key-palco_btns'>", unsafe_allow_html=True)
        # O Console de 6 botões fiel ao retrato
        n1, n2, n3, n4, n5, n6 = st.columns(6)
        n1.button("＋", key="p_add")   # Novo
        n2.button("＜", key="p_prev")  # Ant
        n3.button("＊", key="p_star")  # Aleat
        n4.button("＞", key="p_next")  # Prox
        n5.button("☐", key="p_auto")  # Auto
        n6.button("？", key="p_help")  # Help
        st.markdown("</div>", unsafe_allow_html=True)

    with c_lista:
        try:
            arquivos = [f.replace(".ypo", "") for f in os.listdir("data") if f.endswith(".ypo")]
            st.selectbox("Temas", arquivos if arquivos else ["Padrão"], key="p_temas")
        except:
            st.selectbox("Temas", ["Proust", "Urbano"], key="p_temas_fallback")

st.markdown("<hr>", unsafe_allow_html=True)

# --- 4. ÁREA DE CONTEÚDO ---
st.markdown("""
<div style='text-align: center; color: #1a1a1a; font-family: Georgia; margin-top: 40px; font-style: italic;'>
    O Palco está centralizado e aguarda a entrada dos versos da Máquina.
</div>
""", unsafe_allow_html=True)
