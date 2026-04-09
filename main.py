import streamlit as st
from deep_translator import GoogleTranslator
import re

# --- PROTOCOLO PTC: MANUTENÇÃO DO ESTADO ---
if 'lang' not in st.session_state:
    st.session_state.lang = "pt"
if 'last_lang' not in st.session_state:
    st.session_state.last_lang = "pt"

# --- BLOCO #1: TRADUÇÃO E LIMPEZA ---
def translate(input_text):
    if st.session_state.lang == "pt":
        return input_text

    # Simulação da checagem de internet (conforme seu bloco)
    if not have_internet():
        st.session_state.lang = "pt"
        return input_text

    try:
        output_text = GoogleTranslator(
            source="pt", target=st.session_state.lang
        ).translate(text=input_text)

        # Limpezas manuais específicas (conforme seu bloco #1)
        output_text = output_text.replace("<br>>", "<br>")
        output_text = output_text.replace("< br>", "<br>")
        output_text = output_text.replace("<br >", "<br>")
        output_text = output_text.replace("<br ", "<br>")
        output_text = output_text.replace(" br>", "<br>")
        return output_text
    except:
        return translate("Arquivo muito grande para ser traduzido.")

# --- BLOCO #3: SANITIZAÇÃO PARA VOZ ---
def talk_fala(text):
    # Limpeza para a voz não ler tags (conforme seu bloco #3)
    text_clean = text.replace("<br>", " ").replace("< br>", "").replace("<br >", "").replace("<br/>", " ")
    return text_clean

# --- LÓGICA DE EXIBIÇÃO E FORMATAÇÃO (BLOCO #2 e #4) ---
def formatar_poema(raw_text, dados_tema):
    # Extração de dados para o Bloco #2
    nome_tema, genero, imagem, qtd_versos, qtd_wordin, qtd_lexico, qtd_itimos, qtd_analiz, qtd_cienti = dados_tema
    
    # Bloco #4: Formatação de linhas e &nbsp;
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

    # Bloco #2: Metadados
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

# --- BLOCO #5: GERENCIAMENTO DE CARREGAMENTO (OFF-BOOK) ---
def gerenciar_fluxo(pipe_line):
    off_book_text = ""
    
    if "@ " in pipe_line[1]:
        if st.session_state.lang != st.session_state.last_lang:
            off_book_text = load_lypo()  # Mudança de idioma, mantém LYPO
        else:
            nome_tema = pipe_line[1].replace("@ ", "")
            off_book_text = load_poema(nome_tema, "")
            off_book_text = "<br>" + load_lypo()
    else:
        for text in pipe_line:
            off_book_text += text + "<br>"
            
    return off_book_text

# --- MAIN INTERFACE ---
def main():
    st.sidebar.title("yPoemas - Cockpit")
    # Lógica do seletor de idiomas aqui...
    
    # Exemplo de fluxo de renderização
    # (Aqui entra a integração dos seus processos de geração)
    pass

if __name__ == "__main__":
    main()
