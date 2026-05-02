import streamlit as st
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="a Máquina de Fazer Poesia", layout="wide")

# --- FUNÇÕES DE SUPORTE (ESMERO E RESILIÊNCIA) ---

def load_md_file(file_name):
    """
    Carregamento resiliente: se a perna de apoio (arquivo) falhar, 
    o sistema apenas informa e segue em frente.
    """
    file_path = f"./docs/{file_name}"
    
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"### ⚠️ Erro técnico ao ler {file_name}\n{e}"
    
    return f"### 🔍 Documento ausente: {file_name}\n*Verifique a pasta /docs.*"

def page_sobre():
    """
    Biblioteca Documental: O Farol da Machina.
    """
    # A lista oficial, consolidada e sem redundâncias
    sobre_list = [
        "prefácio", "machina", "off-machina", "opinião",
        "outros", "traduttore", "imagens", "samizdát",
        "notes", "index", "bibliografia", "license"
    ]

    options = list(range(len(sobre_list)))
    
    # Seletor independente: nunca fica inativo
    opt_sobre = st.selectbox(
        "↓ SOBRE",
        options,
        format_func=lambda x: sobre_list[x],
        key="opt_sobre",
    )

    choice = sobre_list[opt_sobre].strip().upper()
    
    # Moldura do palco documental
    about_expander = st.expander(f"BIBLIOTECA: {choice}", expanded=True)
    
    with about_expander:
        if choice == "MACHINA":
            # Estrutura tripartida: Texto A -> Visual -> Texto D
            st.markdown(load_md_file("ABOUT_MACHINA_A.md"))
            
            # Caminho para a nova raiz /images
            tema_atual = st.session_state.get('tema', 'default')
            logo_path = f"./images/{tema_atual}.jpg"
            
            if os.path.exists(logo_path):
                st.image(logo_path, use_container_width=True)
            else:
                st.caption(f"Visual não localizado: {logo_path}")
                
            st.markdown(load_md_file("ABOUT_MACHINA_D.md"))
        else:
            # Carregamento dinâmico baseado na escolha
            st.markdown(load_md_file(f"ABOUT_{choice}.md"))

# --- MOTOR DA INTERFACE ---

def main():
    # Inicialização silenciosa de estados
    if 'pagina_ativa' not in st.session_state: 
        st.session_state.pagina_ativa = "mini"
    if 'idioma' not in st.session_state:
        st.session_state.idioma = "Português"
    if 'trigger_tts' not in st.session_state:
        st.session_state.trigger_tts = False

    # CSS de Alta Precisão (Alinhamento m -> e)
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

    # SIDEBAR: Controle e Tradução
    with st.sidebar:
        st.markdown("### a Máquina de Fazer Poesia")
        st.caption("yPoema / Machina")
        st.divider()

        # 22 Idiomas Ocidentais
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

    # PALCO: 6 Botões Definidos (m -> e)
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

    # ROTEAMENTO DE CONTEÚDO
    if st.session_state.pagina_ativa == "sobre":
        page_sobre()
    else:
        st.markdown(f"<h2 style='text-align: center;'>{st.session_state.pagina_ativa.upper()}</h2>", unsafe_allow_html=True)

    # RODAPÉ: ÁUDIO TTS (Zerado até o disparo)
    if st.session_state.trigger_tts:
        texto = st.session_state.pagina_ativa
        audio_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={texto}&tl=pt&client=tw-ob"
        st.write("")
        st.audio(audio_url)
        st.caption(f"<p style='text-align: center;'>Voz Ativa | Falando: {texto}</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
