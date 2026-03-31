import streamlit as st
import os
import random
import streamlit.components.v1 as components

# ==========================================
# 1º ANDAR: CONFIGURAÇÃO
# ==========================================
st.set_page_config(page_title="a Machina de fazer Poesia", layout="wide")

try:
    from lay_2_ypo import gera_poema
except ImportError:
    def gera_poema(tema, seed=""): return ["Erro: motor não encontrado."]

# ==========================================
# 2º ANDAR: A LENTE (HTML/CSS) - LIMPEZA DE ESPAÇOS
# ==========================================
def write_ypoema(TITULO, TEXTO_RAW, URL_IMAGEM=None):
    # Limpa linhas vazias duplicadas do motor
    if isinstance(TEXTO_RAW, list):
        linhas = [str(l).strip() for l in TEXTO_RAW if str(l).strip()]
        TEXTO_RAW = "\n".join(linhas)
    
    html_layout = f"""
    <style>
        .p-main-container {{
            display: flex;
            justify-content: space-between;
            gap: 40px;
            font-family: serif;
        }}
        .p-text-area {{ flex: 2; min-width: 60%; }}
        .p-img-area {{ flex: 1; text-align: right; }}
        .p-title {{ font-size: 38px; font-weight: 800; margin-bottom: 20px; color: #111; }}
        .p-content {{ 
            font-size: 28px; 
            line-height: 1.4; 
            white-space: pre-line; /* Mantém estrofes sem duplicar vazios */
            color: #333;
        }}
        img {{ max-width: 100%; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }}
    </style>
    <div class="p-main-container">
        <div class="p-text-area">
            <div class="p-title">{TITULO}</div>
            <div class="p-content">{TEXTO_RAW}</div>
        </div>
        {"<div class='p-img-area'><img src='" + URL_IMAGEM + "'></div>" if URL_IMAGEM else ""}
    </div>
    """
    components.html(html_layout, height=1000, scrolling=True)

# ==========================================
# 3º ANDAR: UTILITÁRIOS
# ==========================================
if "initialized" not in st.session_state:
    st.session_state.update({'lang': 'pt', 'tema': 'Fatos', 'take': 0, 'book': "livro vivo", 'initialized': True})

@st.cache_data(show_spinner=False)
def load_temas(book):
    caminho = os.path.join("base", f"rol_{book}.txt")
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return ["Fatos", "Elogio", "Prefácil"]

def load_poema(nome_tema):
    script = gera_poema(nome_tema, "")
    return "\n".join([str(l) for l in script if l]) if isinstance(script, list) else str(script)

# ==========================================
# 4º ANDAR: A SALA (YPOEMAS)
# ==========================================
def page_ypoemas():
    temas_list = load_temas(st.session_state.book)
    idx = st.session_state.take % len(temas_list)
    st.session_state.tema = temas_list[idx]

    # --- 4.1 MENU DE TOPO (IDENTIDADE) ---
    # Centralizado usando colunas de respiro nas pontas
    v1, m1, m2, m3, m4, v2 = st.columns([4, 0.5, 0.5, 0.5, 0.5, 4])
    with m1: st.button("🌐", key="t_lang")
    with m2: st.button("🔊", key="t_talk")
    with m3: st.button("🎬", key="t_video")
    with m4: st.button("🖼️", key="t_img")
    st.divider()

    # --- 4.2 CONTEÚDO ---
    col_painel, col_palco = st.columns([1.2, 4])

    with col_painel:
        # LOGO DA PÁGINA
        st.image("https://via.placeholder.com/200x100?text=LOGO+TEMA", use_column_width=True)
        st.write("---")
        
        # NAVEGAÇÃO COMPACTA NO PAINEL
        st.caption("Navegação:")
        n1, n2, n3, n4 = st.columns(4)
        with n1: 
            if st.button("✚", key="n_more"): st.rerun()
        with n2: 
            if st.button("◀", key="n_back"):
                st.session_state.take = (st.session_state.take - 1) % len(temas_list); st.rerun()
        with n3: 
            if st.button("✻", key="n_rand"):
                st.session_state.take = random.randrange(len(temas_list)); st.rerun()
        with n4: 
            if st.button("▶", key="n_next"):
                st.session_state.take = (st.session_state.take + 1) % len(temas_list); st.rerun()
        
        st.write("")
        # SELETOR DE TEMAS (LARGURA DO PAINEL)
        escolha = st.selectbox("Escolha o Tema", options=temas_list, index=idx, key="sel_tema")
        if escolha != st.session_state.tema:
            st.session_state.take = temas_list.index(escolha); st.rerun()

    with col_palco:
        poema_raw = load_poema(st.session_state.tema)
        url_teste = "https://images.unsplash.com/photo-1454117096348-e4abbeae002c?w=500"
        write_ypoema(st.session_state.tema, poema_raw, URL_IMAGEM=url_teste)

# ==========================================
# 5º ANDAR: O MOTOR (MAIN)
# ==========================================
def main():
    with st.sidebar:
        st.title("yPoemas")
        sala = st.radio("Menu:", ["Exploração", "Sobre"])
    
    if sala == "Exploração":
        page_ypoemas()
    else:
        st.write("### Sobre a Machina")

if __name__ == "__main__":
    main()
    
