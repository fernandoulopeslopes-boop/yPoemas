""" build_lexico.py
    Função para gerar lexico.txt
    com todas as palavras de todos os temas em ativos.txt

    Obs : remover 25 para colar pipes...
    s =  set(string.punctuation)  # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~

def load_Words():
    with open('words.txt', 'r') as G:
        textfile = G.read()
    return textfile

def rand_Word():
    textfile = loadWords()
    sl = textfile.split()
    return(random.choice(sl))
    
def cata_pala():  # return: alguma palavra do grupo 'onde' no arquivo cata_pala.txt
    palas = []
    with open(os.path.join("./base/cata_pala.txt"), encoding="utf8") as file:
        for line in file:
            part_string = line.partition(" : ")
            # if part_string[0] == onde:
            palas.append(part_string[2])
        file.close()

    x = randrange(0, len(palas))
    pala = palas[x].replace("\n", "")
    return pala
"""

import os
import time
import string

from datetime import datetime
from lay_2_ypo import gera_poema
from build_indexy import gera_indexy


gera_indexy()  # update análises combinatórias


indexes_itimos = []
with open(os.path.join('./base/itimos.txt'), encoding='utf-8') as file:
    for line in file:
        indexes_itimos.append(line)


index_numbers = []
with open(os.path.join('./md_files/' + 'ABOUT_INDEX.md'), encoding='utf-8') as file:
    for line in file:
        index_numbers.append(line)


def say_itimos(tema):  # search index title for qtd de itimos no tema
    itimos = 'nonono'
    for line in indexes_itimos:
        this_line = line.strip('\n')
        part_line = this_line.partition(' : ')
        if part_line[0].upper() == tema.upper():
            itimos = part_line[2]
            break
    return itimos


def say_number(tema):  # search index title for palavras no tema
    number = 'nonono'
    for line in index_numbers:
        this_line = line.strip('\n')
        part_line = this_line.partition(' : ')
        if part_line[0].upper() == tema.upper():
            number = part_line[2]
            break
    return number


def zay_number(tema):  # search index title for palavras no tema
    number = 'nonono'
    if tema in index_numbers:
        nany = index_numbers.index(tema)
        line = index_numbers[nany]
        print(line, nany)
        this_line = line.strip('\n')
        part_line = this_line.partition(' : ')
        # if part_line[0].upper() == tema.upper():  # redundante!
        number = part_line[2]
    else:
        print(number)
    return number
        

def conta_palas(frase):  # conta palavras da frase == wordin
    palas = 0
    texto = ''
    for letra in frase:
        texto += letra

    for chars in texto:
        if chars == ' ':
            palas += 1
    return palas


