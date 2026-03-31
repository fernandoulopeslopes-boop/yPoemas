import streamlit as st
import os
import random

# 1. CONFIGURAÇÃO (Deve ser a primeira linha de Streamlit)
st.set_page_config(page_title="a Machina de fazer Poesia", layout="wide")

# --- MOTORES EXTERNOS ---
try:
    from lay_2_ypo import gera_poema
except ImportError:
    def gera_poema(tema, seed=""): return ["Erro: motor lay_2_ypo não encontrado."]

# 2. A LENTE (EXIBIÇÃO) 

def write_ypoema(TITULO, TEXTO_RAW):
    # 1. Se for lista, vira texto agora
    if isinstance(TEXTO_RAW, list):
        TEXTO_RAW = "\n".join(TEXTO_RAW).strip()
    
    # 2. CSS Puro (Sem f-string para não dar erro de chaves)
    estilo = """
    <style>
        .p-title { 
            font-size: 42px !important; 
            font-weight: 800 !important; 
            color: #111 !important; 
            display: block !important;
            margin-bottom: 15px !important;
            font-family: sans-serif;
        }
        .p-content { 
            font-size: 34px !important; 
            font-weight: 500 !important; 
            color: #333 !important; 
            line-height: 1.4 !important;
            white-space: pre-wrap !important; 
            display: block !important;
            font-family: sans-serif;
        }
    </style>
    """
    
    # 3. Conteúdo (Aqui usamos f-string apenas para as variáveis)
    corpo = f'<div class="p-title">{TITULO}</div><div class="p-content">{TEXTO_RAW}</div>'
    
    # 4. A Entrega Final (Soma das strings)
    st.markdown(estilo + corpo, unsafe_allow_html=True)
    
    # 3. Montagem do HTML com as variáveis
    corpo_html = f'<div class="p-title">{TITULO}</div><div class="p-content">{TEXTO_RAW}</div>'
    
    # 4. Execução Final (A soma do Estilo + Corpo)
    st.markdown(estilo + corpo_html, unsafe_allow_html=True)
    
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
    return ["Fatos", "Elogio", "Prefácil"]

def load_poema(nome_tema):
    script = gera_poema(nome_tema, "")
    if isinstance(script, list): return "\n".join([str(l) for l in script if l])
    return str(script)

# 4. A SALA (YPOEMAS) - Definida ANTES do main()
def page_ypoemas():
    temas_list = load_temas(st.session_state.book)
    st.session_state.tema = temas_list[st.session_state.take % len(temas_list)]
    
    # BOTOES
    c1, more, last, rand, nest, manu, c2 = st.columns([2, 0.5, 0.5, 0.5, 0.5, 0.5, 2])
    
    if more.button("✚", key="btn_more"): st.rerun()
    if last.button("◀", key="btn_last"):
        st.session_state.take = (st.session_state.take - 1) % len(temas_list)
        st.rerun()
    if rand.button("✻", key="btn_rand"):
        st.session_state.take = random.randrange(len(temas_list))
        st.rerun()
    if nest.button("▶", key="btn_next"):
        st.session_state.take = (st.session_state.take + 1) % len(temas_list)
        st.rerun()
    
    with manu:
        with st.popover("?", help="Help !!!"):
            st.write(f"**Matriz: {st.session_state.tema}**")

    poema_raw = load_poema(st.session_state.tema)
    write_ypoema(st.session_state.tema.upper(), poema_raw)

# 5. O MOTOR (MAIN) - No final do arquivo
def main():
    with st.sidebar:
        st.title("yPoemas")
        sala = st.radio("Navegar:", ["Exploração", "Sobre"])
    
    if sala == "Exploração":
        page_ypoemas()
    else:
        st.write("### Sobre a Machina")

if __name__ == "__main__":
    main()

