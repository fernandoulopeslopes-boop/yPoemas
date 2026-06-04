import os
import time
import string

"""
    Função para gerar lexico.txt
    com todas as palavras em this_tema
"""

def build_lexico(this_tema):
    start_time = time.time()
    file = os.path.join("./data", this_tema + ".ypo")

    # lista de palavras em this_tema
    list_lexico = []

    with open(file, encoding="utf-8") as lexifile:  # iterate lexifile line by line
        path = os.path.basename(file)
        os.path.splitext(path)
        for line in lexifile:
            if line.startswith("|"):
                alinhas = line.split("|")
                if len(alinhas) == 0:
                    pass
                elif len(alinhas) >= 7:
                    fonte = (
                        this_tema + '_' + alinhas[1] + alinhas[2]
                    )  # fonte = alinhas[3]
                    palas = alinhas[7 : len(alinhas) - 1]
                    for itimo in palas:
                        unicas = itimo.split(" ")
                        for word in unicas:
                            word = word.replace(".", "")
                            word = word.replace('"', "")
                            if not "<" in word:
                                # para não eliminar achar-se; perder-me...
                                if not "-" in word:
                                    for c in string.punctuation:
                                        word = word.replace(c, "")
    
                            if len(word) > 2:
                                if (
                                    not word
                                    in "_dNormas_dOficio_dPublic_gCelcius_pCidadeOficio_pCity_pUmido"
                                ):
                                    if not word + " : " + fonte in list_lexico:
                                        list_lexico.append(word + " : " + fonte)


    with open(os.path.join("./base/lexico_pt.txt"), encoding="utf-8") as lista:
        for line in lista:
            this_line = line.strip("\n")
            part_line = this_line.partition(' : ')
            palas = part_line[0]
            fonte = part_line[2]
            nome_tema = part_line[2:-5]

            if not nome_tema == this_tema: # colocar o "\n" no final do list_lexico - sem rebuild

                list_lexico.append((palas + " : " + fonte) + "\n")

    # printing runtime
    print("Runtime:", time.time() - start_time)
    print('done !')

# Driver Code:
if __name__ == "__main__":
    filename = input("Tema para o Léxico: ")
    build_lexico(filename.capitalize())
