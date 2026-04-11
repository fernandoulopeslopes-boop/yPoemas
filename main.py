import streamlit as st
import random
import os

# --- MOTOR POÉTICO (Backup Restaurado) ---

@st.cache_data
def abre(nome_tema):
    """
    Abre o arquivo .ypo da pasta /data conforme o tema selecionado.
    """
    full_name = f"./data/{nome_tema}.ypo"
    try:
        with open(full_name, encoding="utf-8") as file:
            conteudo = file.read().splitlines()
        return conteudo
    except FileNotFoundError:
        return [f"Erro: Arquivo {nome_tema}.ypo não encontrado."]

def gera_poema(nome_tema, seed_eureka=""):
    """
    Lógica central do motor: processa o arquivo e gera os versos.
    """
    # Se houver semente (Eureka), fixa a aleatoriedade
    if seed_eureka:
        random.seed(seed_eureka)
    else:
        random.seed() # Aleatório livre

    dados = abre(nome_tema)
    
    # Se o arquivo retornar erro, repassa para o palco
    if not dados or "Erro:" in dados[0]:
        return dados

    # Lógica de sorteio estável
    poema_gerado = []
    for linha in dados:
        if "|" in linha:
            opcoes = linha.split("|")
            poema_gerado.append(random.choice(opcoes))
        else:
            poema_gerado.append(linha)
            
    return poema_gerado
