import streamlit as st
import os

# --- 1. CONFIGURAÇÃO DE ESTÉTICA E GEOMETRIA (CPC) ---
def configurar_estetica():
    st.set_page_config(layout="wide", initial_sidebar_state="expanded")
    st.markdown("""
        <style>
        /* Palco 100% Real: Reset de margens para a linha encostar nas laterais */
        html, body, [data-testid="stAppViewContainer"] {
            overflow-x: hidden;
        }
        .main .block-container { 
            max-width: 100% !important; 
            padding-top: 1rem !important; 
            padding-left: 0rem !important; 
            padding-right: 0rem !important; 
        }
        
        /* Respiro interno apenas para os controles superiores */
        .controles-palco {
            padding-left: 1.5rem;
            padding-right: 1.5rem;
        }

        /* Botões do Navegador Central */
        .stButton > button { width: 100%; border-radius: 5px; font-weight: bold; height: 3rem; }
        
        /* Alinhamento de Selectboxes */
        div[data-testid="stSelectbox"] { margin-top: -10px; }

        /* Sidebar: Botões Arte e Voz nas extremidades */
        [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
            padding: 0 0.5rem;
        }

        /* LINHA FINA: Ocupação total de margem a margem do palco */
        .separador-palco {
            width: 100%; 
            margin: 10px 0px 20px 0px; 
            border: 0;
            border-top: 1px solid #ccc;
        }

        /* Área de Conteúdo Markdown */
        .conteudo-principal {
            padding-left: 2rem;
            padding-right: 2rem;
            font-family: serif;
        }
        </style>
        """, unsafe_allow_html=True)

# --- 2. CARREGAMENTO DE DADOS (ROLS) ---
@st.cache_data
def carregar_estrutura_pastas():
    # Caminho base para os arquivos normalizados
    base_path = "md_files"
    estrutura = {}
    
    if os.path.exists(base_path):
        # Lê as pastas (Livros)
        livros = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
        for livro in livros:
            # Lê os arquivos .md (Temas) removendo a extensão para exibição
            caminho_livro = os.path.join(base_path, livro)
            temas = [f.replace(".md", "") for f in os.listdir(caminho_livro) if f.endswith(".md")]
            estrutura[livro] = sorted(temas)
    
    # Fallback caso a pasta esteja vazia para não quebrar a interface
    if not estrutura:
        estrutura = {"Aviso": ["Pasta md_files não encontrada"]}
        
    return estrutura

def carregar_sidebar():
    with st.sidebar:
        st.write("---")
        idiomas = ["Português", "Espanhol", "Italiano", "Francês", "Inglês", "Catalão", "Russo"]
        st.selectbox("idioma", idiomas, label_visibility="collapsed")
        st.write("---")
        
        col_v1, col_v2 = st.columns(2)
        with col_v1: st.button("Arte")
        with col_v2: st.button("Voz")

def main():
    configurar_estetica()
    carregar_sidebar()
    
    # Carrega a estrutura real dos arquivos .md
    dicionario_dados = carregar_estrutura_pastas()

    # --- 3. PALCO: NAVEGAÇÃO ---
    st.markdown('<div class="controles-palco">', unsafe_allow_html=True)
    col_l, col_nav, col_t = st.columns([2.5, 3.0, 2.5])

    with col_l:
        livro_sel = st.selectbox("livros", list(dicionario_dados.keys()), label_visibility="collapsed", key="sel_livro_final")
    
    with col_nav:
        n1, n2, n3, n4, n5 = st.columns(5)
        with n1: st.button("+") 
        with n2: st.button("<") 
        with n3: st.button("*") 
        with n4: st.button(">") 
        with n5: st.button("?") 

    with col_t:
        temas_disponiveis = dicionario_dados.get(livro_sel, ["..."])
        tema_sel = st.selectbox("temas", temas_disponiveis, label_visibility="collapsed", key="sel_tema_final")
    st.markdown('</div>', unsafe_allow_html=True)

    # Linha separadora colada nas laterais
    st.markdown('<div class="separador-palco"></div>', unsafe_allow_html=True)

    # --- 4. EXIBIÇÃO DO CONTEÚDO (ACESSO TOTAL AO MD) ---
    caminho_arquivo = os.path.join("md_files", livro_sel, f"{tema_sel}.md")
    
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()
        
        st.markdown('<div class="conteudo-principal">', unsafe_allow_html=True)
        st.markdown(conteudo)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
