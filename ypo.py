import streamlit as st
import os
import random
from PIL import Image

# --- CONFIGURAÇÃO DA NAVE ---
st.set_page_config(page_title="Editora Samizdát", layout="wide", initial_sidebar_state="collapsed")

# --- 1. MOTORES DE BUSCA (A ESTRUTURA DATA) ---

def load_temas(livro):
    """Varre a subpasta do livro dentro de /data e retorna os temas"""
    path = f"./data/{livro}"
    if os.path.exists(path):
        # Lista arquivos .txt, remove a extensão e ignora arquivos ocultos
        return sorted([f.replace(".txt", "") for f in os.listdir(path) if f.endswith(".txt") and not f.startswith('.')])
    return []

def load_poema(tema, livro):
    """Lê o conteúdo do poema dentro de data/livro/tema.txt"""
    path = f"./data/{livro}/{tema}.txt"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "Poema não encontrado no hangar."

def load_arts(tema):
    """Busca a imagem correspondente na pasta /images"""
    extensions = ['.jpg', '.png', '.jpeg', '.webp']
    for ext in extensions:
        img_path = f"./images/{tema}{ext}"
        if os.path.exists(img_path):
            return Image.open(img_path)
    return None

def write_ypoema(texto, imagem=None):
    """A Prensa Samizdát: O texto é a alma, a imagem é o eco"""
    # Estética minimalista: Fonte Courier, limpa e legível
    st.markdown(f"""
        <div style="font-family: 'Courier New', Courier, monospace; font-size: 1.3rem; line-height: 1.6; color: #333; margin-bottom: 2.5rem; text-align: left;">
            {texto.replace('\n', '<br>')}
        </div>
    """, unsafe_allow_html=True)
    
    if imagem:
        st.image(imagem, use_column_width=True)

# --- 2. PÁGINA PRINCIPAL: YPOEMAS ---

def page_ypoemas():
    # Verificação da Raiz de Dados
    if not os.path.exists("./data"):
        st.error("🚨 Pasta /data não encontrada. Verifique o repositório.")
        return

    # Identifica os 13 Rols (Subpastas de /data)
    books_list = sorted([f for f in os.listdir("./data") if os.path.isdir(os.path.join("./data", f)) and not f.startswith('.')])
    
    if not books_list:
        st.warning("Nenhum livro encontrado na pasta /data.")
        return

    # Inicialização do Estado
    if 'book' not in st.session_state: st.session_state.book = books_list[0]
    if 'take' not in st.session_state: st.session_state.take = 0
    if 'draw' not in st.session_state: st.session_state.draw = True

    # --- TETO: SELETOR DE LIVROS ---
    book_sel = st.selectbox("BIBLIOTECA", books_list, index=books_list.index(st.session_state.book), label_visibility="collapsed")
    
    if book_sel != st.session_state.book:
        st.session_state.book = book_sel
        st.session_state.take = 0
        st.rerun()

    temas_list = load_temas(st.session_state.book)
    if not temas_list:
        st.info("Este ROL parece não conter arquivos .txt.")
        return

    # --- COCKPIT: COMANDOS ---
    c1, c2, c3, c4, c5, c_sel = st.columns([0.5, 0.5, 0.5, 0.5, 0.5, 4.5])
    
    with c1: prev = st.button("◀", key="b_prev")
    with c2: rand = st.button("✻", key="b_rand")
    with c3: nxt  = st.button("▶", key="b_next")
    with c4: draw = st.button("✚", key="b_draw", help="Alternar Imagens")
    with c5: help_btn = st.button("?", key="b_help")

    if draw:
        st.session_state.draw = not st.session_state.draw
        st.rerun()

    with c_sel:
        # Seletor de Temas (Radar)
        t_idx = st.selectbox("Radar", range(len(temas_list)), 
                             index=st.session_state.take,
                             format_func=lambda x: temas_list[x].replace("_", " ").title(),
                             label_visibility="collapsed", key="radar_active")

    # Lógica de Navegação
    if t_idx != st.session_state.take:
        st.session_state.take = t_idx
        st.rerun()
    if prev:
        st.session_state.take = (st.session_state.take - 1) % len(temas_list)
        st.rerun()
    if nxt:
        st.session_state.take = (st.session_state.take + 1) % len(temas_list)
        st.rerun()
    if rand:
        st.session_state.take = random.randrange(len(temas_list))
        st.rerun()

    # --- EXECUÇÃO ---
    tema_atual = temas_list[st.session_state.take]
    texto = load_poema(tema_atual, st.session_state.book)
    imagem = load_arts(tema_atual) if st.session_state.draw else None
    
    write_ypoema(texto, imagem)

# --- 3. COMANDO CENTRAL ---

def main():
    st.sidebar.markdown("### 🖋️ Editora Samizdát")
    menu = ["yPoemas", "Eureka", "Mini", "Sobre"]
    choice = st.sidebar.radio("Menu", menu, label_visibility="collapsed")

    if choice == "yPoemas":
        page_ypoemas()
    elif choice == "Eureka":
        st.title("🔍 Sonar Eureka")
        st.write("Em fase de calibração...")
    elif choice == "Mini":
        st.title("📱 Edição Mini")
        st.write("Em fase de montagem...")
    elif choice == "Sobre":
        st.title("📂 Sobre / Acerca")
        st.write("Manifestos e o Ato de Bendita Natureza Textual (A.B.N.T).")

    # Rodapé da Sidebar
    st.sidebar.markdown("---")
    st.sidebar.write("☕ Apoie a Poesia")
    st.sidebar.caption("Links: FB | IG | WA")

if __name__ == "__main__":
    main()
