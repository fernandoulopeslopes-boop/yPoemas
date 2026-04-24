# --- GAMBIARRA TÉCNICA: COMPATIBILIDADE PYTHON 3.13+ ---
import sys
try:
    import cgi
except ImportError:
    from types import ModuleType
    mock_cgi = ModuleType("cgi")
    mock_cgi.parse_header = lambda x: (x, {}) 
    sys.modules["cgi"] = mock_cgi

import streamlit as st
import streamlit_antd_components as sac
import extra_streamlit_components as stx
from googletrans import Translator
from lay_2_ypo import *
import edge_tts
import asyncio
import os
import random
import socket
import time

# --- PROTOCOLO PTC: GO SEGURO ---

# Configuração de Página e Estética
st.set_page_config(page_title="a Máquina de Fazer Poesia", layout="wide", initial_sidebar_state="expanded")

# --- INICIALIZAÇÃO DE ESTADO (SESSION STATE) ---
if "init" not in st.session_state:
    st.session_state.init = True
    st.session_state.book = "livro vivo"
    st.session_state.lang = "pt"
    st.session_state.last_lang = "pt"
    st.session_state.take = 0
    st.session_state.off_book = 0
    st.session_state.off_take = 0
    st.session_state.eureka = 0
    st.session_state.poly_file = "idiomas.json"
    st.session_state.poly_name = "Português"
    st.session_state.poly_lang = "pt"
    st.session_state.poly_take = 0
    st.session_state.draw = False
    st.session_state.talk = False
    st.session_state.vydo = False
    st.session_state.tema = "paz"

# Captura de IP segura
if "user_ip" not in st.session_state:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        st.session_state.user_ip = s.getsockname()[0]
        s.close()
    except Exception:
        st.session_state.user_ip = "127.0.0.1"

# --- FUNÇÕES DE SUPORTE (BACKEND) ---

def translate(text):
    if st.session_state.lang == "pt" or not text:
        return text
    try:
        translator = Translator()
        return translator.translate(text, dest=st.session_state.lang).text
    except Exception:
        return text

def load_md_file(file_name):
    path = os.path.join("./base/", file_name)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def talk(text):
    if not text:
        return
    
    voices_neural = {
        "pt": "pt-BR-AntonioNeural",
        "en": "en-US-GuyNeural",
        "es": "es-ES-AlvaroNeural",
        "it": "it-IT-DiegoNeural",
        "fr": "fr-FR-HenriNeural"
    }
    
    selected_voice = voices_neural.get(st.session_state.lang, "pt-BR-AntonioNeural")

    async def generate_voice():
        clean_text = text.replace("<br>", " ").replace("\n", " ")
        communicate = edge_tts.Communicate(clean_text, selected_voice)
        temp_audio = f"./temp/voice_{st.session_state.user_ip}.mp3"
        await communicate.save(temp_audio)
        return temp_audio

    try:
        audio_file = asyncio.run(generate_voice())
        with open(audio_file, "rb") as f:
            st.audio(f.read(), format="audio/mp3")
    except Exception as e:
        st.error(f"Erro no Neural Talk: {e}")

def show_video(page_name):
    video_path = f"./videos/{page_name}.mp4"
    if os.path.exists(video_path):
        with open(video_path, "rb") as f:
            st.video(f.read())

def write_ypoema(texto, imagem=None):
    col1, col2 = st.columns([6, 4]) if imagem else (st.container(), None)
    with col1:
        st.markdown(f"<div style='font-size:1.2em;'>{texto}</div>", unsafe_allow_html=True)
    if imagem and col2:
        with col2:
            st.image(imagem, use_column_width=True)

# --- PÁGINAS DO APP ---

