# ypo_config.py — porta CONFIG da Machina
import streamlit as st

st.set_page_config(
    page_title="a Machina de fazer Poesia - Config",
    page_icon="🚧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from basico import start_machina

start_machina("local")
