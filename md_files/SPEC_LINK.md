# SPEC_LINK — Machina/yPoemas  
  
## Objetivo  
Criar um elemento autoral `LINK` dentro dos próprios arquivos `.ypo`, permitindo  
relacionar temas da Machina e construir roteiros vivos de leitura.  
  
## Sintaxe  
`<tag><content>`  
  
- `<tag>` = nome do tema de destino, incluindo `.ypo`  
- `<content>` = texto clicável apresentado ao leitor  
- os pares `< >` garantem rastreabilidade única do elemento no ambiente Machina  
  
### Exemplo  
`<eus.ypo><o psicanalista da Lady Murphy...>`  
  
Na tela, o leitor vê apenas:  
  
`o psicanalista da Lady Murphy...`  
  
## Ação  
Ao clicar em `<content>`:  
  
1. a Machina identifica o tema indicado em `<tag>`;  
2. gera um novo yPoema desse tema;  
3. exibe o yPoema gerado no palco.  
  
## Regras  
- O `LINK` pertence ao conteúdo autoral do `.ypo`.  
- O código apenas reconhece e executa o LINK; não cria nem mantém  
relações entre temas.  
- Um tema pode conter um ou vários LINKs.  
- Os LINKs são permanentes no tema; o leitor decide se e quando  
atravessa cada porta.  
- O percurso não é linear nem obrigatório.  
- Não criar estrutura paralela, índice externo ou mapa obrigatório de navegação.  
  
## Conceito  
**Guia autoral embutido:** um roteiro vivo, livre e dinâmico  
de relações entre os temas da Machina.  
  
O autor deixa as portas. A Machina gera. O leitor escolhe o percurso.  
  
## Estado  
**REGISTRADO — NÃO IMPLEMENTAR AGORA.**  
