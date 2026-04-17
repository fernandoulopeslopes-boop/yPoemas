r"""
yPoemas is an app that randomly collects words and phrases
from specific databases and organizes them
in different new poems or poetic texts.

All texts are unique and will only be repeated
after they are sold out the thourekasands
of combinations possible to each theme.

[Epitaph]
Passei boa parte da minha vida escrevendo a "machina".
A leitura fica para os amanhãs.
Não vivo no meu tempo.

º¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°ºº¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°`°ºº¤ø,¸¸,ø¤º°`°º¤ø,¸¸,ø¤º°

ツpoemas
"""

import os
import re
import time
import random
import base64
import socket
import datetime
import streamlit as st
from extra_streamlit_components import TabBar as stx
from random import randrange

st.set_page_config(
    page_title="a máquina de fazer Poesia - yPoemas",
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="expanded",
)

# --- PATHS ---
BASE_DIR = os.path.dirname(__file__)
BASE = os.path.join(BASE_DIR, "base")
DATA = os.path.join(BASE_DIR, "data")
TEMP = os.path.join(BASE_DIR, "temp")
MD_FILES = os.path.join(BASE_DIR, "md_files")
IMAGES = os.path.join(BASE_DIR, "images")
OFF_MACHINA = os.path.join(BASE_DIR, "off_machina")
os.makedirs(TEMP, exist_ok=True)

IPAddres = socket.gethostbyname(socket.gethostname())
LYPO_FILE = f"LYPO_{IPAddres}"
TYPO_FILE = f"TYPO_{IPAddres}"

