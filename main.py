# ... (manter imports e inicialização de estados)

# Regra 0: Look & Feel (Ajuste para Palco Fluido)
st.markdown(
    """ <style>
    footer {visibility: hidden;}
    
    /* FORÇAR O PALCO A ACOMPANHAR A SIDEBAR */
    .main .block-container { 
        max-width: 95% !important;  /* Deixa uma pequena margem de respiro nas bordas */
        padding-top: 1.5rem; 
        padding-left: 2rem;
        padding-right: 2rem;
        transition: max-width 0.3s ease; /* Suaviza a transição */
    }
    
    /* Blindagem contra Fullscreen e Toolbar */
    [data-testid="stImage"] button, [data-testid="stElementToolbar"] { display: none !important; }
    [data-testid="stImage"] img { pointer-events: none; }

    /* Sidebar 240px */
    [data-testid="stSidebar"] { 
        width: 240px !important; 
        min-width: 240px !important;
        background-color: #fafafa; 
    }
    
    /* ... (manter o restante do CSS de botões e cabeçalhos) */
    
    div.stButton > button {
        width: 116px !important; 
        border-radius: 12px; 
        height: 3.2em;
        background-color: #ffffff; 
        border: 1px solid #d1d5db; 
        font-size: 12px;
    }
    div.stButton > button:hover { border-color: powderblue; color: powderblue; }
    </style> """,
    unsafe_allow_html=True,
)

# ... (manter o restante do código da sidebar e navegação)
