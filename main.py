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

    /* ESTILO DOS TOGGLES (Cores e Alinhamento) */
    div[data-testid="stCheckbox"] { margin-bottom: 5px !important; }
    
    /* BOTÕES CIRCULARES DO PALCO (Negrito Profundo) */
    .st-key-palco_btns div.stButton > button {
        background-color: #f0f2f6 !important;
        color: #000000 !important;
        border-radius: 50% !important;
        width: 36px !important;
        height: 36px !important;
        border: 2px solid #000000 !important;
        font-size: 20px !important;
        font-weight: 900 !important;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0px !important;
    }

    /* INFO BOX: Estética de Nota de Rodapé ou Dicionário */
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

    /* REDES SOCIAIS: Negrito e Espaçamento */
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
        max-width: 800px !important;
        margin: 0 auto !important;
        padding-top: 1.5rem !important;
    }
    
    hr { border: 0; height: 1px; background: #ddd; margin: 15px 0 !important; }
    
    /* Ajuste para o selectbox não ter label */
    label { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR: CONSOLE DE COMANDO ---
with st.sidebar:
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    
    # A. IDIOMAS: Elite List no topo
    elite_langs = ["Português", "Español", "Italiano", "Français", "English", "Català"]
    outros_langs = ["Deutsch", "Nederlands", "Polski", "Svenska", "Dansk", "Suomi"]
    st.selectbox("Idiomas", elite_langs + outros_langs, key="sb_idiomas")
    
    st.markdown("---")

    # B. TOGGLES: Talk, Draw, Vídeo
    st.toggle("TALK (Voz)", key="tg_talk")
    st.toggle("DRAW (Imagem)", key="tg_draw")
    st.toggle("VÍDEO (Motion)", key="tg_video")

    st.markdown("---")

    # C. INFO PÁGINA (Contexto Dinâmico)
    st.markdown("""
    <div class='info-box'>
        <b>Status da Página:</b><br>
        Processando matriz rítmica. Sincronia de tradução ativa para os idiomas de elite.
    </div>
    """, unsafe_allow_html=True)
    
    # D. ARTE DA PÁGINA (Identidade)
    # Aqui entra o componente que carrega a arte do ypo_seguro
    st.image("https://via.placeholder.com/300x200.png?text=ARTE+DA+PÁGINA", use_container_width=True)

    st.markdown("---")

    # E. FOOTER: Redes Sociais
    st.markdown("""
    <div class='social-links'>
        <a href='#'>INSTAGRAM</a> • <a href='#'>GITHUB</a> • <a href='#'>LINKEDIN</a>
    </div>
    """, unsafe_allow_html=True)

# --- 3. PALCO: BARRA DE COMANDO CENTRALIZADA ---
_, col_barra, _ = st.columns([0.6, 2.8, 0.6])

with col_barra:
    c_btns, c_lista = st.columns([2.0, 1.0])
    
    with c_btns:
        st.markdown("<div class='st-key-palco_btns'>", unsafe_allow_html=True)
        n1, n2, n3, n4, n5 = st.columns(5)
        n1.button("＋", key="p_add") 
        n2.button("＜", key="p_prev")
        n3.button("＊", key="p_star")
        n4.button("＞", key="p_next")
        n5.button("？", key="p_help")
        st.markdown("</div>", unsafe_allow_html=True)

    with c_lista:
        try:
            arquivos = [f.replace(".ypo", "") for f in os.listdir("data") if f.endswith(".ypo")]
            st.selectbox("Temas", arquivos, key="p_temas")
        except:
            st.write("data/")

st.markdown("<hr>", unsafe_allow_html=True)

# --- 4. ÁREA DE CONTEÚDO ---
st.markdown("""
<div style='text-align: center; color: #888; font-family: Georgia; margin-top: 40px; font-style: italic;'>
    O Palco está centralizado e aguarda a entrada dos versos.
</div>
""", unsafe_allow_html=True)