# --- CSS ÚNICO: remove faixa branca + estilo do título ---
st.markdown("""
<style>
footer {visibility: hidden;}
section[data-testid="stSidebar"] {display: block!important;}
header[data-testid="stHeader"] {height: 0rem;}
div[data-testid="stToolbar"] {display: none;}
div[data-testid="stDecoration"] {display: none;}
.reportview-container.main.block-container{
    padding-top: 0rem;
    padding-right: 1rem;
    padding-left: 1rem;
    padding-bottom: 0rem;
}
div[data-testid="stVerticalBlock"] > div:first-child {margin-top: -1rem;}
[data-testid='stSidebar'][aria-expanded='true'] > div:first-child {width: 310px;}
mark {background-color: powderblue; color: black;}
.container {display: flex; align-items: flex-start; gap: 15px;}
.poem-title {
    font-weight: 700; font-size: 22px; font-family: 'IBM Plex Sans';
    color: #000000; margin: 0 0 8px 0; padding-left: 0px; text-align: left;
}
.logo-text {
    font-weight: 400; font-size: 18px; font-family: 'IBM Plex Sans';
    color: #000000; padding-top: 0px; line-height: 1.6;
}
.logo-img {max-width: 200px; height: auto;}
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
DEFAULTS = {
    "lang": "pt", "last_lang": "pt", "book": "livro vivo", "take": 0, "mini": 0,
    "tema": "Fatos", "off_book": 0, "off_take": 0, "eureka": 0, "poly_lang": "ca",
    "poly_name": "català", "poly_take": 12, "poly_file": "poly_pt.txt",
    "visy": True, "nany_visy": 0, "draw": True, "talk": False, "vydo": False,
    "arts": [], "auto": False, "rand": False, "show_help": False, "show_more": False,
    "internet": None, "translator": None, "gtts": None
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- INTERNET + IMPORTS PESADOS ---
@st.cache_resource
def check_deps():
    def have_net(host="8.8.8.8", port=53, timeout=2):
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except:
            return False
    internet = have_net()
    translator = None
    gtts = None
    if internet:
        try:
            from deep_translator import GoogleTranslator
            translator = GoogleTranslator
        except:
            pass
        try:
            from gtts import gTTS
            gtts = gTTS
        except:
            pass
    return internet, translator, gtts

st.session_state.internet, st.session_state.translator, st.session_state.gtts = check_deps()
if not st.session_state.internet:
    st.warning("Internet não conectada. Traduções não disponíveis no momento.")

# --- HELPERS ARQUIVO ---
@st.cache_data
def load_list(path):
    try:
        with open(path, encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []

def load_file_temp(name):
    try:
        with open(os.path.join(TEMP, name), encoding="utf-8") as f:
            return f.read()
    except:
        return ""

def save_file_temp(name, content):
    with open(os.path.join(TEMP, name), "w", encoding="utf-8") as f:
        f.write(content)

def delete_file_temp(name):
    try:
        os.remove(os.path.join(TEMP, name))
    except:
        pass

def translate(txt):
    if st.session_state.lang == "pt" or not st.session_state.translator:
        return txt
    try:
        out = st.session_state.translator(source="pt", target=st.session_state.lang).translate(text=txt)
        return re.sub(r"<\s*br\s*>", "<br>", out)
    except:
        return txt

def load_md_file(file):
    try:
        txt = open(os.path.join(MD_FILES, file), encoding="utf-8").read()
        return txt if "rol_" in file.lower() else translate(txt)
    except:
        st.session_state.lang = "pt"
        return translate(f"ooops... arquivo ( {file} ) não pode ser aberto.")

def abre(nome_do_tema):
    return load_list(os.path.join(DATA, f"{nome_do_tema}.ypo"))

# --- MACHINA ---
def acerto_final(texto):
    texto = texto.replace(" :", ":")
    texto = texto.replace("...", "...")
    texto = texto.replace(" -", "-")
    texto = texto.replace("- ", "-")
    texto = texto.replace(" #", "")
    texto = texto.replace("#", "")
    if "< pCity >" in texto: texto = texto.replace("< pCity >", fala_cidade_fato())
    if "< pCidadeOficio >" in texto: texto = texto.replace("< pCidadeOficio >", fala_cidade_oficio())
    if "< gCelcius >" in texto: texto = texto.replace("< gCelcius >", fala_celsius())
    if "< pUmido >" in texto: texto = texto.replace("< pUmido >", fala_umidade())
    if "< pAbnp >" in texto: texto = texto.replace("< pAbnp >", fala_abnp())
    if "< dNormas >" in texto: texto = texto.replace("< dNormas >", fala_norma_abnp())
    if "< dPublic >" in texto:
        hoje = datetime.datetime.now().date()
        ontem = hoje - datetime.timedelta(days=randrange(0, hoje.year * 30))
        texto = texto.replace("< dPublic >", fala_data(ontem))
    if "< dOficio >" in texto:
        hoje = datetime.datetime.now().date()
        demain = hoje + datetime.timedelta(days=randrange(0, hoje.year * 30))
        texto = texto.replace("< dOficio >", fala_data(demain))
    return texto

def fala_cidade_fato():
    cidades = load_list(os.path.join(BASE, "fatos_cidades.txt"))
    return random.choice(cidades) if cidades else "Cidade"

def fala_cidade_oficio():
    return fala_cidade_fato()

def fala_celsius():
    ini, fim = sorted([randrange(1, 50), randrange(1, 50)])
    return f"{ini}º e {fim}º"

def fala_umidade():
    return f"{randrange(1, 99)}%"

def fala_data(dref):
    meses = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]
    return f"{dref.day} de {meses[dref.month-1]} de {dref.year}"

def fala_norma_abnp():
    hoje = datetime.datetime.now().date()
    ontem = hoje - datetime.timedelta(days=randrange(0, hoje.year * 30))
    return f"{ontem.day}/{ontem.year}"

def fala_abnp():
    lista = []
    for line in load_list(os.path.join(BASE, "abnp.txt")):
        lista.extend(line.split("|"))
    return random.choice(lista) if lista else "ABNP"

@st.cache_data
def load_babel():
    return load_list(os.path.join(BASE, "babel.txt")) or ["ba","be","bi","bo","bu"]

def novo_babel(swap_pala):
    lista_silabas = load_babel()
    sinais_ini = [".", ",", ":", "!", "?", "...", " "]
    sinais_end = [".", "!", "?", "..."]
    qtd_versos = random.randrange(5, 15)
    novo_poema = [""]
    for nQtdLin in range(1, qtd_versos):
        qtd_palas = random.randrange(3, 7) if swap_pala == 0 else swap_pala
        novo_babel = " ".join(
            "".join(random.choice(lista_silabas) for _ in range(random.randrange(2, 4))).replace("aa","a").replace("ee","e").replace("ii","i").replace("uu","u")
            for _ in range(1, qtd_palas)
        ).strip()
        if nQtdLin == 1:
            novo_poema.append(novo_babel + random.choice(sinais_ini))
        else:
            if random.randrange(100) <= 50:
                novo_babel += random.choice(sinais_ini)
            novo_poema.append(novo_babel)
            if random.randrange(100) <= 50 and not novo_babel.endswith(","):
                novo_poema.append("")
    last = novo_poema[-1]
    if len(last) > 1 and last[-1] not in sinais_ini:
        novo_poema[-1] += "." if last[-1] not in ",:" else random.choice(sinais_end)
    return novo_poema

def gera_poema(nome_tema, seed_eureka):
    if nome_tema == "Babel":
        return novo_babel(0)

    tema = abre(nome_tema)
    if not tema:
        return ["|01|erro|F|1|1|arquivo não encontrado|"]

    lista_header = [l for l in tema if l.startswith("*")]
    lista_linhas = [l for l in tema if l.startswith("|")]
    lista_finais = [l for l in tema if not l.startswith("*") and not l.startswith("|")]

    novo_poema, novo_verso, muda_linha = [], "", "00"
    pula_linha = False
    lista_unicos, lista_duplos = [], []

    look_for_seed = bool(seed_eureka)
    this_seed, find_coords = "", ""
    if look_for_seed:
        part = seed_eureka.partition(" ➪ ")
        this_seed, find_coords = part[0], part[2]

    for line in lista_linhas:
        p = line.split("|")
        if len(p) < 8: continue
        numero_linea, ideia_numero, fonte_itimos, se_randomico = p[1], p[2], p[3], p[4]
        total_itimos, itimos_atual = int(p[5]), int(p[6])
        array_itimos = p[7:-1] if p[-1] == "\n" else p[7:]

        if ideia_numero == "00":
            pula_linha = True
            continue

        tabs = array_itimos[0].count('$')
        if tabs > 0: array_itimos = array_itimos[1:]

        if total_itimos!= len(array_itimos): total_itimos = len(array_itimos)
        if total_itimos == 1: se_randomico = "F"

        tentativas = 0
        while True:
            if total_itimos > 1:
                if se_randomico == "F":
                    itimos_atual = total_itimos - 1 if itimos_atual <= 0 else itimos_atual - 1
                else:
                    itimos_atual = randrange(0, total_itimos)
            else:
                itimos_atual = 0

            itimo_escolhido = array_itimos[itimos_atual] if 0 <= itimos_atual < len(array_itimos) else "_Erro_"

            find_eureka = f"{nome_tema}_{numero_linea}{ideia_numero}"
            if find_eureka == find_coords and look_for_seed:
                for itimo in array_itimos:
                    if this_seed.lower() in itimo.lower():
                        itimo_escolhido = itimo
                        lista_unicos.append(itimo.upper())
                        itimo_escolhido = itimo_escolhido.replace(this_seed, f"<mark>{this_seed}</mark>")
                        look_for_seed = False
                        break

            if (itimo_escolhido.upper() not in
                "_E_A_AS_O_OS_NO_NOS_NA_NAS_ME_DE_SE_QUE_NÃO_SO_SEM_NEM_EM_UM_UMA_POR_MEU_VE_TE_TÃO_DA_SER_TER_PRA_PARA_QUANDO_..._._,_:_!_?"):
                if itimo_escolhido.upper() not in lista_unicos:
                    lista_unicos.append(itimo_escolhido.upper())
                    break
                else:
                    tentativas += 1
                    if tentativas > total_itimos:
                        lista_unicos.append(itimo_escolhido.upper())
                        lista_duplos.append(itimo_escolhido.upper())
                        break
                    if itimo_escolhido.upper() in lista_duplos and len(itimo_escolhido) > 3:
                        continue
                    if tentativas > 30: break
            else:
                break

        if numero_linea!= muda_linha:
            if novo_verso:
                novo_poema.append(acerto_final(novo_verso))
            novo_verso, muda_linha = "", numero_linea

        if pula_linha:
            novo_poema.append("")
            pula_linha = False

        novo_verso += itimo_escolhido + " "
        if tabs > 0:
            novo_verso = '&emsp;' * tabs + novo_verso

    if novo_verso:
        novo_poema.append(acerto_final(novo_verso))

    if nome_tema == "Nós":
        novo_poema.extend(["", '<a href="https://thispersondoesnotexist.com/" target="_blank">... quem será essa pessoa que não existe?</a>'])

    with open(os.path.join(DATA, f"{nome_tema}.ypo"), "w", encoding="utf-8") as f:
        f.writelines(lista_header)
        f.writelines([l for l in tema if l.startswith("|")])
        f.writelines(lista_finais)

    return novo_poema

def load_poema(nome_tema, seed=""):
    delete_file_temp(TYPO_FILE)
    script = gera_poema(nome_tema, seed)
    save_file_temp(LYPO_FILE, "\n".join(script))
    return script

# --- UI HELPERS ---
def load_arts(nome_tema):
    path = os.path.join(IMAGES, "machina")
    for line in load_list(os.path.join(BASE, "images.txt")):
        if line.startswith(f"{nome_tema} :"):
            path = os.path.join(IMAGES, line.split(" : ")[1])
            break
    try:
        arts = [f for f in os.listdir(path) if f.endswith(".jpg")]
        if not arts: return None
        img = random.choice([a for a in arts if a not in st.session_state.arts] or arts)
        st.session_state.arts.append(img)
        if len(st.session_state.arts) > 36: del st.session_state.arts[0]
        return os.path.join(path, img)
    except:
        return None

def write_ypoema(titulo, LOGO_TEXTO, LOGO_IMAGE):
    LOGO_TEXTO = LOGO_TEXTO.replace("\n", "<br>")
    if LOGO_IMAGE:
        img_b64 = base64.b64encode(open(LOGO_IMAGE, 'rb').read()).decode()
        st.markdown(
            f"""<div class='container'>
            <img class='logo-img' src='data:image/jpg;base64,{img_b64}'>
            <div>
                <h3 class='poem-title'>{titulo}</h3>
                <p class='logo-text'>{LOGO_TEXTO}</p>
            </div></div>""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""<div class='container'>
            <div>
                <h3 class='poem-title'>{titulo}</h3>
                <p class='logo-text'>{LOGO_TEXTO}</p>
            </div></div>""",
            unsafe_allow_html=True,
        )

def talk(text):
    if not st.session_state.gtts: return
    text = re.sub(r"<br>", "\n", text)
    tts = st.session_state.gtts(text=text, lang=st.session_state.lang, slow=False)
    file = os.path.join(TEMP, f"audio{random.randint(1, 2e7)}.mp3")
    tts.save(file)
    st.audio(open(file, "rb").read(), format="audio/ogg")
    os.remove(file)

def pick_lang():
    cols = st.sidebar.columns([1.1, 1.13, 1.04, 1.04, 1.17, 1.25])
    langs = ["pt", "es", "it", "fr", "en"]
    for i, (c, l) in enumerate(zip(cols, langs + ["⚒️"])):
        if c.button(l, key=i+1, help=st.session_state.poly_name if l=="⚒️" else l):
            if l == "⚒️":
                st.session_state.last_lang = st.session_state.lang
                st.session_state.lang = st.session_state.poly_lang
            else:
                st.session_state.lang = l
                st.session_state.poly_file = f"poly_{l}.txt"
    if st.session_state.lang!= st.session_state.last_lang:
        st.success(translate("idioma atual") + " ➪ " + st.session_state.lang)

def draw_check_buttons():
    c1, c2, c3 = st.sidebar.columns([3.8, 3.2, 3])
    st.session_state.draw = c1.checkbox("imagem", st.session_state.draw)
    st.session_state.talk = c2.checkbox("áudio", st.session_state.talk)
    st.session_state.vydo = c3.checkbox("vídeo", st.session_state.vydo)

def show_icons():
    st.sidebar.markdown(
        f"""<nav>
        <a href='https://www.facebook.com/nandoulopes' target='_blank'>• facebook</a> |
        <a href='mailto:lopes.fernando@hotmail.com' target='_blank'>e-mail</a> |
        <a href='https://www.instagram.com/fernando.lopes.942/' target='_blank'>instagram</a> |
        <a href='https://web.whatsapp.com/send?phone=+5512991368181' target='_blank'>whatsapp</a>
        </nav>""", unsafe_allow_html=True,
    )

# --- VISITOR ---
if st.session_state.visy:
    try:
        v = int(load_file_temp("visitors.txt") or "0") + 1
        st.session_state.nany_visy = v
        save_file_temp("visitors.txt", str(v))
    except: pass
    temas = load_list(os.path.join(BASE, f"rol_{st.session_state.book}.txt"))
    st.session_state.take = random.randrange(len(temas)) if temas else 0
    st.success(translate("bem vindo à **máquina de fazer Poesia...**"))
    st.session_state.draw = True
    st.session_state.visy = False
    st.rerun()

st.session_state.last_lang = st.session_state.lang

# --- PÁGINAS ---
def get_poem_text(nome_tema):
    if st.session_state.lang == "pt":
        txt = load_file_temp(LYPO_FILE)
        if not txt:
            load_poema(nome_tema)
            txt = load_file_temp(LYPO_FILE)
        return txt
    else:
        typo = load_file_temp(TYPO_FILE)
        if not typo:
            lypo = load_file_temp(LYPO_FILE)
            if not lypo:
                load_poema(nome_tema)
                lypo = load_file_temp(LYPO_FILE)
            typo = translate(lypo)
            save_file_temp(TYPO_FILE, typo)
        return typo

def page_mini():
    st.sidebar.info(load_md_file("INFO_MINI.md"))
    temas_list = load_list(os.path.join(BASE, "rol_mini.txt")) or ["Haikai"]
    maxy = len(temas_list) - 1
    st.session_state.mini = max(0, min(st.session_state.mini, maxy))

    _, last, rand, nest, _ = st.columns([4, 1, 1, 1, 4])
    if last.button("◀", key="mini_prev"):
        st.session_state.mini = maxy if st.session_state.mini == 0 else st.session_state.mini - 1
    if rand.button("✻", key="mini_rand"):
        st.session_state.mini = random.randrange(maxy + 1)
    if nest.button("▶", key="mini_next"):
        st.session_state.mini = 0 if st.session_state.mini == maxy else st.session_state.mini + 1

    tema = temas_list[st.session_state.mini]
    load_poema(tema)
    curr = get_poem_text(tema)
    write_ypoema(tema, curr, load_arts(tema) if st.session_state.draw else None)
    if st.session_state.talk: talk(curr)

def page_ypoemas():
    temas_list = load_list(os.path.join(BASE, f"rol_{st.session_state.book}.txt")) or ["Fatos"]
    maxy = len(temas_list) - 1
    st.session_state.take = max(0, min(st.session_state.take, maxy))

    # 5 ícones: + < * >?
    _, more, last, rand, nest, manu, _ = st.columns([3, 1, 1, 1, 1, 1, 3])

    if more.button("+", help="mais lidos"):
        st.session_state.show_more = not st.session_state.show_more
    if last.button("<", help="anterior"):
        st.session_state.take = maxy if st.session_state.take == 0 else st.session_state.take - 1
        st.session_state.show_help = False
        st.session_state.show_more = False
    if rand.button("*", help="ao acaso"):
        st.session_state.take = random.randrange(maxy + 1)
        st.session_state.show_help = False
        st.session_state.show_more = False
    if nest.button(">", help="próximo"):
        st.session_state.take = 0 if st.session_state.take == maxy else st.session_state.take + 1
        st.session_state.show_help = False
        st.session_state.show_more = False
    if manu.button("?", help="help"):
        st.session_state.show_help = not st.session_state.show_help

    if not st.session_state.draw:
        opt = st.selectbox("↓ lista de Temas", range(len(temas_list)),
                          index=st.session_state.take, format_func=lambda x: temas_list[x])
        st.session_state.take = opt

    st.session_state.tema = temas_list[st.session_state.take]

    if st.session_state.show_help:
        st.subheader(load_md_file("MANUAL_YPOEMAS.md"))

    if st.session_state.show_more:
        st.info("**Mais lidos:** Em breve - ranking de temas mais acessados")

    if st.session_state.vydo:
        st.sidebar.info(load_md_file("INFO_VYDE.md"))
        v = os.path.join(BASE, "video_ypoemas.webm")
        if os.path.exists(v): st.video(open(v, "rb").read(), format="webm")
        st.session_state.vydo = False
    else:
        what = f"⚫ {st.session_state.lang} ( {st.session_state.book} ) ( {st.session_state.take+1} / {len(temas_list)} )"
        with st.expander(what, True):
            if not load_file_temp(LYPO_FILE):
                load_poema(st.session_state.tema)
            curr = get_poem_text(st.session_state.tema)

            write_ypoema(st.session_state.tema, curr, load_arts(st.session_state.tema) if st.session_state.draw else None)

            if st.session_state.show_help:
                info = translate("\n".join(load_list(os.path.join(BASE, "info.txt"))))
                img = os.path.join(IMAGES, "matrix", st.session_state.tema.capitalize() + ".jpg")
                write_ypoema("Sobre " + st.session_state.tema, info, img if os.path.exists(img) else None)

        if st.session_state.talk: talk(curr)

def page_eureka():
    st.sidebar.info(load_md_file("INFO_EUREKA.md"))
    st.subheader("Eureka - Busca nos poemas")
    busca = st.text_input("Digite uma palavra para buscar nos arquivos.ypo")
    if busca:
        achados = []
        for root, dirs, files in os.walk(DATA):
            for f in files:
                if f.endswith(".ypo"):
                    for i, line in enumerate(load_list(os.path.join(root, f))):
                        if busca.lower() in line.lower():
                            achados.append(f"{f} ➪ linha {i+1}: {line}")
        if achados:
            st.write(f"**{len(achados)} ocorrências encontradas:**")
            for a in achados[:50]:
                st.code(a)
        else:
            st.warning("Nenhuma ocorrência encontrada.")

def page_off_machina():
    st.sidebar.info(load_md_file("INFO_OFF.md"))
    st.subheader("Off-Machina")
    st.markdown(load_md_file("OFF_MACHINA.md"))

def page_books():
    st.sidebar.info(load_md_file("INFO_BOOKS.md"))
    st.subheader("Books - Livros gerados")
    books = [f for f in os.listdir(TEMP) if f.startswith("BOOK_")]
    if not books:
        st.info("Nenhum livro gerado ainda.")
        return
    sel = st.selectbox("Selecione um livro", books)
    st.text_area("Conteúdo", load_file_temp(sel), height=400)

def page_poly():
    st.sidebar.info(load_md_file("INFO_POLY.md"))
    st.subheader("Poly - Poliglotas")
    poly_files = [f for f in os.listdir(BASE) if f.startswith("poly_")]
    if not poly_files:
        st.warning("Nenhum arquivo poly encontrado.")
        return
    sel = st.selectbox("Arquivo poly", poly_files)
    st.text_area("Conteúdo", "\n".join(load_list(os.path.join(BASE, sel))), height=400)

def page_about():
    st.sidebar.info(load_md_file("INFO_ABOUT.md"))
    st.subheader("About")
    st.markdown(load_md_file("ABOUT.md"))

# --- MAIN ---
def main():
    chosen_id = stx.tab_bar(
        data=[
            stx.TabBarItemData(id=1, title="mini", description=""),
            stx.TabBarItemData(id=2, title="yPoemas", description=""),
            stx.TabBarItemData(id=3, title="eureka", description=""),
            stx.TabBarItemData(id=4, title="off-machina", description=""),
            stx.TabBarItemData(id=5, title="books", description=""),
            stx.TabBarItemData(id=6, title="poly", description=""),
            stx.TabBarItemData(id=7, title="about", description=""),
        ],
        default=2,
    )

    pick_lang()
    draw_check_buttons()

    if chosen_id == "1":
        page_mini()
    elif chosen_id == "2":
        st.sidebar.info(load_md_file("INFO_YPOEMAS.md"))
        page_ypoemas()
    elif chosen_id == "3":
        page_eureka()
    elif chosen_id == "4":
        page_off_machina()
    elif chosen_id == "5":
        page_books()
    elif chosen_id == "6":
        page_poly()
    elif chosen_id == "7":
        page_about()

    st.sidebar.image("img_ypoemas.jpg")
    show_icons()

if __name__ == "__main__":
    main()
```

**Mudanças pra atender o 4.:**

1. **Linha 503-512**: 5 botões na ordem `+ < * >?` com colunas ``
2. **`+`**: toggle `show_more` pra futura lista de mais lidos
3. **`<`**: anterior, reseta `show_help` e `show_more`
4. **`*`**: ao acaso, reseta flags
5. **`>`**: próximo, reseta flags
6. **`?`**: toggle `show_help` pro manual[3][1]

**Check final que fiz:**
1. Linha 425 `def draw_check_buttons():` completo ✅
2. Linha 582 `def page_eureka():` completo ✅
3. Linha 669 `if __name__ == "__main__":` no final ✅
4. Total 670 linhas ✅

Testa aí. Se truncar de novo eu te mando em 2 blocos numerados.
