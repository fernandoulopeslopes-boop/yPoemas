import os
import random
import base64
import streamlit as st
from lay_2_ypo import gera_poema

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="yPoemas", layout="centered")

st.markdown("""
    <style>
    /* Fixa a largura da sidebar em 300px */
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child {
        width: 300px;
    }
    /* Estética do Poema */
    .poema-box {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        font-family: 'serif';
        font-size: 1.3rem;
        color: #1a1a1a;
        line-height: 1.7;
    }
    </style>
""", unsafe_allow_html=True)

# --- ESTADOS DE SESSÃO ---
if "lang" not in st.session_state: st.session_state.lang = "pt"
if "take" not in st.session_state: st.session_state.take = 0
if "draw" not in st.session_state: st.session_state.draw = False
if "talk" not in st.session_state: st.session_state.talk = False

# --- COMPONENTES ---

def get_ui_labels():
    labels = {
        "pt": ["Anterior", "Acaso", "Próximo", "Ajuda", "🎨 Imagem", "🔊 Áudio"],
        "en": ["Previous", "Random", "Next", "Help", "🎨 Art", "🔊 Talk"],
        "es": ["Anterior", "Azar", "Próximo", "Ayuda", "🎨 Imagen", "🔊 Áudio"]
    }
    return labels.get(st.session_state.lang, labels["pt"])

def build_sidebar():
    with st.sidebar:
        st.write("### yPoemas")
        
        # Idiomas
        st.write("---")
        cols = st.columns(5)
        langs = ["pt", "es", "it", "fr", "en"]
        for i, l in enumerate(langs):
            if cols[i].button(l, key=f"lang_{l}"):
                st.session_state.lang = l
                st.rerun()
        
        st.write("---")
        # Navegação
        page = st.radio("Navegação", ["yPoemas", "Mini", "Eureka"])
        
        st.write("---")
        # Sentidos
        labels = get_ui_labels()
        st.session_state.draw = st.checkbox(labels[4], st.session_state.draw)
        st.session_state.talk = st.checkbox(labels[5], st.session_state.talk)
        
        return page

def page_ypoemas():
    labels = get_ui_labels()
    
    # 1. Barra de Navegação Superior (Navegação, Acaso, Help)
    c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
    
    if c1.button(f"⬅️ {labels[0]}"):
        st.session_state.take -= 1
    if c2.button(f"🎲 {labels[1]}"):
        st.session_state.take = random.randint(0, 1000)
    if c3.button(f"➡️ {labels[2]}"):
        st.session_state.take += 1
    
    with c4:
        with st.expander(f"❓ {labels[3]}"):
            st.write("Use as setas para navegar entre as variações temáticas ou o dado para saltar no acaso.")

    st.write("---")

    # 2. Geração de Conteúdo
    tema = "Fatos" # Exemplo fixo para visualização
    poema_raw = gera_poema(tema, "")
    poema_html = "<br>".join(poema_raw)

    # 3. Exibição: Texto e Imagem
    if st.session_state.draw:
        col_txt, col_img = st.columns([1.5, 1])
        with col_txt:
            st.markdown(f"<div class='poema-box'>{poema_html}</div>", unsafe_allow_html=True)
        with col_img:
            # Placeholder para imagem da Machina
            st.image("https://via.placeholder.com/400x600.png?text=Machina+Art", use_container_width=True)
    else:
        st.markdown(f"<div class='poema-box'>{poema_html}</div>", unsafe_allow_html=True)

# --- EXECUÇÃO ---

current_page = build_sidebar()

if current_page == "yPoemas":
    page_ypoemas()
elif current_page == "Mini":
    st.info("Página Mini: Próxima da sequência.")
elif current_page == "Eureka":
    st.info("Página Eureka: Aguardando.")
