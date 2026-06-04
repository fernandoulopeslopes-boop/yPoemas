"""build_matrix.py
    Função para gerar matrix 3D de cada tema .ypo em /data.

Contrato usado pelo ypo_seguro.py / tools_Machina:
    from build_matrix import gera_matrix
    gera_matrix()

Regra importante:
    Não usar .capitalize(), .title() ou transformação parecida em nomes de tema/arquivo.
    A Machina pode ter nomes curatoriais sensíveis, como CIA_alguma_coisa.
"""

import os
import time

import numpy as np
import matplotlib.pyplot as plt


BASE_DIR = "./base"
DATA_DIR = "./data"
MATRIX_DIR = "./images/matrix"


def _clean_theme_name(value):
    """Limpa espaços/BOM sem alterar maiúsculas, minúsculas ou underscores."""
    return str(value).replace("\ufeff", "").strip()


def _load_active_theme_paths():
    """Carrega os temas ativos a partir de ./base/ativos.txt."""
    temas_list = []
    ativos_file = os.path.join(BASE_DIR, "ativos.txt")

    with open(ativos_file, encoding="utf-8", errors="replace") as file:
        for line in file:
            this_line = line.strip()
            if not this_line or this_line.startswith(("#", "//", "--")):
                continue

            ativo = _clean_theme_name(this_line.partition(" : ")[0])
            if not ativo:
                continue

            script_path = os.path.join(DATA_DIR, ativo + ".ypo")
            if os.path.exists(script_path):
                temas_list.append(script_path)
            else:
                print(f"AVISO: tema ativo sem arquivo .ypo: {ativo}")

    return temas_list


def gera_matrix():
    start_time = time.time()

    os.makedirs(MATRIX_DIR, exist_ok=True)

    temas_list = _load_active_theme_paths()
    lista_itimos = []
    lista_versos = []

    for script in temas_list:  # iterate all files .ypo
        with open(script, encoding="utf-8", errors="replace") as file:  # iterate file line by line
            path = os.path.basename(script)
            tabela = os.path.splitext(path)[0]  # preserva o nome curatorial exato

            curlin = "01"  # obrigatoriamente começa com |01|
            linini = 1
            itimos_acm = 0

            x_pos = np.array([])
            y_pos = np.array([])
            z_pos = np.array([])
            z_val = np.array([])

            fg = plt.figure(figsize=(7, 7))
            ax = fg.add_subplot(111, projection="3d")

            for line in file:
                if not line.startswith("|"):
                    continue

                linhas = line.split("|")
                if len(linhas) < 6:
                    continue

                try:
                    newcol = int(linhas[2])
                except ValueError:
                    continue

                if linhas[1] != curlin:
                    linini += 1
                    curlin = linhas[1]

                if newcol == 0:  # linha em branco
                    x_pos = np.append(x_pos, linini)
                    y_pos = np.append(y_pos, 0)
                    z_pos = np.append(z_pos, 0)
                    z_val = np.append(z_val, 0)
                else:
                    try:
                        itimos = int(linhas[5])
                    except ValueError:
                        itimos = 0

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
                )

                file_save = os.path.join(MATRIX_DIR, tabela + ".jpg")
                plt.savefig(file_save, dpi=50)
                plt.close(fg)

                lista_versos.append(tabela + " : " + str(linini))
                lista_itimos.append(tabela + " : " + str(itimos_acm))
            else:
                plt.close(fg)

            print(tabela, linini, itimos_acm)

    with open(os.path.join(BASE_DIR, "itimos.txt"), "w", encoding="utf-8") as file_to_save:
        for line in lista_itimos:
            file_to_save.write(line + "\n")

    with open(os.path.join(BASE_DIR, "versos.txt"), "w", encoding="utf-8") as file_to_save:
        for line in lista_versos:
            file_to_save.write(line + "\n")

    print("Runtime:", time.time() - start_time)


# Driver Code:
if __name__ == "__main__":
    gera_matrix()
