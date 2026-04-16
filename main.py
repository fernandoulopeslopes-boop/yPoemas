import streamlit as st
import os
import random
import datetime
from random import randrange

st.set_page_config(page_title="yPoemas @ a Machina de fazer Poesia", layout="wide")

lista_livros = [
    "livro vivo",
    "poemas",
    "jocosos",
    "ensaios",
    "sociais",
    "variações",
    "metalinguagem",
    "outros autores",
    "signos_fem",
    "signos_mas",
    "todos os signos",
    "todos os temas",
]

def load_temas(book):  # List of themes inside a Book
    temas_list = []
    with open(
        os.path.join("./base/rol_" + book + ".txt"), "r", encoding="utf-8"
    ) as file:
        for line in file:
            line = line.replace(" ", "")
            temas_list.append(line.strip("\n"))

    return temas_list
lista_temas = load_temas("livro vivo")

lista_idiomas = ["Português", "English", "Español", "Français", "Italiano", "Deutsch"]

# --- [ FUNÇÕES AUXILIARES ] ---
def abre(nome_do_tema):
    full_name = os.path.join("./data/", nome_do_tema) + ".ypo"
    lista = []
    with open(full_name, encoding="utf-8") as file:
        for line in file:
            lista.append(line)
    return lista

@st.cache_data
def load_babel():
    lista = []
    with open(os.path.join("./base/babel.txt"), "r", encoding="utf-8") as babel:
        for line in babel:
            lista.append(line)
    return lista

def novo_babel(swap_pala):
    lista_silabas = load_babel()
    sinais_ini = [".", ",", ":", "!", "?", "...", " "]
    sinais_end = [".", "!", "?", "..."]
    min_versos = 5
    max_versos = 15
    qtd_versos = random.randrange(min_versos, max_versos)
    novo_poema = []
    for nQtdLin in range(1, qtd_versos):
        novo_babel = ""
        if swap_pala == 0:
            qtd_palas = random.randrange(3, 7)
        else:
            qtd_palas = swap_pala
        for nova_frase in range(1, qtd_palas):
            nova_pala = ""
            qtd_silabas = random.randrange(2, 4)
            for palavra in range(1, qtd_silabas):
                njump = random.randrange(0, len(lista_silabas))
                nova_silaba = str(lista_silabas[njump])
                nova_pala += nova_silaba.strip()
            nova = nova_pala.replace("aa", "a").replace("ee", "e").replace("ii", "i").replace("uu", "u")
            novo_babel += nova.strip() + " "
        if nQtdLin == 1:
            njump = random.randrange(0, len(sinais_ini))
            sinal = sinais_ini[njump]
            novo_poema.append("")
            novo_poema.append(novo_babel.strip() + sinal)
        else:
            nany = random.randrange(0, 99)
            if nany <= 50:
                njump = random.randrange(0, len(sinais_ini))
                sinal = sinais_ini[njump]
                novo_babel = novo_babel.rstrip() + sinal
            novo_poema.append(novo_babel.strip())
            if nany <= 50 and ","!= sinal:
                novo_poema.append("")
    last = novo_poema[-1]
    njump = random.randrange(0, len(sinais_end))
    sinal = sinais_end[njump]
    if len(last) > 1 and not last[-1] in sinais_ini:
        if "," == last or ":" == last:
            novo_poema[-1] += sinal
        else:
            novo_poema[-1] += "."
    return novo_poema

def fala_cidade_fato():
    cidades = []
    with open(os.path.join("./base/fatos_cidades.txt"), encoding="utf8") as file:
        for line in file:
            cidades.append(line)
    x = randrange(0, len(cidades))
    city = cidades[x].replace("\n", "")
    return city

def fala_cidade_oficio():
    cidades = []
    with open(os.path.join("./base/fatos_cidades.txt"), encoding="utf8") as file:
        for line in file:
            cidades.append(line)
    x = randrange(0, len(cidades))
    city = cidades[x].replace("\n", "")
    return city

def fala_celsius():
    ini = randrange(1, 50)
    fim = randrange(1, 50)
    if ini > fim:
        ini, fim = fim, ini
    else:
        ini -= 1
    return str(ini) + "º e " + str(fim) + "º"

def fala_umidade():
    ini = randrange(1, 99)
    return str(ini) + "%"

def fala_data(dref):
    meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
             "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    dia = dref.day
    mes = max(0, min(dref.month - 1, 11))
    mestxt = meses[mes]
    ano = dref.year
    return str(dia) + " de " + str(mestxt) + " de " + str(ano)

def fala_norma_abnp():
    hoje = datetime.datetime.now().date()
    rand = randrange(0, hoje.year * 30)
    ontem = hoje - datetime.timedelta(days=rand)
    return str(ontem.day) + "/" + str(ontem.year)

