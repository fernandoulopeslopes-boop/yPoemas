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

def write_ypoema(LOGO_TEXTO, LOGO_IMAGE):
    st.markdown("""
        <style>
        .poem-card {
            background: white; padding: 40px; border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05); border: 1px solid #f0f0f0;
            display: flex; gap: 40px; align-items: flex-start; margin-top: 10px;
        }
        .logo-text { 
            font-family: 'Georgia', serif; font-size: 28px; /* FONTE GRANDE */
            line-height: 1.6; color: #1a1a1a; flex: 1.5; 
        }
        .logo-img { flex: 1; max-width: 350px; border-radius: 10px; }
        @media (max-width: 768px) { .poem-card { flex-direction: column; } }
        </style>
    """, unsafe_allow_html=True)

    img_html = ""
    if LOGO_IMAGE:
        with open(LOGO_IMAGE, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        img_html = f"<img class='logo-img' src='data:image/jpg;base64,{img_b64}'>"

    st.markdown(f"""
        <div class='poem-card'>
            <div class='logo-text'>{LOGO_TEXTO}</div>
            {img_html}
        </div>
    """, unsafe_allow_html=True)

# =================================================================
# 5. SALA: YPOEMAS (CONTROLE COMPLETO)
# =================================================================

def page_ypoemas():
    temas_list = load_temas(st.session_state.book)
    c1, b_back, b_rand, b_plus, b_next, b_voice, c2 = st.columns([2, 1, 1, 1, 1, 1, 2])
    
    if b_back.button("◀"):
        st.session_state.take = (st.session_state.take - 1) % len(temas_list)
        st.rerun()
    if b_rand.button("✻"):
        st.session_state.take = random.randrange(len(temas_list))
        st.rerun()
    if b_plus.button("+"): # REPETE O TEMA (NOVA VARIAÇÃO)
        st.rerun()
    if b_next.button("▶"):
        st.session_state.take = (st.session_state.take + 1) % len(temas_list)
        st.rerun()
    
    st.session_state.tema = temas_list[st.session_state.take % len(temas_list)]
    poema_raw = load_poema(st.session_state.tema)
    if st.session_state.lang != "pt": poema_raw = translate(poema_raw)
    
    if b_voice.button("🔊"):
        audio = falar_poema(poema_raw, st.session_state.lang)
        if audio: st.audio(audio, format='audio/mp3', autoplay=True)

    st.markdown(f"<p style='text-align:center; color:#999; letter-spacing:4px; font-size:14px;'>{st.session_state.tema.upper()}</p>", unsafe_allow_html=True)
    texto_formatado = "".join([f"<p>{v.strip()}</p>" for v in poema_raw.split('<br>') if v.strip()])
    
    # Busca a Arte e exibe
    img = load_arts(st.session_state.tema)
    write_ypoema(texto_formatado, img)

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

    if sala == "Exploração (Rand)":
        page_ypoemas()
    else:
        st.info("Sala Sobre a Machina")

if __name__ == "__main__":
    main()
    