def gera_lexico():
    start_time = time.time()

    temas_list = []  # lista de scripts.ypo - incluindo signos

    with open(os.path.join('./base/ativos.txt'), encoding='utf-8') as file:
        for line in file:
            this_line = line.strip('\n')
            part_line = this_line.partition(' : ')
            ativo = part_line[0]
            file = os.path.join('./data/', ativo + '.ypo')
            if not 'Babel' in file:
                temas_list.append(file)

    kill_errata = []
    list_capita = []
    list_lexico = []
    list_occurs = []
    list_unicos = []
    list_winlex = []
    list_wordin = []

    for script in temas_list:  # iterate all files.ypo
        try:
            list_header = []
            list_corpus = []
            list_footer = []

            with open(script, encoding='utf-8') as file:  # iterate file line by line
                path = os.path.basename(script)
                os.path.splitext(path)
                tabela = os.path.splitext(path)[0]
                print(tabela)

                qtd_winlex = 0
                for line in file:
                    if line.startswith('*'):  # comment lines
                        list_header.append(line)
                    elif line.startswith('|'):  # ítimos lines
                        list_corpus.append(line)
                        alinhas = line.split('|')
                        if len(alinhas) == 0:
                            pass
                        elif len(alinhas) >= 7:
                            fonte = (
                                tabela + '_' + alinhas[1] + alinhas[2]
                            )  # fonte = alinhas[3]
                            banco_de_itimos = alinhas[7 : len(alinhas) - 1]
                            for itimo in banco_de_itimos:
                                verbetes = itimo.split(' ')
                                for word in verbetes:
                                    word = word.replace('.', '')
                                    word = word.replace('"', '')
                                    if not '<' in word:  # macros dos yPoemas
                                        if (
                                            not '-' in word
                                        ):  # para não eliminar achar-se; perder-me...
                                            for c in string.punctuation:
                                                word = word.replace(c, '')

                                    if len(word) > 2:
                                        if (word.isalpha()) == True:
                                            qtd_winlex += 1

                                        if not word in list_unicos:
                                            list_unicos.append(word)

                                        if not word.capitalize() in list_capita:
                                            list_capita.append(word.capitalize())
                                            list_occurs.append(1)
                                        else:
                                            occurs = list_capita.index(
                                                word.capitalize()
                                            )
                                            list_occurs[occurs] += 1

                                        if (
                                            not word
                                            in '_dNormas_dOficio_dPublic_gCelcius_pCidadeOficio_pCity_pUmido_pAbnp'  # macros dos yPoemas
                                        ):
                                            if not word + ' : ' + fonte in list_lexico:
                                                list_lexico.append(word + ' : ' + fonte)
                    else:  # info lines
                        if line.startswith('<EOF>'):
                            list_corpus.append(line)
                        else:
                            if (
                                'CATAPALA' in line
                                or 'VERBETES' in line
                                or 'PALAVRAS' in line
                                or 'VARIATIO' in line
                                or 'COMBINAS' in line
                                or 'ANALIS' in line
                                or 'Análise' in line
                                or 'Palavras' in line
                                or 'Verbetes' in line
                                or 'Banco' in line
                            ):
                                continue
                            else:
                                if not line.startswith('#'):
                                    line = '# ' + line
                                list_footer.append(line)

                ypoema = gera_poema(tabela, '')
                qtd_wordin = conta_palas(ypoema)
                qtd_itimos = say_itimos(tabela)
                qtd_analiz = say_number(tabela)

                list_wordin.append(tabela + ' : ' + str(qtd_wordin))
                list_winlex.append(tabela + ' : ' + str(qtd_winlex))

                substr = 'Build_By_Lay_2_Ipo'
                if not any(substr in str for str in list_footer):
                    today = datetime.now()
                    datay = today.strftime('%d/%m/%Y, %H:%M:%S')
                    list_footer.insert(0, '# Build_By_Lay_2_Ipo: ' + datay + '\n')

                list_footer.insert(0, '# ' + '\n')
                list_footer.insert(
                    0, "# Análise combinatória: " + str(qtd_analiz) + '\n'
                )
                list_footer.insert(0, '# ' + '\n')
                list_footer.insert(
                    0, "#      Banco de ítimos: " + str(qtd_itimos) + '\n'
                )
                list_footer.insert(
                    0, "#     Verbetes do tema: " + str(qtd_winlex) + '\n'
                )
                list_footer.insert(
                    0, "#      Verbetes usados: " + str(qtd_wordin) + '\n'
                )
                list_footer.insert(0, "# " + '\n')

            file.close()
            #
            #  rebuild_yPoema
            #
            with open(
                os.path.join('./data/' + tabela + '.ypo'), 'w', encoding='utf-8'
            ) as file:
                for linha in list_header:
                    file.write(linha)

                for linha in list_corpus:
                    file.write(linha)

                last = "# "
                for linha in list_footer:
                    if not (last == linha):  # elimina linhas '#' duplas
                        file.write(linha)
                        last = linha
            file.close()

        except UnicodeDecodeError:
            kill_errata.append(script)
            pass

    # rebuild lexico
    with open(os.path.join('./base/' + 'lexico_pt.txt'), 'w', encoding='utf-8') as fooo:
        for line in list_lexico:
            fooo.write(line + '\n')

    # rebuild list of occurs
    list_quants = []
    list_totais = []
    with open(os.path.join('./base/' + 'occurs_pt.txt'), 'w', encoding='utf-8') as fooo:
        for word in list_capita:
            indexy = list_capita.index(word)
            fooo.write(str(list_occurs[indexy]) + " : " + word.lower() + '\n')

            if str(list_occurs[indexy]) not in list_quants:
                list_quants.append(str(list_occurs[indexy]))
                list_totais.append(1)
            else:
                occurs = list_quants.index(str(list_occurs[indexy]))
                list_totais[occurs] += 1

        fooo.write("---" + '\n')

        list_finaly = []
        for item in list_quants:
            indexy = list_quants.index(item)
            if not item in list_finaly:
                toty = list_totais[indexy]
                if toty == 1:
                    vezy = " vez"
                else:
                    vezy = " vezes"

                list_finaly.append(item + " : " + str(toty) + vezy)

        list_finaly.sort()
        for item in list_finaly:
            fooo.write(item + '\n')

    # rebuild list of unical words
    with open(os.path.join('./base/' + 'unicos_pt.txt'), 'w', encoding='utf-8') as fooo:
        for word in list_unicos:
            fooo.write(word + '\n')

    # rebuild list of words in wordin.txt == verbetes usados no texto gerado
    with open(os.path.join('./base/' + 'wordin.txt'), 'w', encoding='utf-8') as fooo:
        for word in list_wordin:
            fooo.write(word + '\n')

    # rebuild list of words in winlex.txt == words_in_lexico de cada tema
    with open(os.path.join('./base/' + 'winlex.txt'), 'w', encoding='utf-8') as fooo:
        for word in list_winlex:
            fooo.write(word + '\n')

    # printing runtime
    print("Runtime:", time.time() - start_time)
    if len(kill_errata) > 0:
        print(kill_errata)
    else:
        print("done !")


# Driver Code:
if __name__ == '__main__':
    gera_lexico()
