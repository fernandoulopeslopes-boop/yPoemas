import os
import re
import time
import random
import base64
import socket
import streamlit as st
from datetime import datetime
from lay_2_ypo import gera_poema

### bof: settings

st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="auto",
)

# REGRA 0: O DNA Visual do Projeto
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    .reportview-container .main .block-container{ padding: 0rem; }
    [data-testid='stSidebar'][aria-expanded='true'] > div:first-child { width: 310px; }
    mark { background-color: powderblue; color: black; }
    .container { display: flex; }
    .logo-text {
        font-weight: 600; font-size: 18px;
        font-family: 'IBM Plex Sans'; color: #000000;
        padding-top: 0px; padding-left: 15px;
    }
    .logo-img { float:right; }
    /* Estilização para simular Abas/Tabs se necessário via Markdown */
    </style> """,
    unsafe_allow_html=True,
)

if "lang" not in st.session_state: st.session_state.lang = "pt"
if "page" not in st.session_state: st.session_state.page = "mini"

### bof: navigation (A Aba Principal - Regras 1 e 2)

# Criando a barra de navegação horizontal (Tabs) no topo da página
# Respeitando a ordem do Manual de Intenções
t1, t2, t3, t4, t5, t6 = st.columns(6)

if t1.button("mini"): st.session_state.page = "mini"
if t2.button("ypoemas"): st.session_state.page = "ypoemas"
if t3.button("eureka"): st.session_state.page = "eureka"
if t4.button("biblioteca"): st.session_state.page = "biblioteca"
if t5.button("oficina"): st.session_state.page = "oficina"
if t6.button("sobre"): st.session_state.page = "sobre"

st.markdown("---")

### bof: pages (Regra 3)

if st.session_state.page == "mini":
    st.subheader("ツ mini")
    st.info("Aprovada !!! go'in to next")

elif st.session_state.page == "ypoemas":
    st.subheader("ツ ypoemas")
    st.write("Em estudo...")

elif st.session_state.page == "eureka":
    st.subheader("ツ eureka")
    st.write("Em estudo...")

elif st.session_state.page == "biblioteca":
    st.subheader("ツ biblioteca")
    st.warning("Under Construction")

elif st.session_state.page == "oficina":
    st.subheader("ツ oficina")
    st.warning("Under Construction")

elif st.session_state.page == "sobre":
    st.subheader("ツ sobre")
    st.warning("Under Construction")
