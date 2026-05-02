import streamlit as st
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="a Máquina de Fazer Poesia", layout="wide")

# --- FUNÇÕES DE SUPORTE (O ESMERO TÉCNICO) ---

def load_md_file(file_name):
    """
    Localiza os arquivos na pasta correta: ./md_files/
    Garante a firmeza do passo antes da leitura.
    """
    # Ajuste preciso do caminho conforme o seu "housekeeping"
    file_path = f"./md_files/{file_name}" 
    
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"### ⚠️ Erro de leitura em {file_name}\n{e}"
    
    return f"### 🔍 Arquivo não encontrado\nCaminho esperado: `{file_path}`"

def page_sobre():
    """
    Biblioteca documental consolidada.
    """
    sobre_list = [
        "ypoemas", "machina", "off-machina", "comments", "prefácio", 
        "outros", "imagens", "notes", "traduttore", "samizdát",
        "index", "bibliografia", "license",
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
    about_expander = st.expander(f"DOCUMENTO: {choice}", expanded=True)
    
    with about_expander:
        if choice == "MACHINA":
            # Estrutura: Texto A -> Imagem (em /images) -> Texto D
            st.markdown(load_md_file("ABOUT_MACHINA_A.md"))
            
            tema_atual = st.session_state.get('tema', 'default')
            logo_path = f"./images/{tema_atual}.jpg"
            
            if os.path.exists(logo_path):
                st.image(logo_path, use_container_width=True)
            
            st.markdown(load_md_file("ABOUT_MACHINA_D.md"))
        else:
            # Carregamento dinâmico: ABOUT_OPINIÃO.md, etc.
            st.markdown(load_md_file(f"ABOUT_{choice}.md"))

# --- MOTOR DA INTERFACE ---

def main():
    # Estados iniciais
    if 'pagina_ativa' not in st.session_state: 
        st.session_state.pagina_ativa = "mini"
    if 'idioma' not in st.session_state:
        st.session_state.idioma = "Português"
    if 'trigger_tts' not in st.session_state:
        st.session_state.trigger_tts = False

    # CSS para Alinhamento Milimétrico (m -> e)
    st.markdown("""
        <style>
            [data-testid="stAppViewContainer"] { display: flex; flex-direction: row; }
            .main .block-container { max-width: 98vw !important; padding-top: 2rem !important; }
            [data-testid="stSidebar"] { min-width: 300px !important; width: 300px !important; }
            .stButton > button { 
                width: 100%; font-size: 22px !important; 
                background: transparent !important; border: none !important; 
                padding: 0px !important;
            }
            div[data-testid="stAudio"] { width: 60% !important; margin: 0 auto !important; }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### a Máquina de Fazer Poesia")
        st.caption("yPoema / Machina")
        st.divider()

        idiomas = sorted(["Português", "English", "Español", "Français", "Deutsch", "Italiano",
                          "Català", "Dansk", "Euskara", "Suomi", "Galego", "Islandska", 
                          "Lëtzebuergesch", "Magyar", "Nederlands", "Norsk", "Polski", 
                          "Portuñol", "Română", "Slovenčina", "Slovenščina", "Russia", "Suécia"])
        st.session_state.idioma = st.selectbox("Translator", idiomas)
        
        st.divider()
        col_art, col_aud = st.columns(2)
        with col_art: st.button("Arte")
        with col_aud:
            if st.button("Áudio"): st.session_state.trigger_tts = True
        st.divider()

    # PALCO: 6 Botões
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

    # CONTEÚDO
    if st.session_state.pagina_ativa == "sobre":
        page_sobre()
    else:
        st.markdown(f"<h2 style='text-align: center;'>{st.session_state.pagina_ativa.upper()}</h2>", unsafe_allow_html=True)

    # ÁUDIO (TTS)
    if st.session_state.trigger_tts:
        texto = st.session_state.pagina_ativa
        audio_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={texto}&tl=pt&client=tw-ob"
        st.audio(audio_url)

if __name__ == "__main__":
    main()
