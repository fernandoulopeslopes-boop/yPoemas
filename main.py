import streamlit as st
import os
import time

# --- IMPORTAÇÃO ---
try:
    from lay_2_ypo import gera_poema
except ImportError:
    st.error("Erro: O motor 'lay_2_ypo.py' não foi encontrado ou está corrompido.")
    st.stop()

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="a Máquina de Fazer Poesia", page_icon="ツ")

# --- ESTADO INICIAL ---
if "auto_run" not in st.session_state:
    st.session_state.auto_run = False
if "mini_idx" not in st.session_state:
    st.session_state.mini_idx = 0

# --- SIDEBAR ---
st.sidebar.title("ツ Machina")
menu = {"1": "Mini", "2": "yPoemas", "3": "Eureka"}
escolha = st.sidebar.radio("Navegação", list(menu.keys()), format_func=lambda x: menu[x].upper())
tema_selecionado = menu[escolha]

st.sidebar.markdown("---")
col1, col2 = st.sidebar.columns(2)
if col1.button("Talk"): st.session_state.action = "talk"
if col2.button("Arte"): st.session_state.action = "draw"

# --- LÓGICA MODO AUTO (Sem Loop While) ---
if tema_selecionado == "Mini":
    st.sidebar.subheader("Modo Automático")
    st.session_state.auto_run = st.sidebar.checkbox("Ativar Auto", value=st.session_state.auto_run)
    intervalo = st.sidebar.slider("Segundos entre versos", 5, 60, 10)

# --- BOTÃO DE GERAÇÃO ---
st.title(f"Modo: {tema_selecionado}")

if st.button(f"Gerar {tema_selecionado}") or st.session_state.auto_run:
    with st.spinner("Semeando..."):
        # Se for Eureka, poderia pedir input, aqui simplificamos:
        resultado = gera_poema(tema_selecionado, "")
        
        if resultado:
            st.markdown("---")
            for linha in resultado:
                st.write(linha)
            st.markdown("---")
            
    # Se o Auto estiver ligado, ele espera e recarrega a página sozinho
    if st.session_state.auto_run:
        time.sleep(intervalo)
        st.rerun() 

# --- RODAPÉ ---
st.sidebar.info("Aguardando comando...")
