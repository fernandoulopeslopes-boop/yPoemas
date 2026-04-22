import streamlit as st
import os

# --- 1. CONFIGURAÇÃO DE LAYOUT E ESTÉTICA ---
def configurar_estetica():
    st.set_page_config(layout="wide", initial_sidebar_state="expanded")
    st.markdown("""
        <style>
        /* Remove o scroll horizontal e ajusta o palco para 100% real */
        html, body, [data-testid="stAppViewContainer"] {
            overflow-x: hidden;
        }
        .main .block-container { 
            max-width: 100% !important; 
            padding-top: 1rem !important; 
            padding-left: 0rem !important; 
            padding-right: 0rem !important; 
        }
        
        /* Botões do Navegador Central */
        .stButton > button { width: 100%; border-radius: 5px; font-weight: bold; height: 3rem; }
        
        /* Ajuste das selectboxes para ocupar o espaço lateral sem scroll */
        div[data-testid="stSelectbox"] { 
            margin-top: -10px; 
            padding-left: 0.5rem; 
            padding-right: 0.5rem; 
        }

        /* Alinhamento dos botões da Sidebar: Arte (esq) e Voz (dir) */
        [data-testid="stSidebar"] .stButton > button {
            width: 100%;
        }
        
        /* LINHA FINA: 100% da largura, sem margens */
        .separador-palco {
            width: 100%; 
            margin: 10px 0px 20px 0px; 
            border: 0;
            border-top: 1px solid #ccc;
        }
        </style>
        """, unsafe_allow_html=True)

# --- 2. CARREGAMENTO EXTERNO (FIM DA TRAVA DE DEPLOY) ---
@st.cache_data
def carregar_listas_externas():
    # Aqui a lógica busca arquivos .txt ou .json na pasta do projeto
    # Se os arquivos não existirem, retorna estrutura básica para não quebrar
    try:
        # Exemplo: carregando de temas.txt ou similar
        # dicionario = seu_metodo_de_leitura()
        pass
    except:
        pass
    
    # Estrutura padrão (Substituir pela leitura de arquivo conforme sua estrutura de pastas)
    return {
        "livro vivo": ["Prefácil", "Fatos", "Manifesto", "Manusgrite", "Beaba", "Paroles", "Essa", "Tiro", "Aolero", "Atido", "Lato", "Avevida", "Joker", "Feiras", "Cartaz", "Conto", "Festim", "I-Mundo", "Sos", "Meteoro", "Brado", "Inhos", "Astros", "Cromossomo", "Clandestino", "Pessoa", "Minuto", "Reger", "Preciso", "Pedidos", "Seguro", "Fugaz", "Nós", "Enfrente", "Leituras", "Rever", "Ocio", "Essas", "Mirante", "Indolor", "Elogio", "Distintos", "Gula", "Dolores", "Clarice", "Cuores", "Zoia", "Amaré", "Ciuminho", "Saudades", "Sentença", "Finalmentes", "Ser", "Rito", "Sonoro", "Anjos", "Epitafiando", "Tempo", "Usinas", "Veio", "Sopros", "Silente", "Oficio", "Posfácio"],
        "poemas": ["Amaré", "Atido", "Becos", "Ciuminho", "Clandestino", "Clarice", "Conto", "Cuores", "Elogio", "Festim", "Indolor", "Lato", "Machbeth", "Machbrait", "Mirante", "Oca", "Oco", "Ogiva", "Olhares", "Papilio", "Psiu", "Reger", "Rever", "Saudades", "Ser", "Silente", "Sinais", "Sonoro", "Sopros", "Tempo", "Usinas", "Veio", "Victor", "Zelo", "Zoia"]
    }

def carregar_sidebar():
    with st.sidebar:
        st.write("---")
        # Idiomas fixos ou carregados
        idiomas = ["Português", "Espanhol", "Italiano", "Francês", "Inglês"]
        st.selectbox("idioma", idiomas, label_visibility="collapsed")
        st.write("---")
        
        # Alinhamento Arte e Voz
        c1, c2 = st.columns(2)
        with c1: st.button("Arte")
        with c2: st.button("Voz")
    return

def main():
    configurar_estetica()
    carregar_sidebar()
    dicionario_dados = carregar_listas_externas()

    # --- 3. PALCO CORRIGIDO (LARGURA E SCROLL) ---
    # Colunas com pesos que priorizam espaço para o texto das listas
    col_l, col_nav, col_t = st.columns([2.5, 2.0, 2.5])

    with col_l:
        livro_sel = st.selectbox("livros", list(dicionario_dados.keys()), label_visibility="collapsed", key="sel_livro")
    
    with col_nav:
        n1, n2, n3, n4, n5 = st.columns(5)
        with n1: st.button("+") 
        with n2: st.button("<") 
        with n3: st.button("*") 
        with n4: st.button(">") 
        with n5: st.button("?") 

    with col_t:
        temas_disponiveis = dicionario_dados.get(livro_sel, ["..."])
        tema_sel = st.selectbox("temas", temas_disponiveis, label_visibility="collapsed", key="sel_tema")

    # Linha separadora colada nas laterais
    st.markdown('<div class="separador-palco"></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
