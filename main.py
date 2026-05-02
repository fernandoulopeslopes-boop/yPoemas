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
    """CSS: Alinhamento horizontal absoluto e provocação visual."""
    st.markdown(
        """
        <style>
        [data-testid="stMainInternal"] { max-width: 95% !important; padding: 2rem !important; }
        
        .titulo-logo {
            font-size: 2.1rem !important;
            font-weight: bold !important;
            margin: 1.5rem 0;
            color: #1E1E1E;
        }

        /* Alinhamento Horizontal dos Widgets */
        [data-testid="stHorizontalBlock"] {
            align-items: end !important;
        }

        /* Estilização dos Botões */
        .stButton > button {
            height: 2.8rem !important;
            border-radius: 4px;
            font-weight: bold;
            transition: all 0.2s ease;
            width: 100% !important;
        }
        
        /* Provocação: Fundo Vermelho no Sair */
        .btn-sair > div > button {
            background-color: #ff4b4b !important;
            color: white !important;
            border: 1px solid #ff4b4b !important;
        }
        .btn-sair > div > button:hover {
            background-color: #d43f3f !important;
            border: 1px solid #d43f3f !important;
        }

        .btn-audio > div > button {
            border: 1px solid #333 !important;
            background-color: transparent !important;
            color: #333 !important;
        }

        /* Formatação para números gigantes (Quindecilhões) */
        .metadados-tempo {
            font-family: monospace;
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 5px;
            white-space: pre-wrap;
            word-break: break-all;
            line-height: 1.4;
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
    
    # 1. ALINHAMENTO HORIZONTAL: Grid com ajuste de base
    c_sair, c_audio, c_doc, c_lang = st.columns([0.6, 0.8, 2, 1])
    
    with c_sair:
        st.markdown('<div class="btn-sair">', unsafe_allow_html=True)
        if st.button("sair", key="btn_exit"):
            st.session_state.pagina_ativa = "principal"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with c_audio:
        st.markdown('<div class="btn-audio">', unsafe_allow_html=True)
        if st.button("audio 🔈", key="btn_talk"):
            pass
        st.markdown('</div>', unsafe_allow_html=True)

    with c_doc:
        choice_label = st.selectbox("documentação", sobre_list, 
                                   index=sobre_list.index(st.session_state.sub_sobre),
                                   key="sel_doc")
        st.session_state.sub_sobre = choice_label.lower()

    with c_lang:
        idiomas_labels = list(idiomas_dict.keys())
        sel_lang = st.selectbox("idiomas", idiomas_labels, 
                               index=st.session_state.lang_idx,
                               key="sel_lang")
        st.session_state.lang_idx = idiomas_labels.index(sel_lang)
        lang_code = idiomas_dict[sel_lang]

    st.divider()

    # Título calibrado
    st.markdown('<div class="titulo-logo">a Machina de Fazer Poesia</div>', unsafe_allow_html=True)

    # --- TODO LIST ---
    # [ ] Refazer Análise Combinatória (Divergência nos Quindecilhões)

    with st.container():
        if st.session_state.sub_sobre.upper() == "INDEX":
            # 3. AJUSTE TEMA TEMPO: Preservando tabs e espaços
            st.markdown("### Metadados do Tema: TEMPO")
            st.markdown(
                """<div class="metadados-tempo">
Tempo : 112.765.820.236.797.923.580.529.825.269.143.876.665.344.000.000.000
Total : 112.765.820.265.471.186.578.333.495.090.938.981.765.900.724.963.269
                </div>""", unsafe_allow_html=True
            )
            st.divider()

        # Renderização Normal
        choice_file = st.session_state.sub_sobre.upper()
        raw_text = load_md_file("ABOUT_MACHINA_A") + "\n\n" + load_md_file("ABOUT_MACHINA_D") if choice_file == "MACHINA" else load_md_file(f"ABOUT_{choice_file}")
        
        with st.spinner(f"Processando tradução ({sel_lang})..."):
            translated_text = translate_content(raw_text, lang_code)
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
