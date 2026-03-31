import streamlit as st
import os
import random
import streamlit.components.v1 as components

# 1. CONFIGURAÇÃO (Deve ser a primeira linha de Streamlit)
st.set_page_config(page_title="a Machina de fazer Poesia", layout="wide")

# --- MOTORES EXTERNOS ---
try:
    from lay_2_ypo import gera_poema
except ImportError:
    def gera_poema(tema, seed=""): return ["Erro: motor lay_2_ypo não encontrado."]

# 2. A LENTE (EXIBIÇÃO) 
def write_ypoema(TITULO, TEXTO_RAW):
    # Por enquanto mantemos a versão simples, focando na navegação
    if isinstance(TEXTO_RAW, list):
        TEXTO_RAW = "\n".join(TEXTO_RAW).strip()
    
    html_layout = f"""
    <style>
        .p-title {{ 
            font-size: 38px; font-weight: 800; color: #111; 
            margin-bottom: 15px; font-family: sans-serif; 
        }}
        .p-content {{ 
            font-size: 30px; font-weight: 500; color: #333; 
            line-height: 1.4; font-family: sans-serif;
            white-space: pre-wrap;
        }}
    </style>
    <div class="p-title">{TITULO}</div>
    <div class="p-content">{TEXTO_RAW}</div>
    """
    components.html(html_layout, height=600, scrolling=True)

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

# 4. A SALA (YPOEMAS)
def page_ypoemas():
    temas_list = load_temas(st.session_state.book)
    
    # Sincroniza o tema atual com o índice 'take'
    st.session_state.tema = temas_list[st.session_state.take % len(temas_list)]
    
    # --- BOTOES E SELETOR (Tarefas 1 e 3) ---
    c1, more, last, rand, nest, manu, c2 = st.columns([1, 0.5, 0.5, 0.5, 0.5, 0.5, 3])
    
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
        # TAREFA 3: Help limpo (apenas a info interna)
        with st.popover("?", help="Info da Matrix"):
            st.write(f"**Matriz: {st.session_state.tema}**")

    with c2:
        # TAREFA 1: Dropdown sincronizado
        escolha = st.selectbox(
            "Seletor de Temas", 
            options=temas_list, 
            index=st.session_state.take % len(temas_list),
            label_visibility="collapsed"
        )
        if escolha != st.session_state.tema:
            st.session_state.take = temas_list.index(escolha)
            st.rerun()

    # --- EXIBIÇÃO (Tarefa 2) ---
    poema_raw = load_poema(st.session_state.tema)
    # TAREFA 2: Sem .upper(), respeitando a grafia original
    write_ypoema(st.session_state.tema, poema_raw)

# 5. O MOTOR (MAIN)
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
    
