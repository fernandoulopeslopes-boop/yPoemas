import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="a Máquina de Fazer Poesia", layout="wide")

# --- ESTÉTICA PTC: LARGURA 300px E FORMATAÇÃO ---
st.markdown(
    """
    <style>
        /* Fixa a largura da sidebar em 300px conforme protocolo */
        [data-testid="stSidebar"][aria-expanded="true"] {
            min-width: 300px;
            max-width: 300px;
        }
        
        /* Centraliza e ajusta o seletor de idiomas */
        .stSelectbox div[data-baseweb="select"] {
            max-width: 260px;
            margin: 0 auto;
        }

        /* Container para a Arte da Página (Mandala/Símbolo) */
        .sidebar-arte {
            display: flex;
            justify-content: center;
            padding: 20px 0;
            text-align: center;
            font-family: monospace;
            white-space: pre;
        }

        /* Texto da Descrição da Variação */
        .sidebar-descricao {
            font-size: 0.95rem;
            line-height: 1.6;
            text-align: justify;
            padding: 10px;
            color: #444;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- SIDEBAR: O COCKPIT DO LEITOR ---
with st.sidebar:
    # 1. Dropdown de Idiomas (Curadoria ABC Latino + Suporte gTTS)
    idiomas_opcoes = {
        "Português": "pt",
        "Español": "es",
        "Italiano": "it",
        "Français": "fr",
        "English": "en",
        "Català": "ca",
        "--- Mundo Latino ---": None,
        "Alemão": "de",
        "Croata": "hr",
        "Dinamarquês": "da",
        "Filipino": "tl",
        "Finlandês": "fi",
        "Holandês": "nl",
        "Húngaro": "hu",
        "Indonésio": "id",
        "Latim": "la",
        "Norueguês": "no",
        "Polonês": "pl",
        "Romeno": "ro",
        "Sueco": "sv",
        "Turco": "tr",
        "Vietnamita": "vi"
    }

    idioma_nome = st.selectbox(
        "Idioma",
        options=list(idiomas_opcoes.keys()),
        index=0,
        label_visibility="collapsed",
        key="cockpit_lang_select"
    )
    
    # Lógica para capturar a sigla (fallback para PT em caso de separador)
    idioma_sigla = idiomas_opcoes.get(idioma_nome) or "pt"

    st.divider()

    # 2. Arte da Página (Dinâmica)
    st.markdown('<div class="sidebar-arte">', unsafe_allow_html=True)
    if 'arte_da_pagina' in st.session_state:
        st.write(st.session_state.arte_da_pagina)
    elif 'arte_da_pagina' in globals():
        st.write(arte_da_pagina)
    else:
        st.write("((( ๑ )))") # Arte minimalista de espera
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # 3. Descritivo da Página (Dinâmica)
    st.markdown('<div class="sidebar-descricao">', unsafe_allow_html=True)
    if 'descricao_da_pagina' in st.session_state:
        st.write(st.session_state.descricao_da_pagina)
    elif 'descricao_da_pagina' in globals():
        st.write(descricao_da_pagina)
    else:
        st.write("Aguardando definição da variação...")
    st.markdown('</div>', unsafe_allow_html=True)

# --- CORPO PRINCIPAL ---
st.title("a Máquina de Fazer Poesia")

# Confirmação de estado para o teste
st.info(f"Cockpit ativo em **{idioma_nome}**. Pronto para a próxima engrenagem.")
