import streamlit as st
import os

# --- MOTOR DE BUSCA (ESTÁVEL) ---

def load_md_file(file_name):
    """Localiza e lê arquivos na pasta md_files."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    folder = r"C:\ypo\md_files" if os.path.exists(r"C:\ypo") else os.path.join(base_dir, "md_files")
    
    target_upper = file_name.upper()
    if os.path.exists(folder):
        try:
            for arquivo in os.listdir(folder):
                if arquivo.upper() == target_upper:
                    with open(os.path.join(folder, arquivo), "r", encoding="utf-8") as f:
                        return f.read()
        except Exception as e:
            return f"⚠️ Erro: {str(e)}"
    return f"⚠️ {target_upper} não localizado."

# --- MOTOR PRINCIPAL ---

def main():
    st.set_page_config(
        page_title="yPoemas",
        layout="wide"
    )

    # Estilização dos botões redondos/suaves para sub-navegação
    st.markdown("""
        <style>
        div.stButton > button {
            border-radius: 20px;
            background-color: rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(0, 0, 0, 0.1);
            padding: 5px 15px;
        }
        [data-testid="stSidebar"] {
            min-width: 300px;
            max-width: 300px;
        }
        </style>
    """, unsafe_allow_html=True)

    # 1. PALCO: NAVEGAÇÃO SUPERIOR (PÁGINAS)
    tabs = ["Demo", "yPoemas", "Eureka", "Off-Machina", "Comments", "About"]
    tab_objs = st.tabs(tabs)

    # Determinar qual tab está ativa para atualizar a Sidebar
    # Nota: Streamlit não retorna o índice da tab nativamente de forma simples, 
    # então usamos a lógica de renderização para definir o contexto.

    # 2. RENDERIZAÇÃO DO CONTEÚDO E DEFINIÇÃO DO CONTEXTO
    for i, tab in enumerate(tab_objs):
        with tab:
            nome_pagina = tabs[i]
            if nome_pagina == "About":
                col1, col2, col3, col4 = st.columns(4)
                if col1.button("Prefácio"): st.session_state.sub = "prefácio"
                if col2.button("Machina"): st.session_state.sub = "machina"
                if col3.button("Imagens"): st.session_state.sub = "imagens"
                if col4.button("Index"): st.session_state.sub = "index"
                sub = st.session_state.get('sub', 'prefácio')
                st.markdown(load_md_file(f"ABOUT_{sub.upper()}.MD"))
                current_page = nome_pagina
            else:
                st.markdown(load_md_file(f"MANUAL_{nome_pagina.upper()}.MD") if nome_pagina != "Demo" else load_md_file("INFO_DEMO.MD"))
                current_page = nome_pagina

    # 3. SIDEBAR (CONTEÚDO DINÂMICO)
    with st.sidebar:
        # Idiomas no topo
        idiomas_abc = [
            "Português", "Español", "English", "Français", "Italiano", "Deutsch",
            "Català", "Galego", "Latin", "Română"
        ]
        st.selectbox("🌐 IDIOMA", options=idiomas_abc)
        st.divider()

        # Arte da página (Substituir pelo caminho real das suas imagens)
        # st.image(f"assets/arte_{current_page.lower()}.png") 
        st.write(f"🎨 [ARTE: {current_page.upper()}]")
        
        st.divider()

        # INFO_PAGINA (Carregado da pasta md_files)
        info_content = load_md_file(f"INFO_{current_page.upper()}.MD")
        st.markdown(info_content)

        st.divider()

        # Contatos na rede
        st.markdown("### Contatos")
        st.markdown("🌐 [GitHub](https://github.com/)")
        st.markdown("✉️ [Email](mailto:contato@exemplo.com)")

if __name__ == "__main__":
    main()
