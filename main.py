import streamlit as st
import os
import random
from gtts import gTTS
from deep_translator import GoogleTranslator
import base64

# CONFIGURAÇÃO DO PALCO (O.V.N.I.)
st.set_page_config(page_title="Machina de Fazer Poesia", layout="wide", initial_sidebar_state="expanded")

# --- LINHA ZERO: CARREGAMENTO DE ATIVOS ---
@st.cache_data
def carregar_base(arquivo):
    path = os.path.join("base", arquivo)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().splitlines()
    return []

def get_video_base64(page_name):
    video_path = os.path.join("base", f"video_{page_name}.webm")
    if os.path.exists(video_path):
        with open(video_path, "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode()
    return None

# --- O MOTOR: O ÍTIMO E O EIXO Z ---
def gera_ypoema(tema_selecionado):
    # Aqui reside a inteligência de 1983 (resumida para o teste)
    # O Protocolo exige que as regras de concordância e rima operem aqui
    linhas = carregar_base(f"{tema_selecionado}.txt")
    if not linhas:
        return "O vácuo não contém palavras no momento."
    
    # Simulação do Franco-Atirador (Eixo Z)
    corpo = random.sample(linhas, min(len(linhas), 5))
    return "\n".join(corpo)

# --- SIDEBAR: O COCKPIT DE PREFERÊNCIAS ---
with st.sidebar:
    st.title("📟 Painel de Controle")
    st.subheader("Configurações do Observador")
    
    draw = st.checkbox("🎨 Artes (Draw)", value=True)
    talk = st.checkbox("🎙️ Áudio (Talk)", value=False)
    vyde = st.checkbox("🎬 Vídeo (Vyde)", value=False)
    
    st.divider()
    idioma = st.selectbox("🌐 Idioma", ["pt", "en", "es", "fr", "it"])
    
    st.info("O cockpit pode ser recolhido para foco total no Palco.")

# --- O PALCO CENTRAL ---
tabs = st.tabs(["🛸 Mini", "📜 yPoemas", "💡 Eureka", "📚 Biblioteca"])

for i, tab in enumerate(tabs):
    tab_names = ["mini", "ypoemas", "eureka", "biblioteca"]
    current_tab = tab_names[i]
    
    with tab:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.button(f"Disparar Franco-Atirador ({current_tab})", key=f"btn_{current_tab}"):
                poema = gera_ypoema(current_tab)
                
                # Tradução (Se necessário)
                if idioma != "pt":
                    poema = GoogleTranslator(source='pt', target=idioma).translate(poema)
                
                st.markdown(f"### {current_tab.upper()}")
                st.write(poema)
                
                # Resposta aos Sensores da Sidebar
                if talk:
                    tts = gTTS(poema, lang=idioma)
                    tts.save("speech.mp3")
                    st.audio("speech.mp3")
                
                if draw:
                    st.image("https://placekitten.com/800/400", caption="Arte Gerada pelo Ítimo") # Exemplo de placeholder

        with col2:
            if vyde:
                video_data = get_video_base64(current_tab)
                if video_data:
                    st.video(f"data:video/webm;base64,{video_data}")
                else:
                    st.warning(f"Vídeo de instrução ({current_tab}) não localizado.")

# --- RODAPÉ DO PROTOCOLO ---
st.caption("Machina de Fazer Poesia | 1983 - 2026 | Protocolo Linha Zero Ativo")
