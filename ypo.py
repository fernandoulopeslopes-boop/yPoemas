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
    # 1. PAIOL: Pega a lista de temas do livro selecionado
    temas_list = load_temas(st.session_state.book)
    if not temas_list: return

    # 2. LENTE: Painel de Controle (Centralizado)
    # Criamos 5 colunas para os botões ficarem simétricos
    c1, btn_back, btn_rand, btn_next, btn_voice, c2 = st.columns([2, 1, 1, 1, 1, 2])
    
    if btn_back.button("◀", help="Tema Anterior"):
        st.session_state.take = (st.session_state.take - 1) % len(temas_list)
        st.rerun()
        
    if btn_rand.button("✻", help="Sortear Tema"):
        st.session_state.take = random.randrange(len(temas_list))
        st.rerun()
        
    if btn_next.button("▶", help="Próximo Tema"):
        st.session_state.take = (st.session_state.take + 1) % len(temas_list)
        st.rerun()

    # O Botão de Voz (Farol) - Preparado para o gTTS
    if btn_voice.button("🔊", help="Ouvir Poema"):
        st.info("Preparando a voz da Machina...")
        # Aqui chamaremos a função de áudio no próximo passo
    
    # 3. MOTOR: Define o tema e exibe
    st.session_state.tema = temas_list[st.session_state.take % len(temas_list)]
    exibir_conteudo()
def exibir_conteudo():
    # 1. Busca o Poema
    poema_raw = load_poema(st.session_state.tema)
    if st.session_state.lang != "pt":
        poema_raw = translate(poema_raw)
    
    # 2. Formata o Texto (Markdown precisa de 2 espaços no fim para quebrar linha)
    texto_final = "  \n".join([line.strip() for line in poema_raw.split('<br>')])
    
    # 3. Busca a Arte (Se st.session_state.draw for 'Y')
    img_final = None
    if st.session_state.draw == 'Y':
        img_final = load_arts(st.session_state.tema)
    
    # 4. Envia para a Lente (Markdown + HTML)
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
    