def fala_abnp():
    lista = []
    full_name = os.path.join("./base/abnp.txt")
    with open(full_name, encoding="utf-8") as file:
        for line in file:
            alinhas = line.split("|")
            for item in alinhas:
                lista.append(item)
    nany = randrange(0, len(lista))
    return lista

def acerto_final(texto):
    texto = texto.replace(".", ".").replace(",", ",").replace("?", "?")
    texto = texto.replace("!", "!").replace(" :", ":").replace("...", "...")
    texto = texto.replace(" -", "-").replace("- ", "-")
    texto = texto.replace(" #", "").replace("#", "")
    if "< pCity >" in texto: texto = texto.replace("< pCity >", fala_cidade_fato())
    if "< pCidadeOficio >" in texto: texto = texto.replace("< pCidadeOficio >", fala_cidade_oficio())
    if "< gCelcius >" in texto: texto = texto.replace("< gCelcius >", fala_celsius())
    if "< pUmido >" in texto: texto = texto.replace("< pUmido >", fala_umidade())
    if "< pAbnp >" in texto: texto = texto.replace("< pAbnp >", fala_abnp())
    if "< dNormas >" in texto: texto = texto.replace("< dNormas >", fala_norma_abnp())
    if "< dPublic >" in texto:
        hoje = datetime.datetime.now().date()
        rand = randrange(0, hoje.year * 30)
        ontem = hoje - datetime.timedelta(days=rand)
        texto = texto.replace("< dPublic >", fala_data(ontem))
    if "< dOficio >" in texto:
        hoje = datetime.datetime.now().date()
        rand = randrange(0, hoje.year * 30)
        demain = hoje + datetime.timedelta(days=rand)
        texto = texto.replace("< dOficio >", fala_data(demain))
    return texto

