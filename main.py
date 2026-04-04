import streamlit as st
import random
import streamlit_antd_components as sac
from lay_2_ipo import gera_poema  # Peça original homologada

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
aba = sac.tabs([
    sac.TabsItem(label='Mini', icon='lightning-charge'),
    sac.TabsItem(label='yPoemas', icon='pentagon'),
    sac.TabsItem(label='Eureka', icon='search'),
    sac.TabsItem(label='Help', icon='question-circle'),
], align='center', variant='compact')

# Lista de temas da Mini (Nomes dos arquivos .txt ou identificadores)
lista_mini_nomes = ["mini_01", "mini_02", "mini_03"] 

# Ajuste do limite_max baseado na estrada
if aba == 'Mini':
    st.session_state.limite_max = len(lista_mini_nomes) - 1
elif aba == 'yPoemas':
    st.session_state.limite_max = 144
else:
    st.session_state.limite_max = 0

# Reset de posição ao trocar de aba
if aba != st.session_state.aba_atual:
    st.session_state.tema = 0
    st.session_state.sub_take = 0
    st.session_state.aba_atual = aba

# --- 4. O VOLANTE (NAVEGAÇÃO OBJETIVA) ---
_, b_more, b_last, b_rand, b_next, b_help, b_love, _ = st.columns([2, 1, 1, 1, 1, 1, 1, 2])

with b_more:
    if st.button("✚"):
        st.session_state.sub_take += 1
        st.rerun()

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
    st.button("?")

with b_love:
    st.button("❤")

# --- 5. A PAISAGEM (PALCO) ---
st.divider()

try:
    if aba == 'Mini':
        nome_atual = lista_mini_nomes[st.session_state.tema]
        # IGNICAÇÃO: gera_poema(nome_tema, seed_eureka)
        # O sub_take entra como string para garantir a variação
        texto_poema = gera_poema(nome_atual, str(st.session_state.sub_take))
        st.markdown(texto_poema, unsafe_allow_html=True)

    elif aba == 'yPoemas':
        # Aplicar a mesma lógica de nomes para a estrada principal
        st.markdown(f"### Estrada yPoemas - Tema {st.session_state.tema}")

except Exception as e:
    st.error(f"Erro na pista: {e}")
