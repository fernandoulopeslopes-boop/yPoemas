import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import os

# Configuração da página
st.set_page_config(page_title="a Máquina de Fazer Poesia", layout="wide")

# CSS para customização da Sidebar (300px, texto justificado e centralizado)
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        width: 300px;
    }
    [data-testid="stSidebar"] .stMarkdown {
        text-align: justify;
    }
    .stButton button {
        width: 100%;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# 1. SIDEBAR (TODO [TEST] - REVISADO)
with st.sidebar:
    # ITEM 1: Dropdown list com os idiomas do PCC no topo
    idiomas_pcc = [
        "Português", "Español", "Italiano", "Français", "English", 
        "Català", "Deutsch", "Nederlands", "Dansk", "Svenska", "Norsk"
    ]
    st.selectbox("PCC - Idioma", idiomas_pcc, label_visibility="collapsed")
    
    st.markdown("---")
    
    # ITEM 3: radio_chk []som []arte []vídeo
    # Nota: Substitui os antigos botões de áudio, imagem e vídeo
    modo_exibicao = st.radio(
        "Modo",
        ["[]som", "[]arte", "[]vídeo"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # ITEM 4: Navegação (Restante da sidebar)
    if st.button("mini"):
        st.session_state.page = "mini"
    if st.button("yPoemas"):
        st.session_state.page = "ypoemas"
    if st.button("eureka"):
        st.session_state.page = "eureka"
    if st.button("books"):
        st.session_state.page = "books"
    if st.button("comments"):
        st.session_state.page = "comments"
    if st.button("about"):
        st.session_state.page = "about"

# 2. ÁREA PRINCIPAL
# Botões de interação no topo da tela conforme planejado
col1, col2 = st.columns(2)
with col1:
    if st.button("💬 Talk"):
        st.write("Iniciando interação por voz...")
with col2:
    if st.button("🎨 Arts"):
        st.write("Exibindo galeria de artes...")

st.title("a Máquina de Fazer Poesia")

# Lógica de conteúdo (Removendo elementos de vídeo conforme instrução)
if modo_exibicao == "[]vídeo":
    st.info("O suporte a vídeo foi removido para manter a interface leve.")
elif modo_exibicao == "[]arte":
    st.write("Área de visualização artística.")
else:
    st.write("Área de áudio/poesia.")

# O restante do código de processamento de tradução e gTTS segue aqui...
