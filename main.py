# --- NAVEGAÇÃO (SUBSTITUINDO OS RADIO BUTTONS INTRUSOS) ---
# Em vez de st.radio, usamos botões diretos para o Portal ficar limpo.

if "page" not in st.session_state:
    st.session_state.page = "yPoemas"

c1, c2, c3 = st.sidebar.columns(3)
if c1.button("Mini"): st.session_state.page = "Mini"
if c2.button("yPoemas"): st.session_state.page = "yPoemas"
if c3.button("Eureka"): st.session_state.page = "Eureka"

st.sidebar.write("---")

# --- LÓGICA DE EXIBIÇÃO ---
if st.session_state.page == "yPoemas":
    page_ypoemas()
elif st.session_state.page == "Mini":
    page_mini()
elif st.session_state.page == "Eureka":
    st.info("Página Eureka em construção.")
