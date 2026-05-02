import streamlit as st
import os
import re
import urllib.parse
from deep_translator import GoogleTranslator

# --- 0. MOTORES DA MACHINA (SUPORTE) ---
def sanitize_links(text):
    """
    Limpa URLs complexas e remove rastreadores (fbclid, si, igshid, etc).
    """
    # 1. Remove redirecionadores (Facebook/Google)
    redir_pattern = r"https?://[l|www]\.(?:facebook|google)\.[a-z\.]+/l\.php\?u=([^& \n]+)&?[^ \n]*"
    def clean_redir(match):
        return urllib.parse.unquote(match.group(1))
    text = re.sub(redir_pattern, clean_redir, text)

    # 2. Remove parâmetros de lixo de URLs diretas (como fbclid, si, etc)
    # Procura por ?fbclid=... ou &fbclid=... e remove até o próximo espaço ou fechamento de parênteses
    junk_pattern = r"(\?|&)(fbclid|si|igshid|utm_[a-z]+)=[^ \n\)]+"
    text = re.sub(junk_pattern, "", text)
    
    return text

def set_style_machina():
    """Estilo refinado para o Palco e para o botão Sair."""
    st.markdown(
        """
        <style>
        [data-testid="stMainInternal"] { max-width: 95% !important; padding: 2rem !important; }
        
        /* Tipografia Elegante */
        h1 { font-size: 1.8rem !important; font-weight: bold !important; color: #1E1E1E; }
        h2 { font-size: 1.5rem !important; font-weight: bold !important; color: #2E2E2E; }
        h3 { font-size: 1.2rem !important; font-weight: bold !important; color: #3E3E3E; }
        p { font-size: 1.05rem !important; line-height: 1.6; text-align: justify; }

        /* Transformação do Botão Sair (De Patinho Feio a Cisne) */
        div.stButton > button {
            width: 100%;
            border-radius: 4px;
            border: 1px solid #ff4b4b;
            background-color: white;
            color: #ff4b4b;
            font-weight: bold;
            transition: all 0.3s ease;
            height: 3rem;
        }
        div.stButton > button:hover {
            background-color: #ff4b4b;
            color: white;
            border: 1px solid #ff4b4b;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# --- 1. BOOTSTRAP ---
if 'pagina_ativa' not in st.session_state:
    st.session_state.pagina_ativa = "sobre"
if 'sub_sobre' not in st.session_state:
    st.session_state.sub_sobre = "comments"
if 'lang_idx' not in st.session_state:
    st.session_state.lang_idx = 0 

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# --- 2. O FAROL (SOBRE) ---
def page_sobre():
    set_style_machina()
    
    idiomas_dict = {
        "português": "pt", "espanhol": "es", "italiano": "it", 
        "francês": "fr", "inglês": "en", "catalão": "ca"
    }
    idiomas_labels = list(idiomas_dict.keys())
    
    sobre_list = [
        "comments", "prefácio", "machina", "off-machina", "outros",
        "traduttore", "imagens", "samizdát", "notes", "index",
        "bibliografia", "license"
    ]
    
    # Header: Grid alinhado
    c1, c2, c3 = st.columns([1, 2, 1])
    
    with c1:
        # O botão agora tem destaque visual condizente com a interface
        if st.button("← SAIR", use_container_width=True):
            st.session_state.pagina_ativa = "principal"
            st.rerun()

    with c2:
        try:
            curr_idx = sobre_list.index(st.session_state.sub_sobre.lower())
        except ValueError:
            curr_idx = 0
        choice = st.selectbox("↓ SOBRE", sobre_list, index=curr_idx).upper()
        st.session_state.sub_sobre = choice.lower()

    with c3:
        sel_lang = st.selectbox("🌐 IDIOMA", idiomas_labels, index=st.session_state.lang_idx)
        st.session_state.lang_idx = idiomas_labels.index(sel_lang)
        lang_code = idiomas_dict[sel_lang]

    st.divider()

    with st.container():
        # Carregamento e Sanitização (incluindo o link da Beth Alvim)
        if choice == "MACHINA":
            raw_text = load_md_file("ABOUT_MACHINA_A.MD") + "\n\n" + load_md_file("ABOUT_MACHINA_D.MD")
        else:
            raw_text = load_md_file(f"ABOUT_{choice}.MD")
        
        with st.spinner(f"Processando conteúdo para {sel_lang}..."):
            translated_text = translate_content(raw_text, lang_code)
            # A sanitização final garante que mesmo links traduzidos fiquem limpos
            st.markdown(sanitize_links(translated_text))

# --- 3. EXECUÇÃO ---
if __name__ == "__main__":
    if st.session_state.pagina_ativa == "sobre":
        page_sobre()
    else:
        st.title("a Machina de Fazer Poesia")
        if st.button("Configurações / Sobre"):
            st.session_state.pagina_ativa = "sobre"
            st.rerun()
