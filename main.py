# --- 1. GÊNESE (ESTADOS) ---
if 'page' not in st.session_state: 
    st.session_state.page = "mini"

if 'book' not in st.session_state: 
    st.session_state.book = "todos os temas"

if 'take' not in st.session_state: 
    st.session_state.take = 0

if 'tema' not in st.session_state: 
    st.session_state.tema = ""

if 'lang' not in st.session_state: 
    st.session_state.lang = "pt"

if 'last_lang' not in st.session_state: 
    st.session_state.last_lang = "pt"

if 'arts' not in st.session_state: 
    st.session_state.arts = []

if 'draw' not in st.session_state: 
    st.session_state.draw = True

if 'talk' not in st.session_state: 
    st.session_state.talk = False

if 'vydo' not in st.session_state: 
    st.session_state.vydo = False