def page_ypoemas():
    temas_list = load_temas(st.session_state.book)
    maxy = len(temas_list) - 1
    
    if st.session_state.take > maxy or st.session_state.take < 0:
        st.session_state.take = random.randrange(0, maxy) if maxy > 0 else 0

    cols = st.columns([3, 1, 1, 1, 1, 1, 3])
    help_tips = load_help(st.session_state.lang)
    
    if cols[1].button("✚", help=help_tips[4]): pass 
    if cols[2].button("◀", help=help_tips[0]):
        st.session_state.take = maxy if st.session_state.take <= 0 else st.session_state.take - 1
    if cols[3].button("✻", help=help_tips[1]):
        st.session_state.take = random.randrange(0, maxy)
    if cols[4].button("▶", help=help_tips[2]):
        st.session_state.take = 0 if st.session_state.take >= maxy else st.session_state.take + 1
    manu = cols[5].button("?", help="help !!!")

    if not st.session_state.draw:
        opt_take = st.selectbox("↓  lista de Temas", range(len(temas_list)), index=st.session_state.take, 
                                format_func=lambda z: temas_list[z], key="opt_take")
        if opt_take != st.session_state.take:
            st.session_state.take = opt_take

    st.session_state.tema = temas_list[st.session_state.take]

    if manu:
        st.subheader(load_md_file("MANUAL_YPOEMAS.md"))

    if st.session_state.vydo:
        show_video("ypoemas")
        update_readings("video_ypoemas")
        st.session_state.vydo = False
    else:
        what_book = f"⚫ {st.session_state.lang} ( {st.session_state.book} ) ( {st.session_state.take + 1} / {len(temas_list)} )"
        with st.expander(what_book, expanded=True):
            if st.session_state.lang != st.session_state.last_lang:
                curr_ypoema = load_lypo()
            else:
                curr_ypoema = load_poema(st.session_state.tema, "")
                curr_ypoema = load_lypo()

            typo_path = f"./temp/TYPO_{st.session_state.user_ip}"
            with open(typo_path, "w", encoding="utf-8") as f:
                f.write(curr_ypoema)
            
            curr_ypoema = translate(load_typo())
            update_readings(st.session_state.tema)
            
            img = load_arts(st.session_state.tema) if st.session_state.draw else None
            write_ypoema(curr_ypoema, img)

        if st.session_state.talk:
            talk(curr_ypoema)

def page_eureka():
    help_tips = load_help(st.session_state.lang)
    seed, more_btn, rand_btn, manu_btn, occurrences = st.columns([2.5, 1.5, 1.5, 0.7, 4])

    with seed:
        find_what = st.text_input(label=translate("digite algo para buscar..."))

    more = more_btn.button("✚", help=help_tips[4])
    rand = rand_btn.button("✻", help=help_tips[1])
    manu = manu_btn.button("?", help="help !!!")

    if manu:
        st.subheader(load_md_file("MANUAL_EUREKA.md"))

    if len(find_what) >= 3:
        seed_list, soma_tema = [], []
        eureka_list = load_eureka(find_what)
        
        for line in eureka_list:
            palas, _, fonte = line.strip().partition(" : ")
            if palas and fonte:
                seed_list.append(f"{palas} ➪ {fonte}")
                t_name = fonte[0:-5]
                if t_name not in soma_tema: soma_tema.append(t_name)

        if not (more or manu): st.session_state.eureka = 0

        if not seed_list:
            st.warning(translate(f'nenhuma ocorrência de "{find_what}" encontrada...'))
        else:
            seed_list.sort()
            info_find = translate('ocorrência' if len(seed_list) == 1 else 'ocorrências') + f' de "{find_what}"'
            if len(soma_tema) > 1:
                info_find += translate(f'" em {len(soma_tema)} temas')

            if rand:
                st.session_state.eureka = random.randrange(0, len(seed_list))

            with occurrences:
                opt_ocur = st.selectbox(f"↓ {len(seed_list)} {info_find}", range(len(seed_list)), 
                                        index=st.session_state.eureka, format_func=lambda y: seed_list[y])
            
            st.session_state.eureka = opt_ocur
            this_seed = seed_list[st.session_state.eureka]
            seed_tema = this_seed.partition(" ➪ ")[2][0:-5]
            st.session_state.tema = seed_tema

            if st.session_state.lang != st.session_state.last_lang:
                curr_ypoema = load_lypo()
            else:
                curr_ypoema = load_poema(seed_tema, this_seed)
                curr_ypoema = load_lypo()

            curr_ypoema = translate(curr_ypoema)
            with open(f"./temp/TYPO_{st.session_state.user_ip}", "w", encoding="utf-8") as f:
                f.write(curr_ypoema)
            
            if st.session_state.vydo:
                show_video("eureka")
                st.session_state.vydo = False
            else:
                with st.expander("", expanded=True):
                    img = load_arts(seed_tema) if st.session_state.draw else None
                    write_ypoema(curr_ypoema, img)
                    update_readings(seed_tema)
                if st.session_state.talk: talk(curr_ypoema)

