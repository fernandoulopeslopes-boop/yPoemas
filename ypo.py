import streamlit as st
import os
import random
import streamlit.components.v1 as components

# ==========================================
# 1º ANDAR: CONFIGURAÇÃO E MOTORES
# ==========================================
st.set_page_config(page_title="a Machina de fazer Poesia", layout="wide")

try:
    from lay_2_ypo import gera_poema
except ImportError:
    def gera_poema(tema, seed=""): return ["Erro: motor lay_2_ypo não encontrado."]

# ==========================================
# 2º ANDAR: A LENTE (EXIBIÇÃO HTML/CSS)
# ==========================================
def write_ypoema(TITULO, TEXTO_RAW, URL_IMAGEM=None):
    if isinstance(TEXTO_RAW, list):
        # TAREFA 5: Garante a separação original das estrofes (\n\n)
        TEXTO_RAW = "\n".join([str(l) for l in TEXTO_RAW]).strip()
    
    # TAREFA 4: Layout Flexbox (Texto à esquerda, Imagem à direita)
    html_layout = f"""
    <style>
        .p-main-container {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 35px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        .p-text-area {{
            flex: 2;
            min-width: 65%;
        }}
        .p-img-area {{
            flex: 1;
            text-align: right;
        }}
        .p-title {{ 
            font-size: 40px; font-weight: 800; color: #111; 
            margin-bottom: 20px; 
        }}
        .p-content {{ 
            font-size: 32px; font-weight: 500; color: #333; 
            line-height: 1.5;
            white-space: pre-wrap; /* PRESERVA ESTROFES */
        }}
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 12px;
            box-shadow: 3px 3px 15px rgba(0,0,0,0.1);
        }}
    </style>
    <div class="p-main-container">
        <div class="p-text-area">
            <div class="p-title">{TITULO}</div>
            <div class="p-content">{TEXTO_RAW}</div>
        </div>
        {"<div class='p-img-area'><img src='" + URL_IMAGEM + "'></div>" if URL_IMAGEM else ""}
    </div>
    """
    components.html(html_layout, height=1200, scrolling=True)

# ==========================================
# 3º ANDAR: O PAIOL (CARGA DE DADOS)
# ==========================================
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

# ==========================================
# 4º ANDAR: O PAIOL (CARGA DE DADOS)
# ==========================================
def page_ypoemas():
    temas_list = load_temas(st.session_state.book)
    idx = st.session_state.take % len(temas_list)
    st.session_state.tema = temas_list[idx]

    # --- 4.1 LAYOUT: PAINEL ESQUERDO | PALCO CENTRAL ---
    col_painel, col_palco = st.columns([1.2, 4])

    with col_painel:
        # Espaço reservado apenas para o LOGO da página/tema atual
        st.image("https://via.placeholder.com/200x100?text=LOGO+TEMA", use_column_width=True)

    with col_palco:
        # --- NAVEGAÇÃO INTERNA (SETAS E SELETOR) ---
        # c2 reduzido para 0.8 para encurtar o dropdown pela metade
        c1, more, last, rand, nest, manu, c2, c_vazio = st.columns([0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.8, 2.5])
        
        with more: 
            if st.button("✚", key="btn_more"): st.rerun()
        with last: 
            if st.button("◀", key="btn_last"):
                st.session_state.take = (st.session_state.take - 1) % len(temas_list); st.rerun()
        with rand: 
            if st.button("✻", key="btn_rand"):
                st.session_state.take = random.randrange(len(temas_list)); st.rerun()
        with nest: 
            if st.button("▶", key="btn_next"):
                st.session_state.take = (st.session_state.take + 1) % len(temas_list); st.rerun()
        with manu:
            with st.popover("?", help="Info"):
                st.write(f"**Matriz:** {st.session_state.tema}")
        with c2:
            # Dropdown agora com metade da largura anterior
            escolha = st.selectbox("Seletor", options=temas_list, index=idx, label_visibility="collapsed", key="sel_master")
            if escolha != st.session_state.tema:
                st.session_state.take = temas_list.index(escolha); st.rerun()

        # --- EXIBIÇÃO DA OBRA ---
        poema_raw = load_poema(st.session_state.tema)
        url_teste = "https://images.unsplash.com/photo-1454117096348-e4abbeae002c?w=500"
        write_ypoema(st.session_state.tema, poema_raw, URL_IMAGEM=url_teste)
        # --- EXIBIÇÃO DA OBRA ---
        poema_raw = load_poema(st.session_state.tema)
        url_teste = "https://images.unsplash.com/photo-1454117096348-e4abbeae002c?w=500"
        write_ypoema(st.session_state.tema, poema_raw, URL_IMAGEM=url_teste)
        
# ==========================================
# 5º ANDAR: O MOTOR (MAIN)
# ==========================================
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
    
