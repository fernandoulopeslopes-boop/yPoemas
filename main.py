def main():
    pagina, delay = sidebar_machina()
    
    # 1. Recuperamos o nome do tema (que corresponde ao arquivo em \data)
    # Se a página for 'Mini' ou 'yPoemas', usamos o tema selecionado no session_state
    # Caso contrário, definimos um padrão ou buscamos o tema atual.
    tema_arquivo = st.session_state.get("tema", "Fatos") 

    # 2. Configuração do segundo parâmetro (Exclusivo Eureka)
    seed_param = ""
    if pagina == "Eureka":
        seed_param = st.text_input("Semente ➪ Coords:", value="")
    
    # Controles de repetição
    if pagina in ["Mini", "yPoemas"]:
        st.session_state.auto_run = st.sidebar.checkbox("MODO AUTO", value=st.session_state.auto_run)
        delay = st.sidebar.slider("Intervalo", 5, 60, 15)

    # 3. Chamada correta do Motor
    if st.button(f"Gerar {pagina}") or st.session_state.auto_run:
        with st.spinner(""):
            try:
                # O primeiro parâmetro deve ser o nome do tema que existe em \data
                # O motor vai procurar por f"./data/{tema_arquivo}.ypo"
                resultado = gera_poema(tema_arquivo, seed_param)
                
                if resultado:
                    st.markdown("---")
                    for linha in resultado:
                        st.subheader(linha)
                    st.markdown("---")
                
                if st.session_state.auto_run:
                    time.sleep(delay)
                    st.rerun()

            except Exception:
                st.error("Falha na execução do motor poético.")
                st.code(traceback.format_exc())
