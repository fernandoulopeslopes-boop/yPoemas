import streamlit as st
import os
import glob
from lista_oficial import IDIOMAS

# Configuração CSS obrigatória para fixar a largura da Sidebar em 300px
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 300px !important;
            max-width: 300px !important;
            min-width: 300px !important;
        }
    </style>
    """,
    unsafe_with_html=True
)

# Inicialização do estado das variáveis de controle se não existirem
if "focus_page" not in st.session_state:
    st.session_state.focus_page = "livros"  # Iniciando em uma das páginas ativas para avaliação
if "lang_selector" not in st.session_state:
    st.session_state.lang_selector = list(IDIOMAS.keys())[0] if IDIOMAS else ""
if "draw" not in st.session_state:
    st.session_state.draw = False
if "talk" not in st.session_state:
    st.session_state.talk = False
if "auto" not in st.session_state:
    st.session_state.auto = False

# ============================================================
# ⚙️ COMPONENTE: SIDEBAR (CENTRO DE CONTROLE)
# ============================================================
def render_sidebar():
    with st.sidebar:
        # Layout do topo com o botão linkey sem função no canto direito
        col_top_left, col_top_right = st.columns([8, 2])
        with col_top_right:
            st.button("🔗", key="btn_linkey", help="Linkey")
            
        # 1. IMAGEM DA PÁGINA EM FOCO
        if st.session_state.focus_page:
            nome_base_upper = str(st.session_state.focus_page).upper()
            nome_arte = f"img_{nome_base_upper}.JPG"
            arte_path = f"images/{nome_arte}"
            
            if os.path.exists("images"):
                arquivos_imagens = os.listdir("images")
                alvo_arte = next((arq for arq in arquivos_imagens if arq.upper() == nome_arte), None)
                if alvo_arte:
                    st.image(f"images/{alvo_arte}", use_column_width=True)
                    
        # 2. CONTEÚDO INFORMATIVO MD_FILE
        if st.session_state.focus_page:
            nome_md = f"INFO_{nome_base_upper}.MD"
            pasta_md = "md_files"
            
            if os.path.exists(pasta_md):
                arquivos_md = os.listdir(pasta_md)
                alvo_md = next((arq for arq in arquivos_md if arq.upper() == nome_md), None)
                if alvo_md:
                    with open(f"{pasta_md}/{alvo_md}", "r", encoding="utf-8") as f:
                        st.markdown(f.read())
                    st.markdown("---")

        # 3. SELETOR DE IDIOMAS (Lista Oficial) e Botões de Controle
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
    # Seletor de páginas para simular e habilitar o teste completo da estrutura
    paginas_disponiveis = ["mini", "yPoemas", "eureka", "livros", "poly", "Sobre"]
    
    # Linha superior de navegação global para desenvolvimento/avaliação
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
        
        # Busca dinâmica de arquivos md na pasta correta
        pasta_md = "md_files"
        arquivos_livros = []
        if os.path.exists(pasta_md):
            # Filtra tudo que não seja arquivos auxiliares conhecidos para listar como conteúdo
            todos_files = os.listdir(pasta_md)
            arquivos_livros = [f for f in todos_files if f.upper().endswith(".MD") and not f.upper().startswith("INFO_") and not f.upper().startswith("HELP_") and not f.upper().startswith("ABOUT_")]

        if arquivos_livros:
            # Dropdown ocupa o palco inteiro
            livro_selecionado = st.selectbox("Selecione um Livro:", arquivos_livros, key="select_livros")
            
            # Bloco de botões específicos
            col_b1, col_b2, col_b3, col_b4, col_b5, _ = st.columns([1, 1, 1, 1, 1, 7])
            with col_b1: st.button("<-", key="livros_prev")
            with col_b2: st.button("⭐", key="livros_star")
            with col_b3: st.button("->", key="livros_next")
            with col_b4: st.button("❤️", key="livros_heart")
            with col_b5: 
                # Help associado
                help_path = "md_files/HELP_OFF-MACHINA.MD"
                help_content = ""
                if os.path.exists(help_path):
                    with open(help_path, "r", encoding="utf-8") as h_f:
                        help_content = h_f.read()
                st.button("?", key="livros_help", help=help_content if help_content else "Help indisponível")
                
            # Exibição do conteúdo do arquivo md selecionado
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
            # Coleta arquivos de poemas/textos específicos para o ambiente poly
            arquivos_poly = [f for f in os.listdir(pasta_md) if f.upper().endswith(".MD") and not f.upper().startswith("INFO_") and not f.upper().startswith("HELP_") and not f.upper().startswith("ABOUT_")]

        if arquivos_poly:
            poema_selecionado = st.selectbox("Selecione o Texto Poliglota:", arquivos_poly, key="select_poly")
            
            # Bloco de botões específicos
            col_p1, col_p2, _ = st.columns([1, 1, 10])
            with col_p1: 
                st.button("❤️", key="poly_heart", help="temas mais lidos")
            with col_p2:
                # Help associado
                help_path = "md_files/HELP_POLY.MD"
                help_content = ""
                if os.path.exists(help_path):
                    with open(help_path, "r", encoding="utf-8") as h_f:
                        help_content = h_f.read()
                st.button("?", key="poly_help", help=help_content if help_content else "Help indisponível")
                
            st.markdown("---")
            with open(f"{pasta_md}/{poema_selecionado}", "r", encoding="utf-8") as p_f:
                st.markdown(p_f.read())
        else:
            st.warning("Nenhum arquivo de texto encontrado para a Poly em \\md_files.")

    # --------------------------------------------------------
    # 6. SOBRE
    # --------------------------------------------------------
    elif st.session_state.focus_page == "Sobre":
        st.subheader("Sobre a Machina")
        
        pasta_md = "md_files"
        # Resgate de todos os arquivos ABOUT_*.md de forma dinâmica
        arquivos_about = glob.glob(os.path.join(pasta_md, "ABOUT_*.md")) if os.path.exists(pasta_md) else []
        
        if arquivos_about:
            # Mapeamento do dicionário para exibição limpa (remove o prefixo 'ABOUT_' e a extensão '.MD')
            mapa_exibicao = {}
            for caminho_completo in arquivos_about:
                nome_arquivo = os.path.basename(caminho_completo)
                # Separa sem o prefixo e sem a extensão .md
                nome_limpo = nome_arquivo[6:-3] if nome_arquivo.upper().startswith("ABOUT_") else nome_arquivo[:-3]
                mapa_exibicao[nome_limpo] = caminho_completo
            
            # Selectbox dinâmico alimentado pelos arquivos reais
            opcao_escolhida = st.selectbox("Seções Informativas:", list(mapa_exibicao.keys()), key="select_about")
            
            st.markdown("---")
            # Leitura e exibição do arquivo real correspondente
            caminho_alvo = mapa_exibicao[opcao_escolhida]
            with open(caminho_alvo, "r", encoding="utf-8") as a_f:
                st.markdown(a_f.read())
        else:
            st.warning("Nenhum arquivo 'ABOUT_*.md' foi encontrado em \\md_files para compor esta página.")

# ============================================================
# ⚙️ EXECUÇÃO ORQUESTRADA DO SISTEMA
# ============================================================
render_sidebar()
render_palco()
