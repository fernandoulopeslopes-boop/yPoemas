import os
import time
import string

"""
    Funções para gerar ./base/lexico_pt.txt
    a partir dos arquivos .ypo em ./data.

    Contrato com tools_Machina / Build All:
    - gera_lexico() não pede input.
    - gera_lexico() reconstrói e salva o léxico completo.
    - build_lexico(this_tema) continua disponível para gerar um tema isolado.
"""

IGNORAR_LEXICO = "_dNormas_dOficio_dPublic_gCelcius_pCidadeOficio_pCity_pUmido"


def _limpa_palavra(word):
    """Preserva a regra histórica de limpeza usada no build original."""
    word = word.replace(".", "")
    word = word.replace('"', "")

    if "<" not in word:
        # Para não eliminar achar-se; perder-me...
        if "-" not in word:
            for c in string.punctuation:
                word = word.replace(c, "")

    return word


def _lista_temas_data():
    """Lista os temas existentes em ./data sem alterar nenhum arquivo .ypo."""
    data_dir = "./data"
    if not os.path.isdir(data_dir):
        raise FileNotFoundError("Pasta ./data não encontrada.")

    temas = []
    for file_name in os.listdir(data_dir):
        if file_name.endswith(".ypo"):
            temas.append(os.path.splitext(file_name)[0])

    temas.sort(key=str.lower)
    return temas


def build_lexico(this_tema):
    """Gera as linhas de léxico de um único tema, sem salvar o arquivo final."""
    file_path = os.path.join("./data", this_tema + ".ypo")
    list_lexico = []

    with open(file_path, encoding="utf-8") as lexifile:
        for line in lexifile:
            if not line.startswith("|"):
                continue

            alinhas = line.split("|")
            if len(alinhas) < 8:
                continue

            fonte = this_tema + "_" + alinhas[1] + alinhas[2]
            palas = alinhas[7 : len(alinhas) - 1]

            for itimo in palas:
                unicas = itimo.split(" ")
                for word in unicas:
                    word = _limpa_palavra(word)

                    if len(word) > 2:
                        if not word in IGNORAR_LEXICO:
                            entrada = word + " : " + fonte
                            if entrada not in list_lexico:
                                list_lexico.append(entrada)

    return list_lexico


def gera_lexico():
    """Reconstrói ./base/lexico_pt.txt para uso pelo Eureka e pelo Build All."""
    start_time = time.time()
    temas = _lista_temas_data()
    list_lexico = []
    vistos = set()

    for tema in temas:
        for entrada in build_lexico(tema):
            if entrada not in vistos:
                vistos.add(entrada)
                list_lexico.append(entrada)

    os.makedirs("./base", exist_ok=True)
    output_file = os.path.join("./base", "lexico_pt.txt")

    with open(output_file, "w", encoding="utf-8") as lex:
        for line in list_lexico:
            lex.write(line + "\n")

    print("Temas:", len(temas))
    print("Entradas no léxico:", len(list_lexico))
    print("Runtime:", time.time() - start_time)
    print("done !")

    return len(list_lexico)


# Driver Code:
if __name__ == "__main__":
    filename = input("Tema para o Léxico ou ENTER para todos: ").strip()
    if filename:
        for line in build_lexico(filename.capitalize()):
            print(line)
    else:
        gera_lexico()
