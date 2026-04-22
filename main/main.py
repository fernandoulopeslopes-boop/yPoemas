import streamlit as st
import os

# --- 1. LISTA DE IDIOMAS OBRIGATÓRIA (PCP) ---
IDIOMAS_MACHINA = {
    "Português": "pt", "Espanhol": "es", "Italiano": "it", "Francês": "fr",
    "Inglês": "en", "Catalão": "ca", "Córsico": "co", "Galego": "gl",
    "Basco": "eu", "Esperanto": "eo", "Latin": "la", "Galês": "cy",
    "Sueco": "sv", "Polonês": "pl", "Holandês": "nl", "Norueguês": "no",
    "Finlandês": "fi", "Dinamarquês": "da", "Irlandês": "ga", "Romeno": "ro", "Russo": "ru"
}

def configurar_estetica():
    """Define a identidade visual e o layout do palco."""
    st.set_page_config(layout="wide", initial_sidebar_state="expanded")
    st.markdown("""
        <style>
        [data-testid="stSidebarNav"] {padding-top: 0rem;}
        .main .block-container { max-width: 95%; padding-top: 2rem; }
        [data-testid="stSidebar"] [data-testid="column"] { display: flex; justify-content: center; }
        .stButton > button { width: 100%; border-radius: 20px; }
        </style>
        """, unsafe_allow_html=True)

def carregar_sidebar():
    """Painel de Controle: Onde o leitor escolhe o 'como'."""
    with st.sidebar:
        # Arco Narrativo: mini -> yPoemas -> eureka -> about
        menu = ["mini", "yPoemas", "eureka", "about"]
        choice = st.radio("navegação", menu, label_visibility="collapsed")
        
        st.write("---")
        
        idioma_exibido = st.selectbox("idioma", list(IDIOMAS_MACHINA.keys()))
        sigla_traducao = IDIOMAS_MACHINA[idioma_exibido]
        
        st.write("---")
        
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            st.button("Arts")
        with col_v2:
            st.button("Voice")
            
    return choice, sigla_traducao

def carregar_palco(choice, sigla_traducao):
    """Área de Exibição: Onde o leitor descobre o 'quê'."""
    
    if choice in ["mini", "yPoemas", "eureka"]:
        col_livro, col_tema = st.columns(2)
        
        with col_livro:
            # lista_livros e dicionario_dados devem estar definidos no seu motor
            livro_sel = st.selectbox("livros", lista_livros)
        
        with col_tema:
            temas_disponiveis = dicionario_dados[livro_sel]
            tema_sel = st.selectbox("temas", temas_disponiveis)
        
        st.write("---")
        
        # Direcionamento para os motores específicos da Machina
        if choice == "mini":
            # Ex: motor_mini(tema_sel, sigla_traducao)
            pass
        elif choice == "yPoemas":
            # Ex: motor_ypoemas(tema_sel, sigla_traducao)
            pass
        elif choice == "eureka":
            # Ex: motor_eureka(livro_sel, tema_sel)
            pass

    elif choice == "about":
        about_map = {
            "Prefácio": "ABOUT_PREFÁCIO.md",
            "A Máquina (A)": "ABOUT_MACHINA_A.md",
            "A Máquina (D)": "ABOUT_MACHINA_D.md",
            "Traduttore": "ABOUT_TRADUTTORE.md",
            "off-machina": "ABOUT_OFF-MACHINA.md",
            "Outros Autores": "ABOUT_OUTROS.md",
            "Samizdát": "ABOUT_SAMIZDÁT.md",
            "Bibliografia": "ABOUT_BIBLIOGRAFIA.md",
            "Comments": "ABOUT_COMMENTS.md"
        }
        
        sel_about = st.selectbox("sobre", list(about_map.keys()))
        path = os.path.join("md_files", about_map[sel_about])
        
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                st.markdown(f.read())

def main():
    configurar_estetica()
    escolha, sigla = carregar_sidebar()
    carregar_palco(escolha, sigla)

if __name__ == "__main__":
    main()
