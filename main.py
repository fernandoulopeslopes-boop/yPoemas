# change padding and fix layout overlap
st.markdown(
    """
    <style>
    /* 1. Garante que o conteúdo principal não seja invadido pela sidebar */
    .main .block-container {
        padding-top: 1rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 1rem;
        max-width: 800px; /* Mantém o palco centrado e protegido */
        margin: auto;
    }

    /* 2. Ajuste fixo da Sidebar para evitar que ela 'empurre' o centro */
    [data-testid="stSidebar"] {
        min-width: 310px;
        max-width: 310px;
    }

    /* 3. Estabilização do palco centrado na área-mãe */
    section[data-testid="stSidebar"] + section {
        margin-left: 0px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
