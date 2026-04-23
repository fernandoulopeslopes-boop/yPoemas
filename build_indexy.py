""" build_indexy.py

    Função para gerar ./md_files/ABOUT_INDEX.md
    para todos os temas do ambiente ypo

"""

import os
import time
import string
from tools import load_temas_ativos


def gera_indexy():

    start_time = time.time()
    escala = [
        "mil",
        "milhões",
        "bilhões",
        "trilhões",
        "quatrilhões",
        "quintilhões",
        "sextilhões",
        "setilhões",
        "octilhões",
        "nonilhões",
        "decilhões",
        "undecilhões",
        "dodecilhões",
        "tredecilhões",
        "quatuordecilhões",
        "quindecilhões",
        "sedecilhões",
        "septendecilhões",
    ]

    temas_list = []
    with open(os.path.join("./base/ativos.txt"), encoding="utf-8") as file:
        for line in file:
            this_line = line.strip("\n")
            part_line = this_line.partition(" : ")
            tema_ativo = part_line[0]
            file = os.path.join("./data/" + tema_ativo + ".ypo")
            temas_list.append(file)

    error_list = []
    table_list = []
    index_list = []
    acm_variatio = 0

    for script in temas_list:  # loop to iterate all files.ypo
        try:
            with open(script, encoding="utf-8") as file:  # iterate file line by line
                path = os.path.basename(script)
                os.path.splitext(path)
                tabela = os.path.splitext(path)[0]
                tabela.replace(".ypo", " : ")
                print(tabela)

                fontes_list = []
                corrige_qtd = 1
                qtd_itimos_list = []

                for line in file:
                    if line.startswith("|"):
                        alinhas = line.split("|")
                        if len(alinhas) == 0:
                            pass
                        elif len(alinhas) >= 7:
                            nova_fonte = alinhas[3]
                            total_itimos = len(alinhas[7 : len(alinhas) - 1])
                            if (
                                not nova_fonte in fontes_list
                            ):  # Lista das FONTES que estão sendo usadas no Tema
                                fontes_list.append(nova_fonte)
                                qtd_itimos_list.append(total_itimos)
                            else:  # Fonte já foi usada uma vez... Ajuste na Qtd de Regs...
                                index = fontes_list.index(nova_fonte)
                                saldo_itimos = (
                                    qtd_itimos_list[index] - corrige_qtd
                                )  # corrige multiplicação
                                if saldo_itimos == 0:
                                    saldo_itimos = 1  # because "trois fois rien"
                                fontes_list.append(nova_fonte)
                                qtd_itimos_list.append(saldo_itimos)
                                corrige_qtd += 1

            qtd_variatio = 1
            for nany in qtd_itimos_list:
                qtd_variatio = +(qtd_variatio * nany)
            qtd_variatio = abs(qtd_variatio)
            acm_variatio += qtd_variatio
            num_variatio = f"{qtd_variatio:,}"

            potent = "nonono"
            pontos = num_variatio.count(",") - 1
            if pontos >= 0:
                potent = escala[pontos]

            index_list.append(
                tabela + " : " + f"{qtd_variatio:,}" + " (" + potent + ")"
            )

        except UnicodeDecodeError:
            error_list.append(script)
            pass

    # reconstrói ABOUT_INDEX.md
    with open(
        os.path.join("./md_files/" + "ABOUT_INDEX.md"), "w", encoding="utf-8"
    ) as file:
        file.write("variações para cada tema:  \n")
        file.write("___  \n")

        for linhas in index_list:
            file.write(linhas.replace(",", ".") + "  \n")  # add 2 spaces for md files

        file.write("___\n")
        file.write("[escala dos nomes das potências de 10]  \n")
        file.write("  \n")
        file.write("> mil=1.000|10e3|  \n")
        file.write("> milhão=1.000.000|10e6|  \n")
        file.write("> bilhão=1.000.000.000|10e9|  \n")
        file.write("> trilhão=1.000.000.000.000|10e12|  \n")
        file.write("> quatrilhão=1.000.000.000.000.000|10e15|  \n")
        file.write("> quintilhão=1.000.000.000.000.000.000|10e18|  \n")
        file.write("> sextilhão=1.000.000.000.000.000.000.000|10e21|  \n")
        file.write("> setilhão=1.000.000.000.000.000.000.000.000|10e24|  \n")
        file.write("> octilhão=1.000.000.000.000.000.000.000.000.000|10e27|  \n")
        file.write("> nonilhão=1.000.000.000.000.000.000.000.000.000.000|10e30|  \n")
        file.write(
            "> decilhão=1.000.000.000.000.000.000.000.000.000.000.000|10e33|  \n"
        )
        file.write(
            "> undecilhão=1.000.000.000.000.000.000.000.000.000.000.000.000|10e36|  \n"
        )
        file.write(
            "> dodecilhão=1.000.000.000.000.000.000.000.000.000.000.000.000.000|10e39|  \n"
        )
        file.write(
            "> tredecilhão=1.000.000.000.000.000.000.000.000.000.000.000.000.000.000|10e42|  \n"
        )
        file.write(
            "> quatordecilhão=1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000|10e45|  \n"
        )
        file.write(
            "> quindecilhão=1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000|10e48|  \n"
        )
        file.write(
            "> sedecilhão=1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000|10e51|  \n"
        )
        file.write(
            "> septendecilhão=1.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000.000|10e54|  \n"
        )
        file.write("> googol=dez duotrigintilhões|10e100|  \n")
        file.write("> googolplexo=quanto dá isso?|10e googol|  \n")
        file.write(
            "> googolplexiano=por enquanto, o maior número com nome|10e googolplexo|  \n"
        )
        file.write("  \n")
        file.write(
            "[fonte dos dados](http://www.fisica-interessante.com/matematica-divertida-ordens-classes-multiplos.html)  \n"
        )
        file.write("___\n")
        file.write(
            "Copyright © 1983-2022 Nando Lopes - **yPoemas @ máquina de fazer Poesia**  \n"
        )

        num_variatio = f"{acm_variatio:,}"
        potent = "nonono"
        pontos = num_variatio.count(",") - 1
        if pontos >= 0:
            potent = escala[pontos]

        acm_variatio = (
            "Total de variações: " + f"{acm_variatio:,}" + " (" + potent + ")"
        )
        file.write(
            "\n" + acm_variatio.replace(",", ".") + "\n"
        )  # add 2 spaces for md files

    print(error_list)
    print(len(index_list))
    print("Runtime:", time.time() - start_time)


# Driver Code:
if __name__ == "__main__":
    gera_indexy()
