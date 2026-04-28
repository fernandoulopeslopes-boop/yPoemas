import streamlit as st
import os
import random
import time
import base64
import edge_tts as gTTS

# from gtts import gTTS

# Nota: Certifique-se de que suas funções personalizadas (translate, gera_poema, etc.) 
# estejam acessíveis ou importadas aqui se estiverem em outro arquivo.

# --- ESTILIZAÇÃO MÍNIMA E SEGURA ---
st.set_page_config(page_title="a Machina de Fazer Poesia", layout="wide")

# --- FUNÇÕES DE CARREGAMENTO (LOADERS) ---

def translate(input_text):
    if st.session_state.lang == "pt":  # don't need translations here
        return input_text

    if not have_internet():
        st.session_state.lang = "pt"
        return input_text

    try:
        output_text = GoogleTranslator(
            source="pt", target=st.session_state.lang
        ).translate(text=input_text)

        output_text = output_text.replace("<br>>", "<br>")
        output_text = output_text.replace("< br>", "<br>")
        output_text = output_text.replace("<br >", "<br>")
        output_text = output_text.replace("<br ", "<br>")
        output_text = output_text.replace(" br>", "<br>")
        return output_text
    except:
        return translate("Arquivo muito grande para ser traduzido.")

@st.cache_data
def load_temas(book):
    book_list = []
    path = os.path.join("./base/rol_" + book + ".txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.replace(" ", "")
                book_list.append(line.strip("\n"))
    return translate(book_list)

@st.cache_data
def load_info(nome_tema):
    path = os.path.join("./base/info.txt")
    result = "nonono"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("|"):
                    pipe = line.split("|")
                    if pipe[1].upper() == nome_tema.upper():
                        genero, imagem, qtd_versos = pipe[2], pipe[3], pipe[4]
                        qtd_wordin, qtd_lexico, qtd_itimos = pipe[5], pipe[6], pipe[7]
                        qtd_analiz, qtd_cienti = pipe[8], pipe[9]
                        result = f"<br><br>Titulo: {nome_tema}<br>Gênero: {genero}<br>Versos: {qtd_versos}<br>"
                        result += f"Verbetes no texto: {qtd_wordin}<br>Verbetes do Tema: {qtd_lexico}<br>"
                        result += f"Banco de Ítimos: {qtd_itimos}<br>Análise: {qtd_analiz}<br>Notação: {qtd_cienti}<br>"
    return translate(result)

@st.cache_data
def load_index():
    index_list = []
    path = "./md_files/ABOUT_INDEX.md"
    if os.path.exists(path):
        with open(path, encoding="utf-8") as lista:
            for line in lista:
                index_list.append(line)
    return index_list

def load_lypo():
    lypo_text = ""
    path = os.path.join("./temp/LYPO_" + IPAddres)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as script:
            for line in script:
                lypo_text += line.strip() + "<br>"
    return lypo_text

def load_typo():
    typo_text = ""
    path = os.path.join("./temp/TYPO_" + IPAddres)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as script:
            for line in script:
                line = line.strip()
                line = line.replace(" >", "\n").replace("< ", "\n").replace(" br", "\n").replace("br ", "\n")
                line = line.replace("< <", ">").replace("> >", ">")
                typo_text += line + "<br>"
    return typo_text

def load_all_offs():
    return ["a_torre_de_papel", "livro_vivo", "quase_que_eu_Poesia", "faz_de_conto", "essencial", "desvoto", "um_romance", "linguafiada", "secreto"]

def load_off_book(book):
    book_full = []
    full_name = os.path.join("./off_machina/", book) + ".Pip"
    if os.path.exists(full_name):
        with open(full_name, encoding="utf-8") as file:
            for line in file:
                if line.startswith("|"):
                    book_full.append(line)
    return translate(book_full)

def load_book_pages(book_lines):
    book_pages = []
    for line in book_lines:
        if line.startswith("<EOF>"): break
        if line.startswith("|"):
            book_pages.append(line.split("|")[1])
    return translate(book_pages)

def gera_poema(nome_tema, seed_eureka):
#    script = gera_poema(nome_tema, seed_eureka)
    novo_ypoema = ""
    path = os.path.join("./temp/LYPO_" + IPAddres)
    if not os.path.exists("./temp"): os.makedirs("./temp")
    with open(path, "w", encoding="utf-8") as save_lypo:
        save_lypo.write(nome_tema + "\n")
        for line in script:
            save_lypo.write(line + "\n")
            novo_ypoema += line + "<br>"
    return translate(novo_ypoema)

def load_arts(nome_tema):
    path = "./images/machina/"
    images_txt = os.path.join("./base/images.txt")
    if os.path.exists(images_txt):
        with open(images_txt, encoding="utf-8") as lista:
            for line in lista:
                if line.startswith(nome_tema):
                    part = line.strip().partition(" : ")
                    if nome_tema == part[0]:
                        path = "./images/" + part[2] + "/"
                        break
    
    if os.path.exists(path):
        arts_list = [f for f in os.listdir(path) if f.endswith(".jpg")]
        if arts_list:
            image = random.choice(arts_list)
            if image in st.session_state.arts:
                st.session_state.arts.append(image)
            else:
                st.session_state.arts.append(image)
            if len(st.session_state.arts) > 36: del st.session_state.arts[0]
            return path + image
    return None

# --- FUNÇÕES DE INTERFACE (OUTPUT) ---

def write_ypoema(LOGO_TEXTO, LOGO_IMAGE):
    if LOGO_IMAGE and os.path.exists(LOGO_IMAGE):
        with open(LOGO_IMAGE, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""<div style='text-align:center'>
            <img src='data:image/jpg;base64,{data}' style='max-width:100%; border-radius:10px;'>
            <div style='text-align:left; font-size:18px; margin-top:15px;'>{LOGO_TEXTO}</div>
            </div>""", unsafe_allow_html=True
        )
    else:
        st.markdown(f"<div>{LOGO_TEXTO}</div>", unsafe_allow_html=True)

def talk(text):
    try:
        clean = text.replace("<br>", "\n").replace("< br>", "").replace("<br >", "")
        tts = gTTS(text=clean, lang=st.session_state.lang, slow=False)
        filename = f"./temp/audio_{random.randint(1, 10000)}.mp3"
        if not os.path.exists("./temp"): os.makedirs("./temp")
        tts.save(filename)
        st.audio(filename)
        os.remove(filename)
    except: pass

def say_number(tema):
    analise = "nonono"
    indexes = load_index()
    for line in indexes:
        if line.startswith(tema):
            analise = line.strip().partition(" : ")[2]
            break
    return translate(analise)

# --- PÁGINAS ---

def page_mini():
    temas_list = load_temas("todos os temas")
    maxy = len(temas_list)
    cols = st.columns([4, 1, 1, 1, 4])
    if cols[2].button("✻"): 
        st.session_state.mini = random.randrange(0, maxy)
    st.session_state.auto = cols[3].checkbox("auto")
    
    wait_time = 10
    if st.session_state.auto:
        wait_time = st.sidebar.slider(translate("Segundos:"), 5, 60, 10)

    placeholder = st.empty()
    while True:
        st.session_state.tema = temas_list[st.session_state.mini % maxy]
        curr = load_poema(st.session_state.tema, "")
        with placeholder.container():
            write_ypoema(curr, load_arts(st.session_state.tema) if st.session_state.draw else None)
        if not st.session_state.auto: break
        time.sleep(wait_time)
        st.session_state.mini = random.randrange(0, maxy)
        st.rerun()

def page_ypoemas():
    temas_list = load_temas(st.session_state.book)
    maxy = len(temas_list) - 1
    cols = st.columns([3, 1, 1, 1, 1, 1, 3])
    if cols[2].button("◀"): st.session_state.take = (st.session_state.take - 1) % maxy
    if cols[3].button("✻"): st.session_state.take = random.randint(0, maxy)
    if cols[4].button("▶"): st.session_state.take = (st.session_state.take + 1) % maxy
    
    st.session_state.tema = temas_list[st.session_state.take]
    with st.expander(f"⚫ {st.session_state.lang} - {st.session_state.tema}", expanded=True):
        curr = load_poema(st.session_state.tema, "")
        write_ypoema(curr, load_arts(st.session_state.tema) if st.session_state.draw else None)
    if st.session_state.talk: talk(curr)

def page_eureka():
    find_what = st.text_input(translate("Buscar..."))
    if len(find_what) >= 3:
        eureka_list = load_eureka(find_what)
        seeds = [l.strip().replace(" : ", " ➪ ") for l in eureka_list if " : " in l]
        if seeds:
            st.session_state.eureka = st.selectbox(f"Ocorrências: {len(seeds)}", range(len(seeds)), format_func=lambda x: seeds[x])
            tema = seeds[st.session_state.eureka].partition(" ➪ ")[2].replace(".txt", "")
            write_ypoema(load_poema(tema, seeds[st.session_state.eureka]), load_arts(tema) if st.session_state.draw else None)
        else: st.warning("Nada encontrado.")

def page_off_machina():
    offs = load_all_offs()
    idx = st.selectbox(translate("Livro Off"), range(len(offs)), format_func=lambda x: offs[x])
    book_lines = load_off_book(offs[idx])
    pages = load_book_pages(book_lines)
    st.session_state.off_take = st.select_slider("Página", options=range(len(pages)), value=st.session_state.off_take % len(pages))
    content = book_lines[st.session_state.off_take].replace("|", "<br>")
    write_ypoema(translate(content), load_arts(offs[idx]) if st.session_state.draw else None)

def page_books():
    books = ["todos os temas", "livro vivo", "poemas", "ensaios", "jocosos", "sociais"]
    sel = st.selectbox("Escolha o Livro", books, index=books.index(st.session_state.book))
    if st.button("Confirmar"):
        st.session_state.book = sel
        st.session_state.take = 0
        st.rerun()

def page_polys():
    # Carrega idiomas do arquivo base de forma bruta e segura
    if os.path.exists("./base/poly.txt"):
        with open("./base/poly.txt", "r", encoding="utf-8") as f:
            langs = [l.strip() for l in f]
        sel = st.selectbox("Idioma", range(len(langs)), format_func=lambda x: langs[x])
        if st.button("Trocar"):
            st.session_state.lang = langs[sel].split(" : ")[1]
            st.rerun()

def page_abouts():
    abouts = ["comments", "prefácio", "machina", "bibliografia", "license", "index"]
    choice = st.selectbox("Sobre", abouts)
    st.markdown(load_md_file(f"ABOUT_{choice.upper()}.md"))

# --- MAIN ---

def main():
    if st.session_state.visy:
        #update_visy()
        st.session_state.visy = False

    # Menu lateral padrão Streamlit (evita quebra de bibliotecas externas)
    with st.sidebar:
        st.title("Cockpit")
        page = st.radio("Navegação", ["mini", "yPoemas", "eureka", "off-machina", "books", "poly", "about"])
        st.session_state.draw = st.checkbox("Imagens", st.session_state.draw)
        st.session_state.talk = st.checkbox("Voz", st.session_state.talk)
        
        img_map = {"mini": "mini", "yPoemas": "ypoemas", "eureka": "eureka", "off-machina": "off-machina", "books": "books", "poly": "poly", "about": "about"}
        st.image(f"./images/img_{img_map[page]}.jpg")

    if page == "mini": page_mini()
    elif page == "yPoemas": page_ypoemas()
    elif page == "eureka": page_eureka()
    elif page == "off-machina": page_off_machina()
    elif page == "livros": page_books()
    elif page == "poly": page_polys()
    elif page == "sobre": page_abouts()

if __name__ == "__main__":
    # Inicialização de Session State
    for key, val in {'book': 'todos os temas', 'take': 0, 'mini': 0, 'off_book': 0, 'off_take': 0, 
                     'lang': 'pt', 'draw': True, 'talk': False, 'visy': True, 'eureka': 0, 'arts': []}.items():
        if key not in st.session_state: st.session_state[key] = val
    
    # Placeholder global para variáveis de IP se necessário
    if 'IPAddres' not in globals(): IPAddres = "local_user"
    
    main()
    
