import streamlit as st
import os
import random

# ==========================================
# 1º ANDAR: CONFIGURAÇÃO E CSS DE PRECISÃO
# ==========================================
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="wide", 
    initial_sidebar_state="expanded",
)

st.markdown(
    """ 
    <style> 
    /* TRAVA RIGOROSA DA SIDEBAR EM 310PX */
    [data-testid="stSidebar"] {
        min-width: 310px !important;
        max-width: 310px !important;
    }

    /* CENTRALIZA O PALCO DA POESIA NO LAYOUT WIDE */
    [data-testid="stAppViewBlockContainer"] {
        max-width: 850px !important;
        margin: 0 auto !important;
        padding-top: 1rem !important;
    }

    /* TIPOGRAFIA DA ÁREA DE LEITURA */
    .poema-box {
        font-family: serif !important;
        font-size: 26px !important;
        line-height: 1.5 !important;
        color: #1a1a1a !important;
        white-space: pre-wrap;
        margin-top: 30px;
        padding: 15px;
    }

    /* PADRONIZAÇÃO DOS BOTÕES */
    .stButton>button { 
        width: 100%; 
        height: 3.2em; 
        border-radius: 4px; 
        font-weight: bold;
    }
    </style> """,
    unsafe_allow_html=True,
)

# --- IMPORTAÇÃO DO MOTOR ---
try:
    from lay_2_ypo import gera_poema
except Exception as e:
    def gera_poema(t, s=""): return [f"Erro ao carregar motor: {str(e)}"]

# ==========================================
# 2º ANDAR: GESTÃO DE ESTADOS (SESSION STATE)
# ==========================================
if 'take' not in st.session_state:
    st.session_state.take = random.randint(1000, 9999)
if 'sala' not in st.session_state:
    st.session_state.sala = "yPoemas"
if 'lang' not in st.session_state:
    st.session_state.lang = "Português"

# ==========================================
# 3º ANDAR: ESTRUTURA DA PÁGINA (HIERARQUIA)
# ==========================================

# --- A. NÍVEL 1: NAVEGAÇÃO (FAROL) ---
st.write("### 🧭 Farol")
n1, n2, n3, n4, n_id = st.columns([1, 1, 1, 1, 1.5])

if n1.button("✚ NOVO"):
    st.session_state.take = random.randint(1000, 9999)
    st.rerun()
if n2.button("◀ VOLTAR"):
    st.session_state.take -= 1
    st.rerun()
if n3.button("✻ SORTEIO"):
    st.session_state.take = random.randint(1000, 9999)
    st.rerun()
if n4.button("▶ AVANÇAR"):
    st.session_state.take += 1
    st.rerun()
with n_id:
    st.info(f"Poema ID: {st.session_state.take}")

st.write("") # Respiro visual

# --- B. NÍVEL 2: MENU DE PÁGINAS (SALAS) ---
mapa_artes = {
    "mini": "img_mini.jpg",
    "yPoemas": "img_ypoemas.jpg",
    "eureka": "img_eureka.jpg",
    "off-machina": "img_off-machina.jpg",
    "books": "img_books.jpg",
    "poly": "img_poly.jpg",
    "sobre": "img_about.jpg"
}

salas = list(mapa_artes.keys())
cols_menu = st.columns(len(salas))

for i, nome_sala in enumerate(salas):
    if cols_menu[i].button(nome_sala.upper(), key=f"btn_{nome_sala}"):
        st.session_state.sala = nome_sala
        st.rerun()

st.divider()

# --- C. NÍVEL 3: ÁREA DE LEITURA ---
if st.session_state.sala == "yPoemas":
    # Passamos o tema e a semente (string) explicitamente
    resultado_bruto = gera_poema("Fatos", str(st.session_state.take))
    
    # TRATAMENTO DE DADOS (LIMPEZA DE DICIONÁRIO/LISTA)
    if isinstance(resultado_bruto, dict):
        texto_limpo = "\n".join([str(v) for v in resultado_bruto.values()])
    elif isinstance(resultado_bruto, list):
        texto_limpo = "\n".join([str(p) for p in resultado_bruto])
    else:
        texto_limpo = str(resultado_bruto)

    # Exibição Final
    st.markdown(f'<div class="poema-box">{texto_limpo}</div>', unsafe_allow_html=True)
else:
    st.subheader(f"Sala: {st.session_state.sala.upper()}")
    st.write("Aguardando calibração de conteúdo...")

# ==========================================
# 4º ANDAR: SIDEBAR (CONTROLES E ARTE)
# ==========================================
with st.sidebar:
    st.title("A Machina")
    st.selectbox("Idioma", ["Português", "English", "Español"], key="lang")
    
    st.write("---")
    st.checkbox("🖼️ Arte", key="draw_machina")
    st.checkbox("🔊 Voz", key="talk_machina")
    st.checkbox("🎬 Vídeo", key="vyde_machina")
    
    st.write("---")
    # Imagem dinâmica baseada na sala ativa
    img_atual = mapa_artes.get(st.session_state.sala, "img_ypoemas.jpg")
    if os.path.exists(img_atual):
        st.image(img_atual, use_column_width=True)
    else:
        st.caption(f"Arquivo de imagem não encontrado: {img_atual}")

if __name__ == "__main__":
    # Garantia final de que o estado não vai 'congelar'
    pass
    
