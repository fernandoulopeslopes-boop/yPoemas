import streamlit as st
import os
import re
import urllib.parse
from deep_translator import GoogleTranslator

# --- 0. MOTORES DA MACHINA (SUPORTE & LIMPEZA) ---
def sanitize_links(text):
    """
    Remove redirecionadores e varre parâmetros de rastreamento (fbclid, si, etc).
    """
    if not text:
        return ""
        
    # 1. Limpeza de redirecionadores (Facebook/Google)
    redir_pattern = r"https?://[l|www]\.(?:facebook|google)\.[a-z\.]+/l\.php\?u=([^& \n]+)&?[^ \n]*"
    def clean_redir(match):
        return urllib.parse.unquote(match.group(1))
    text = re.sub(redir_pattern, clean_redir, text)

    # 2. Limpeza de parâmetros de lixo (fbclid, si, igshid, utm)
    # Remove o lixo mantendo a base da URL limpa
    junk_pattern = r"(\?|&)(fbclid|si|igshid|utm_[a-z]+)=[^ \n\)]+"
    text = re.sub(junk_pattern, "", text)
    
    return text

def load_md_file(filename):
    """Busca arquivos MD com tratamento robusto de nomes e extensões."""
    folder = "md_files"
    # Normaliza o nome para evitar duplicidade de extensão
    base_name = filename.replace(".md", "").replace(".MD", "")
    search_targets = [f"{base_name}.MD", f"{base_name}.md"]
    
    if os.path.exists(folder):
        available_files = os.listdir(folder)
        for target in search_targets:
            for arq in available_files:
                if arq.upper() == target.upper():
                    with open(os.path.join(folder, arq), "r", encoding="utf-8") as f:
                        return sanitize_links(f.read())
    return f"<!-- {base_name}.MD não encontrado -->"

def translate_content(text, target_lang_code):
    if target_lang_code == "pt":
        return text
    try:
        return GoogleTranslator(source='auto', target=target_lang_code).translate(text)
    except:
        return text

def set_style_machina():
    """Injeta a elegância visual e o 'Cisne' (Botão Sair)."""
    st.markdown(
        """
        <style>
        [data-testid="stMainInternal"] { max-width: 95% !important; padding: 2rem !important; }
        
        /* Tipografia de Calibre */
        h1 { font-size: 1.8rem !important; font-weight: bold !important; color: #1E1E1E; }
        h2 { font-size: 1.5rem !important; font-weight: bold !important; color: #2E2E2E; }
        h3 { font-size: 1.2rem !important; font-weight: bold !important; color: #3E3E3E; }
        p { font-size: 1.05rem !important; line-height: 1.6; text-align: justify; }

        /* O Botão Sair: De Patinho Feio a Cisne */
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
        
        /* Ajuste de links para não estourarem o palco */
        a { word-wrap: break-word; color: #ff4b4b; text-decoration: none; }
        a:hover { text-decoration: underline; }
        </style>
        """,
        unsafe_allow_html=True
    )

# --- 1. BOOTSTRAP (ESTADO INICIAL) ---
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
    
    # Navegação Superior
    c1, c2, c3 = st.columns([1, 2, 1])
    
    with c1:
        if st.button("← SAIR", use_container_width=True):
            st.session_state.pagina_ativa = "principal"
            st.rerun()

    with c2:
        try:
            curr_idx = sobre_list.index(st.session_state.sub_sobre.lower())
        except (ValueError, AttributeError):
            curr_idx = 0
        choice_label = st.selectbox("↓ SOBRE", sobre_list, index=curr_idx)
        st.session_state.sub_sobre = choice_label.lower()

    with c3:
        sel_lang = st.selectbox("🌐 IDIOMA", idiomas_labels, index=st.session_state.lang_idx)
        st.session_state.lang_idx = idiomas_labels.index(sel_lang)
        lang_code = idiomas_dict[sel_lang]

    st.divider()

    # ÁREA DE EXPOSIÇÃO DO PALCO EXPANDIDO
    with st.container():
        choice_file = st.session_state.sub_sobre.upper()
        
        if choice_file == "MACHINA":
            raw_text = load_md_file("ABOUT_MACHINA_A") + "\n\n" + load_md_file("ABOUT_MACHINA_D")
        else:
            raw_text = load_md_file(f"ABOUT_{choice_file}")
        
        with st.spinner(f"Sincronizando Machina ({sel_lang})..."):
            translated_text = translate_content(raw_text, lang_code)
            # Sanitização final aplicada ao Markdown renderizado
            st.markdown(sanitize_links(translated_text))

# --- 3. EXECUÇÃO ---
if __name__ == "__main__":
    if st.session_state.pagina_ativa == "sobre":
        page_sobre()
    else:
        # Palco Principal da Machina
        st.title("a Machina de Fazer Poesia")
        st.write("A escala de complexidade quindecilhônica em operação.")
        if st.button("Retornar ao Farol (Sobre)"):
            st.session_state.pagina_ativa = "sobre"
            st.rerun()
