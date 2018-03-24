# Domínio Hotel
### Recuperação da Informação

### Autores e Responsabilidades
- Douglas Soares Lins | dsl@cin.ufpe.br (Extração)
- Jonatas de Oliveira Clementino | joc@cin.ufpe.br (Classificador)
- Valdemiro Rosa Vieira Santos | vrvs@cin.ufpe.br (Crawling)

### Tarefas
#### Localizar Páginas Relevantes
1. Encontrar manualmente	10	sites	no	domínio
2. Implementar	2	estratégias:
– Baseline:	busca em largura <br />
– Heurística <br />
3. Comparar estatégias:	
– Harvest	ratio:	(número	de	páginas relevantes coletadas)/(total	de	
páginas visitadas)	
– Mostrar tabela	com	resultados
• Importante:	
– Evitar sobrecarregar	o	site	
– Respeitar	o	robots.txt
– Detectar	o	conteúdo	da	página	com	o	campo	Content-Type	

#### Detectar Páginas	com	Instâncias
1. Rotular exemplos positivos	e	negativos	(10	positivos	e	10	
negativos por	site)	
2. Criar	o	conjunto	de	features	(ex.:	bag	of	words)	usando	feature	
selection	(ex.	frequência ou	information	gain)	
3. Treinar	o	classificador	com	uma ferramenta	de	ML	(ex.:	scikitlearn,
weka etc)		
– Métodos:	Naïve	bayes,	Decision	tree	(J48),	SVM	(SMO),	Logitic	
regression	(logistic),	Multilayer	perceptron	
4. Comparar estratégias:	
– Accuracy,	precision	e	recall	
– Tempo	de	treinamento
– Mostrar tabela	com	os resultados

#### Extrair Instâncias	com	seus Valores	e	Atributos
1. Criar	um	wrapper	para cada	site	
– Criação	do	conjunto rotulado
2. Implementar uma solução que funcione para todos os	sites	
– Ex:	detectores	de	tipos	do	domínio
3. Comparar estratégias:	
– Accuracy,	precision	e	recall	
– Mostrar tabela	com	os resultados


### Curso
Universidade Federal de Pernambuco <br />
Centro de Informática <br />
Gradução em Ciência da Computação <br />
