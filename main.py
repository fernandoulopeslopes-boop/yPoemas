import streamlit as st
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="a Máquina de Fazer Poesia", layout="wide")

# --- FUNÇÕES DE SUPORTE (O ESMERO TÉCNICO) ---

def load_md_file(file_name):
    """
    Verifica a existência física do arquivo antes de tentar a leitura.
    Garante que a 'perna de apoio' esteja firme.
    """
    file_path = f"./docs/{file_name}" # Pasta centralizada de documentos
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"### Erro ao ler {file_name}: {e}"
    return f"### [ {file_name} em processamento ou ausente ]"

def page_sobre():
    """
    Biblioteca documental: a memória recente e histórica da Machina.
    """
    sobre_list = [
        "prefácio", "machina", "off-machina", "opinião",
        "outros", "traduttore", "imagens", "samizdát",
        "notes", "index", "bibliografia", "license"
    ]

    options = list(range(len(sobre_list)))
    sobrios = "↓ SOBRE" 
    
    opt_sobre = st.selectbox(
        sobrios,
        options,
        format_func=lambda x: sobre_list[x],
        key="opt_sobre",
    )

    choice = sobre_list[opt_sobre].upper()
    about_expander = st.expander("", expanded=True)
    
    with about_expander:
        if choice == "MACHINA":
            # Estrutura Farol: Texto A -> Visual -> Texto D
            st.markdown(load_md_file("ABOUT_MACHINA_A.md"))
            
            # Localização de imagem na nova raiz \images
            tema_atual = st.session_state.get('tema', 'default')
            logo_path = f"./images/{tema_atual}.jpg"
            
            if os.path.exists(logo_path):
                st.image(logo_path, use_container_width=True)
            else:
                st.caption(f"Aguardando imagem: {logo_path}")
                
            st.markdown(load_md_file("ABOUT_MACHINA_D.md"))
        else:
            # Carregamento dinâmico e seguro do conteúdo gigante
            st.markdown(load_md_file(f"ABOUT_{choice}.md"))

# --- MOTOR PRINCIPAL ---

def main():
    # Inicialização de estados
    if 'pagina_ativa' not in st.session_state: 
        st.session_state.pagina_ativa = "mini"
    if 'idioma' not in st.session_state:
        st.session_state.idioma = "Português"
    if 'trigger_tts' not in st.session_state:
        st.session_state.trigger_tts = False

    # CSS: Alinhamento, Moldura e Proporcionalidade
    st.markdown("""
        <style>
            [data-testid="stAppViewContainer"] { display: flex; flex-direction: row; }
            .main .block-container { max-width: 98vw !important; padding-top: 2rem !important; }
            [data-testid="stSidebar"] { min-width: 300px !important; width: 300px !important; }
            .stButton > button { 
                width: 100%; font-size: 22px !important; 
                background: transparent !important; border: none !important; 
                padding: 0px !important; transition: 0.3s;
            }
            .stButton > button:hover { color: #ff4b4b; }
            div[data-testid="stAudio"] { width: 60% !important; margin: 0 auto !important; }
        </style>
    """, unsafe_allow_html=True)

    # SIDEBAR: O comando da Machina
    with st.sidebar:
        st.markdown("### a Máquina de Fazer Poesia")
        st.caption("yPoema / Machina")
        st.divider()

        # Translator: 22 idiomas (Alfabeto Ocidental)
        idiomas = ["Português", "English", "Español", "Français", "Deutsch", "Italiano",
                   "Català", "Dansk", "Euskara", "Suomi", "Galego", "Islandska", 
                   "Lëtzebuergesch", "Magyar", "Nederlands", "Norsk", "Polski", 
                   "Portuñol", "Română", "Slovenčina", "Slovenščina", "Russia", "Suécia"]
        st.session_state.idioma = st.selectbox("Translator", sorted(idiomas))
        
        st.divider()
        col_art, col_aud = st.columns(2)
        with col_art: st.button("Arte")
        with col_aud:
            if st.button("Áudio"): st.session_state.trigger_tts = True # Clique dispara o Talk
        st.divider()

    # PALCO: Navegação de 6 Botões (Alinhamento 'm' de mini e 'e' de sobre)
    paginas = ["mini", "yPoema", "eureka", "livros", "poly", "sobre"]
    pesos = [len(pg) for pg in paginas]
    
    cols = st.columns(pesos)
    for i, pg in enumerate(paginas):
        with cols[i]:
            if st.button(pg, key=f"btn_{pg}"):
                st.session_state.pagina_ativa = pg
                st.session_state.trigger_tts = False 
                st.rerun()

    st.divider()

    # CONTEÚDO DO PALCO
    if st.session_state.pagina_ativa == "sobre":
        page_sobre()
    else:
        # Placeholder para as outras páginas de poesia
        st.markdown(f"<h1 style='text-align: center;'>{st.session_state.pagina_ativa}</h1>", unsafe_allow_html=True)

    # TALK / TTS (Sempre no rodapé do palco, centrado)
    if st.session_state.trigger_tts:
        texto = st.session_state.pagina_ativa
        audio_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={texto}&tl=pt&client=tw-ob"
        st.write("")
        st.audio(audio_url)
        st.caption(f"<p style='text-align: center;'>Talk/TTS Ativo | Página: {texto}</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
