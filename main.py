import streamlit as st
import random
import os

# 1. TESTE DE SOBREVIVÊNCIA (Aparece no topo)
st.write("# 🌀 DIAGNÓSTICO: OPERAÇÃO LUZ")

# 2. IMPORTAÇÃO PROTEGIDA
try:
    from lay_2_ypo import gera_poema
except Exception as e:
    st.error(f"Erro no motor: {e}")
    def gera_poema(t, s): return "Erro de Importação"

# 3. ESTADO
if 'output' not in st.session_state: st.session_state.output = ""

# 4. INTERFACE PADRÃO (SEM CSS CUSTOMIZADO)
# Se a tela continuar preta com este código, o problema é o seu Navegador (Cache).

st.sidebar.title("CONTROLE")
tema = st.sidebar.text_input("TEMA", value="poesia")

if st.sidebar.button("GERAR"):
    # Blindagem total: mandando string
    st.session_state.output = gera_poema(tema, str(random.randint(1, 1000)))

st.subheader("PALCO PRINCIPAL")
st.text_area("POEMA", value=st.session_state.output, height=500)

# Botões de Navegação Simples
cols = st.columns(6)
labels = ["+", "<", "*", ">", "?", "@"]
for i, lab in enumerate(labels):
    if cols[i].button(lab):
        st.write(f"Clicou em {lab}")
        if lab == "*":
            st.session_state.output = gera_poema(tema, str(random.randint(1, 1000)))
            st.rerun()

st.markdown("---")
if st.button("LIMPAR TUDO (RESET)"):
    st.session_state.clear()
    st.rerun()
