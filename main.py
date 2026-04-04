import os
import sys
import random
import socket
import streamlit as st

# --- 1. LOGÍSTICA (SEM RUIDO) ---
st.set_page_config(page_title="yPoemas 2026 - Mini", layout="wide")

# Caminho para o motor
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from lay_2_ypo import gera_poema
except ImportError:
    st.error("ERRO: O arquivo 'lay_2_ypo.py' não foi localizado.")
    st.stop()

# Identificação para arquivos temporários
hostname = socket.gethostname()
IPAddres = socket.gethostbyname(hostname)

# --- 2. GAIOLA DE PROTEÇÃO (SESSÃO MINI) ---
if 'mini_idx' not in st.session_state:
    st.session_state.mini_idx = 0
if 'sub_take' not in st.session_state:
    st.session_state.sub_take = 0

# --- 3. MOTOR INTERNO (PONTE DIRETA) ---
def load_poema_interno(nome_tema, seed_eureka):
    """Executa o motor estritamente para arquivos em ./data/"""
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
                # O motor entrega as linhas; formatamos para o Leitor
                novo_ypoema += (line if line != "\n" else "") + "<br>"
        return novo_ypoema
    except Exception as e:
        return f"Erro no motor: {e}"

# --- 4. CONTEÚDO RESTRITO À PÁGINA MINI ---
# FOCO: Apenas o que reside fisicamente em \data e pertence ao fluxo Mini.
# Removidos: Linguafiada, Um_Romance, e qualquer outro 'off-machina'.
lista_mini_real = ["Fatos", "Livro_Vivo", "Faz_de_Conto"]
st.session_state.limite_mini = len(lista_mini_real) - 1

# --- 5. O COCKPIT (VOLANTE DE 1 LINHA) ---
# NAVEGAÇÃO: ✚ (more) | ◀ (last) | ✻ (rand) | ▶ (next) | ? (help) | ❤ (love)
_, b_more, b_last, b_rand, b_next, b_help, b_love, _ = st.columns([2, 1, 1, 1, 1, 1, 1, 2])

with b_more:
    if st.button("✚"):
        st.session_state.sub_take += 1
        st.rerun()

with b_last:
    if st.button("◀"):
        st.session_state.mini_idx = (st.session_state.mini_idx - 1) % (st.session_state.limite_mini + 1)
        st.rerun()

with b_rand:
    if st.button("✻"):
        st.session_state.mini_idx = random.randint(0, st.session_state.limite_mini)
        st.rerun()

with b_next:
    if st.button("▶"):
        st.session_state.mini_idx = (st.session_state.mini_idx + 1) % (st.session_state.limite_mini + 1)
        st.rerun()

with b_help:
    st.button("?")

with b_love:
    st.button("❤")

# --- 6. EXIBIÇÃO (INTERFACE) ---
st.divider()

# Segurança de índice
if st.session_state.mini_idx > st.session_state.limite_mini:
    st.session_state.mini_idx = 0

tema_alvo = lista_mini_real[st.session_state.mini_idx]
conteudo_final = load_poema_interno(tema_alvo, str(st.session_state.sub_take))

# Exibição Final para o Leitor
st.markdown(
    f"""
    <div style='text-align: center; font-family: serif;'>
        <p style='color: #999; font-size: 0.8rem; margin-bottom: 20px;'>{tema_alvo}</p>
        <div style='font-size: 1.4rem; line-height: 1.5;'>
            {conteudo_final}
        </div>
    </div>
    """, 
    unsafe_allow_html=True
)
