import streamlit as st
import os

# --- 1. MOTOR ---
@st.cache_data(show_spinner=False)
def abre(nome_do_tema):
    base_path = os.path.dirname(__file__)
    full_name = os.path.join(base_path, "data", nome_do_tema + ".ypo")
    lista = []
    with open(full_name, encoding="utf-8") as file:
        for line in file:
            lista.append(line)
    return lista

# --- 2. ESTADO ---
if 'mini_idx' not in st.session_state:
    st.session_state.mini_idx = 0

# --- 3. LISTA (A SEQUÊNCIA DO LIVRO) ---
lista_mini_real = [
    "mini_01",
    "mini_02",
    "mini_03"
]

st.session_state.limite_mini = len(lista_mini_real) - 1

# --- 4. EXECUÇÃO ---
tema_alvo = lista_mini_real[st.session_state.mini_idx]
conteudo_fiel = abre(tema_alvo)

# --- 5. INTERFACE (LINHA ÚNICA) ---
c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1: st.button("more")
with c2:
    if st.button("last") and st.session_state.mini_idx > 0:
        st.session_state.mini_idx -= 1
        st.rerun()
with c3: st.button("rand")
with c4:
    if st.button("next") and st.session_state.mini_idx < st.session_state.limite_mini:
        st.session_state.mini_idx += 1
        st.rerun()
with c5: st.button("help")
with c6: st.button("love")

# --- 6. EXIBIÇÃO ---
st.write(f"### {tema_alvo}")
for linha in conteudo_fiel:
    st.write(linha.strip())
