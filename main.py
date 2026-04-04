import os
import sys
import random
import socket
import streamlit as st

# --- 1. CONFIGURAÇÃO BÁSICA ---
st.set_page_config(page_title="yPoemas 2026 - Mini", layout="wide")

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from lay_2_ypo import gera_poema
except ImportError:
    st.error("ERRO: 'lay_2_ypo.py' não encontrado na raiz.")
    st.stop()

hostname = socket.gethostname()
IPAddres = socket.gethostbyname(hostname)

# --- 2. GESTÃO DE SESSÃO (MINI) ---
if 'mini_idx' not in st.session_state:
    st.session_state.mini_idx = 0
if 'sub_take' not in st.session_state:
    st.session_state.sub_take = 0

# --- 3. FUNÇÃO DE CARREGAMENTO (INTERMEDIÁRIA) ---
def load_poema_interno(nome_tema, seed_eureka):
    """Aciona o motor e formata a saída HTML."""
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
                # Converte as quebras de linha para o navegador
                novo_ypoema += (line if line != "\n" else "") + "<br>"
        return novo_ypoema
    except Exception as e:
        return f"Erro no motor: {e}"

# --- 4. LISTA DE TEMAS (CONTEÚDO DO USUÁRIO) ---
# Adicione aqui apenas os temas que existem na pasta \data
lista_mini_real = ["Fatos", "Faz_de_Conto"] 
st.session_state.limite_mini = len(lista_mini_real) - 1

# --- 5. INTERFACE DE NAVEGAÇÃO (1 LINHA) ---
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

# --- 6. ÁREA DE EXIBIÇÃO ---
st.divider()

# Garantia de índice válido
if st.session_state.mini_idx > st.session_state.limite_mini:
    st.session_state.mini_idx = 0

tema_alvo = lista_mini_real[st.session_state.mini_idx]
conteudo_exibicao = load_poema_interno(tema_alvo, str(st.session_state.sub_take))

# Renderização centralizada
st.markdown(
    f"""
    <div style='text-align: center; font-size: 1.4rem; line-height: 1.6;'>
        {conteudo_exibicao}
    </div>
    """, 
    unsafe_allow_html=True
)
