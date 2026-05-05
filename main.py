import streamlit as st
import os
import glob
import base64

# ============================================================
# 📥 PROTOCOLO DE IDIOMAS (Filtro: Original.py)
# ============================================================
# Carregamento seguro para evitar ModuleNotFoundError ou ImportError
IDIOMAS = {}
if os.path.exists("Original.py"):
    try:
        with open("Original.py", "r", encoding="utf-8") as f:
            conteudo_orig = f.read()
            # Se o arquivo contiver um dicionário IDIOMAS, extrai de forma segura
            local_vars = {}
            exec(conteudo_orig, {}, local_vars)
            if "IDIOMAS" in local_vars:
                IDIOMAS = local_vars["IDIOMAS"]
    except Exception:
        pass

# Fallback robusto caso o arquivo esteja vazio ou estruturado de outra forma
if not IDIOMAS:
    IDIOMAS = {"Português": "pt", "English": "en", "Español": "es"}

# ============================================================
# 🎨 CONFIGURAÇÃO DE INTERFACE (CSS)
# ============================================================
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
    st.session_state.lang_selector = list(IDIOMAS.keys())[0]
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

        # 3. SELETOR DE IDIOMAS
        st.markdown("*idiomas disponíveis...*")
        col_lang, col_art, col_aud = st.columns([6, 2, 2])
