### ... (todo o código anterior permanece igual até o final das funções) ...

# ---------------------------------------------------------
# bof: Navegação Principal (A Chave de Ignição)
# ---------------------------------------------------------

# Sidebar: Configurações e Idioma
pick_lang()
show_icons()
draw_check_buttons()

# Sidebar: Menu de Navegação
st.sidebar.title("Navegação")
menu = ["yPoemas", "Mini", "Eureka", "Leituras"]
escolha = st.sidebar.radio(translate("Ir para:"), menu)

# Chamada das Páginas
if escolha == "yPoemas":
    page_ypoemas()
elif escolha == "Mini":
    page_mini()
elif escolha == "Eureka":
    page_eureka()
elif escolha == "Leituras":
    list_readings()

# Rodapé Técnico Silencioso
if st.sidebar.button("Limpar Cache"):
    st.cache_data.clear()
