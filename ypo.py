import streamlit as st
import os
import random

# ==========================================
# 1. CSS DE IMPACTO (FONTE GRANDE E SIDEBAR TRAVADA)
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
    /* 1. TRAVA SIDEBAR EM 310PX */
    [data-testid="stSidebar"] {
        min-width: 310px !important;
        max-width: 310px !important;
    }

    /* 2. CENTRALIZA E ESTILIZA O PALCO (ÁREA DE LEITURA) */
    [data-testid="stAppViewBlockContainer"] {
        max-width: 850px !important;
        margin: 0 auto !important;
    }

    /* 3. FONTE DA POESIA (AUMENTADA PARA LEITURA CLARA) */
    .poema-palco {
        font-family: 'Times New Roman', Times, serif !important;
        font-size: 32px !important; /* Fonte grande conforme solicitado */
        line-height: 1.6 !important;
        color: #1a1a1a !important;
        white-space: pre-wrap;
        padding: 40px 20px;
        background-color: #ffffff;
        border-radius: 8px;
    }

    /* 4. BOTÕES E COMPONENTES */
    .stButton>button { 
        width: 100%; 
        height: 3.5em; 
        font-weight: bold;
        font-size: 16px;
    }
    </style> """,
    unsafe_allow_html=True,
)

# --- MOTOR ---
try:
    from lay_2_ypo import gera_poema
except Exception as e:
    def gera_poema(t, s=""): return [f"Erro no motor: {str(e)}"]

# ==========================================
# 2. GESTÃO DE ESTADO (SEM CONGELAMENTO)
# ==========================================
if 'take' not in st.session_state:
    st.session_state.take = random.randint(1000, 9999)
if 'sala' not in st.session_state:
    st.session_state.sala = "yPoemas"

# ==========================================
# 3. HIERARQUIA VISUAL (CIMA -> BAIXO)
# ==========================================

# --- NÍVEL 1: NAVEGAÇÃO (FAROL) ---
n1, n2, n3, n4, n_info = st.columns([1, 1, 1, 1, 1.5])

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
with n_info:
    st.info(f"ID: {st.session_state.take}")

st.write("") # Espaço

# --- NÍVEL 2: MENU DE PÁGINAS (SALAS) ---
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

# --- NÍVEL 3: ÁREA DE LEITURA (O PALCO) ---
if st.session_state.sala == "yPoemas":
    # Passamos a semente explicitamente para forçar a mudança de tema
    resultado = gera_poema("Fatos", str(st.session_state.take))
    
    # Limpeza de dados (para não virar dicionário feio)
    if isinstance(resultado, dict):
        texto_final = "\n".join([str(v) for v in resultado.values()])
    elif isinstance(resultado, list):
        texto_final = "\n".join([str(p) for p in resultado])
    else:
        texto_final = str(resultado)

    # EXIBIÇÃO NO PALCO COM FONTE GRANDE
    st.markdown(f'<div class="poema-palco">{texto_final}</div>', unsafe_allow_html=True)
else:
    st.subheader(f"Sala: {st.session_state.sala.upper()}")
    st.write("Em calibração...")

# ==========================================
# 4. SIDEBAR (CONTROLES E IMAGEM)
# ==========================================
with st.sidebar:
    st.title("A Machina")
    st.selectbox("Idioma", ["Português", "English", "Español"], key="lang")
    st.write("---")
    st.checkbox("🖼️ Arte", key="draw_machina")
    st.checkbox("🔊 Voz", key="talk_machina")
    st.checkbox("🎬 Vídeo", key="vyde_machina")
    st.write("---")
    
    img_path = mapa_artes.get(st.session_state.sala, "img_ypoemas.jpg")
    if os.path.exists(img_path):
        st.image(img_path, use_column_width=True)
        