# --- [ MACHINA DE FAZER POESIA ] ---
def gera_poema(nome_tema, seed_eureka):
    lista_header = []
    lista_linhas = []
    lista_finais = []
    lista_change = []
    lista_duplos = []
    lista_errata = []
    lista_unicos = []
    this_seed = ""
    find_coords = ""
    look_for_seed = False
    if seed_eureka!= "":
        look_for_seed = True
        part_string = seed_eureka.partition(" ➪ ")
        this_seed = part_string[0]
        find_coords = part_string[2]
    nome_tema = nome_tema.strip("\n")
    try:
        if nome_tema == "Babel":
            novo_poema = novo_babel(0)
            return novo_poema
        else:
            tema = abre(nome_tema)
            for line in tema:
                if line.startswith("*", 0, 1):
                    lista_header.append(line)
                elif line.startswith("|", 0, 1):
                    lista_linhas.append(line)
                else:
                    lista_finais.append(line)
    except (UnicodeDecodeError, FileNotFoundError):
        lista_errata.append(nome_tema)
        st.error(f"Arquivo./data/{nome_tema}.ypo não encontrado ou com erro de encoding.")
        return [f"Erro ao abrir tema {nome_tema}"]

    novo_poema = []
    novo_verso = ""
    muda_linha = "00"
    pula_linha = "no"
    find_eureka = ""
    for line in lista_linhas:
        alinhas = line.split("|")
        if len(alinhas) == 0:
            continue
        if len(alinhas) < 2:
            lista_errata.append(nome_tema)
            continue
        if alinhas[2] == "00":
            pula_linha = "si"
            lista_change.append(line)
            continue
        if len(alinhas) >= 7:
            numero_linea = alinhas[1]
            ideia_numero = alinhas[2]
            fonte_itimos = alinhas[3]
            se_randomico = alinhas[4]
            total_itimos = int(alinhas[5])
            itimos_atual = int(alinhas[6])
            array_itimos = alinhas[7 : len(alinhas) - 1]
            tabs = array_itimos[0].count('$')
            if tabs > 0:
                array_itimos = array_itimos[1 : len(array_itimos)]
            find_eureka = nome_tema + "_" + numero_linea + ideia_numero
            if itimos_atual > len(array_itimos):
                itimos_atual = len(array_itimos)
            if total_itimos!= len(array_itimos):
                total_itimos = len(array_itimos)
            if total_itimos == 1:
                se_randomico = "F"
            tentativas = 0
            while True:
                if 1!= total_itimos:
                    if se_randomico == "F":
                        itimos_atual -= 1
                        if itimos_atual < 0:
                            itimos_atual = (total_itimos - 1)
                    else:
                        if total_itimos >= 1:
                            itimos_atual = randrange(0, total_itimos - 1)
                        else:
                            itimos_atual = 0
                else:
                    itimos_atual = 0
                if 0 <= itimos_atual < len(array_itimos):
                    itimo_escolhido = array_itimos[itimos_atual]
                else:
                    st.warning(f"Algo deu errado em {fonte_itimos}. Entre em contato com o [autor](mailto:lopes.fernando@hotmail.com)")
                    itimo_escolhido = "_Erro_"
                if (find_eureka == find_coords):
                    if look_for_seed:
                        for itimo in array_itimos:
                            if this_seed.lower() in itimo.lower():
                                itimo_escolhido = itimo
                                lista_unicos.append(itimo_escolhido.upper())
                                itimo_escolhido = itimo_escolhido.replace(this_seed, "<mark>" + this_seed + "</mark>")
                                look_for_seed = False
                temp_random = se_randomico
                if not itimo_escolhido.upper() in "_E_A_AS_O_OS_NO_NOS_NA_NAS_ME_DE_SE_QUE_NÃO_SO_SEM_NEM_EM_UM_UMA_POR_MEU_VE_TE_TÃO_DA_SER_TER_PRA_PARA_QUANDO_..._._,_:_!_?":
                    if itimo_escolhido.upper() not in lista_unicos:
                        lista_unicos.append(itimo_escolhido.upper())
                        break
                    else:
                        tentativas += 1
                        if tentativas > total_itimos:
                            if temp_random == "T":
                                tentativas = 0
                                temp_random = "F"
                            else:
                                lista_unicos.append(itimo_escolhido.upper())
                                lista_duplos.append(itimo_escolhido.upper())
                                break
                        if itimo_escolhido.upper() in lista_duplos:
                            if len(itimo_escolhido) > 3:
                                continue
                        if tentativas > 30:
                            break
                else:
                    break
            if numero_linea!= muda_linha:
                novo_verso = acerto_final(novo_verso)
                novo_poema.append(novo_verso)
                novo_verso = ""
                muda_linha = numero_linea
            novo_verso += itimo_escolhido + " "
            if tabs > 0:
                novo_verso = tabs*'&emsp;' + novo_verso
                tabs = 0
            if "si" == pula_linha:
                novo_poema.append("\n")
                pula_linha = "no"
            changed_line = ("|" + numero_linea + "|" + ideia_numero + "|" + fonte_itimos + "|")
            if itimos_atual < 1:
                if total_itimos == 1:
                    itimos_atual = 1
                else:
                    itimos_atual = total_itimos
            if se_randomico == "T":
                changed_line += "T"
            else:
                changed_line += "F"
            changed_line += "|" + str(total_itimos) + "|" + str(itimos_atual)
            for v in alinhas[7 : len(alinhas) - 1]:
                changed_line += "|" + v
            changed_line += "|\n"
            lista_change.append(changed_line)
    novo_poema.append(acerto_final(novo_verso))
    if nome_tema == "Nós":
        novo_poema.append("\n")
        novo_poema.append('<a href="https://thispersondoesnotexist.com/" target="_blank">... quem será essa pessoa que não existe?</a>')
    if len(lista_errata) > 0:
        st.warning(f"Algo deu errado com o tema {nome_tema.upper()}. Entre em contato com o [autor](mailto:lopes.fernando@hotmail.com)")
    else:
        try:
            with open(os.path.join("./data/" + nome_tema + ".ypo"), "w", encoding="utf-8") as file:
                for linha in lista_header:
                    file.write(linha)
                for linha in lista_change:
                    file.write(linha)
                for linha in lista_finais:
                    file.write(linha)
        except Exception as e:
            st.warning(f"Não consegui regravar./data/{nome_tema}.ypo: {e}")
    return novo_poema

# --- [ SIDEBAR ] ---
with st.sidebar:
    st.title("yPoemas @ Machina")
    livro = st.selectbox("Escolha o iLivro", lista_livros, key="sb_livro")
    tema = st.selectbox("Escolha o Tema", lista_temas, index=0, key="sb_tema") # Fatos como default
    st.markdown("---")
    idioma = st.selectbox("Idioma do Palco", lista_idiomas, key="sb_idioma")
    seed = st.text_input("Semente Eureka (opcional)", placeholder="Máquina ➪ Fatos_0104")
    gerar = st.button("Gerar yPoema", type="primary", use_container_width=True)

# --- [ PALCO ] ---
st.title(f"📖 {livro}")
st.write(f"**Tema:** {tema} | **Língua:** {idioma}")
st.markdown("---")

with st.container():
    st.subheader("yPoema Gerado:")
    if gerar:
        with st.spinner("A Machina está compondo..."):
            try:
                poema_lista = gera_poema(tema, seed)
                poema_final = "\n".join(poema_lista)
                st.session_state["ultimo_poema"] = poema_final
            except Exception as e:
                st.error(f"Erro na Machina: {e}")
                poema_final = "Erro ao gerar poema."
    else:
        poema_final = st.session_state.get("ultimo_poema", "Clique em 'Gerar yPoema' para começar.")


st.markdown("---")
st.caption("Copyright © 1983-2026 Nando Lopes - Machina de Fazer Poesia")