def page_off_machina():
    off_books_list = load_all_offs()
    opt_off_book = st.selectbox("↓ " + translate("lista de Livros"), range(len(off_books_list)), 
                                index=st.session_state.off_book, format_func=lambda x: off_books_list[x])

    if opt_off_book != st.session_state.off_book:
        st.session_state.off_book = opt_off_book
        st.session_state.off_take = 0

    off_book_name = off_books_list[st.session_state.off_book]
    help_tips = load_help(st.session_state.lang)
    
    cols = st.columns([2.5, 1, 1, 1, 1, 1, 2.5])
    this_off_book = load_off_book(off_book_name)
    pages = load_book_pages(this_off_book)
    maxy_off = len(pages) - 1

    if cols[1].button("◀", help=help_tips[0]):
        st.session_state.off_take = maxy_off if st.session_state.off_take <= 0 else st.session_state.off_take - 1
    if cols[2].button("✻", help=help_tips[1]):
        st.session_state.off_take = random.randrange(0, maxy_off + 1)
    if cols[3].button("▶", help=help_tips[2]):
        st.session_state.off_take = 0 if st.session_state.off_take >= maxy_off else st.session_state.off_take + 1
    love = cols[4].button("❤", help=help_tips[3])
    manu = cols[5].button("?", help="help !!!")

    if st.session_state.off_take > maxy_off: st.session_state.off_take = 0

    if not st.session_state.draw:
        st.selectbox("↓ " + translate("lista de Títulos"), range(len(pages)), index=st.session_state.off_take, 
                     format_func=lambda x: pages[x], key="opt_off_take_sb")

    if manu: st.subheader(load_md_file("MANUAL_OFF-MACHINA.md"))
    elif love:
        list_readings()
        st.markdown(get_binary_file_downloader_html("./temp/read_list.txt", "views"), unsafe_allow_html=True)
    elif st.session_state.vydo:
        show_video("off-machina")
        st.session_state.vydo = False
    else:
        with st.expander(f"⚫ {st.session_state.lang} ( {st.session_state.off_take + 1}/{len(pages)} )", expanded=True):
            pipe_line = this_off_book[st.session_state.off_take].split("|")
            off_text = ""
            if "@ " in pipe_line[1]:
                t_name = pipe_line[1].replace("@ ", "")
                off_text = "<br>" + (load_poema(t_name, "") if st.session_state.lang == st.session_state.last_lang else load_lypo())
            else:
                off_text = "<br>".join(pipe_line)
            
            if st.session_state.off_take == 0:
                c1, c2 = st.columns([2.5, 7.5])
                img_path = load_arts("livro_vivo") if off_book_name == "livro_vivo" else f"./off_machina/capa_{off_book_name}.jpg"
                c1.image(img_path, use_column_width=True)
                c2.markdown(off_text, unsafe_allow_html=True)
            else:
                off_text = translate(off_text)
                img = load_arts(off_book_name) if st.session_state.draw else None
                write_ypoema(off_text, img)
                update_readings(off_book_name)
            if st.session_state.talk: talk(off_text)

def page_books():
    books_list = ["livro vivo", "poemas", "jocosos", "ensaios", "variações", "metalinguagem", "sociais", "todos os temas", "outros autores", "signos_fem", "signos_mas", "todos os signos"]
    cols = st.columns([9.3, 0.7])
    with cols[0]:
        opt_book = st.selectbox("↓ " + translate("lista de Livros"), range(len(books_list)), 
                                index=books_list.index(st.session_state.book))
    doit = cols[1].button("✔", help="confirm ?")

    if st.session_state.vydo:
        show_video("books")
        st.session_state.vydo = False
    else:
        temas = load_temas(books_list[opt_book])
        st.write(f"{', '.join([t.strip() for t in temas])[:200]}... ▶ {len(temas)} páginas")
        with st.expander("", expanded=True):
            st.subheader(load_md_file("MANUAL_BOOKS.md"))
        if doit:
            st.session_state.take = 0
            st.session_state.book = books_list[opt_book]
            st.rerun()

