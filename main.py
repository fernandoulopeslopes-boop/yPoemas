import streamlit as st
import os
import re
import urllib.parse
from deep_translator import GoogleTranslator

# --- 0. MOTORES DA MACHINA (SUPORTE & FLUXO) ---

def process_text_flow(text):
    """
    MOTOR DE SOLDAGEM: Une linhas órfãs em fluxos contínuos.
    Se a linha for curta (uma sobra), ela é soldada à próxima.
    Preserva parágrafos (quebra dupla) e estruturas de lista/títulos.
    """
    if not text: return ""
    
    # Divide por parágrafos para manter a separação de blocos
    paragraphs = text.split('\n\n')
    processed_paragraphs = []
    
    for p in paragraphs:
        # Se for lista ou cabeçalho, mantém a formatação original do .MD
        if p.strip().startswith(('*', '-', '1.', '#')):
            processed_paragraphs.append(p)
        else:
            # Substitui quebras de linha simples por espaço (a "solda")
            # Isso absorve a 'pequena sobra' na linha seguinte automaticamente
            joined_line = p.replace('\n', ' ').strip()
            # Limpa espaços duplos resultantes da substituição
            joined_line = re.sub(r'\s+', ' ', joined_line)
            processed_paragraphs.append(joined_line)
            
    return '\n\n'.join(processed_paragraphs)

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
    """CSS: Geometria da Página e Padronização Oculta."""
    st.markdown(
        """
        <style>
        [data-testid="stMainInternal"] { max-width: 95% !important; padding: 2rem !important; }
        
        .conteudo-padronizado {
            max-width: 850px;
            margin: 0 auto;
            line-height: 1.7;
            word-wrap: break-word;
            text-align: justify; /* Justificado para evitar buracos no layout */
            font-size: 1.1rem;
        }

        .titulo-logo {
            font-size: 2.1rem !important;
            font-weight: bold !important;
            margin-bottom: 1.5rem;
        }

        .btn-sair > div > button {
            background-color: #ff4b4b !important;
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# --- 1. BOOTSTRAP & STATE ---
if 'pagina_ativa' not in st.session_state:
    st.session_state.pagina_ativa = "sobre"
if 'sub_sobre' not in st.session_state:
    st.session_state.sub_sobre = "comments"

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# --- 2. EXECUÇÃO DO FAROL ---
def page_sobre():
    set_style_machina()
    
    # Cabeçalho de Controle
    c_sair, c_audio, c_doc, c_lang = st.columns([0.6, 0.8, 2, 1])
    
    with c_sair:
        if st.button("sair", key="btn_exit"):
            st.session_state.pagina_ativa = "principal"
            st.rerun()

    # ... (outros seletores omitidos para brevidade) ...

    st.divider()
    st.markdown('<div class="titulo-logo">a Machina de Fazer Poesia</div>', unsafe_allow_html=True)

    # RENDERIZAÇÃO EM RUNTIME
    with st.container():
        # 1. Carrega o bruto
        raw_text = load_md_file(f"ABOUT_{st.session_state.sub_sobre.upper()}")
        
        # 2. Traduz (se necessário)
        # (Considerando tradução simplificada para o teste)
        translated_text = translate_content(raw_text, "pt")
        
        # 3. O PULO DO GATO: Soldagem de fluxo
        # Aqui a 'sobra' é anexada à próxima linha automaticamente.
        flow_text = process_text_flow(translated_text)
        
        # 4. Exibe com a moldura invisível
        st.markdown(f'<div class="conteudo-padronizado">{flow_text}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    if st.session_state.pagina_ativa == "sobre":
        page_sobre()
