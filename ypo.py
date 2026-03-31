# =================================================================
# 🚀 MACHINA DE FAZER POESIA (ABNP) - Versão 2.0 (Estruturada)
# =================================================================
import streamlit as st
import os
import random
import socket
import base64
from PIL import Image

# --- MOTORES EXTERNOS (Certifique-se que lay_2_ypo.py está na mesma pasta) ---
try:
    from lay_2_ypo import gera_poema
except ImportError:
    def gera_poema(tema, seed=""): return ["Erro: motor lay_2_ypo não encontrado."]

# =================================================================
# 1. LENTE: CONFIGURAÇÃO E VISUAL (CSS)
# =================================================================
st.set_page_config(
    page_title="a Machina de fazer Poesia",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* 1. Reset e Fundo */
    .main { background-color: #fcfcfc; }
    
    /* 2. O Cartão da Poesia (State of the Art) */
    .poem-card {
        background: white;
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
        margin-top: 20px;
        display: flex;
        flex-direction: row;
        align-items: flex-start;
    }

    /* 3. Tipografia Refinada */
    .logo-text {
        font-family: 'Georgia', serif;
        font-size: 22px;
        color: #2c3e50;
        line-height: 1.8;
        flex: 1;
        padding-right: 20px;
    }

    .logo-img { 
        max-width: 300px; 
        border-radius: 8px;
        filter: sepia(20%); /* Toque artístico */
    }
    </style>
""", unsafe_allow_html=True)

# =================================================================
# 2. PAIOL: INICIALIZAÇÃO E CARREGADORES (CACHE)
# =================================================================
if "initialized" not in st.session_state:
    st.session_state.lang = 'pt'
    st.session_state.tema = 'Fatos'
    st.session_state.book = "livro vivo"
    st.session_state.take = 0
    st.session_state.draw = 'Y'
    try:
        st.session_state.user_id = socket.gethostbyname(socket.gethostname())
    except:
        st.session_state.user_id = "user_88"
    st.session_state.initialized = True

@st.cache_data
def load_temas(book):
    book_list = []
    caminho = os.path.join("base", "rol_" + book + ".txt")
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as file:
            for line in file:
                tema_limpo = line.replace(" ", "").strip()
                if tema_limpo: book_list.append(tema_limpo)
    return book_list if book_list else ["Fatos"]

# =================================================================
# 3. UTILIDADES: O PAIOL DA MACHINA
# =================================================================

# =================================================================
# 2.5 TRADUTOR: O SOPRO POLIGLOTA
# =================================================================

def translate(texto):
    # Se o idioma for Português, não faz nada
    if st.session_state.lang == "pt":
        return texto
    
    try:
        from deep_translator import GoogleTranslator
        # Traduz do Português para o idioma selecionado no Sidebar
        traduzido = GoogleTranslator(source='pt', target=st.session_state.lang).translate(texto)
        return traduzido
    except Exception as e:
        # Se a tradução falhar, mantém o original para não travar a Machina
        return texto

def load_poema(nome_tema):
    try:
        script = gera_poema(nome_tema, "")
        if not script or not isinstance(script, list):
            return "A Machina processa em silêncio..."
        return "<br>".join([str(line).strip() for line in script if str(line).strip()])
    except Exception as e:
        return f"Erro de Sincronia: {str(e)}"

def load_arts(nome_tema):
    # Testamos os caminhos mais comuns no Linux/Railway
    caminhos_possiveis = [
        f"images/machina/{nome_tema}.jpg",
        f"Images/machina/{nome_tema}.jpg",
        f"images/machina/logo_ypoemas.jpg"
    ]
    for caminho in caminhos_possiveis:
        if os.path.exists(caminho):
            return caminho
    return None

def falar_poema(texto, lang):
    try:
        from gtts import gTTS
        import io
        tts = gTTS(text=texto.replace('<br>', ' '), lang=lang)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        return fp
    except: return None

# =================================================================
# 4. LENTE: RENDERIZAÇÃO (TEXTO GRANDE + IMAGEM)
# =================================================================

def write_ypoema(TITULO, TEXTO_RAW):
    # CSS focado em preservar a estrutura do Soneto e aumentar a letra
    st.markdown(f"""
        <style>
        /* 1. Expansão da tela */
        .block-container {{
            padding: 2rem 5rem !important;
            max-width: 100% !important;
        }}
        
        /* 2. O Container do Poema */
        .poem-box {{
            font-family: 'IBM Plex Sans', sans-serif;
            background-color: transparent;
            text-align: left;
            width: 100%;
        }}

        /* 3. O Título (Destaque) */
        .poem-title {{
            font-size: 34px;
            font-weight: 700;
            color: #333;
            margin-bottom: 40px;
            letter-spacing: 2px;
            text-transform: uppercase;
        }}

        /* 4. O Texto (Preservando Espaços e Quebras) */
        .poem-content {{
            font-weight: 600;
            font-size: 32px !important; /* LETRA GRANDE PARA MONITOR */
            line-height: 1.5;
            color: #000;
            /* O SEGREDO: pre-line respeita as quebras de linha do seu texto Python */
            white-space: pre-line !important; 
            display: block;
        }}
        </style>
        
        <div class='poem-box'>
            <div class='poem-title'>{TITULO}</div>
            <div class='poem-content'>{TEXTO_RAW}</div>
        </div>
    """, unsafe_allow_html=True)        
# =================================================================
# 5. SALA: YPOEMAS (CONTROLE COMPLETO)
# =================================================================

def write_ypoema(TITULO, TEXTO_RAW):
    # CSS para dar peso ao título e liberdade aos versos
    st.markdown(f"""
        <style>
        .block-container {{
            padding: 3rem 5rem !important;
            max-width: 100% !important;
        }}
        
        /* TÍTULO: Agora realmente grande e visível */
        .poem-title {{
            font-family: 'IBM Plex Sans', sans-serif;
            font-size: 42px !important; /* Tamanho de destaque */
            font-weight: 800;
            color: #222;
            margin-bottom: 50px;
            letter-spacing: 2px;
            border-bottom: 3px solid #f0f0f0;
            padding-bottom: 10px;
            display: block;
        }}

        /* CORPO DO POEMA: Respeita Minúsculas e Espaços */
        .poem-content {{
            font-family: 'IBM Plex Sans', sans-serif;
            font-weight: 600;
            font-size: 36px !important; 
            line-height: 1.6;
            color: #000;
            /* pre-wrap mantém as quebras de linha e espaços em branco */
            white-space: pre-wrap !important; 
            text-transform: none !important; /* GARANTE QUE NÃO FIQUE TUDO EM MAIÚSCULO */
        }}
        </style>
        
        <div class='poem-title'>{TITULO}</div>
        <div class='poem-content'>{TEXTO_RAW}</div>
    """, unsafe_allow_html=True)
    
# =================================================================
# 6. METAS: EXECUÇÃO
# =================================================================

def main():
    with st.sidebar:
        st.title("yPoemas")
        sala = st.radio("Navegar:", ["Exploração (Rand)", "Sobre a Machina"])
        st.divider()
        st.session_state.lang = st.selectbox("Idioma:", ["pt", "en", "es", "fr", "it"])
        st.session_state.draw = 'Y' # Ativado para testarmos

    #if sala == "Exploração (Rand)":
        page_ypoemas()
    #else:
    #   st.info("Sala Sobre a Machina")

if __name__ == "__main__":
    main()
    
