
import os
import time

'''
    Função para padronizar arquivos '.dip' == documentação dos yPoemas
    Salvar como md_file
'''

def search (lista, valor):
    return [(lista.index(x), x.index(valor)) for x in lista if valor in x]

def build_docs():
    start_time = time.time()
    list_docs = []
    for file in os.listdir( './docs' ):
        if file.lower().endswith( '.dip' ):
            file = os.path.join( './docs', file )
            list_docs.append( file )

    for script in list_docs:  # iterate all files.dip
        changed = []
        with open( script, encoding='ansi') as file:  # iterate file line by line
            path = os.path.basename( script )
            os.path.splitext( path )
            tabela = os.path.splitext( path )[0]

            for line in file:  # append '  ' for new_file.md
                line = line.strip() + '  ' + '\n'
                changed.append(line)

        # rebuild file
        with open(os.path.join('./docs/' + tabela + '.md'), 'w', encoding = 'utf-8') as new_doc:
            for line in changed:
                new_doc.write(line)

            new_doc.write("---" + '\n')
            new_doc.write("Copyright © 1983-Hoje Nando Lopes - **yPoemas @ Machina de fazer Poesia**" + '\n')

    print( 'Runtime:', time.time() - start_time )

# Driver Code:
if __name__ == '__main__':
    build_docs()
