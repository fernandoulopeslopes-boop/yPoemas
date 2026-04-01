import streamlit as st
import os
import random

# 1. CONFIGURAÇÃO (WIDE É O ÚNICO QUE TRAVA SIDEBAR)
st.set_page_config(page_title="yPoemas", layout="wide")

# 2. MARRETA CSS (FORÇANDO 310PX E HIERARQUIA)
st.markdown("""
    <style>
        /* Trava Sidebar */
        [data-testid="stSidebar"] {
            min-width: 310px !important;
            max-width: 310px !important;
        }
        /* Centraliza Conteúdo */
        [data-testid="stAppViewBlockContainer"] {
            max-width: 800px !important;
            margin: 0 auto !important;
        }
        /* Fonte Única Poesia */
        .poesia {
            font-family: serif !important;
            font-size: 24px !important;
            line-height: 1.5;
            white-space: pre-wrap;
        }
        .stButton>button { height: 3em; }
    </style>
""", unsafe_allow_html=True)

# Import do Motor
try:
    from lay_2_ypo import gera_poema
except:
    def gera_poema(t, s=""): return "Motor Offline"

# Inicialização de Estados
if 'take' not in st.session_state: st.session_state.take = 0
if 'sala' not in st.session_state: st.session_state.sala = "YPOEMAS"

# --- HIERARQUIA DE CIMA PARA BAIXO ---

# A. BOTÕES DE NAVEGAÇÃO (FAROL)
c1, c2, c3, c4, c5 = st.columns(5)
if c1.button("✚"): st.session_state.take = random.randint(0, 999); st.rerun()
if c2.button("◀"): st.session_state.take -= 1; st.rerun()
if c3.button("✻"): st.session_state.take = random.randint(0, 999); st.rerun()
if c4.button("▶"): st.session_state.take += 1; st.rerun()
with c5: st.write("Ref: " + str(st.session_state.take))

st.write("---")

# B. BUTTONS DAS PÁGINAS
salas = ["MINI", "YPOEMAS", "EUREKA", "OFF", "BOOKS", "POLY", "SOBRE"]
cols_m = st.columns(len(salas))
for i, s in enumerate(salas):
    if cols_m[i].button(s):
        st.session_state.sala = s
        st.rerun()

st.write("---")

# C. ÁREA DE LEITURA
if st.session_state.sala == "YPOEMAS":
    raw = gera_poema("Fatos", str(st.session_state.take))
    # Limpeza radical de lixo de dados
    if isinstance(raw, (list, dict)):
        texto = "\n".join([str(v) for v in (raw.values() if isinstance(raw, dict) else raw)])
    else:
        texto = str(raw)
    
    st.markdown(f'<div class="poesia">{texto}</div>', unsafe_allow_html=True)
else:
    st.write(f"SALA: {st.session_state.sala}")

# SIDEBAR (LIMPA)
with st.sidebar:
    st.title("yPoemas")
    st.selectbox("Idioma", ["Português", "English"], key="lang")
    st.checkbox("🖼️ Desenho", key="draw_machina")
    st.checkbox("🔊 Voz", key="talk_machina")
    st.checkbox("🎬 Vídeo", key="vyde_machina")
    st.write("---")
    # Tenta carregar imagem se existir
    img = f"img_{st.session_state.sala.lower()}.jpg"
    if os.path.exists(img):
        st.image(img)
