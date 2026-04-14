import streamlit as st
import os

# --- 1. BOOT: HARDWARE ---
st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    layout="wide", 
    initial_sidebar_state="expanded"
)

if 'page' not in st.session_state:
    st.session_state.page = 'Demo'

# --- 2. MOTOR: RESGATE ---
def get_md(p):
    path = f"md_files/INFO_{p.upper()}.md"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# --- 3. CSS: O ESTADO DA ARTE (CLEAN & FIDELITY) ---
st.markdown("""<style>
    [data-testid="stHeader"] {display: none !important;}
    
    /* SIDEBAR: COCKPIT DISCRETO */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #f0f0f0;
    }

    /* NAV: CENTRALIZAÇÃO E SOBRIEDADE (11PX) */
    .stButton>button {
        width: 100% !important;
        height: 38px !important;
        border-radius: 20px !important;
        font-family: 'Georgia', serif !important;
        font-size: 11px !important; 
        font-weight: 400 !important;
        white-space: nowrap !important; 
        text-transform: uppercase;
        letter-spacing: 0.8px;
        transition: all 0.3s ease;
    }
    
    .st-key-on button {background-color: #000 !important; color: #fff !important; border: none !important;}
