import streamlit as st
import random
import streamlit_antd_components as sac

# --- 1. CONFIGURAÇÃO DE ENGENHARIA ---
st.set_page_config(page_title="yPoemas 2026", layout="wide")

# --- 2. GAIOLA DE PROTEÇÃO (ESTADO DO MOTOR) ---
if 'tema' not in st.session_state:
    st.session_state.tema = 0
if 'sub_take' not in st.session_state:
    st.session_state.sub_take = 0
if 'aba_atual' not in st.session_state:
    st.session_state.aba_atual = "Mini"

# --- 3. ESTRADAS (AS PÁGINAS) ---
# O seletor no topo define o limite_max da pista
aba = sac.tabs([
    sac.TabsItem(label='Mini', icon='lightning-charge'),
    sac.TabsItem(label='yPoemas', icon='pentagon'),
    sac.TabsItem(label='Eureka', icon='search'),
    sac.TabsItem(label='Help', icon='question-circle'),
], align='center', variant='compact')

# Ajuste do limite_max baseado na estrada escolhida
if aba == 'Mini':
    st.session_state.limite_max = 20 # Exemplo: len(lista_mini)
elif aba == 'yPoemas':
    st.session_state.limite_max = 144
else:
    st.session_state.limite_max = 0

# Reset se mudar de estrada
if aba != st.session_state.aba_atual:
    st.session_state.tema = 0
    st.session_state.aba_atual = aba

# --- 4. O VOLANTE (NAVEGAÇÃO OBJETIVA) ---
# Colado ao texto, centralizado para o leitor
_, b_more, b_last, b_rand, b_next, b_help, b_love, _ = st.columns([2, 1, 1, 1, 1, 1, 1, 2])

with b_more:
    if st.button("✚"):
        st.session_state.sub_take += 1

with b_last:
    if st.button("◀"):
        st.session_state.tema = (st.session_state.tema - 1) % (st.session_state.limite_max + 1)
        st.rerun()

with b_rand:
    if st.button("✻"):
        st.session_state.tema = random.randint(0, st.session_state.limite_max)
        st.rerun()

with b_next:
    if st.button("▶"):
        st.session_state.tema = (st.session_state.tema + 1) % (st.session_state.limite_max + 1)
        st.rerun()

with b_help:
    if st.button("?"):
        st.info("Menu de ajuda contextual.")

with b_love:
    if st.button("❤"):
        pass # Reservado: "Os mais lidos"

# --- 5. A PAISAGEM (PALCO) ---
st.divider()

if aba == 'Mini':
    # Exemplo de saída objetiva na página Mini
    st.markdown(f"### Mini Poema nº {st.session_state.tema}")
    st.write(f"Variação ativa: {st.session_state.sub_take}")
    # render_mini(st.session_state.tema, st.session_state.sub_take)

elif aba == 'yPoemas':
    st.markdown(f"### yPoema Tema {st.session_state.tema}")
    # render_ypoema(st.session_state.tema)
