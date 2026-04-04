import streamlit as st
import os
import random

# --- 1. MOTOR: ABERTURA (MANDALA / CASE-SENSITIVE) ---
@st.cache_data(show_spinner=False)
def abre(nome_do_tema):
    """
    Motor original ajustado para o Axioma_Zero.
    Resolve a divergência entre Windows (ypo) e Linux (YPO).
    """
    # Localização absoluta no servidor /mount/src/ypoemas/
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    # A força da extensão em maiúsculas (.YPO)
    arquivo = f"{nome_do_tema}.YPO"
    full_name = os.path.join(base_path, "data", arquivo)
    
    lista = []
    try:
        with open(full_name, encoding="utf-8") as file:
            for line in file:
                lista.append(line)
            # file.close() automático pelo 'with'
    except FileNotFoundError:
        return [f"ERRO: {arquivo} não encontrado no diretório /data."]
        
    return lista

# --- 2. GESTÃO DE ESTADO (NAVEGAÇÃO) ---
if 'mini_idx' not in st.session_state:
    st.session_state.mini_idx = 0

# --- 3. BIBLIOTECA DE TEMAS ---
# Lista que rege a sequência da Machina
lista_mini_real = [
    "mini_01",
    "mini_02",
    "mini_03"
]

st.session_state.limite_mini = len(lista_mini_real) - 1

# --- 4. IDENTIFICAÇÃO DO ALVO ---
tema_alvo = lista_mini_real[st.session_state.mini_idx]
conteudo_fiel = abre(tema_alvo)

# --- 5. INTERFACE (PAINEL HEXAGONAL) ---
# more / last / rand / next / help / love
c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:
    st.button("more")

with c2:
    if st.button("last"):
        if st.session_state.mini_idx > 0:
            st.session_state.mini_idx -= 1
            st.rerun()

with c3:
    if st.button("rand"):
        st.session_state.mini_idx = random.randint(0, st.session_state.limite_mini)
        st.rerun()

with c4:
    if st.button("next"):
        if st.session_state.mini_idx < st.session_state.limite_mini:
            st.session_state.mini_idx += 1
            st.rerun()

with c5:
    if st.button("help"):
        st.toast("Protocolo de Navegação Ativo")

with c6:
    if st.button("love"):
        st.snow()

# --- 6. EXIBIÇÃO (O POEMA) ---
st.markdown("---")
st.write(f"### {tema_alvo}")

# O loop que imprime a alma do arquivo
for linha in conteudo_fiel:
    st.write(linha.strip())

st.markdown("---")
