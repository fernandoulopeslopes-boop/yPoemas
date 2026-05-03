import streamlit as st
import os
import re
import urllib.parse
from deep_translator import GoogleTranslator

# --- 0. MOTORES DA MACHINA (SUPORTE & LIMPEZA) ---
def sanitize_links(text):
    if not text: return ""
    redir_pattern = r"https?://[l|www]\.(?:facebook|google)\.[a-z\.]+/l\.php\?u=([^& \n]+)&?[^ \n]*"
    def clean_redir(match): return urllib.parse.unquote(match.group(1))
    text = re.sub(redir_pattern, clean_redir, text)
    junk_pattern = r"(\?|&)(fbclid|si|igshid|utm_[a-z]+)=[^ \n\)]+"
    text = re.sub(junk_pattern, "", text)
    return text

def load_md_file(filename):
    folder = "md_files"
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
    if target_lang_code == "pt": return text
    try:
        return GoogleTranslator(source='auto', target=target_lang_code).translate(text)
    except: return text

def set_style_machina():
    """CSS: Alinhamento, Provocação Vermelha e Padronização de Texto."""
    st.markdown(
        """
        <style>
        [data-testid="stMainInternal"] { max-width: 95% !important; padding: 2rem !important; }
        
        /* 1. O MOTOR DE LAYOUT DE TEXTO */
        .conteudo-padronizado {
            max-width: 850px;
            margin: 0 auto;
            line-height: 1.7;
            word-wrap: break-word;
            text-align: justify;
            font-size: 1.1rem;
            color: #262730;
        }

        .titulo-logo {
            font-size: 2.1rem !important;
            font-weight: bold !important;
            margin: 1.5rem 0;
            color: #1E1E1E;
        }

        [data-testid="stHorizontalBlock"] {
            align-items: flex-end !important;
        }

        .btn-sair > div > button {
            background-color: #ff4b4b !important;
            color: white !important;
            font-weight: bold !important;
        }
        
        .metadados-tempo {
            font-family: monospace;
            background-color: #f8f9fb;
            padding: 1.2rem;
            border-left: 5px solid #ff4b4b;
            white-space: pre-wrap;
            word-break: break-all;
            margin: 1rem 0;
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
    
    sobre_list = [
        "comments", "prefácio", "machina", "off-machina", "outros",
        "traduttore", "imagens", "samizdát", "notes", "index",
        "bibliografia", "license"
    ]
    
    c_sair, c_audio, c_doc, c_lang = st.columns([0.6, 0.8, 2, 1])
    
    with c_sair:
        st.markdown('<div class="btn-sair">', unsafe_allow_html=True)
        if st.button("sair", key="btn_exit"):
            st.session_state.pagina_ativa = "principal"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with c_audio:
        st.markdown('<div class="btn-audio">', unsafe_allow_html=True)
        st.button("audio 🔈", key="btn_talk")
        st.markdown('</div>', unsafe_allow_html=True)

    with c_doc:
        def on_doc_change():
            st.session_state.sub_sobre = st.session_state.sel_doc.lower()
        st.selectbox("documentação", sobre_list, 
                     index=sobre_list.index(st.session_state.sub_sobre) if st.session_state.sub_sobre in sobre_list else 0,
                     key="sel_doc", on_change=on_doc_change)

    with c_lang:
        idiomas_labels = list(idiomas_dict.keys())
        def on_lang_change():
            st.session_state.lang_idx = idiomas_labels.index(st.session_state.sel_lang)
        st.selectbox("idiomas", idiomas_labels, 
                     index=st.session_state.lang_idx,
                     key="sel_lang", on_change=on_lang_change)
        
    st.divider()
    st.markdown('<div class="titulo-logo">a Machina de Fazer Poesia</div>', unsafe_allow_html=True)

    # 2. RENDERIZAÇÃO COM O MOTOR DE LAYOUT
    with st.container():
        choice_file = st.session_state.sub_sobre.upper()
        
        # Lógica de carga
        if choice_file == "MACHINA":
            raw_text = load_md_file("ABOUT_MACHINA_A") + "\n\n" + load_md_file("ABOUT_MACHINA_D")
        else:
            raw_text = load_md_file(f"ABOUT_{choice_file}")
        
        lang_code = idiomas_dict[list(idiomas_dict.keys())[st.session_state.lang_idx]]
        
        with st.spinner("Sincronizando..."):
            translated_text = translate_content(raw_text, lang_code)
            # A mágica acontece aqui: div injetada para controlar o layout
            st.markdown(f'<div class="conteudo-padronizado">{translated_text}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    if st.session_state.pagina_ativa == "sobre":
        page_sobre()
    else:
        st.title("a Machina de Fazer Poesia")
        if st.button("Configurações / Sobre"):
            st.session_state.pagina_ativa = "sobre"
            st.rerun()
