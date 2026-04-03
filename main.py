def carregar_poesia_real(tema, id_seed):
    try:
        # Tenta rodar a sua engine original
        script = gera_poema(tema, id_seed)
        return "<br>".join([line.strip() for line in script if line.strip() != ""])
    except Exception as e:
        # Isso vai mostrar na tela o erro real (ex: FileNotFoundError ou ImportError)
        return f"Erro na Engine: {str(e)}"
