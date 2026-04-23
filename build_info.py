''' build_info.py

    build_info, from ativos.txt ---> update info.txt
    
    tema.jpg == usados em ypo/ypoemas/help e ypo/comments/machina

    - Titulo            : tema       : lista a partir de ativos.txt
    - Gênero            : gênero     : ativos.txt = manual update
    - Imagem            : imagem     : images.txt = manual update
    - Versos            : qtd_versos : gerado por build_matrix
    - Verbetes no texto : qtd_wordin : gerado por build_lexico --> wordin     (Words In text) de cada tema
    - Verbetes do Tema  : qtd_winlex : gerado por build_lexico --> winlex.txt (Words In LEXico) de cada tema
    - Banco de Ítimos   : qtd_itimos : gerado por build_matrix
    - Análise           : qtd_analiz : gerado por build_indexy
    - Notação Científica: qtd_cienti : np.format_float_scientific(analise)
    
    [update_all.py]
    build_indexy: from /data/*.ypo   | update ABOUT_INDEX.md
    build_lexico: from /data/*.ypo   | update lexico_pt.txt (todos os verbetes de todos os temas) e unicos_pt + reformat scripts
    build_matrix: from /data/*.ypo   | update itimos.txt, versos.txt e '/images/matrix/*.png'
    build_info:                      | update info.txt

    totais: versos = 18.974 / itimos = 38.123 / winlexs = 43.567
    
'''

import os
import time
import numpy as np

from tools import *

def gera_info():

    start_time = time.time()
    info = []

    info.append('|nome_tema|genero|imagem|versos|words_in|lexico|ítimos|analise|notação|')
    info.append('|   [0]   |  [1] |  [2] |  [3] |   [4]  |  [5] |  [6] |  [7]  |  [8]  |')
    info.append('')

    list_ativos = load_temas_ativos()
    
    for line in list_ativos:  # iterate all files.ypo
        this_line = line.strip("\n")
        part_line = this_line.partition(' : ')
        tema = part_line[0]
        txt_genero = part_line[2].strip()
        
        txt_imagem = say_imagem(tema)
        qtd_versos = say_versos(tema)
        qtd_wordin = say_wordin(tema)
        qtd_lexico = say_winlex(tema)
        qtd_itimos = say_itimos(tema)
        qtd_analiz = say_number(tema)
        
        decimal = ''
        for y in qtd_analiz:
            if y in '0123456789.':
                decimal += y
                
        decimal = decimal.replace(".", "")
        decimal = int(decimal)
        decimal = float(decimal)
        qtd_scient = np.format_float_scientific(np.float64(decimal), precision=3)
        qtd_scient = qtd_scient.replace(".", ",")
        qtd_scient = qtd_scient.replace("e+", " e+")

        text = ''
        text += '|' + tema
        text += '|' + txt_genero  # say_genero(tema)
        text += '|' + txt_imagem  # say_imagem(tema)
        text += '|' + qtd_versos  # say_versos(tema)
        text += '|' + qtd_wordin  # say_wordin(tema)
        text += '|' + qtd_lexico  # say_winlex(tema)
        text += '|' + qtd_itimos  # say_itimos(tema)
        text += '|' + qtd_analiz  # say_number(tema)
        text += '|' + qtd_scient  # say_number(tema)
        text += '|'
        info.append(text)
        print(tema)
        
    save_file("./base/", "info.txt", info)

    print("Runtime:", time.time() - start_time)

# Driver Code:
if __name__ == "__main__":
    gera_info()
