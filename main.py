import streamlit as st
import extra_streamlit_components as stx
import random
import os

# --- CONFIGURAÇÃO DE CAMINHOS ---
PATH_DATA = "data"          # Onde residem os arquivos .ypo (ítimos)
PATH_MD = "md_files"
PATH_BASE = "base"
PATH_OFF = "off-maquina"

# --- MOTOR DE CARREGAMENTO NOBRE ---
def get_md(file_name):
    path = os.path.join(PATH_MD, file_name)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    return f"Manual {file_name} não localizado."

def get_rol(book_name):
    file_name = f"rol_{book_name}.txt" if not book_name.startswith("rol_") else f"{book_name}.txt"
    path = os.path.join(PATH_BASE, file_name)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return [l.strip() for l in f if l.strip() and not l.startswith("[")]
    return []

def parse_ypo_line(line):
    """
    Extrai o conteúdo da 7ª coluna de uma linha .ypo (ítimo).
    Exemplo: |01|01|Amaré_0101|F|1|1|O amor, o que é?| -> 'O amor, o que é?'
    """
    parts = line.split('|')
    if len(parts) >= 8:
        return parts[7].strip()
    return None

def get_verso_by_lexico(tema, seed):
    """
    Busca o verso exato em arquivos .ypo baseado no endereçamento interno.
    """
    path = os.path.join(PATH_DATA, f"{tema}.ypo")
    if not os.path.exists(path):
        return f"Arquivo {tema}.ypo não encontrado em {PATH_DATA}."
    
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        # Filtra apenas linhas que seguem o padrão |00|00|...
        linhas_validas = [l.strip() for l in f if l.startswith('|')]
        
        if seed:
            # Procura a linha que contém a seed exata (ex: Amaré_0101) na 3ª coluna
            for l in linhas_validas:
                parts = l.split('|')
                if len(parts) >= 4 and parts[3].strip() == f"{tema}_{seed}":
                    return parse_ypo_line(l)
        
        # Fallback: Escolha aleatória entre as linhas de conteúdo real
        # Filtra linhas vazias de metadados como |02|00|
        conteudo_real = [parse_ypo_line(l) for l in linhas_validas if parse_ypo_line(l)]
        return random.choice(conteudo_real) if conteudo_real else "Ítimo não localizado."

# --- PÁGINAS ---
def page_eureka():
    st.subheader("🔍 Busca Eureka")
    query = st.text_input("Verbete:").strip().lower()
    path_lexico = os.path.join(PATH_BASE, "lexico.txt")
    
    if len(query) >= 3 and os.path.exists(path_lexico):
        hits = []
        with open(path_lexico, "r", encoding="utf-8", errors="ignore") as f:
            for linha in f:
                if ":" in linha and query in linha.lower():
                    parts = linha.split(":")
                    verbete = parts[0].strip()
                    endereco = parts[1].strip() # Ex: Amaré_0101
                    if "_" in endereco:
                        t, s = endereco.split("_")
                        hits.append({"v": verbete, "t": t, "s": s})
        
        if hits:
            sel = st.selectbox(f"Encontrados: {len(hits)}", range(len(hits)),
                               format_func=lambda i: f"« {hits[i]['v']} » em {hits[i]['t']} ({hits[i]['s']})")
            h = hits[sel]
            txt = get_verso_by_lexico(h['t'], h['s'])
            if txt:
                st.markdown(f"**{h['t'].upper()}**")
                st.markdown(f"### {txt.replace(query, f' « {query} » ')}")

# --- (Restante das funções page_mini, page_ypoemas seguem a mesma lógica de get_verso_by_lexico) ---

def main():
    # ... (lógica de Tab Bar e Sidebar idêntica à anterior, chamando as novas funções de .ypo)
    pass

if __name__ == "__main__":
    main()
