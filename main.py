import os
import sys
import random
import socket
import streamlit as st
import streamlit_antd_components as sac

# --- 1. LOGÍSTICA DE PISTA (CONFIG) ---
st.set_page_config(page_title="yPoemas 2026 - Mini", layout="wide")

# Localização do motor (lay_2_ypo.py)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from lay_2_ypo import gera_poema
except ImportError:
    st.error("ERRO: O arquivo 'lay_2_ypo.py' não foi localizado.")
    st.stop()

# Identidade de rede para arquivos temporários
hostname = socket.gethostname()
IPAddres = socket.gethostbyname(hostname)

# --- 2. GAIOLA DE PROTEÇÃO (SESSÃO MINI) ---
if 'mini_idx' not in st.session_state:
    st.session_state.mini_idx = 0
if 'sub_take' not in st.session_state:
    st.session_state.sub_take = 0

# --- 3. A PONTE (MOTOR INTERNO) ---
def load_poema_interno(nome_tema, seed_eureka):
    """Executa o motor e formata a saída para o Leitor."""
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
                novo_ypoema += (line if line != "\n" else "") + "<br>"
        return novo_ypoema
    except Exception as e:
        return f"Erro no motor: {e}"

# --- 4. CONTEÚDO DA PÁGINA MINI ---
# Lista rigorosa de temas que possuem .ypo na pasta \data
lista_mini_temas = ["Fatos", "Linguafiada", "Livro_Vivo", "Faz_de_Conto", "Um_Romance"]
st.session_state.limite_mini = len(lista_mini_temas) - 1

# --- 5. O COCKPIT (VOLANTE DE 1 LINHA) ---
# Centralizado e direto para o Leitor
_, b_more, b_last, b_rand, b_next, b_help, b_love, _ = st.columns([2, 1, 1, 1, 1, 1, 1, 2])

with b_more:
    if st.button("✚", help="Mais variações do tema atual"):
        st.session_state.sub_take += 1
        st.rerun()

with b_last:
    if st.button("◀", help="Tema anterior"):
        st.session_state.mini_idx = (st.session_state.mini_idx - 1) % (st.session_state.limite_mini + 1)
        st.rerun()

with b_rand:
    if st.button("✻", help="Tema aleatório"):
        st.session_state.mini_idx = random.randint(0, st.session_state.limite_mini)
        st.rerun()

with b_next:
    if st.button("▶", help="Próximo tema"):
        st.session_state.mini_idx = (st.session_state.mini_idx + 1) % (st.session_state.limite_mini + 1)
        st.rerun()

with b_help:
    if st.button("?", help="Ajuda"):
        pass

with b_love:
    if st.button("❤", help="Favoritos"):
        pass

# --- 6. A EXIBIÇÃO (INTERAÇÃO MACHINA-LEITOR) ---
st.divider()

# Busca o tema atual da lista Mini
tema_atual = lista_mini_temas[st.session_state.mini_idx]

# Aciona o motor e entrega ao Leitor
texto_saida = load_poema_interno(tema_atual, str(st.session_state.sub_take))

# Exibição centralizada do conteúdo
st.markdown(
    f"""
    <div style='text-align: center; font-family: sans-serif; line-height: 1.6;'>
        <h3 style='color: #555;'>{tema_atual}</h3>
        <p style='font-size: 1.2rem;'>{texto_saida}</p>
    </div>
    """, 
    unsafe_allow_html=True
)
