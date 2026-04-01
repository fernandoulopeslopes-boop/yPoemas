import streamlit as st
import os
import random
import streamlit.components.v1 as components

# ==========================================
# 1º ANDAR: CONFIGURAÇÃO (LAYOUT LARGO)
# ==========================================
st.set_page_config(page_title="a Machina de fazer Poesia", layout="wide")

# CSS para garantir que o conteúdo não cole no topo da tela
st.markdown("<style>.block-container {padding-top: 1rem;}</style>", unsafe_allow_html=True)

try:
    from lay_2_ypo import gera_poema
except ImportError:
    def gera_poema(tema, seed=""): return ["Erro: motor não encontrado."]

# ==========================================
# 2º ANDAR: A LENTE (HTML/CSS) - CURA DE ESPAÇOS
# ==========================================
def write_ypoema(TITULO, TEXTO_RAW, URL_IMAGEM=None):
    # REMOVE LINHAS DUPLICADAS: filtra apenas linhas com conteúdo real
    if isinstance(TEXTO_RAW, list):
        linhas = [str(l).strip() for l in TEXTO_RAW if str(l).strip()]
        TEXTO_RAW = "\n".join(linhas)
    
    html_layout = f"""
    <style>
        .p-main-container {{
            display: flex;
            justify-content: space-between;
            gap: 40px;
            font-family: 'Georgia', serif;
        }}
        .p-text-area {{ flex: 2.5; }}
        .p-img-area {{ flex: 1.2; text-align: right; }}
        .p-title {{ font-size: 40px; font-weight: bold; margin-bottom: 15px; color: #000; }}
        .p-content {{ 
            font-size: 30px; 
            line-height: 1.25; /* Espaçamento firme entre versos */
            white-space: pre-wrap; 
            color: #222;
        }}
        img {{ max-width: 100%; border-radius: 5px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
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
# 3º ANDAR: ESTADO E UTILITÁRIOS
# ==========================================
if "take" not in st.session_state:
    st.session_state.update({'tema': 'Fatos', 'take': 0, 'book': "livro vivo"})

def load_temas(book):
    caminho = os.path.join("base", f"rol_{book}.txt")
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return ["Fatos", "Elogio", "Prefácil"]

def load_poema(nome_tema):
    res = gera_poema(nome_tema, "")
    return res if isinstance(res, list) else [str(res)]

# ==========================================
# 4º ANDAR: A SALA (YPOEMAS)
# ==========================================
def page_ypoemas():
    temas_list = load_temas(st.session_state.book)
    idx = st.session_state.take % len(temas_list)
    st.session_state.tema = temas_list[idx]

    # --- 4.1 MENU DE TOPO CENTRALIZADO (SEM IDIOMAS) ---
    v_esq, m1, m2, m3, m4, v_dir = st.columns([5, 0.5, 0.5, 0.5, 0.5, 5])
    m1.button("🔊", key="top_voice", help="Voz")
    m2.button("🎬", key="top_video", help="Vídeo")
    m3.button("🖼️", key="top_gallery", help="Galeria")
    m4.button("📋", key="top_info", help="Info")
    st.divider()

    # --- 4.2 COLUNAS DE CONTEÚDO ---
    # col_ctrl (Controles) | col_art (Poema)
    col_ctrl, col_art = st.columns([1.2, 4])

    with col_ctrl:
        # LOGO E TEMA ATUAL
        st.image("https://via.placeholder.com/200x100?text=MACHINA", use_column_width=True)
        st.write(f"**Matriz:** {st.session_state.tema}")
        st.write("---")
        
        # NAVEGAÇÃO (Botões Limpos)
        st.caption("Navegação")
        c1, c2, c3, c4 = st.columns(4)
        if c1.button("✚", key="go_more"): st.rerun()
        if c2.button("◀", key="go_back"):
            st.session_state.take = (st.session_state.take - 1) % len(temas_list); st.rerun()
        if c3.button("✻", key="go_rand"):
            st.session_state.take = random.randrange(len(temas_list)); st.rerun()
        if c4.button("▶", key="go_next"):
            st.session_state.take = (st.session_state.take + 1) % len(temas_list); st.rerun()
        
        st.write("")
        # SELETOR DE TEMAS (Ocupando a largura da lateral)
        st.write("**Lista de Temas:**")
        escolha = st.selectbox("Seletor", options=temas_list, index=idx, label_visibility="collapsed", key="sel_master")
        if escolha != st.session_state.tema:
            st.session_state.take = temas_list.index(escolha); st.rerun()

    with col_art:
        # ÁREA DO POEMA
        poema_raw = load_poema(st.session_state.tema)
        url_teste = "https://images.unsplash.com/photo-1454117096348-e4abbeae002c?w=500"
        write_ypoema(st.session_state.tema, poema_raw, URL_IMAGEM=url_teste)

# ==========================================
# 5º ANDAR: O MOTOR (MAIN)
# ==========================================
def main():
    with st.sidebar:
        st.title("yPoemas")
        sala = st.radio("Menu Principal", ["Exploração", "Sobre"])
        
        st.divider()
        # IDIOMAS MOVIDOS PARA A SIDEBAR
        st.subheader("🌐 Idiomas")
        st.selectbox("Tradução automática:", ["Português", "English", "Español"], key="side_lang")
        st.info("A seleção de idioma afeta a tradução da obra gerada.")

    if sala == "Exploração":
        page_ypoemas()
    else:
        st.write("### Sobre a Machina de fazer Poesia")

if __name__ == "__main__":
    main()
    