def page_polys():
    cols = st.columns([9.3, 0.7])
    poly_list, poly_pais, poly_ling = [], [], []
    with open(os.path.join("./base/", st.session_state.poly_file), "r", encoding="utf-8") as f:
        for line in f:
            poly_list.append(line.strip())
            pais, _, ling = line.strip().partition(" : ")
            poly_pais.append(translate(pais))
            poly_ling.append(ling)

    with cols[0]:
        opt_poly = st.selectbox(f"↓ lista: {len(poly_list)} idiomas", range(len(poly_list)), index=st.session_state.poly_take)
    doit = cols[1].button("✔", help="confirm ?")

    if st.session_state.vydo:
        show_video("poly")
        st.session_state.vydo = False
    elif doit:
        st.session_state.poly_name = translate(poly_pais[opt_poly])
        st.session_state.poly_lang = poly_ling[opt_poly]
        st.session_state.poly_take = opt_poly
        st.session_state.last_lang = st.session_state.lang
        st.session_state.lang = st.session_state.poly_lang
        st.rerun()
    
    with st.expander("", expanded=True):
        st.subheader(load_md_file("MANUAL_POLY.md"))

def page_abouts():
    abouts_list = ["comments", "prefácio", "machina", "off-machina", "outros", "traduttore", "bibliografia", "imagens", "samizdát", "notes", "license", "index"]
    opt_abouts = st.selectbox("↓ " + translate("sobre"), range(len(abouts_list)), format_func=lambda x: abouts_list[x])

    if st.session_state.vydo:
        show_video("about")
        st.session_state.vydo = False
    else:
        choice = abouts_list[opt_abouts].upper()
        with st.expander("", expanded=True):
            if choice == "MACHINA":
                st.subheader(load_md_file("ABOUT_MACHINA_A.md"))
                write_ypoema(load_info(st.session_state.tema), f"./images/matrix/{st.session_state.tema}.jpg")
                st.subheader(load_md_file("ABOUT_MACHINA_D.md"))
            else:
                st.subheader(load_md_file(f"ABOUT_{choice}.md"))

def page_mini():
    st.subheader(load_md_file("ABOUT_MINI.md"))

# --- MAIN ---

def main():
    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id=1, title="mini", description=""),
        stx.TabBarItemData(id=2, title="yPoemas", description=""),
        stx.TabBarItemData(id=3, title="eureka", description=""),
        stx.TabBarItemData(id=4, title="off-machina", description=""),
        stx.TabBarItemData(id=5, title="books", description=""),
        stx.TabBarItemData(id=6, title="poly", description=""),
        stx.TabBarItemData(id=7, title="about", description=""),
    ], default=2)

    # Nota: Assumindo que funções como pick_lang() e show_icons() 
    # estão em módulos importados ou no yPoemas original.
    
    pages = {
        "1": ("INFO_MINI.md", "img_mini.jpg", page_mini),
        "2": ("INFO_YPOEMAS.md", "img_ypoemas.jpg", page_ypoemas),
        "3": ("INFO_EUREKA.md", "img_eureka.jpg", page_eureka),
        "4": ("INFO_OFF-MACHINA.md", "img_off-machina.jpg", page_off_machina),
        "5": ("INFO_BOOKS.md", "img_books.jpg", page_books),
        "6": ("INFO_POLY.md", "img_poly.jpg", page_polys),
        "7": ("INFO_ABOUT.md", "img_about.jpg", page_abouts)
    }

    info_file, img_side, func = pages.get(chosen_id, pages["2"])
    st.sidebar.info(load_md_file(info_file))
    with st.sidebar:
        st.image(img_side)
    
    func()

if __name__ == "__main__":
    main()
