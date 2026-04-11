import os
import random

def gera_poema(nome_tema, seed_eureka=""):
    """
    Motor lógico: Recebe o tema e a semente, sorteia os versos
    e devolve a lista para a interface.
    """
    
    # 1. Localização da base de dados (exemplo)
    # Supondo que seus versos estejam em arquivos dentro de /base
    caminho_base = os.path.join("./base", f"{nome_tema}.txt")
    
    # --- AQUI ENTRA A SUA LÓGICA ORIGINAL DE SORTEIO ---
    # Se o arquivo não existir, retornamos um aviso ou um sorteio padrão
    if not os.path.exists(caminho_base):
        poema_gerado = [f"Iniciando versos sobre {nome_tema}...", "O silêncio precede a criação."]
    else:
        with open(caminho_base, "r", encoding="utf-8") as f:
            linhas = f.readlines()
            # Sorteia, por exemplo, 5 versos aleatórios
            poema_gerado = random.sample(linhas, min(len(linhas), 5))
            poema_gerado = [l.strip() for l in poema_gerado]

    # 2. Gravação do histórico (.ypo)
    try:
        if not os.path.exists("./data"):
            os.makedirs("./data")
        
        caminho_save = os.path.join("./data", f"{nome_tema}.ypo")
        with open(caminho_save, "w", encoding="utf-8") as f_save:
            for verso in poema_gerado:
                f_save.write(str(verso) + "\n")
    except Exception:
        pass # Silencioso conforme o protocolo

    return poema_gerado
