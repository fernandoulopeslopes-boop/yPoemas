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
    /* Limpeza e Layout */
    footer {visibility: hidden;}
    [data-testid='stSidebar'] > div:first-child { width: 310px; }
    
    /* Estilo dos Botões de Navegação */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #f0f2f6;
        border: 1px solid #d1d5db;
        color: #374151;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        border-color: #ff4b4b;
        color: #ff4b4b;
        background-color: #ffffff;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }

    /* Texto e Imagem do Poema */
    .logo-text {
        font-weight: 600; font-size: 19px; font-family: 'IBM Plex Sans', sans-serif;
        color: #1a1a1a; padding-left: 15px; text-align: left;
        display: block; line-height: 1.7; white-space: pre-wrap !important;
    }
    .logo-img { 
        float: right; max-width: 350px; margin-left: 20px; 
        border-radius: 10px; box-shadow: 2px 2px 15px rgba(0,0,0,0.1);
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
# 3. MOTOR: GERAÇÃO E TRADUÇÃO
# =================================================================
def load_poema(nome_tema):
    try:
        # AGORA COM OS 2 PARÂMETROS: (Tema, Semente)
        # semente="" garante que ele retorne apenas o ypoema
        semente_eureka = "" 
        
        script = gera_poema(nome_tema, semente_eureka)
        
        if not script or not isinstance(script, list):
            return "A Machina está processando... <br> (Aguardando resposta do lexico)"
            
        return "<br>".join([str(line).strip() for line in script if str(line).strip()])
    
    except Exception as e:
        return f"Erro de Sincronia no Motor: {str(e)} <br> Tema: {nome_tema}"
        
def translate(text):
    if st.session_state.lang == "pt": return text
    try:
        from deep_translator import GoogleTranslator
        return GoogleTranslator(source='pt', target=st.session_state.lang).translate(text)
    except: return text

def load_arts(nome_tema):
    # Caminho padrão das suas artes
    pasta_artes = "images/machina"
    
    # Tenta encontrar uma imagem com o nome do tema (ex: Fatos.jpg)
    foto_tema = os.path.join(pasta_artes, f"{nome_tema}.jpg")
    
    if os.path.exists(foto_tema):
        return foto_tema
    
    # Se não houver arte específica, usa o logo padrão
    fallback = os.path.join(pasta_artes, "logo_ypoemas.jpg")
    return fallback if os.path.exists(fallback) else None

# =================================================================
# 4. EXPOSIÇÃO: FUNÇÃO DE ESCRITA
# =================================================================
def write_ypoema(LOGO_TEXTO, LOGO_IMAGE):
    if LOGO_IMAGE and os.path.exists(LOGO_IMAGE):
        with open(LOGO_IMAGE, "rb") as img_file:
            img_b64 = base64.b64encode(img_file.read()).decode()
        st.markdown(f"""
            <div class='container'>
                <img class='logo-img' src='data:image/jpg;base64,{img_b64}'>
                <p class='logo-text'>{LOGO_TEXTO}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"<p class='logo-text'>{LOGO_TEXTO}</p>", unsafe_allow_html=True)

# =================================================================
# 5. SALAS: INTERFACE MODULAR
# =================================================================


# =================================================================
# 5. SALAS: INTERFACE MINIMALISTA
# =================================================================

def page_mini():
    # Apenas o essencial: O motor e o verso
    exibir_conteudo()

def page_ypoemas():
    # Sala com o controle de sorteio manual
    col1, b_rand, col2 = st.columns([4, 2, 4])
    
    if b_rand.button("✻ SORTEAR NOVO", help="Gera uma variação aleatória"):
        temas_list = load_temas(st.session_state.book)
        st.session_state.take = random.randrange(len(temas_list))
        st.rerun()
    
    temas_list = load_temas(st.session_state.book)
    st.session_state.tema = temas_list[st.session_state.take % len(temas_list)]
    exibir_conteudo()

def exibir_conteudo():
    # O coração visual: Poema + Imagem
    poema_raw = load_poema(st.session_state.tema)
    if st.session_state.lang != "pt":
        poema_raw = translate(poema_raw)
    
    texto_final = "  \n".join(poema_raw.split('<br>'))
    img_final = load_arts(st.session_state.tema) if st.session_state.draw == 'Y' else None
    write_ypoema(texto_final, img_final)

# =================================================================
# 6. METAS: EXECUÇÃO PRINCIPAL (RADIO E LOGICA)
# =================================================================
def main():
    with st.sidebar:
        st.title("yPoemas")
        
        # O Rádio: O único seletor de destino
        sala = st.radio("Selecione o modo:", ["Leitura (Mini)", "Exploração (Rand)"])
        
        st.divider()
        # Seletor de Idioma simples no Paiol
        st.session_state.lang = st.selectbox("Traduzir para:", ["pt", "en", "es", "fr", "it"])
        st.write(f"ID: {st.session_state.user_id}")

    # Roteamento baseado no Rádio
    if sala == "Leitura (Mini)":
        page_mini()
    else:
        page_ypoemas()

if __name__ == "__main__":
    main()
    
