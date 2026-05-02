import streamlit as st
import os
import re
import urllib.parse
from deep_translator import GoogleTranslator

# --- 0. MOTORES DA MACHINA (SUPORTE & LIMPEZA) ---
def sanitize_links(text):
    """Limpa URLs e remove rastreadores."""
    if not text: return ""
    redir_pattern = r"https?://[l|www]\.(?:facebook|google)\.[a-z\.]+/l\.php\?u=([^& \n]+)&?[^ \n]*"
    def clean_redir(match): return urllib.parse.unquote(match.group(1))
    text = re.sub(redir_pattern, clean_redir, text)
    junk_pattern = r"(\?|&)(fbclid|si|igshid|utm_[a-z]+)=[^ \n\)]+"
    text = re.sub(junk_pattern, "", text)
    return text

def load_md_file(filename):
    """Carrega arquivos MD com sanitização na origem."""
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
    """Motor de tradução via deep-translator."""
    if target_lang_code == "pt": return text
    try:
        return GoogleTranslator(source='auto', target=target_lang_code).translate(text)
    except: return text

def set_style_machina():
    """CSS: Alinhamento assimétrico, botão áudio e títulos elegantes."""
    st.markdown(
        """
        <style>
        [data-testid="stMainInternal"] { max-width: 95% !important; padding: 2rem !important; }
        
        /* Título Principal Logo abaixo do Divider */
        .titulo-logo {
            font-size: 2.2rem !important;
            font-weight: bold !important;
            margin-top: 1rem;
            margin-bottom: 1.5rem;
            color: #1E1E1E;
        }

        /* Padronização de Títulos do Corpo (H1, H2, H3) */
        h1 { font-size: 1.8rem !important; font-weight: bold !important; }
        h2 { font-size: 1.5rem !important; font-weight: bold !important; }
        h3 { font-size: 1.2rem !important; font-weight: bold !important; }
        p { font-size: 1.05rem !important; line-height: 1.6; text-align: justify; }

        /* Sincronização de Alturas */
        .stSelectbox div[data-baseweb="select"] > div {
            height: 2.8rem !important;
        }

        /* Botões Sair e Áudio */
        .stButton > button {
            height: 2.8rem !important;
            border-radius: 4px;
            font-weight: bold;
            transition: all 0.2s ease-in-out;
            margin-top: 28px;
        }
        
        /* Estilo Sair (Provocação Vermelha) */
        .btn-sair > div > button {
            border: 1px solid #ff4b4b !important;
            background-color: transparent !important;
            color: #ff4b4b !important;
            width: 80px !important;
        }
        .btn-sair > div > button:hover {
            background-color: #ff4b4b !important;
            color: white !important;
        }

        /* Estilo Áudio (Inclusão) */
        .btn-audio > div > button {
            border: 1px solid #333 !important;
            background-color: transparent !important;
            color: #333 !important;
            width: 100% !important;
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
    
    # Grid de Navegação Assimétrico
    c_sair, c_audio, c_doc, c_lang = st.columns([0.5, 0.8, 2, 1])
    
    with c_sair:
        st.markdown('<div class="btn-sair">', unsafe_allow_html=True)
        if st.button("sair", key="btn_exit"):
            st.session_state.pagina_ativa = "principal"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with c_audio:
        st.markdown('<div class="btn-audio">', unsafe_allow_html=True)
        if st.button("audio 🔈", key="btn_talk"):
            # TODO: Implementar gTTS
            pass
        st.markdown('</div>', unsafe_allow_html=True)

    with c_doc:
        # Título alterado para minúsculas conforme pedido
        choice_label = st.selectbox("documentação", sobre_list, 
                                   index=sobre_list.index(st.session_state.sub_sobre) if st.session_state.sub_sobre in sobre_list else 0,
                                   key="sel_doc")
        st.session_state.sub_sobre = choice_label.lower()

    with c_lang:
        # Título alterado para minúsculas conforme pedido
        sel_lang = st.selectbox("idiomas", idiomas_labels, 
                               index=st.session_state.lang_idx,
                               key="sel_lang")
        st.session_state.lang_idx = idiomas_labels.index(sel_lang)
        lang_code = idiomas_dict[sel_lang]

    st.divider()

    # Título Principal da Machina (Tamanho calibrado entre logo e corpo)
    st.markdown('<div class="titulo-logo">a Machina de Fazer Poesia</div>', unsafe_allow_html=True)

    # BLOCO DE RENDERIZAÇÃO REATIVO
    with st.container():
        choice_file = st.session_state.sub_sobre.upper()
        
        if choice_file == "MACHINA":
            raw_text = load_md_file("ABOUT_MACHINA_A") + "\n\n" + load_md_file("ABOUT_MACHINA_D")
        else:
            raw_text = load_md_file(f"ABOUT_{choice_file}")
        
        # A reatividade agora é forçada pelo spinner atrelado ao sel_lang
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
