""" build_one.py
    para novos temas:
    - incluir novo_tema em \ypo\base\ativos.txt
    - incluir novo_tema em \ypo\base\images.txt
    - incluir novo_tema em \ypo\temp\readings.txt
    - incluir novo_tema em \base\rol_*.txt
    - atualizar ABOUT_NOTES.md se necessário...

    updates: ABOUT_INDEX.md
             lexico_pt.txt
             matrix.txt
             info.txt

"""

import time
from lexico import build_lexico
from matrix import build_matrix
from build_info import gera_info

filename = ""

def build():

    start_time = time.time()
    
    print("")
    print("gerando léxico + indexes...")
    build_lexico(filename.capitalize())
    print("done léxico + indexes...")
    
    print("")
    print("gerando matrix...")
    build_matrix(filename.capitalize())
    print("done matrix...")
    
    print("")
    print("gerando info...")
    gera_info()
    print("done info...")
    
    print("")
    print("Runtime:", time.time() - start_time)


# Driver Code:
if __name__ == "__main__":
    filename = input("Build Tema ---> ")
    build(filename)
