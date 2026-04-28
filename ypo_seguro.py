import streamlit as st
import os
import random
import time
import base64
import edge_tts as gTTS

import os
import random
import datetime
import streamlit as st

from random import randrange

# new deploy test

def gera_poema(nome_tema, seed_eureka):  # abrir um script.ypo e gerar um novo yPoema
    """
    :param = script, tema
         numero_linea = '01'  # linha
         ideia_numero = '01'  # ideia
         fonte_itimos = nome_tema + '_' + numero_linea + ideia_numero # fonte dos itimos. Pode haver re-uso !!!
         se_randomico = 'F'   # se_random
         total_itimos = N     # qtd_itimos
         itimos_atual = 1     # itimos_atual
         array_itimos = []    # array com todos os itimos da ideia na linha
    return: novo_poema

    ToDo:
       obs: the search for a seed acctualy only works in portuguese. Try to translate your search_seed into this language.
    """

    lista_header = []
    lista_linhas = []
    lista_finais = []
    lista_change = []
    lista_duplos = []
    lista_errata = []
    lista_unicos = []

    conta_palavra = 0

    this_seed = ""
    find_coords = ""
    look_for_seed = False

    if seed_eureka != "":
        look_for_seed = True
        part_string = seed_eureka.partition(" ➪ ")
        this_seed = part_string[0]
        find_coords = part_string[2]

    nome_tema = nome_tema.strip("\n")

    try:
        if nome_tema == "Babel":
            novo_poema = novo_babel(0)
            return novo_poema
        else:
            tema = abre(nome_tema)
            for line in tema:
                if line.startswith("*", 0, 1):  # observações e cabeçalho
                    lista_header.append(line)
                elif line.startswith("|", 0, 1):  # ideias & itimos
                    lista_linhas.append(line)
                else:  # <eof> + análise + build_date
                    lista_finais.append(line)
    except UnicodeDecodeError:
        lista_errata.append(nome_tema)
        pass

    novo_poema = []
    novo_verso = ""
    muda_linha = "00"
    pula_linha = "no"
    find_eureka = ""

    for line in lista_linhas:
        alinhas = line.split("|")

        if len(alinhas) == 0:
            continue

        if len(alinhas) < 2:
            lista_errata.append(nome_tema)
            continue

        if alinhas[2] == "00":
            pula_linha = "si"
            lista_change.append(line)
            continue

        if len(alinhas) >= 7:
            numero_linea = alinhas[1]
            ideia_numero = alinhas[2]
            fonte_itimos = alinhas[3]
            se_randomico = alinhas[4]
            total_itimos = int(alinhas[5])
            itimos_atual = int(alinhas[6])
            array_itimos = alinhas[7 : len(alinhas) - 1]
            
            tabs = array_itimos[0].count('$')
            if tabs > 0:
                array_itimos = array_itimos[1 : len(array_itimos)]

            find_eureka = nome_tema + "_" + numero_linea + ideia_numero

            if itimos_atual > len(array_itimos):
                itimos_atual = len(array_itimos)

            if total_itimos != len(array_itimos):  # just in case...
                total_itimos = len(array_itimos)  # real lenght...

            if total_itimos == 1:  # just in case...
                se_randomico = "F"

            tentativas = 0
            while True:  # seleciona próximo ítimo válido
                if 1 != total_itimos:  # mais de hum ítimo
                    if se_randomico == "F":
                        itimos_atual -= 1  # pega ítimo anterior
                        if itimos_atual < 0:
                            itimos_atual = ( total_itimos - 1)  # because matrix começa em zero
                    else:
                        if total_itimos >= 1:
                            itimos_atual = randrange(0, total_itimos - 1)  # pega ítimo random
                        else:
                            itimos_atual = 0  # just in case
                else:  # apenas hum ítimo
                    itimos_atual = 0

                if itimos_atual >= 0 and itimos_atual <= len(array_itimos):
                    itimo_escolhido = array_itimos[itimos_atual]  # escolheu ítimo
                else:
                    st.warning(
                        "Algo deu errado em "
                        + fonte_itimos
                        + ". Se puder, entre em contato com o '[autor](mailto:lopes.fernando@hotmail.com)'"
                    )
                    itimo_escolhido = "_Erro_"

                if ( find_eureka == find_coords ):  # marcar palavra/semente em eureka parameter
                    if look_for_seed:  # not changed yet...
                        for itimo in array_itimos:
                            if this_seed.lower() in itimo.lower():
                                itimo_escolhido = itimo
                                lista_unicos.append(
                                    itimo_escolhido.upper()
                                )  # no repeated words...
                                itimo_escolhido = itimo_escolhido.replace(
                                    this_seed, "<mark>" + this_seed + "</mark>"
                                )  # markdown text
                                look_for_seed = False

                #  verifica se ítimo ainda não foi escolhido
                temp_random = se_randomico
                if (
                    not itimo_escolhido.upper()  # Elimina duplicidaders óbvias...
                    in "_E_A_AS_O_OS_NO_NOS_NA_NAS_ME_DE_SE_QUE_NÃO_SO_SEM_NEM_EM_UM_UMA_POR_MEU_VE_TE_TÃO_DA_SER_TER_PRA_PARA_QUANDO_..._._,_:_!_?"
                ):
                    if (
                        itimo_escolhido.upper() not in lista_unicos
                    ):  # check if not yet used...
                        lista_unicos.append(itimo_escolhido.upper())
                        break
                    else:
                        tentativas += 1
                        if (
                            tentativas > total_itimos
                        ):  # tentativas > que total de ítimos: pega o próximo sequencial
                            if temp_random == "T":
                                tentativas = 0  # Da Capo
                                temp_random = "F"
                            else:
                                lista_unicos.append(itimo_escolhido.upper())
                                lista_duplos.append(itimo_escolhido.upper())
                                break

                        if (
                            itimo_escolhido.upper() in lista_duplos
                        ):  # para não repetir verbetes/ítimos usados em mais de uma ideia/linha
                            if len(itimo_escolhido) > 3:
                                continue

                        if tentativas > 30:
                            break
                else:
                    break

            if numero_linea != muda_linha:  # check new line in script
                novo_verso = acerto_final(novo_verso)
                novo_poema.append(novo_verso)
                novo_verso = ""
                muda_linha = numero_linea

            novo_verso += itimo_escolhido + " "
            if tabs > 0:
                novo_verso = tabs*'&emsp;' + novo_verso
                tabs = 0
                    

            if "si" == pula_linha:
                novo_poema.append("\n")
                pula_linha = "no"

            changed_line = (
                "|" + numero_linea + "|" + ideia_numero + "|" + fonte_itimos + "|"
            )

            if itimos_atual < 1:  # sequencial = -1
                if total_itimos == 1:
                    itimos_atual = 1
                else:
                    itimos_atual = total_itimos

            if se_randomico == "T":
                changed_line += "T"
            else:
                changed_line += "F"
                
            changed_line += "|" + str(total_itimos) + "|" + str(itimos_atual)

            for v in alinhas[7 : len(alinhas) - 1]:
                changed_line += "|" + v
            changed_line += "|\n"
            lista_change.append(changed_line)
            
        # endif len(alinhas) >= 7:
    # end for... line in lista_linhas

    novo_poema.append(acerto_final(novo_verso))

    if nome_tema == "Nós":
        novo_poema.append("\n")
        novo_poema.append(
            '<a href="https://thispersondoesnotexist.com/" target="_blank">... quem será essa pessoa que não existe?</a>'
        )

    if len(lista_errata) > 0:
        st.warning(
            "Algo deu errado com o tema "
            + nome_tema.upper()
            + ". Se puder, entre em contato com o '[autor](mailto:lopes.fernando@hotmail.com)'"
        )
    else:
        # rebuild script with new positions
        with open(
            os.path.join("./data/" + nome_tema + ".ypo"), "w", encoding="utf-8"
        ) as file:
            for linha in lista_header:
                file.write(linha)

            for linha in lista_change:
                file.write(linha)

            for linha in lista_finais:
                file.write(linha)

        file.close()

    return novo_poema


