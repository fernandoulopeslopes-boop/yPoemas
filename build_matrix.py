""" build_matrix.py
    Função para gerar matrix 3D de cada tema.ypo em /data
"""

import os
import time

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def gera_matrix():

    start_time = time.time()
    
    temas_list = []
    lista_itimos = []
    lista_versos = []

    with open(os.path.join("./base/ativos.txt"), encoding="utf-8") as file:
        for line in file:
            this_line = line.strip("\n")
            part_line = this_line.partition(" : ")
            ativo = part_line[0]
            file = os.path.join("./data/" + ativo + ".ypo")
            temas_list.append(file)

    for script in temas_list:  # iterate all files.ypo

        with open(script, encoding="utf-8") as file:  # iterate file line by line
    
            path = os.path.basename(script)
            os.path.splitext(path)
            tabela = os.path.splitext(path)[0]
            tabela = tabela.capitalize()

            curlin = "01"  # obrigatoriamente começa com |01|
            linini = 1
            itimos_acm = 0
    
            x_pos = np.array([])
            y_pos = np.array([])
            z_pos = np.array([])
            z_val = np.array([])

            fg = plt.figure(figsize=(7,7))
            ax = fg.add_subplot(111, projection="3d")

            for line in file:
                if line.startswith("|", 0, 1):
                    linhas = line.split("|")
                    newlin = int(linhas[1])
                    newcol = int(linhas[2])

                    if linhas[1] != curlin:
                        linini += 1
                        curlin = linhas[1]

                    if newcol == 0:  # linha em branco
                        x_pos = np.append(x_pos, linini)
                        y_pos = np.append(y_pos, 0)
                        z_pos = np.append(z_pos, 0)
                        z_val = np.append(z_val, 0)
                    else:
                        itimos = int(linhas[5])
                        itimos_acm += itimos
                        delta = 1  # because linini começa com 1
                        x_pos = np.append(x_pos, linini - delta)
                        y_pos = np.append(y_pos, newcol - delta)
                        z_pos = np.append(z_pos, 0)
                        z_val = np.append(z_val, itimos)

            x_val = np.ones(len(x_pos))
            y_val = np.ones(len(y_pos))
            z_pos = np.ones(len(z_pos))

            ax.set_xlabel("x ➪ linhas", fontsize=14)
            ax.set_ylabel("y ➪ versos", fontsize=14)
            ax.set_zlabel("z ➪ ítimos", fontsize=14)

            if len(x_val) > 0:
                ax.view_init(elev=30, azim=-30)
                ax.bar3d(
                    x_pos,
                    y_pos,
                    z_pos,
                    x_val,
                    y_val,
                    z_val,
                    color="#00ccaa",
                    alpha=0.85,
                    edgecolor="k",
                )  #

                file_save = os.path.join("./images/matrix/" + tabela + ".jpg")
                plt.savefig(file_save, dpi=50)
                plt.close()

                lista_versos.append( tabela + " : " + str(linini) )
                lista_itimos.append( tabela + " : " + str(itimos_acm) )

            print(tabela, linini, itimos_acm)

    with open(os.path.join("./base/" + "itimos.txt"), "w", encoding="utf-8") as file_to_save:
        for line in lista_itimos:
            file_to_save.write(line + "\n")

    with open(os.path.join("./base/" + "versos.txt"), "w", encoding="utf-8") as file_to_save:
        for line in lista_versos:
            file_to_save.write(line + "\n")

    print("Runtime:", time.time() - start_time)


# Driver Code:
if __name__ == "__main__":
    gera_matrix()
