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
                        # 1. Grafia correta OFF-MACHINA.MD tratada aqui
                        return sanitize_links(f.read())
    return f"<!-- {base_name}.MD não encontrado -->"

def translate_content(text, target_lang_code):
    if target_lang_code == "pt": return text
    try:
        return GoogleTranslator(source='auto', target=target_lang_code).translate(text)
    except: return text

def set_style_machina():
    """CSS: Alinhamento milimétrico e Provocação Vermelha."""
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

        /* 3. ALINHAMENTO: Força todos os elementos da coluna a alinhar na base */
        [data-testid="stHorizontalBlock"] {
            align-items: flex-end !important;
        }

        /* Padronização de altura para botões e campos */
        .stButton > button, .stSelectbox div[data-baseweb="select"] {
            height: 2.8rem !important;
        }

        /* 2. PROVIDÊNCIA: Fundo Vermelho no Sair */
        .btn-sair > div > button {
            background-color: #ff4b4b !important;
            color: white !important;
            border: none !important;
            font-weight: bold !important;
        }
        .btn-sair > div > button:hover {
            background-color: #d43f3f !important;
        }

        .btn-audio > div > button {
            border: 1px solid #333 !important;
            background-color: transparent !important;
            color: #333 !important;
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
    
    # 2. Lista oficial restaurada
    sobre_list = [
        "comments", "prefácio", "machina", "off-machina", "outros",
        "traduttore", "imagens", "samizdát", "notes", "index",
        "bibliografia", "license"
    ]
    
    # Grid de Navegação
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
        # 1. DISPARO ESTÁVEL: Usando index dinâmico baseado no state
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
        
        lang_code = idiomas_dict[idiomas_labels[st.session_state.lang_idx]]

    st.divider()
    st.markdown('<div class="titulo-logo">a Machina de Fazer Poesia</div>', unsafe_allow_html=True)

    with st.container():
        # 3. TRATAMENTO INDEX / TEMPO
        if st.session_state.sub_sobre.upper() == "INDEX":
            st.markdown("### Metadados do Tema: TEMPO")
            st.markdown(
                f"""<div class="metadados-tempo">
Tempo : 112.765.820.236.797.923.580.529.825.269.143.876.665.344.000.000.000
Total : 112.765.820.265.471.186.578.333.495.090.938.981.765.900.724.963.269
                </div>""", unsafe_allow_html=True
            )
            # 4. TODO: Análise Combinatória
            st.warning("TODO: Refazer Análise Combinatória - Divergência detectada nos quindecilhões.")
            st.divider()

        # Renderização do Conteúdo
        choice_file = st.session_state.sub_sobre.upper()
        if choice_file == "MACHINA":
            raw_text = load_md_file("ABOUT_MACHINA_A") + "\n\n" + load_md_file("ABOUT_MACHINA_D")
        else:
            raw_text = load_md_file(f"ABOUT_{choice_file}")
        
        with st.spinner(f"Sincronizando Machina ({idiomas_labels[st.session_state.lang_idx]})..."):
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