def acerto_final(texto):

    if " ." in texto:
        texto = texto.replace(" .", ".")
    if " ," in texto:
        texto = texto.replace(" ,", ",")
    if " ?" in texto:
        texto = texto.replace(" ?", "?")
    if " !" in texto:
        texto = texto.replace(" !", "!")
    if " :" in texto:
        texto = texto.replace(" :", ":")
    if " ..." in texto:
        texto = texto.replace(" ...", "...")
    if " -" in texto:
        texto = texto.replace(" -", "-")
    if "- " in texto:
        texto = texto.replace("- ", "-")
    if " #" in texto:  # apenas usado em Bula para concatenar 3 palavras
        texto = texto.replace(" #", "")
    if "#" in texto:
        texto = texto.replace("#", "")
    if "< pCity >" in texto:
        texto = texto.replace("< pCity >", fala_cidade_fato())
    if "< pCidadeOficio >" in texto:
        texto = texto.replace("< pCidadeOficio >", fala_cidade_oficio())
    if "< gCelcius >" in texto:
        texto = texto.replace("< gCelcius >", fala_celsius())
    if "< pUmido >" in texto:
        texto = texto.replace("< pUmido >", fala_umidade())
    if "< pAbnp >" in texto:
        texto = texto.replace("< pAbnp >", fala_abnp())
    if "< dNormas >" in texto:
        texto = texto.replace("< dNormas >", fala_norma_abnp())
    if "< dPublic >" in texto:
        hoje = datetime.datetime.now().date()
        rand = randrange(0, hoje.year * 30)
        ontem = hoje - datetime.timedelta(days=rand)
        texto = texto.replace("< dPublic >", fala_data(ontem))
    if "< dOficio >" in texto:
        hoje = datetime.datetime.now().date()
        rand = randrange(0, hoje.year * 30)
        demain = hoje + datetime.timedelta(days=rand)
        texto = texto.replace("< dOficio >", fala_data(demain))

    return texto


