import streamlit as st
from deep_translator import GoogleTranslator
import extra_streamlit_components as stx # Para os componentes extras (seletor de abas, etc.)

# --- PROTOCOLO PTC: MANUTENÇÃO DO ESTADO ---
if 'lang' not in st.session_state:
    st.session_state.lang = "pt"
if 'last_lang' not in st.session_state:
    st.session_state.last_lang = "pt"

# --- BLOCO #1: TRADUÇÃO E LIMPEZA ---
def translate(input_text):
    if st.session_state.lang == "pt":
        return input_text

    # Verifica internet (presumindo existência da função no seu escopo)
    try:
        if not have_internet():
            st.session_state.lang = "pt"
            return input_text
    except NameError:
        pass

    try:
        translator = GoogleTranslator(source="pt", target=st.session_state.lang)
        output_text = translator.translate(text=input_text)

        # Limpezas manuais conforme bloco #1
        output_text = output_text.replace("<br>>", "<br>")
        output_text = output_text.replace("< br>", "<br>")
        output_text = output_text.replace("<br >", "<br>")
        output_text = output_text.replace("<br ", "<br>")
        output_text = output_text.replace(" br>", "<br>")
        return output_text
    except:
        return "Arquivo muito grande para ser traduzido."

# --- BLOCO #3: SANITIZAÇÃO PARA VOZ ---
def talk_fala(text):
    # Limpeza para a voz não ler tags (conforme bloco #3)
    text_clean = text.replace("<br>", " ").replace("< br>", "").replace("<br >", "").replace("<br/>", " ")
    return text_clean

# --- BLOCO #2 e #4: FORMATAÇÃO ---
def formatar_poema(raw_text, dados_tema):
    nome_tema, genero, imagem, qtd_versos, qtd_wordin, qtd_lexico, qtd_itimos, qtd_analiz, qtd_cienti = dados_tema
    
    if raw_text:
        linhas_formatadas = []
        for l in raw_text.split('\n'):
            linha_limpa = l.lstrip().strip()
            if not linha_limpa:
                linhas_formatadas.append("&nbsp;")
            else:
                linhas_formatadas.append(linha_limpa)
        texto_formatado = "<br>".join(linhas_formatadas)
    else:
        texto_formatado = "Gerando versos..."

    # Construção do Bloco #2
    result = "<br><br><br>"
    result += "Titulo: " + nome_tema + "<br>"
    result += "Gênero: " + genero + "  " + "<br>"
    result += "Imagem: " + imagem + "  " + "<br>"
    result += "Versos: " + qtd_versos + "  " + "<br>"
    result += "Verbetes no texto: " + qtd_wordin + "  " + "<br>"
    result += "Verbetes  do Tema: " + qtd_lexico + "  " + "<br>"
    result += "• Banco de Ítimos: " + qtd_itimos + "  " + "<br>"
    result += "Análise : " + qtd_analiz + "  " + "<br>"
    result += "Notação Científica: " + qtd_cienti + "  " + "<br>"
    result += "<br>"
    
    return texto_formatado + result

# --- BLOCO #5: FLUXO OFF-BOOK ---
def gerenciar_fluxo(pipe_line):
    off_book_text = ""
    
    if len(pipe_line) > 1 and "@ " in pipe_line[1]:
        if st.session_state.lang != st.session_state.last_lang:
            try:
                off_book_text = load_lypo()
            except NameError:
                off_book_text = ""
        else:
            nome_tema = pipe_line[1].replace("@ ", "")
            try:
                off_book_text = gera_poema(nome_tema, "")
                off_book_text = "<br>" + load_lypo()
            except NameError:
                off_book_text = ""
    else:
        for text in pipe_line:
            off_book_text += text + "<br>"
            
    return off_book_text

# --- INTERFACE ---
def main():
    chosen_id = stx.tab_bar(
        data=[
            stx.tabBarItemData(id=1, title="mini", description=""),
            stx.tabBarItemData(id=2, title="yPoemas", description=""),
            stx.tabBarItemData(id=3, title="eureka", description=""),
            stx.tabBarItemData(id=4, title="off-machina", description=""),
            stx.tabBarItemData(id=5, title="books", description=""),
            stx.tabBarItemData(id=6, title="poly", description=""),
            stx.tabBarItemData(id=7, title="about", description=""),
        ],
        default=2,
    )

    pick_lang()
    draw_check_buttons()

    if chosen_id == "1":
        st.sidebar.info(load_md_file("INFO_MINI.md"))
        magy = "img_mini.jpg"
        page_mini()
    elif chosen_id == "2":
        st.sidebar.info(load_md_file("INFO_YPOEMAS.md"))
        magy = "img_ypoemas.jpg"
        page_ypoemas()
    elif chosen_id == "3":
        st.sidebar.info(load_md_file("INFO_EUREKA.md"))
        magy = "img_eureka.jpg"
        page_eureka()
    elif chosen_id == "4":
        st.sidebar.info(load_md_file("INFO_OFF-MACHINA.md"))
        magy = "img_off-machina.jpg"
        page_off_machina()
    elif chosen_id == "5":
        st.sidebar.info(load_md_file("INFO_BOOKS.md"))
        magy = "img_books.jpg"
        page_books()
    elif chosen_id == "6":
        st.sidebar.info(load_md_file("INFO_POLY.md"))
        magy = "img_poly.jpg"
        page_polys()
    elif chosen_id == "7":
        st.sidebar.info(load_md_file("INFO_ABOUT.md"))
        magy = "img_about.jpg"
        page_abouts()
        ##$ page_docs()

    with st.sidebar:
        st.image(magy)

    show_icons()
    ##$ st.sidebar.state = True

if __name__ == "__main__":
    main()
