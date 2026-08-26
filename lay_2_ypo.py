import os
import random
import datetime
import streamlit as st

from random import randrange

from lay_tools import (
    abre_ypo_preservando_newline,
    comando_espacamento_compacto,
    gravar_ypo_certificado,
    indice_konstante,
    linha_com_itimos_atual,
    linha_fim,
    tabs_payload,
    validar_estrutura_ypo,
)


def gera_poema(nome_tema, seed_eureka):  # abrir um script.ypo e gerar um novo yPoema
    """
    Motor histórico da Machina.

    A arquitetura permanece explícita: HEADER / BODY / FINAIS.
    Na persistência, somente itimos_atual pode mudar no BODY.
    O lay_2_ypo não cria nem altera build_by; atualiza apenas "updated em:".
    """

    lista_header = []
    lista_linhas = []
    lista_finais = []
    lista_change = []
    lista_duplos = []
    lista_errata = []
    lista_unicos = []

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
            return novo_babel(0)

        path = os.path.join("./data", nome_tema + ".ypo")
        tema = abre_ypo_preservando_newline(path)
        validar_estrutura_ypo(tema)
        original_linhas = list(tema)

        # Divisão histórica da casa: HEADER / BODY / FINAIS.
        em_body = False
        em_finais = False
        for line in tema:
            corpo = str(line).rstrip("\r\n")

            if em_finais:
                lista_finais.append(line)
                continue

            if corpo == "<EOF>":
                em_finais = True
                lista_finais.append(line)
                continue

            if line.startswith("|", 0, 1):
                em_body = True
                lista_linhas.append(line)
                continue

            if not em_body:
                lista_header.append(line)
                continue

            # validar_estrutura_ypo já deveria ter bloqueado este caso.
            raise RuntimeError("estrutura .ypo inválida entre BODY e <EOF>")

    except UnicodeDecodeError:
        lista_errata.append(nome_tema)
        original_linhas = []
    except (OSError, RuntimeError, ValueError) as exc:
        lista_errata.append(nome_tema)
        original_linhas = []
        st.warning(str(exc))

    novo_poema = []
    novo_verso = ""
    muda_linha = "00"
    pula_linha = "no"
    tabs_pendente = 0

    for line in lista_linhas:
        tabs_comando = comando_espacamento_compacto(line)
        if tabs_comando:
            tabs_pendente = tabs_comando
            lista_change.append(line)
            continue

        alinhas = line.rstrip("\r\n").split("|")

        if len(alinhas) < 3:
            lista_errata.append(nome_tema)
            lista_change.append(line)
            continue

        if alinhas[2] == "00":
            pula_linha = "si"
            lista_change.append(line)
            continue

        if len(alinhas) < 9:
            lista_errata.append(nome_tema)
            lista_change.append(line)
            continue

        numero_linea = alinhas[1]
        ideia_numero = alinhas[2]
        fonte_itimos = alinhas[3]
        se_randomico = alinhas[4]

        try:
            int(alinhas[5])  # qtd declarada: leitura apenas; não é regravada pelo motor
            itimos_atual = int(alinhas[6])
        except (TypeError, ValueError):
            lista_errata.append(nome_tema)
            lista_change.append(line)
            continue

        array_itimos, tabs = tabs_payload(alinhas[7:-1], tabs_pendente)
        tabs_pendente = 0

        find_eureka = nome_tema + "_" + numero_linea + ideia_numero
        total_itimos = len(array_itimos)

        if total_itimos <= 0:
            lista_errata.append(nome_tema)
            lista_change.append(line)
            continue

        if itimos_atual > total_itimos:
            itimos_atual = total_itimos

        if total_itimos == 1:
            se_randomico = "F"

        tentativas = 0
        while True:
            if total_itimos != 1:
                if se_randomico == "F":
                    itimos_atual -= 1
                    if itimos_atual < 0:
                        itimos_atual = total_itimos - 1
                elif se_randomico == "K":
                    itimo_k = indice_konstante(itimos_atual, total_itimos)
                else:
                    itimos_atual = randrange(0, total_itimos)
            else:
                itimos_atual = 0

            if se_randomico == "K":
                itimo_escolhido = array_itimos[itimo_k]
            elif 0 <= itimos_atual < len(array_itimos):
                itimo_escolhido = array_itimos[itimos_atual]
            else:
                st.warning(
                    "Algo deu errado em "
                    + fonte_itimos
                    + ". Se puder, entre em contato com o '[autor](mailto:lopes.fernando@hotmail.com)'"
                )
                itimo_escolhido = "_Erro_"

            if find_eureka == find_coords and look_for_seed:
                for itimo in array_itimos:
                    if this_seed.lower() in itimo.lower():
                        itimo_escolhido = itimo
                        lista_unicos.append(itimo_escolhido.upper())
                        itimo_escolhido = itimo_escolhido.replace(
                            this_seed, "<mark>" + this_seed + "</mark>"
                        )
                        look_for_seed = False
                        break

            if se_randomico == "K":
                if itimo_escolhido.upper() not in lista_unicos:
                    lista_unicos.append(itimo_escolhido.upper())
                break

            temp_random = se_randomico
            if (
                itimo_escolhido.upper()
                not in "_E_A_AS_O_OS_OU_NO_NOS_NA_NAS_ME_DE_SE_QUE_NÃO_SO_SEM_NEM_EM_UM_UMA_POR_MEU_VE_TE_TÃO_DA_SER_TER_PRA_PARA_QUANDO_..._._,_:_!_?"
            ):
                if itimo_escolhido.upper() not in lista_unicos:
                    lista_unicos.append(itimo_escolhido.upper())
                    break

                tentativas += 1
                if tentativas > total_itimos:
                    if temp_random == "T":
                        tentativas = 0
                        temp_random = "F"
                    else:
                        lista_unicos.append(itimo_escolhido.upper())
                        lista_duplos.append(itimo_escolhido.upper())
                        break

                if itimo_escolhido.upper() in lista_duplos and len(itimo_escolhido) > 3:
                    continue

                if tentativas > 30:
                    break
            else:
                break

        if numero_linea != muda_linha:
            novo_verso = acerto_final(novo_verso)
            novo_poema.append(novo_verso)
            novo_verso = ""
            muda_linha = numero_linea

        novo_verso += itimo_escolhido + " "
        if tabs > 0:
            novo_verso = tabs * "&emsp;" + novo_verso

        if pula_linha == "si":
            novo_poema.append("\n")
            pula_linha = "no"

        # Única alteração autorizada no BODY: itimos_atual (campo 6).
        persist_index = itimos_atual
        if persist_index < 1:
            persist_index = 1 if total_itimos == 1 else total_itimos
        lista_change.append(linha_com_itimos_atual(line, persist_index))

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
        novas_linhas = lista_header + lista_change + lista_finais
        gravar_ypo_certificado(path, original_linhas, novas_linhas)

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
    if "< nome_una >" in texto:
        texto = texto.replace("< nome_una >", fala_nome_OLA())
    if "< pCity >" in texto:
        texto = texto.replace("< pCity >", fala_cidade_fato())
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


def fala_nome_OLA():
    lista = gera_poema("OLA","")
    sigla = ""
    for line in lista:
        sigla += line + " "
    return(sigla)


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


@st.cache_data
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

#   5 - 15
    min_versos = 5
    max_versos = 15
    qtd_versos = random.randrange(min_versos, max_versos)

    sinal = "."
    novo_poema = []
    for nQtdLin in range(1, qtd_versos):
        novo_babel = ""
#   3 - 7
        if swap_pala == 0:
            qtd_palas = random.randrange(2, 10)
        else:
            qtd_palas = swap_pala
#   2 - 4
        for nova_frase in range(1, qtd_palas):
            nova_pala = ""

            qtd_silabas = random.randrange(1, 4)
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