def fala_cidade_fato():
    """
    :return: alguma cidade do arquivo fatos_cidades.txt
    """
    cidades = []
    with open(os.path.join("./base/fatos_cidades.txt"), encoding="utf8") as file:
        for line in file:
            cidades.append(line)
        file.close()

    x = randrange(0, len(cidades))
    city = cidades[x]
    city = city.replace("\n", "")
    return city


def fala_cidade_oficio():
    """
    :return: alguma cidade do arquivo cidade_país.txt
    """
    cidades = []
    with open(os.path.join("./base/fatos_cidades.txt"), encoding="utf8") as file:
        for line in file:
            cidades.append(line)
        file.close()

    x = randrange(0, len(cidades))
    city = cidades[x]
    city = city.replace("\n", "")

    return city


def fala_celsius():
    """
    :return: temperatura randômica entre 1 e 50 graus celcius - Meteoro
    """
    ini = randrange(1, 50)
    fim = randrange(1, 50)
    if ini > fim:
        tmp = ini
        ini = fim
        fim = tmp
    else:
        ini -= 1
    return str(ini) + "º e " + str(fim) + "º"


def fala_umidade():
    """
    :return: umidade randômica entre 1 e 99% - Meteoro
    """
    ini = randrange(1, 99)
    return str(ini) + "%"


def fala_data(dref):
    """
    :param data de referência
    :return: data genérica: dia + mês_extenso + ano
    """
    meses = [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]

    dia = dref.day
    mes = dref.month
    if mes > 0 and mes < 13:
        mes -= 1
    else:
        mes = 5

    mestxt = meses[mes]
    ano = dref.year
    return str(dia) + " de " + str(mestxt) + " de " + str(ano)


