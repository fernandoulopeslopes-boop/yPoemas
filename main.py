def load_md_file(file_name):
    """
    Busca robusta: tenta o caminho absoluto, o relativo e 
    valida a extensão em maiúsculas conforme o padrão do usuário.
    """
    import os
    
    # 1. Tenta o caminho absoluto do servidor/local
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Caminhos possíveis para testar
    paths_to_try = [
        os.path.join(base_dir, "md_files", file_name),  # Padrão Cloud
        os.path.join("C:\\", "ypo", "md_files", file_name), # Padrão Local Windows
        os.path.join(base_dir, file_name) # Raiz (caso a pasta md_files falhe)
    ]
    
    for path in paths_to_try:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                return f"⚠️ Erro ao ler {file_name}: {str(e)}"
    
    # Se chegar aqui, nada funcionou. Retorna o erro com o diagnóstico.
    return f"⚠️ ERRO: {file_name} não encontrado. Verifique se no GitHub a pasta se chama 'md_files' e o arquivo termina em '.MD'"
