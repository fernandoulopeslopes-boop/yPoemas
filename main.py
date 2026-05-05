import streamlit as st
import os
import glob
import base64
# Importação corrigida respeitando o case exato do arquivo físico (Original.py)
from Original import IDIOMAS

# Configuração CSS obrigatória para fixar a largura da Sidebar em 300px
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 300px !important;
            max-width: 300px !important;
            min-width: 300px !important;
        }
        .linkey-container {
            display: flex;
            justify-content: flex-end;
            padding-right: 5px;
        }
        .linkey-button {
            background: none;
            border: none;
            padding: 0;
            cursor: pointer;
        }
    </style>
    """,
    unsafe_with_html=True
)

# Inicialização segura do estado das variáveis de controle
if "focus_page" not in st.session_state:
    st.session_state.focus_page = "livros"  
if "lang_selector" not in st.session_state:
    st.session_state.lang_selector = list(IDIOMAS.keys())[0] if IDIOMAS else ""
if "draw" not in st.session_state:
    st.session_state.draw = False
if "talk" not in st.session_state:
    st.session_state.talk = False
if "auto" not in st.session_state:
    st.session_state.auto = False

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# ============================================================
# ⚙️ COMPONENTE: SIDEBAR (CENTRO DE CONTROLE)
# ============================================================
def render_sidebar():
    with st.sidebar:
        # Layout do topo com o botão linkey sem função no canto direito
        col_top_left, col_top_right = st.columns([8, 2])
        with col_top_right:
            chave_base64 = get_base64_image("images/chave_dourada.png")
            if chave_base64:
                st.markdown(
                    f'<div class="linkey-container">'
                    f'<button class="linkey-button" title="Linkey">'
                    f'<img src="data:image/png;base64,{chave_base64}" width="20" height="20" style="image-rendering: pixelated;"/>'
                    f'</button>'
                    f'</div>',
                    unsafe_with_html=True
                )
            else:
                st.button("🔗", key="btn_linkey", help="Linkey")
            
        # 1. IMAGEM DA PÁGINA EM FOCO (\images + "img_" + pagina + ".JPG")
        if st.session_state.focus_page:
            nome_pagina = str(st.session_state.focus_page)
            nome_arte = f"img_{nome_pagina}.JPG"
            pasta_imagens = "images"
            
            if os.path.exists(pasta_imagens):
                arquivos_imagens = os.listdir(pasta_imagens)
                alvo_arte = next((arq for arq in arquivos_imagens if arq.upper() == nome_arte.upper()), None)
                if alvo_arte:
                    st.image(f"{pasta_imagens}/{alvo_arte}", use_column_width=True)
                    
        # 2. CONTEÚDO INFORMATIVO MD_FILE ("INFO_" + pagina + ".MD")
        if st.session_state.focus_page:
            nome_md = f"INFO_{nome_pagina}.MD"
            pasta_md = "md_files"
            
            if os.path.exists(pasta_md):
                arquivos_md = os.listdir(pasta_md)
                alvo_md = next((arq for arq in arquivos_md if arq.upper() == nome_md.upper()), None)
                if alvo_md:
                    with open(f"{pasta_md}/{alvo_md}", "r", encoding="utf-8") as f:
                        st.markdown(f.read())
                    st.markdown("---")

        # 3. SELETOR DE IDIOMAS (Lista Oficial vinda de Original.py)
        st.markdown("*idiomas disponíveis...*")
        col_lang, col_art, col_aud = st.columns([6, 2, 2])
        
        with col_lang:
            opcoes_idiomas = list(IDIOMAS.keys())
            st.selectbox(
                label="seletor_idiomas",
                options=opcoes_idiomas,
                label_visibility="collapsed",
                key="lang_selector"
            )
            
        with col_art:
            st.session_state.draw = st.checkbox("🎨", help="exibir artes", key="chk_draw")
            
        with col_aud:
            st.session_state.talk = st.checkbox("🔊", help="ouvir áudio", key="chk_talk")
            
        st.markdown("---")
        
        # 4. CONTROLE AUTOMÁTICO
        st.session_state.auto = st.checkbox("auto", key="chk_auto")
        if st.session_state.auto:
            st.session_state.talk = False
            
        st.markdown("---")
        
        # 5. BOTÕES SOCIAIS
        col_fb, col_ig, col_yt, col_tw = st.columns(4)
        with col_fb: st.button("📘", help="Facebook", key="sb_fb")
        with col_ig: st.button("📸", help="Instagram", key="sb_ig")
        with col_yt: st.button("📺", help="YouTube", key="sb_yt")
        with col_tw: st.button("🐦", help="Twitter/X", key="sb_tw")

# ============================================================
# 🎭 COMPONENTE: O PALCO (PÁGINAS)
# ============================================================
def render_palco():
    paginas_disponiveis = ["mini", "yPoemas", "eureka", "livros", "poly", "Sobre"]
    
    st.session_state.focus_page = st.radio(
        "Navegação do Palco (Foco):", 
        paginas_disponiveis, 
        index=paginas_disponiveis.index(st.session_state.focus_page),
        horizontal=True
    )
    st.markdown("---")
    
    # --------------------------------------------------------
    # 1, 2 e 3: EM CONSTRUÇÃO
    # --------------------------------------------------------
    if st.session_state.focus_page in ["mini", "yPoemas", "eureka"]:
        st.subheader(f"Página: {st.session_state.focus_page}")
        st.info("under construction...")
        
    # --------------------------------------------------------
    # 4. LIVROS
    # --------------------------------------------------------
    elif st.session_state.focus_page == "livros":
        st.subheader("Biblioteca Off-Machina")
        
        pasta_md = "md_files"
        arquivos_livros = []
        if os.path.exists(pasta_md):
            todos_files = os.listdir(pasta_md)
            arquivos_livros = [f for f in todos_files if f.upper().endswith(".MD") and not f.upper().startswith("INFO_") and not f.upper().startswith("HELP_") and not f.upper().startswith("ABOUT_")]

        if arquivos_livros:
            livro_selecionado = st.selectbox("Selecione um Livro:", arquivos_livros, label_visibility="collapsed", key="select_livros")
            
            col_b1, col_b2, col_b3, col_b4, col_b5, _ = st.columns([1, 1, 1, 1, 1, 7])
            with col_b1: st.button("<-", key="livros_prev")
            with col_b2: st.button("⭐", key="livros_star")
            with col_b3: st.button("->", key="livros_next")
            with col_b4: st.button("❤️", key="livros_heart")
            with col_b5: 
                help_path = "md_files/HELP_OFF-MACHINA.MD"
                help_content = ""
                if os.path.exists(help_path):
                    with open(help_path, "r", encoding="utf-8") as h_f:
                        help_content = h_f.read()
                st.button("?", key="livros_help", help=help_content if help_content else "Help indisponível")
                
            st.markdown("---")
            with open(f"{pasta_md}/{livro_selecionado}", "r", encoding="utf-8") as l_f:
                st.markdown(l_f.read())
        else:
            st.warning("Nenhum arquivo de livro encontrado em \\md_files.")

    # --------------------------------------------------------
    # 5. POLY
    # --------------------------------------------------------
    elif st.session_state.focus_page == "poly":
        st.subheader("Modo Poliglota")
        
        pasta_md = "md_files"
        arquivos_poly = []
        if os.path.exists(pasta_md):
            arquivos_poly = [f for f in os.listdir(pasta_md) if f.upper().endswith(".MD") and not f.upper().startswith("INFO_") and not f.upper().startswith("HELP_") and not f.upper().startswith("ABOUT_")]

        if archivos_poly:
            poema_selecionado = st.selectbox("Selecione o Texto Poliglota:", arquivos_poly, label_visibility="collapsed", key="select_poly")
            
            col_p1, col_p2, _ = st.columns([1, 1, 10])
            with col_p1: 
                st.button("❤️", key="poly_heart", help="temas mais lidos")
            with col_p2:
                help_path = "md_files/HELP_POLY.MD"
                help_content = ""
                if os.path.exists(help_path):
                    with open(help_path, "r", encoding="utf-8") as h_f:
                        help_content = h_f.read()
                st.button("?", key="poly_help", help=help_content if help_content else "Help indisponível")
                
            st.markdown("---")
            with open(f"{pasta_md}/{poema_selecionado}", "r", encoding="utf-8") as p_f:
                st.markdown(p_f.read())