def fala_norma_abnp():
    """
    :return: data randômicamente 'anterior' à data atual
    """
    hoje = datetime.datetime.now().date()
    rand = randrange(0, hoje.year * 30)
    ontem = hoje - datetime.timedelta(days=rand)
    return str(ontem.day) + "/" + str(ontem.year)


def fala_abnp():
    lista = []
    full_name = os.path.join("./base/abnp.txt")
    with open(full_name, encoding="utf-8") as file:
        for line in file:
            alinhas = line.split("|")
            for item in alinhas:
                lista.append(item)

    nany = randrange(0, len(lista))
    return lista[nany]


def abre(nome_do_tema):
    """
    :param nome_do_tema
    :return: lista do arquivo
    """

    full_name = os.path.join("./data/", nome_do_tema) + ".ypo"
    lista = []
    with open(full_name, encoding="utf-8") as file:
        for line in file:
            lista.append(line)
        file.close()

    return lista


@st.cache(allow_output_mutation=True)
def load_babel():
    lista = []
    with open(os.path.join("./base/babel.txt"), "r") as babel:
        for line in babel:
            lista.append(line)
    return lista


def novo_babel(swap_pala):
    """
    :param swap_pala: quantas palavras por linhas no poema: 0 = rand; n = n-1 palavras
    :return: poema aleatório
    """

    lista_silabas = load_babel()
    sinais_ini = [".", ",", ":", "!", "?", "...", " "]
    sinais_end = [".", "!", "?", "..."]

    min_versos = 5
    max_versos = 15
    qtd_versos = random.randrange(min_versos, max_versos)

    sinal = "."
    novo_poema = []
    for nQtdLin in range(1, qtd_versos):
        novo_babel = ""
        if swap_pala == 0:
            qtd_palas = random.randrange(3, 7)
        else:
            qtd_palas = swap_pala

        for nova_frase in range(1, qtd_palas):
            nova_pala = ""
            qtd_silabas = random.randrange(2, 4)
            for palavra in range(1, qtd_silabas):
                njump = random.randrange(0, len(lista_silabas))
                nova_silaba = str(lista_silabas[njump])
                nova_pala += nova_silaba.strip()
            nova = nova_pala.replace("aa", "a")
            nova = nova.replace("ee", "e")
            nova = nova.replace("ii", "i")
            nova = nova.replace("uu", "u")
            novo_babel += nova.strip() + " "
            novo_babel.strip()

        if nQtdLin == 1:
            njump = random.randrange(0, len(sinais_ini))
            sinal = sinais_ini[njump]
            novo_poema.append("")
            novo_poema.append(novo_babel.strip() + sinal)
        else:
            nany = random.randrange(0, 99)
            if nany <= 50:
                njump = random.randrange(0, len(sinais_ini))
                sinal = sinais_ini[njump]
                novo_babel = novo_babel.rstrip() + sinal
            novo_poema.append(novo_babel.strip())
            if nany <= 50:  # put some ","
                if "," != sinal:
                    novo_poema.append("")

    last = novo_poema[-1]
    njump = random.randrange(0, len(sinais_end))
    sinal = sinais_end[njump]

    if len(last) > 1 and not last[-1] in sinais_ini:
        if "," == last or ":" == last:
            novo_poema[-1] += sinal
        else:
            novo_poema[-1] += "."

    return novo_poema

# from gtts import gTTS

# Nota: Certifique-se de que suas funções personalizadas (translate, gera_poema, etc.) 
# estejam acessíveis ou importadas aqui se estiverem em outro arquivo.

# --- ESTILIZAÇÃO MÍNIMA E SEGURA ---
st.set_page_config(page_title="a Machina de Fazer Poesia", layout="wide")

# --- FUNÇÕES DE CARREGAMENTO (LOADERS) ---

