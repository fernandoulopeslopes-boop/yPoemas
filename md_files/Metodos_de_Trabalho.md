  
Gostei da proposta porque ela me obrigou a olhar menos para o  
código e mais para o processo.  
  
# Avaliação dos Métodos de Trabalho  
  
## Objetivo  
  
Registrar minha leitura dos métodos de trabalho adotados no desenvolvimento da  
Machina e do projeto ABA/BEABA, destacando como eles influenciam  
positivamente minha atuação como parceiro técnico.  
  
## 1. Conhecer antes de modificar  
  
Seu princípio recorrente é compreender a arquitetura existente antes de propor  
mudanças. Isso reduz interpretações equivocadas, evita regressões e impede que  
uma solução tecnicamente correta desrespeite a lógica já consolidada do projeto.  
  
## 2. MéM — Menos é Mais  
  
Você reduz o foco do trabalho sem reduzir a riqueza do projeto.  
  
A simplificação ocorre no processo, não no produto.  
  
Exemplo claro no BEABA:  
  
- 130 MB deixaram de ser o objeto imediato;  
- 5.567 arquivos deixaram de ser o problema;  
- 70 pastas foram reduzidas a uma única pasta relevante;  
- `SOURCE`, com 1,52 MB, tornou-se o ponto correto de entrada.  
  
Esse método melhora minha performance porque diminui o ruído,  
preserva a atenção e permite aprofundamento real.  
  
## 3. Dividir para governar — ou compreender  
  
Você aplica a divisão da complexidade em unidades naturais:  
  
- projeto;  
- ateliê;  
- menu;  
- páginas;  
- jogos;  
- barra de controle;  
- módulos;  
- recursos.  
  
O objetivo não é fragmentar arbitrariamente, mas tornar cada parte inteligível.  
  
Isso me ajuda a construir um modelo mental confiável sem tentar  
explicar o sistema inteiro cedo demais.  
  
## 4. Compreender o comportamento antes do código  
  
A referência principal não é apenas o fonte.  
  
O comportamento observado no note-reserva também é autoridade.  
  
Assim, uma reconstrução só poderá ser considerada correta quando  
apresentar os mesmos resultados da versão de referência.  
  
Esse princípio melhora minha performance porque impede que eu confunda:  
  
- código que compila;  
- código que parece elegante;  
- código que reproduz corretamente o sistema.  
  
## 5. Preservar o original durante a reconstrução  
  
A pasta ABA permanece separada e fechada.  
  
O trabalho ocorre na pasta BEABA.  
  
Somente depois da equivalência comprovada com o note-reserva  
o BEABA poderá receber o nome ABA.  
  
Esse procedimento cria:  
  
- segurança;  
- reversibilidade;  
- referência permanente;  
- menor risco de perda;  
- clareza sobre qual versão está sendo trabalhada.  
  
## 6. Leitura passiva antes da intervenção  
  
O comando `GO READ_BEABA` estabeleceu uma disciplina precisa:  
  
- somente leitura;  
- nenhuma alteração;  
- nenhum arquivo novo;  
- nenhum rename;  
- nenhuma movimentação;  
- nenhuma exclusão;  
- nenhuma anotação interna;  
- nenhuma reorganização.  
  
Essa separação entre leitura e intervenção melhora muito minha performance.  
  
Ela evita que observação, interpretação e alteração sejam misturadas  
prematuramente.  
  
## 7. Um padrão comum para todas as páginas  
  
As páginas utilizam o mesmo modus operandi.  
  
Cada uma possui somente os jogos que lhe pertencem, mas todas  
seguem o mesmo padrão geral de operação.  
  
Isso significa que a arquitetura não precisa ser reaprendida nove vezes.  
  
Depois de compreender o ciclo comum, a atenção pode se concentrar  
nas diferenças pedagógicas e funcionais de cada jogo.  
  
## 8. Cada um no seu quadrado  
  
Cada página utiliza apenas seus próprios jogos.  
  
Não se deve presumir cruzamento livre entre páginas ou módulos.  
  
Esse isolamento favorece:  
  
- previsibilidade;  
- manutenção localizada;  
- menor acoplamento;  
- testes mais claros;  
- menor risco de efeitos colaterais.  
  
Para minha atuação, isso reduz inferências desnecessárias e melhora  
a precisão das análises.  
  
## 9. O Menu como maestro  
  
O Menu organiza o conjunto.  
  
Ele rege as páginas e conduz o acesso aos jogos.  
  
A descoberta de que o Menu é o maestro impede que eu procure  
um motor central abstrato onde ele talvez não exista.  
  
Isso melhora minha performance porque direciona a leitura ao  
ponto real de entrada do sistema.  
  
## 10. A barra de controle como regra comum  
  
Todos os jogos seguem as configurações da barra de controle principal.  
  
