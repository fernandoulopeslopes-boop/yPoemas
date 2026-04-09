import streamlit as st
from deep_translator import GoogleTranslator
import extra_streamlit_components as stx

# --- PROTOCOLO PTC: ESTADO ---
if 'lang' not in st.session_state:
    st.session_state.lang = "pt"
if 'last_lang' not in st.session_state:
    st.session_state.last_lang = "pt"

# --- BLOCO #1: TRADUÇÃO ---
def translate(input_text):
    if st.session_state.lang == "pt":
        return input_text
    try:
        if not have_internet():
            st.session_state.lang = "pt"
            return input_text
    except NameError:
        pass
    try:
        translator = GoogleTranslator(source="pt", target=st.session_state.lang)
        output_text = translator.translate(text=input_text)
        output_text = output_text.replace("<br>>", "<br>").replace("< br>", "<br>").replace("<br >", "<br>").replace("<br ", "<br>").replace(" br>", "<br>")
        return output_text
    except:
        return "Arquivo muito grande para ser traduzido."

# --- BLOCO #3: VOZ ---
def talk_fala(text):
    return text.replace("<br>", " ").replace("< br>", "").replace("<br >", "").replace("<br/>", " ")

# --- BLOCO #2 e #4: FORMATAÇÃO ---
def formatar_poema(raw_text, dados_tema):
    nome_tema, genero, imagem, qtd_versos, qtd_wordin, qtd_lexico, qtd_itimos, qtd_analiz, qtd_cienti = dados_tema
    if raw_text:
        linhas_formatadas = [l.lstrip().strip() if l.lstrip().strip() else "&nbsp;" for l in raw_text.split('\n')]
        texto_formatado = "<br>".join(linhas_formatadas)
    else:
        texto_formatado = "Gerando versos..."
    
    result = f"<br><br><br>Titulo: {nome_tema}<br>Gênero: {genero}  <br>Imagem: {imagem}  <br>Versos: {qtd_versos}  <br>Verbetes no texto: {qtd_wordin}  <br>Verbetes do Tema: {qtd_lexico}  <br>• Banco de Ítimos: {qtd_itimos}  <br>Análise : {qtd_analiz}  <br>Notação Científica: {qtd_cienti}  <br><br>"
    return texto_formatado + result

# --- BLOCO #5: FLUXO ---
def gerenciar_fluxo(pipe_line):
    off_book_text = ""
    if len(pipe_line) > 1 and "@ " in pipe_line[1]:
        if st.session_state.lang != st.session_state.last_lang:
            try: off_book_text = load_lypo()
            except NameError: off_book_text = ""
        else:
            nome_tema = pipe_line[1].replace("@ ", "")
            try:
                off_book_text = gera_poema(nome_tema, "")
                off_book_text = "<br>" + load_lypo()
            except NameError: off_book_text = ""
    else:
        for text in pipe_line:
            off_book_text += text + "<br>"
    return off_book_text

# --- INTERFACE PRINCIPAL ---
def main():
    st.set_page_config(page_title="yPoemas", layout="wide")
    
    # CORREÇÃO STX: Capitalização de TabBarItemData
    chosen_id = stx.tab_bar(
        data=[
            stx.TabBarItemData(id=1, title="mini", description=""),
            stx.TabBarItemData(id=2, title="yPoemas", description=""),
            stx.TabBarItemData(id=3, title="eureka", description=""),
            stx.TabBarItemData(id=4, title="off-machina", description=""),
        ]
    )
    
    # Chame aqui a função que processa a lógica baseada no chosen_id
    # Exemplo: cockpit(chosen_id) ou a lógica linear que você já possuía

if __name__ == "__main__":
    main()
