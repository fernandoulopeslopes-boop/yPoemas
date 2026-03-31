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
    # 1. Carga de Dados
    temas_list = load_temas(st.session_state.book)
    
    # 2. SEQUÊNCIA DE BOTÕES (A Nova Ordem)
    # Ajustei as colunas para os 5 botões ficarem alinhados ao centro
    c1, more, last, rand, nest, manu, c2 = st.columns([2, 0.5, 0.5, 0.5, 0.5, 0.5, 2])
    
    # Botão 1: ✚ (Nova Variação)
    if more.button("✚", help="Nova Variação", key="btn_more_ypo"):
        st.rerun()
        
    # Botão 2: ◀ (Anterior)
    if last.button("◀", help="Anterior", key="btn_last_ypo"):
        st.session_state.take = (st.session_state.take - 1) % len(temas_list)
        st.rerun()
        
    # Botão 3: ✻ (Aleatório)
    if rand.button("✻", help="Sorteio", key="btn_rand_ypo"):
        st.session_state.take = random.randrange(len(temas_list))
        st.rerun()
        
    # Botão 4: ▶ (Próximo)
    if nest.button("▶", help="Próximo", key="btn_nest_ypo"):
        st.session_state.take = (st.session_state.take + 1) % len(temas_list)
        st.rerun()
        
    # Botão 5: ? (Manual/Help)
    # Aqui embutimos a Matriz do Tema dentro do Popover de Ajuda
    with manu:
        with st.popover("?", help="Help !!!"):
            st.markdown(f"### Matriz: {st.session_state.tema}")
            img_matrix = load_arts(st.session_state.tema)
            if img_matrix:
                st.image(img_matrix, use_container_width=True)
            else:
                st.caption("Gráfico geométrico não localizado.")
            st.divider()
            st.info("A contemporaneidade remete a Aldus Manutius. Use os controles acima para navegar pela Machina.")

    # 3. LOGICA DE EXIBIÇÃO
    st.session_state.tema = temas_list[st.session_state.take % len(temas_list)]
    poema_raw = load_poema(st.session_state.tema)
    
    # Tradução
    if st.session_state.lang != "pt":
        poema_raw = translate(poema_raw)
    
    # Título do Tema (Sutil)
    st.markdown(f"<p style='text-align:center; color:#999; letter-spacing:5px; font-size:14px; margin-top:30px;'>{st.session_state.tema.upper()}</p>", unsafe_allow_html=True)
    
    # Formatação do Poema (32px via CSS do write_ypoema)
    texto_formatado = "".join([f"<p>{v.strip()}</p>" for v in poema_raw.split('<br>') if v.strip()])
    
    # Renderiza o Card de Poesia
    write_ypoema(texto_formatado, None)
    
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
    