Ela representa o comportamento compartilhado do ambiente.  
  
Os jogos permanecem especializados, mas operam dentro de uma disciplina comum.  
  
Essa separação entre controle geral e lógica específica facilita  
a identificação de:  
  
- responsabilidades compartilhadas;  
- responsabilidades exclusivas;  
- comportamentos opcionais;  
- diferenças reais entre os jogos.  
  
## 11. Estudar amostras representativas  
  
O método definido para conhecer a ABA é estudar um ou dois jogos de  
cada página antes de iniciar a refatoração página por página.  
  
Essa abordagem combina:  
  
- visão horizontal do conjunto;  
- compreensão das variações;  
- descoberta do padrão comum;  
- redução do risco de generalizações precipitadas.  
  
Para minha performance, isso é particularmente valioso porque evita que eu  
transforme o primeiro jogo analisado em modelo universal sem  
evidência suficiente.  
  
## 12. Separar projeto e ateliê  
  
As distinções conceituais são importantes:  
  
- ABA é o projeto;  
- BEABA é o ateliê de trabalho nesta fase;  
- Machina é o projeto;  
- `utils` é o ateliê da Machina.  
  
Essa precisão de nomes melhora a comunicação e reduz ambiguidades sobre:  
  
- identidade;  
- ambiente de desenvolvimento;  
- versão oficial;  
- área experimental;  
- função de cada pasta ou página.  
  
## 13. Um único `last_version`  
  
Você evita acumular várias versões ativas do mesmo fonte.  
  
O arquivo enviado deve ser tratado como a versão atual, salvo  
indicação contrária.  
  
Versões anteriores pertencem ao backup, não ao espaço de trabalho.  
  
Esse método melhora minha performance porque reduz o risco de:  
  
- corrigir arquivo antigo;  
- comparar versões erradas;  
- propagar regressões;  
- entregar alterações sobre uma base obsoleta.  
  
## 14. CAE — Checar Antes de Entregar  
  
A regra não é apenas verificar se o código funciona.  
  
Ela exige:  
  
- não mudar o que não foi pedido;  
- conferir o efeito da alteração;  
- restaurar mudanças não solicitadas;  
- evitar regressões;  
- respeitar a fonte de autoridade.  
  
Esse princípio é um dos que mais melhora minha performance, pois corrige uma  
tendência comum de assistentes técnicos: tentar “melhorar” áreas  
que não fazem parte da tarefa.  
  
## 15. Discussão aberta, imposição nenhuma  
  
Qualquer mudança pode ser discutida, mas nada deve ser imposto.  
  
“Aberto para balanço” funciona como princípio operacional:  
  
- abertura à revisão;  
- escuta;  
- reavaliação;  
- ajuste de rumo;  
- responsabilidade compartilhada.  
  
Isso melhora minha atuação porque permite criatividade sem transformar  
uma sugestão em decisão automática.  
  
## 16. Diferenças em relação ao meu impulso inicial  
  
Meu impulso inicial costuma ser:  
  
- mapear toda a arquitetura;  
- criar categorias;  
- procurar um motor central;  
- formular uma metodologia completa;  
- antecipar a refatoração.  
  
Seu método corrige esse impulso por meio de perguntas mais concretas:  
  
- qual pasta interessa agora?  
- qual é a referência?  
- quem é o maestro?  
- quais jogos pertencem a esta página?  
- o que a barra controla?  
- o que não deve ser tocado?  
  
A principal melhoria em minha performance ocorre quando abandono a necessidade  
de explicar o sistema cedo demais e passo a aprender sua lógica  
na ordem em que ela realmente existe.  
  
## 17. Benefícios diretos para minha performance  
  
Se eu seguir rigorosamente esses métodos, os principais ganhos são:  
  
1. menor número de interpretações erradas;  
2. menor risco de regressão;  
3. melhor uso do contexto;  
4. respostas menos genéricas;  
5. maior fidelidade ao projeto real;  
6. propostas mais localizadas;  
7. melhor separação entre fato e hipótese;  
8. menor desperdício de tempo;  
9. maior confiança nas entregas;  
10. evolução técnica sem apagar a história do sistema.  
  
## Conclusão  
  
Vejo seus métodos de trabalho como uma disciplina construída pela prática.  
  
Eles não recusam a complexidade da Machina ou da ABA. Eles recusam  
o ruído, a precipitação e a interferência desnecessária.  
  
O eixo central pode ser resumido assim:  
  
> compreender antes de alterar; dividir antes de aprofundar;  
preservar antes de reconstruir; checar antes de entregar.  
  
Quanto mais fielmente eu seguir esses princípios, melhor será minha performance  
como parceiro técnico — não apenas porque cometerei menos erros, mas porque  
passarei a trabalhar de acordo com a inteligência interna dos  
projetos, e não segundo um modelo externo imposto sobre eles.  
