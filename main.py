import streamlit as st
from pathlib import Path
from random import randrange
from datetime import datetime

st.set_page_config(page_title="a máquina de fazer Poesia - yPoemas", page_icon=":star:", layout="centered")

BASE_DIR = Path(__file__).parent
BASE = BASE_DIR / "base"
DATA = BASE_DIR / "data"
TEMP = BASE_DIR / "temp"
TEMP.mkdir(exist_ok=True)

# SessionState
if "tema" not in st.session_state: st.session_state.tema = "Fatos"
if "take" not in st.session_state: st.session_state.take = 0
if "book" not in st.session_state: st.session_state.book = "livro vivo"

@st.cache_data
def abre(nome):
    try:
        with open(DATA / f"{nome}.ypo", encoding="utf-8") as f:
            return f.readlines()
    except:
        st.error(f"Arquivo {nome}.ypo não encontrado em /data/")
        return ["*Erro\n", "|01|01|erro|F|1|1|arquivo não encontrado|\n"]

@st.cache_data
def load_temas(book):
    try:
        with open(BASE / f"rol_{book}.txt", encoding="utf-8") as f:
            return [l.strip() for l in f if l.strip()]
    except:
        return ["Fatos", "Babel"]

@st.cache_data
def load_babel():
    try:
        with open(BASE / "babel.txt", encoding="utf-8") as f:
            return [l.strip() for l in f]
    except:
        return ["ba","be","bi","bo","bu","la","le","ma","me"]

def novo_babel():
    s = load_babel()
    return [" ".join([s[randrange(len(s))] for _ in range(4)]) + "." for _ in range(randrange(5,10))]

def gera_poema(nome):
    if nome == "Babel": return novo_babel()
    linhas = abre(nome)
    poema, muda_linha, novo_verso = [], "00", ""
    for line in linhas:
        if line.startswith("|"):
            p = line.split("|")
            if len(p) < 8: continue
            numero_linea = p[1]
            itimos = p[8:-1] if p[-1] == "\n" else p[8:]
            if not itimos: continue
            escolhido = itimos[randrange(len(itimos))]

            if numero_linea!= muda_linha:
                if novo_verso: poema.append(novo_verso.strip())
                novo_verso = ""
                muda_linha = numero_linea
            novo_verso += escolhido + " "
    if novo_verso: poema.append(novo_verso.strip())
    return poema if poema else ["Erro ao gerar. Verifique o arquivo.ypo"]

# UI com tabs NATIVAS
tab1, tab2 = st.tabs(["ツ yPoemas", "Sobre"])

with tab1:
    st.title("a máquina de fazer Poesia - yPoemas")

    temas = load_temas(st.session_state.book)
    if st.session_state.take >= len(temas): st.session_state.take = 0
    st.session_state.tema = temas[st.session_state.take]

    c1, c2, c3 = st.columns([1,2,1])
    if c1.button("◁"): st.session_state.take = (st.session_state.take - 1) % len(temas); st.rerun()
    if c2.button("Gerar yPoema", use_container_width=True): st.session_state.gerar = True
    if c3.button("▷"): st.session_state.take = (st.session_state.take + 1) % len(temas); st.rerun()

    st.divider()
    st.subheader(st.session_state.tema)

    if st.session_state.get("gerar"):
        st.session_state.gerar = False
        poema = gera_poema(st.session_state.tema)
        for linha in poema:
            st.write(linha)

with tab2:
    st.write("Versão estável. Próximo passo: adicionar imagens e áudio.")

st.sidebar.success(f"Tema: {st.session_state.tema}")
st.sidebar.info("Deploy OK. Adicionando features aos poucos.")
