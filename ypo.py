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

# =================================================================
# 3. UTILIDADES: O PAIOL DA MACHINA
# =================================================================

def load_poema(nome_tema):
    try:
        # Envia Tema e Semente Vazia para o seu motor externo
        script = gera_poema(nome_tema, "")
        if not script or not isinstance(script, list):
            return "A Machina processa em silêncio... <br> Verifique a base de dados."
        return "<br>".join([str(line).strip() for line in script if str(line).strip()])
    except Exception as e:
        return f"Erro de Sincronia: {str(e)}"

def load_arts(nome_tema):
    # Ajuste o caminho para a sua pasta de imagens no Railway
    pasta = "images/machina"
    foto = os.path.join(pasta, f"{nome_tema}.jpg")
    if os.path.exists(foto):
        return foto
    # Fallback para o logo se a arte do tema não existir
    logo = os.path.join(pasta, "logo_ypoemas.jpg")
    return logo if os.path.exists(logo) else None

def falar_poema(texto, lang):
    try:
        from gtts import gTTS
        import io
        tts = gTTS(text=texto.replace('<br>', ' '), lang=lang)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        return fp
    except:
        return None

# =================================================================
# 4. LENTE: RENDERIZAÇÃO (STATE OF THE ART)
# =================================================================

def write_ypoema(LOGO_TEXTO, LOGO_IMAGE):
    # CSS interno para garantir o layout de "Cartão"
    st.markdown("""
        <style>
        .poem-card {
            background: white; padding: 40px; border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05); border: 1px solid #f0f0f0;
            display: flex; gap: 30px; align-items: flex-start; margin-top: 10px;
        }
        .logo-text { font-family: 'Georgia', serif; font-size: 20px; line-height: 1.8; color: #2c3e50; flex: 1.5; }
        .logo-img { flex: 1; max-width: 320px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        @media (max-width: 768px) { .poem-card { flex-direction: column; } .logo-img { max-width: 100%; } }
        </style>
    """, unsafe_allow_html=True)

    if LOGO_IMAGE and os.path.exists(LOGO_IMAGE):
        with open(LOGO_IMAGE, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <div class='poem-card'>
                <div class='logo-text'>{LOGO_TEXTO}</div>
                <img class='logo-img' src='data:image/jpg;base64,{img_b64}'>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='poem-card'><div class='logo-text'>{LOGO_TEXTO}</div></div>", unsafe_allow_html=True)

# =================================================================
# 5. SALA: YPOEMAS (EXPLORAÇÃO)
# =================================================================

def page_ypoemas():
    temas_list = load_temas(st.session_state.book)
    
    # Painel de Controle Superior
    c1, b_back, b_rand, b_next, b_voice, c2 = st.columns([2, 1, 1, 1, 1, 2])
    
    if b_back.button("◀"):
        st.session_state.take = (st.session_state.take - 1) % len(temas_list)
        st.rerun()
    if b_rand.button("✻"):
        st.session_state.take = random.randrange(len(temas_list))
        st.rerun()
    if b_next.button("▶"):
        st.session_state.take = (st.session_state.take + 1) % len(temas_list)
        st.rerun()
    
    # Define o tema atual baseado no índice 'take'
    st.session_state.tema = temas_list[st.session_state.take % len(temas_list)]
    
    # Exibição do Conteúdo
    poema_raw = load_poema(st.session_state.tema)
    if st.session_state.lang != "pt":
        poema_raw = translate(poema_raw)
    
    # Botão de Voz dentro da lógica de exibição
    if b_voice.button("🔊"):
        audio = falar_poema(poema_raw, st.session_state.lang)
        if audio: st.audio(audio, format='audio/mp3', autoplay=True)

    # Título sutil e Cartão
    st.markdown(f"<p style='text-align:center; color:#999; letter-spacing:2px; font-size:12px;'>{st.session_state.tema.upper()}</p>", unsafe_allow_html=True)
    texto_formatado = "".join([f"<p>{v.strip()}</p>" for v in poema_raw.split('<br>') if v.strip()])
    img = load_arts(st.session_state.tema) if st.session_state.draw == 'Y' else None
    
    write_ypoema(texto_formatado, img)

# =================================================================
# 6. METAS: EXECUÇÃO E ROTEAMENTO
# =================================================================

def main():
    with st.sidebar:
        st.title("yPoemas")
        sala = st.radio("Navegar:", ["Exploração (Rand)", "Sobre a Machina"])
        st.divider()
        st.session_state.lang = st.selectbox("Idioma:", ["pt", "en", "es", "fr", "it"])
        st.session_state.draw = 'Y' if st.checkbox("Mostrar Artes", True) else 'N'

    if sala == "Exploração (Rand)":
        page_ypoemas()
    else:
        # Função simples de "About" integrada para não perder o foco
        st.markdown("<h2 style='text-align:center;'>Sobre a Machina</h2>", unsafe_allow_html=True)
        st.info("O pergaminho de Dillingen e a ABNP habitam esta sala.")

if __name__ == "__main__":
    main()
    
