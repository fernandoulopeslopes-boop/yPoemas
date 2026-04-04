import streamlit as st
import os
import random

# --- 1. MOTOR DE ABERTURA (PROTOCOLO AXIOMA_ZERO) ---
@st.cache_data(show_spinner=False)
def abre(nome_do_tema):
    """
    :param nome_do_tema
    :return: lista do arquivo
    """
    # Caminho absoluto para garantir funcionamento no Streamlit Cloud (Linux)
    base_path = os.path.dirname(os.path.abspath(__file__))
    # Extensão .YPO em maiúsculas conforme a realidade da pasta /data
    full_name = os.path.join(base_path, "data", nome_do_tema + ".YPO")
    
    lista = []
    try:
        with open(full_name, encoding="utf-8") as file:
            for line in file:
                lista.append(line)
            file.close()
    except FileNotFoundError:
        return [f"ERRO: {nome_do_tema}.YPO não encontrado."]
        
    return lista

# --- 2. GESTÃO DE ESTADO ---
if 'mini_idx' not in st.session_state:
    st.session_state.mini_idx = 0

# --- 3. LISTA DE TEMAS (SEQUÊNCIA AUTORAL) ---
# Substitua pelos nomes reais dos seus arquivos na pasta /data
lista_mini_real = [
    "mini_01",
    "mini_02",
    "mini_03"
]

st.session_state.limite_mini = len(lista_mini_real) - 1

# --- 4. EXECUÇÃO DO TEMA ---
tema_alvo = lista_mini_real[st.session_state.mini_idx]
conteudo_fiel = abre(tema_alvo)

# --- 5. INTERFACE (PAINEL DE LINHA ÚNICA) ---
# more / last / rand / next / help / love
c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:
    if st.button("more"):
        pass

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
        st.toast("Navegação da Machina de Poesia")

with c6:
    if st.button("love"):
        st.snow()

# --- 6. EXIBIÇÃO DO YPOEMA ---
st.markdown("---")
st.write(f"### {tema_alvo}")

for linha in conteudo_fiel:
    st.write(linha.strip())
st.markdown("---")
