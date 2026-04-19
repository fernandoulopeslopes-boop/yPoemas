#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tools import load_temas_ativos, zay_number
import sys

IDIOMAS = {
    'Português': 'pt',
    'Espanhol': 'es',
    'Italiano': 'it',
    'Francês': 'fr',
    'Inglês': 'en',
    'Catalão': 'ca',
    'Córsico': 'co',
    'Galego': 'gl',
    'Basco': 'eu',
    'Esperanto': 'eo',
    'Latin': 'la',
    'Galês': 'cy',
    'Sueco': 'sv',
    'Polonês': 'pl',
    'Holandês': 'nl',
    'Norueguês': 'no',
    'Finlandês': 'fi',
    'Dinamarquês': 'da',
    'Irlandês': 'ga',
    'Romeno': 'ro',
    'Russo': 'ru'
}

def main():
    ativos = load_temas_ativos()

    if len(sys.argv) < 2:
        print("Uso: python main.py <tema>")
        print("Temas disponíveis:")
        for tema, tipo in ativos.items():
            print(f" {tema} : {tipo}")
        return

    tema = sys.argv[1]

    if tema not in ativos:
        print(f"Erro: tema '{tema}' não encontrado em ativos.txt")
        return

    numero = zay_number(tema)
    tipo = ativos[tema]

    print(f"Tema: {tema}")
    print(f"Tipo: {tipo}")
    print(f"Número: {numero}")

if __name__ == "__main__":
    main()