def translate(input_text):
    if st.session_state.lang == "pt":  # don't need translations here
        return input_text

    if not have_internet():
        st.session_state.lang = "pt"
        return input_text

    try:
        output_text = GoogleTranslator(
            source="pt", target=st.session_state.lang
        ).translate(text=input_text)

        output_text = output_text.replace("<br>>", "<br>")
        output_text = output_text.replace("< br>", "<br>")
        output_text = output_text.replace("<br >", "<br>")
        output_text = output_text.replace("<br ", "<br>")
        output_text = output_text.replace(" br>", "<br>")
        return output_text
    except:
        return translate("Arquivo muito grande para ser traduzido.")

@st.cache_data
def load_temas(book):
    book_list = []
    path = os.path.join("./base/rol_" + book + ".txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.replace(" ", "")
                book_list.append(line.strip("\n"))
    return translate(book_list)

@st.cache_data
def load_info(nome_tema):
    path = os.path.join("./base/info.txt")
    result = "nonono"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("|"):
                    pipe = line.split("|")
                    if pipe[1].upper() == nome_tema.upper():
                        genero, imagem, qtd_versos = pipe[2], pipe[3], pipe[4]
                        qtd_wordin, qtd_lexico, qtd_itimos = pipe[5], pipe[6], pipe[7]
                        qtd_analiz, qtd_cienti = pipe[8], pipe[9]
                        result = f"<br><br>Titulo: {nome_tema}<br>Gênero: {genero}<br>Versos: {qtd_versos}<br>"
                        result += f"Verbetes no texto: {qtd_wordin}<br>Verbetes do Tema: {qtd_lexico}<br>"
                        result += f"Banco de Ítimos: {qtd_itimos}<br>Análise: {qtd_analiz}<br>Notação: {qtd_cienti}<br>"
    return translate(result)

@st.cache_data
def load_index():
    index_list = []
    path = "./md_files/ABOUT_INDEX.md"
    if os.path.exists(path):
        with open(path, encoding="utf-8") as lista:
            for line in lista:
                index_list.append(line)
    return index_list

def load_lypo():
    lypo_text = ""
    path = os.path.join("./temp/LYPO_" + IPAddres)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as script:
            for line in script:
                lypo_text += line.strip() + "<br>"
    return lypo_text

def load_typo():
    typo_text = ""
    path = os.path.join("./temp/TYPO_" + IPAddres)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as script:
            for line in script:
                line = line.strip()
                line = line.replace(" >", "\n").replace("< ", "\n").replace(" br", "\n").replace("br ", "\n")
                line = line.replace("< <", ">").replace("> >", ">")
                typo_text += line + "<br>"
    return typo_text

def load_all_offs():
    return ["a_torre_de_papel", "livro_vivo", "quase_que_eu_Poesia", "faz_de_conto", "essencial", "desvoto", "um_romance", "linguafiada", "secreto"]

def load_off_book(book):
    book_full = []
    full_name = os.path.join("./off_machina/", book) + ".Pip"
    if os.path.exists(full_name):
        with open(full_name, encoding="utf-8") as file:
            for line in file:
                if line.startswith("|"):
                    book_full.append(line)
    return translate(book_full)

def load_book_pages(book_lines):
    book_pages = []
    for line in book_lines:
        if line.startswith("<EOF>"): break
        if line.startswith("|"):
            book_pages.append(line.split("|")[1])
    return translate(book_pages)

def load_poema(nome_tema, seed_eureka):
    script = gera_poema(nome_tema, seed_eureka)
    novo_ypoema = ""
    path = os.path.join("./temp/LYPO_" + IPAddres)
    if not os.path.exists("./temp"): os.makedirs("./temp")
    with open(path, "w", encoding="utf-8") as save_lypo:
        save_lypo.write(nome_tema + "\n")
        for line in script:
            save_lypo.write(line + "\n")
            novo_ypoema += line + "<br>"
    return translate(novo_ypoema)

def load_arts(nome_tema):
    path = "./images/machina/"
    images_txt = os.path.join("./base/images.txt")
    if os.path.exists(images_txt):
        with open(images_txt, encoding="utf-8") as lista:
            for line in lista:
                if line.startswith(nome_tema):
                    part = line.strip().partition(" : ")
                    if nome_tema == part[0]:
                        path = "./images/" + part[2] + "/"
                        break
    
    if os.path.exists(path):
        arts_list = [f for f in os.listdir(path) if f.endswith(".jpg")]
        if arts_list:
            image = random.choice(arts_list)
            if image in st.session_state.arts:
                st.session_state.arts.append(image)
            else:
                st.session_state.arts.append(image)
            if len(st.session_state.arts) > 36: del st.session_state.arts[0]
            return path + image
    return None

# --- FUNÇÕES DE INTERFACE (OUTPUT) ---

def write_ypoema(LOGO_TEXTO, LOGO_IMAGE):
    if LOGO_IMAGE and os.path.exists(LOGO_IMAGE):
        with open(LOGO_IMAGE, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""<div style='text-align:center'>
            <img src='data:image/jpg;base64,{data}' style='max-width:100%; border-radius:10px;'>
            <div style='text-align:left; font-size:18px; margin-top:15px;'>{LOGO_TEXTO}</div>
            </div>""", unsafe_allow_html=True
        )
    else:
        st.markdown(f"<div>{LOGO_TEXTO}</div>", unsafe_allow_html=True)

def talk(text):
    try:
        clean = text.replace("<br>", "\n").replace("< br>", "").replace("<br >", "")
        tts = gTTS(text=clean, lang=st.session_state.lang, slow=False)
        filename = f"./temp/audio_{random.randint(1, 10000)}.mp3"
        if not os.path.exists("./temp"): os.makedirs("./temp")
        tts.save(filename)
        st.audio(filename)
        os.remove(filename)
    except: pass

def say_number(tema):
    analise = "nonono"
    indexes = load_index()
    for line in indexes:
        if line.startswith(tema):
            analise = line.strip().partition(" : ")[2]
            break
    return translate(analise)

# --- PÁGINAS ---

def page_mini():
    temas_list = load_temas("todos os temas")
    maxy = len(temas_list)
    cols = st.columns([4, 1, 1, 1, 4])
    if cols[2].button("✻"): 
        st.session_state.mini = random.randrange(0, maxy)
    st.session_state.auto = cols[3].checkbox("auto")
    
    wait_time = 10
    if st.session_state.auto:
        wait_time = st.sidebar.slider(translate("Segundos:"), 5, 60, 10)

    placeholder = st.empty()
    while True:
        st.session_state.tema = temas_list[st.session_state.mini % maxy]
        curr = load_poema(st.session_state.tema, "")
        with placeholder.container():
            write_ypoema(curr, load_arts(st.session_state.tema) if st.session_state.draw else None)
        if not st.session_state.auto: break
        time.sleep(wait_time)
        st.session_state.mini = random.randrange(0, maxy)
        st.rerun()

def page_ypoemas():
    temas_list = load_temas(st.session_state.book)
    maxy = len(temas_list) - 1
    cols = st.columns([3, 1, 1, 1, 1, 1, 3])
    if cols[2].button("◀"): st.session_state.take = (st.session_state.take - 1) % maxy
    if cols[3].button("✻"): st.session_state.take = random.randint(0, maxy)
    if cols[4].button("▶"): st.session_state.take = (st.session_state.take + 1) % maxy
    
    st.session_state.tema = temas_list[st.session_state.take]
    with st.expander(f"⚫ {st.session_state.lang} - {st.session_state.tema}", expanded=True):
        curr = load_poema(st.session_state.tema, "")
        write_ypoema(curr, load_arts(st.session_state.tema) if st.session_state.draw else None)
    if st.session_state.talk: talk(curr)

def page_eureka():
    find_what = st.text_input(translate("Buscar..."))
    if len(find_what) >= 3:
        eureka_list = load_eureka(find_what)
        seeds = [l.strip().replace(" : ", " ➪ ") for l in eureka_list if " : " in l]
        if seeds:
            st.session_state.eureka = st.selectbox(f"Ocorrências: {len(seeds)}", range(len(seeds)), format_func=lambda x: seeds[x])
            tema = seeds[st.session_state.eureka].partition(" ➪ ")[2].replace(".txt", "")
            write_ypoema(load_poema(tema, seeds[st.session_state.eureka]), load_arts(tema) if st.session_state.draw else None)
        else: st.warning("Nada encontrado.")

def page_off_machina():
    offs = load_all_offs()
    idx = st.selectbox(translate("Livro Off"), range(len(offs)), format_func=lambda x: offs[x])
    book_lines = load_off_book(offs[idx])
    pages = load_book_pages(book_lines)
    st.session_state.off_take = st.select_slider("Página", options=range(len(pages)), value=st.session_state.off_take % len(pages))
    content = book_lines[st.session_state.off_take].replace("|", "<br>")
    write_ypoema(translate(content), load_arts(offs[idx]) if st.session_state.draw else None)

def page_books():
    books = ["todos os temas", "livro vivo", "poemas", "ensaios", "jocosos", "sociais"]
    sel = st.selectbox("Escolha o Livro", books, index=books.index(st.session_state.book))
    if st.button("Confirmar"):
        st.session_state.book = sel
        st.session_state.take = 0
        st.rerun()

def page_polys():
    # Carrega idiomas do arquivo base de forma bruta e segura
    if os.path.exists("./base/poly.txt"):
        with open("./base/poly.txt", "r", encoding="utf-8") as f:
            langs = [l.strip() for l in f]
        sel = st.selectbox("Idioma", range(len(langs)), format_func=lambda x: langs[x])
        if st.button("Trocar"):
            st.session_state.lang = langs[sel].split(" : ")[1]
            st.rerun()

def page_abouts():
    abouts = ["comments", "prefácio", "machina", "bibliografia", "license", "index"]
    choice = st.selectbox("Sobre", abouts)
    st.markdown(load_md_file(f"ABOUT_{choice.upper()}.md"))

# --- MAIN ---

def main():
    if st.session_state.visy:
        #update_visy()
        st.session_state.visy = False

    # Menu lateral padrão Streamlit (evita quebra de bibliotecas externas)
    with st.sidebar:
        st.title("Cockpit")
        page = st.radio("Navegação", ["mini", "yPoemas", "eureka", "off-machina", "books", "poly", "about"])
        st.session_state.draw = st.checkbox("Imagens", st.session_state.draw)
        st.session_state.talk = st.checkbox("Voz", st.session_state.talk)
        
        img_map = {"mini": "mini", "yPoemas": "ypoemas", "eureka": "eureka", "off-machina": "off-machina", "books": "books", "poly": "poly", "about": "about"}
        st.image(f"./img_{img_map[page]}.jpg")

    if page == "mini": page_mini()
    elif page == "yPoemas": page_ypoemas()
    elif page == "eureka": page_eureka()
    elif page == "off-machina": page_off_machina()
    elif page == "livros": page_books()
    elif page == "poly": page_polys()
    elif page == "sobre": page_abouts()

if __name__ == "__main__":
    # Inicialização de Session State
    for key, val in {'book': 'todos os temas', 'take': 0, 'mini': 0, 'off_book': 0, 'off_take': 0, 
                     'lang': 'pt', 'draw': True, 'talk': False, 'visy': True, 'eureka': 0, 'arts': []}.items():
        if key not in st.session_state: st.session_state[key] = val
    
    # Placeholder global para variáveis de IP se necessário
    if 'IPAddres' not in globals(): IPAddres = "local_user"
    
    main()
    
