import streamlit as st
import os
from deep_translator import GoogleTranslator

# --- 0. MOTORES DA MACHINA (SUPORTE) ---
def load_md_file(filename):
    folder = "md_files"
    search_name = filename if filename.upper().endswith(".MD") else f"{filename}.MD"
    if os.path.exists(folder):
        for arq in os.listdir(folder):
            if arq.upper() == search_name.upper():
                with open(os.path.join(folder, arq), "r", encoding="utf-8") as f:
                    return f.read()
    return f"<!-- {search_name} não encontrado -->"

def translate_content(text, target_lang_code):
    if target_lang_code == "pt":
        return text
    try:
        return GoogleTranslator(source='auto', target=target_lang_code).translate(text)
    except:
        return text

def set_style_machina():
    st.markdown(
        """
        <style>
        [data-testid="stMainInternal"] { max-width: 95% !important; padding: 2rem !important; }
        h1 { font-size: 1.8rem !important; font-weight: bold !important; margin-bottom: 1rem; }
        h2 { font-size: 1.5rem !important; font-weight: bold !important; }
        h3 { font-size: 1.2rem !important; font-weight: bold !important; }
        p { font-size: 1.05rem !important; line-height: 1.6; text-align: justify; }
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
    
    c1, c2, c3 = st.columns([1, 2, 1])
    
    with c1:
        if st.button("← SAIR", use_container_width=True):
            st.session_state.pagina_ativa = "principal"
            st.rerun()

    with c2:
        try:
            curr_idx = sobre_list.index(st.session_state.sub_sobre.lower())
        except ValueError:
            curr_idx = 0
        # Grafia de exibição corrigida para "MACHINA" conforme instrução
        choice = st.selectbox("↓ SOBRE", sobre_list, index=curr_idx).upper()
        st.session_state.sub_sobre = choice.lower()

    with c3:
        sel_lang = st.selectbox("🌐 IDIOMA", idiomas_labels, index=st.session_state.lang_idx)
        st.session_state.lang_idx = idiomas_labels.index(sel_lang)
        lang_code = idiomas_dict[sel_lang]

    st.divider()

    # TODO LIST: ACESSIBILIDADE (Inclusão Visual)
    # [ ] Implementar talk() gTTS

    with st.container():
        if choice == "MACHINA":
            raw_text = load_md_file("ABOUT_MACHINA_A.MD") + "\n\n" + load_md_file("ABOUT_MACHINA_D.MD")
        else:
            raw_text = load_md_file(f"ABOUT_{choice}.MD")
        
        with st.spinner(f"Traduzindo para {sel_lang}..."):
            translated_text = translate_content(raw_text, lang_code)
            st.markdown(translated_text)

# --- 3. EXECUÇÃO ---
if __name__ == "__main__":
    if st.session_state.pagina_ativa == "sobre":
        page_sobre()
    else:
        # Título ajustado para a grafia obrigatória
        st.title("a Machina de Fazer Poesia")
        if st.button("Configurações / Sobre"):
            st.session_state.pagina_ativa = "sobre"
            st.rerun()
