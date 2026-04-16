import streamlit as st
from pathlib import Path
from random import randrange
import os

st.set_page_config(page_title="yPoemas DEBUG", layout="centered")
st.write("# DEBUG MODE")

BASE = Path(__file__).parent / "base"
DATA = Path(__file__).parent / "data"

st.write(f"BASE existe: {BASE.exists()}")
st.write(f"DATA existe: {DATA.exists()}")
st.write(f"Arquivos em DATA: {os.listdir(DATA) if DATA.exists() else 'PASTA NÃO EXISTE'}")

@st.cache_data
def abre_seguro(nome):
    try:
        with open(DATA / f"{nome}.ypo", encoding="utf-8") as f:
            linhas = f.readlines()
        st.success(f"{nome}.ypo carregado: {len(linhas)} linhas")
        return linhas
    except Exception as e:
        st.error(f"FALHOU {nome}: {e}")
        return ["|01|01|erro|F|1|1|fallback|\n"]

def gera_babel():
    silabas = ["ba","be","bi","bo","bu","ca","co","da","de"]
    return [" ".join([silabas[randrange(len(silabas))] for _ in range(4)]) for _ in range(5)]

def gera_minimo(nome):
    if nome == "Babel":
        return gera_babel()
    linhas = abre_seguro(nome)
    poema = []
    for line in linhas:
        if line.startswith("|"):
            partes = line.split("|")
            if len(partes) > 8:
                poema.append(partes[8])
    return poema if poema else ["Arquivo vazio ou formato errado"]

tema = st.selectbox("Tema", ["Fatos", "Babel", "Amor"])
if st.button("Gerar"):
    resultado = gera_minimo(tema)
    st.write("## Resultado:")
    for linha in resultado:
        st.write(linha)

st.divider()
st.write("Se você viu botões e conseguiu gerar, o motor está OK. O problema é TabBar/imports no Cloud.")
