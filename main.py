import streamlit as st
import os
import random
import base64
from gtts import gTTS
from deep_translator import GoogleTranslator

# --- CONFIGURAÇÃO ESTÉTICA (A ASSINATURA DA MACHINA) ---
st.set_page_config(page_title="Machina de Fazer Poesia", layout="wide", initial_sidebar_state="collapsed")

# CSS para garantir a endentação e a "mancha gráfica" correta do yPoema
st.markdown("""
    <style>
    .yPoema {
        font-family: 'Courier New', Courier, monospace;
        line-height: 1.6;
        padding-left: 10%;
        white-space: pre-wrap;
    }
    .stButton>button { width: 100%; border-radius: 0; background-color: #1e1e1e; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- ENGINE: O PROTOCOLO DO ÍTIMO ---
@st.cache_data
def carregar_itimos(tema):
    path = f"base/{tema}.txt"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().splitlines()
    return []

def disparar_franco_atirador(tema):
    # Onde a "Tosquice" morre e o Eixo Z nasce
    dados = carregar_itimos(tema)
    if not dados: return "Vácuo detectado."
    
    # Aqui reinaremos com as regras de concordância em breve
    # Por enquanto, garantimos a estrutura de blocos do Protocolo
    estrofe = random.sample(dados, min(len(dados), 4))
    return "\n".join(estrofe)

# --- SIDEBAR (O COCKPIT RECOLHÍVEL) ---
with st.sidebar:
    st.header("🛸 O.V.N.I. Command")
    draw = st.toggle("🎨 Artes", value=True)
    talk = st.toggle("🎙️ Talk", value=False)
    vyde = st.toggle("🎬 Vyde", value=False)
    idioma = st.selectbox("Idioma", ["pt", "en", "es", "fr"])
    st.divider()
    st.caption("Protocolo 1983-2026 Ativo")

# --- O PALCO (TABS SEM RUÍDO) ---
abas = ["Mini", "yPoemas", "Eureka", "Biblioteca"]
tabs = st.tabs(abas)

for nome_aba, tab in zip(abas, tabs):
    tema = nome_aba.lower()
    with tab:
        col_txt, col_mid = st.columns([2, 1])
        
        with col_txt:
            if st.button(f"GERAR {nome_aba.upper()}", key=f"btn_{tema}"):
                poema_bruto = disparar_franco_atirador(tema)
                
                # Processamento de Tradução
                texto_final = poema_bruto
                if idioma != "pt":
                    texto_final = GoogleTranslator(source='pt', target=idioma).translate(poema_bruto)
                
                # Exibição com a Estética da Machina
                st.markdown(f'<div class="yPoema">{texto_final}</div>', unsafe_allow_html=True)
                
                if talk:
                    speech = gTTS(text=texto_final, lang=idioma)
                    speech.save("temp.mp3")
                    st.audio("temp.mp3")
        
        with col_mid:
            if vyde:
                # Busca o vídeo correspondente na base
                v_path = f"base/video_{tema}.webm"
                if os.path.exists(v_path):
                    st.video(v_path)
