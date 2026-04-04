import os
import sys
import random
import socket
import streamlit as st
import streamlit_antd_components as sac

# --- 1. ENGENHARIA DE ESTRADA (LOGÍSTICA) ---
st.set_page_config(page_title="yPoemas 2026", layout="wide")

# Caminho para o motor lay_2_ypo.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from lay_2_ypo import gera_poema
except ImportError:
    st.error("ERRO: O arquivo 'lay_2_ypo.py' não foi localizado no GitHub.")
    st.stop()

# Identidade de rede para arquivos temporários (LYPO)
hostname = socket.gethostname()
IPAddres = socket.gethostbyname(hostname)

# --- 2. GAIOLA DE PROTEÇÃO (SESSÃO) ---
if 'tema_idx' not in st.session_state:
    st.session_state.tema_idx = 0
if 'sub_take' not in st.session_state:
    st.session_state.sub_take = 0
if 'aba_atual' not in st.session_state:
    st.session_state.aba_atual = "Mini"

# --- 3. A PONTE (MOTOR INTERNO) ---
def load_poema_interno(nome_tema, seed_eureka):
    """Executa o motor e formata a saída HTML para o Streamlit."""
    try:
        script = gera_poema(nome_tema, seed_eureka)
        novo_ypoema = ""
        lypo_user = f"LYPO_{IPAddres}"
        
        if not os.path.exists("./temp"):
            os.makedirs("./temp")
            
        with open(os.path.join("./temp/", lypo_user), "w", encoding="utf-8") as f:
            f.write(nome_tema + "\n")
            for line in script:
                f.write(line + "\n")
                # Preserva quebras de linha enviadas pelo motor
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

# FUNÇÃO PARA CARREGAR LISTA DE TEMAS (O SEU CONTEÚDO)
def carregar_temas_reais(qual_aba):
    """Lê seus arquivos de controle para alimentar a lista de temas."""
    # Aqui você pode usar sua lógica de carregar de rol_*.txt se preferir
    # Por enquanto, mantemos a estrutura funcional:
    return ["Fatos", "A_Torre_de_Papel", "Linguafiada", "Livro_Vivo", 
            "Faz_de_Conto", "Um_Romance", "Quase_Que_Eu_Poesia", "Segredo_Público"]

lista_temas = carregar_temas_reais(aba)
st.session_state.limite_max = len(lista_temas) - 1

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

# --- 6. A PAISAGEM (SAÍDA DO CONTEÚDO) ---
st.divider()

if st.session_state.tema_idx <= st.session_state.limite_max:
    nome_atual = lista_temas[st.session_state.tema_idx]
    texto = load_poema_interno(nome_atual, str(st.session_state.sub_take))
    st.markdown(f"<div style='text-align: center;'>{texto}</div>", unsafe_allow_html=True)
