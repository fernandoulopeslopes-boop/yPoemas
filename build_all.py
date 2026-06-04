""" build_all.py

    para novos temas:
    - incluir novo_tema em \ypo\base\ativos.txt
    - incluir novo_tema em \ypo\base\images.txt
    - incluir novo_tema em \ypo\temp\readings.txt
    - incluir novo_tema em \base\rol_*.txt
    - atualizar ABOUT_NOTES.md se necessário...

    updates:
             lexico_pt.txt
             ABOUT_INDEX.md
             matrix.txt
             info.txt

"""

import time
from build_lexico import gera_lexico
from build_indexy import gera_indexy
from build_matrix import gera_matrix
from build_info import gera_info


def build():

    start_time = time.time()

    print("")
    print("gerando léxico...")
    gera_lexico()
    print("done léxico.")

    print("")
    print("gerando index / ABOUT_INDEX...")
    gera_indexy()
    print("done index / ABOUT_INDEX.")

    print("")
    print("gerando matrix...")
    gera_matrix()
    print("done matrix.")

    print("")
    print("gerando info...")
    gera_info()
    print("done info.")

    print("")
    print("Runtime:", time.time() - start_time)


# Driver Code:
if __name__ == "__main__":
    build()
