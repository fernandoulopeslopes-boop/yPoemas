import streamlit as st
import os
import random
import socket
import base64

# 1. CONFIGURAÇÃO DA PÁGINA (WIDE E SIDEBAR)
st.set_page_config(page_title="a Machina de fazer Poesia", layout="wide", initial_sidebar_state="expanded")

# --- MOTORES EXTERNOS ---
try:
    from lay_2_ypo import gera_poema
except ImportError:
    def gera_poema(tema, seed=""): return ["Erro: motor lay_2_ypo não encontrado."]

def translate(texto): # Placeholder para não dar erro
    return texto 

# 3. PAIOL E UTILITÁRIOS
if "initialized" not in st.session_state:
    st.session_state.lang, st.session_state.tema, st.session_state.take = 'pt', 'Fatos', 0
    st.session_state.book, st.session_state.initialized = "livro vivo", True

@st.cache_data(show_spinner=False)

def load_temas(book):
    caminho = os.path.join("base", f"rol_{book}.txt")
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return ["Fatos"]

def load_poema(nome_tema):
    script = gera_poema(nome_tema, "")
    if isinstance(script, list): return "\n".join([str(l) for l in script if l])
    return str(script)

def load_arts(nome_tema): # Placeholder para o Help/Matrix
    return None

# 4. A SALA (YPOEMAS)
def write_ypoema(TITULO, TEXTO_RAW):
    # O segredo para as etiquetas sumirem é o unsafe_allow_html=True no final
    st.markdown(f"""
        <style>
        /* Ajuste de margens da página */
        .block-container {{ 
            padding: 2rem 5rem !important; 
            max-width: 100% !important; 
        }}
        
        /* Estilo do Título (42px) */
        .poem-title {{
            font-family: 'IBM Plex Sans', sans-serif;
            font-size: 42px !important;
            font-weight: 800;
            color: #222;
            margin-bottom: 30px;
            border-bottom: 3px solid #f0f0f0;
            padding-bottom: 10px;
            text-transform: uppercase;
        }}
        
        /* Estilo do Corpo (36px) */
        .poem-content {{
            font-family: 'IBM Plex Sans', sans-serif;
            font-weight: 600;
            font-size: 36px !important;
            line-height: 1.6;
            color: #000;
            white-space: pre-wrap !important; /* Mantém o respiro das linhas */
            text-transform: none !important;  /* Respeita as minúsculas */
        }}
        </style>
        
        <div class='poem-title'>{TITULO}</div>
        <div class='poem-content'>{TEXTO_RAW}</div>
    """, unsafe_allow_html=True)
    
# --- FINAL DA FUNÇÃO PAGE_YPOEMAS ---
    
    # 1. Preparação do Título e do Texto
    titulo_limpo = st.session_state.tema.upper()
    corpo_poema = poema_raw

    # 2. O ÚNICO comando que deve imprimir o poema na tela:
    st.markdown(f"""
        <style>
        .poem-title {{
            font-family: 'IBM Plex Sans', sans-serif;
            font-size: 42px !important;
            font-weight: 800;
            color: #222;
            margin-bottom: 30px;
            border-bottom: 3px solid #f0f0f0;
            padding-bottom: 10px;
        }}
        .poem-content {{
            font-family: 'IBM Plex Sans', sans-serif;
            font-weight: 600;
            font-size: 36px !important;
            line-height: 1.6;
            color: #000;
            white-space: pre-wrap !important;
        }}
        </style>
        
        <div class='poem-title'>{titulo_limpo}</div>
        <div class='poem-content'>{corpo_poema}</div>
    """, unsafe_allow_html=True)

# 5. O MOTOR (MAIN)
def main():
    with st.sidebar:
        st.title("yPoemas")
        sala = st.radio("Navegar:", ["Exploração", "Sobre"])
    if sala == "Exploração": page_ypoemas()
    else: st.write("### Sobre a Machina")

if __name__ == "__main__":
    main()
