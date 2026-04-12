import streamlit as st
import os

# --- MOTOR DE BUSCA (v.33.9 - DIAGNÓSTICO INTEGRADO) ---

def load_md_file(file_name):
    """
    Motor de busca com periscópio para identificar falhas de infraestrutura.
    Verifica C:\ypo\md_files (Local) e /mount/src/ypoemas/md_files/ (Cloud).
    """
    # 1. Âncora de Diretório (Cloud)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path_cloud = os.path.join(base_dir, "md_files", file_name)
    
    # 2. Âncora Local (Windows)
    path_local = os.path.join(r"C:\ypo\md_files", file_name)
    
    # 3. Seleção de Alvo
    target = path_local if os.path.exists(r
