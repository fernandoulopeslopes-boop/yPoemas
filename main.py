def load_md_file(file_name):
    """
    Motor de busca v.33.9. 
    Correção de Syntax: Parênteses fechados e caminhos robustos.
    """
    import os
    
    # 1. Âncora de Diretório (Cloud)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path_cloud = os.path.join(base_dir, "md_files", file_name)
    
    # 2. Âncora Local (Windows)
    # Verificação de existência da pasta pai para decidir o ambiente
    if os.path.exists(r"C:\ypo"):
        target = os.path.join(r"C:\ypo\md_files", file_name)
    else:
        target = path_cloud
    
    # 3. TENTATIVA DE LEITURA
    if os.path.exists(target):
        try:
            with open(target, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"⚠️ Erro ao abrir: {str(e)}"
    
    # 4. DIAGNÓSTICO (Caso o arquivo não exista no alvo)
    try:
        itens_raiz = os.listdir(base_dir)
        debug_msg = f"⚠️ ARQUIVO NÃO ENCONTRADO: {file_name}\n\n"
        debug_msg += f"Procurado em: {target}\n"
        if "md_files" in itens_raiz:
            debug_msg += f"Conteúdo da /md_files: {os.listdir(os.path.join(base_dir, 'md_files'))}"
        else:
            debug_msg += f"Estrutura na Raiz: {itens_raiz}"
        return debug_msg
    except:
        return f"⚠️ {file_name} inacessível."
