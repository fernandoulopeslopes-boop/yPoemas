import os
import sys
import random
import socket
import streamlit as st
import streamlit_antd_components as sac

# --- 1. ENGENHARIA DE ESTRADA (CONFIG) ---
st.set_page_config(page_title="yPoemas 2026", layout="wide")

# Garante que o Python ache o motor lay_2_ypo.py na raiz
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from lay_2_ypo import gera_poema
except ImportError:
    st.error("ERRO: O arquivo 'lay_2_ypo.py' não foi encontrado no GitHub.")
    st.stop()

# Identificação para arquivos temporários (LYPO)
hostname = socket.gethostname()
IPAddres = socket.gethostbyname(hostname)

# --- 2. GAIOLA DE PROTEÇÃO (SESSÃO) ---
if 'tema_idx' not in st.session_state:
    st.session_state.tema_idx = 0
if 'sub_take' not in st.session_state:
    st.session_state.sub_take = 0
if 'aba_atual' not in st.session_state:
    st.session_state.aba_atual = "Mini"

# --- 3. MOTOR INTERNO (A PONTE) ---
def load_poema_interno(nome_tema, seed_eureka):
    """Aciona o motor gera_poema e formata para a tela."""
    try:
        script = gera_poema(nome_tema, seed_eureka)
        novo_ypoema = ""
        lypo_user = f"LYPO_{IPAddres}"
        
        # Garante pasta de cache
        if not os.path.exists("./temp"):
            os.makedirs("./temp")
            
        with open(os.path.join("./temp/", lypo_user), "w", encoding="utf-8") as f:
            f.write(nome_tema + "\n")
            for line in script:
                f.write(line + "\n")
                novo_ypoema += (line if line != "\n" else "") + "<br>"
        return novo_ypoema
    except Exception as e:
        return f"Erro no motor: {e}"

# --- 4. AS ESTRADAS (ABAS) ---
aba = sac.tabs([
    sac.TabsItem(label='Mini', icon='lightning-charge'),
    sac.TabsItem(label='yPoemas', icon='pentagon'),
    sac.TabsItem(label='Eureka', icon='search'),
    sac.TabsItem(label='Help', icon='question-circle'),
], align='center', variant='compact')

# SEUS TEMAS REAIS (Ajuste esta lista com os nomes dos seus .txt)
lista_mini_nomes = ["mini_01", "mini_02", "mini_03", "mini_04"] 

# Lógica de limites
if aba == 'Mini':
    st.session_state.limite_max = len(lista_mini_nomes) - 1
elif aba == 'yPoemas':
    st.session_state.limite_max = 144
else:
    st.session_state.limite_max = 0

# Reset ao trocar de aba
if aba != st.session_state.aba_atual:
    st.session_state.tema_idx = 0
    st.session_state.sub_take = 0
    st.session_state.aba_atual = aba

# --- 5. O COCKPIT (VOLANTE DE 1 LINHA) ---
_, b_more, b_last, b_rand, b_next, b_help, b_love, _ = st.columns([2, 1, 1, 1, 1, 1, 1, 2])

with b_more:
    if st.button("✚"):
        st.session_state.sub_take += 1
        st.rerun()

with b_last:
    if st.button("◀"):
        st.session_state.tema_idx = (st.session_state.tema_idx - 1) % (st.session_state.limite_max + 1)
        st.rerun()

with b_rand:
    if st.button("✻"):
        st.session_state.tema_idx = random.randint(0, st.session_state.limite_max)
        st.rerun()

with b_next:
    if st.button("▶"):
        st.session_state.tema_idx = (st.session_state.tema_idx + 1) % (st.session_state.limite_max + 1)
        st.rerun()

with b_help:
    st.button("?")

with b_love:
    st.button("❤")

# --- 6. A PAISAGEM (OUTPUT) ---
st.divider()

if aba == 'Mini':
    nome_atual = lista_mini_nomes[st.session_state.tema_idx]
    texto = load_poema_interno(nome_atual, str(st.session_state.sub_take))
    st.markdown(f"<div style='text-align: center;'>{texto}</div>", unsafe_allow_html=True)

elif aba == 'yPoemas':
    st.info(f"Página yPoemas - Tema atual: {st.session_state.tema_idx}")
