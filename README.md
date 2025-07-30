# Scraper-de-Dados-Publicos

## Este projeto é um scraper (programa automatizado) em Python que coleta notícias do site internacional da BBC News. Ele navega pelas páginas do site, captura informações essenciais de cada notícia, como título, link, resumo, data de publicação, e ainda acessa cada artigo para extrair o conteúdo completo, o autor, a categoria da notícia e o tempo estimado de leitura. Todos esses dados são organizados e salvos em um arquivo CSV, facilitando análises futuras.

## O scraper começa definindo a URL base do site da BBC News e navega pelas páginas de notícias, respeitando o limite máximo definido (por exemplo, 2 ou 3 páginas). Para cada página, ele realiza uma requisição HTTP simulando um navegador, para evitar bloqueios. Com o conteúdo HTML recebido, o programa usa a biblioteca BeautifulSoup para identificar e extrair os blocos de notícias, buscando elementos como título, link, resumo e data de publicação.

Para cada notícia listada, o scraper acessa o link da página individual para coletar informações adicionais: o conteúdo completo do artigo, o nome do autor, a categoria da notícia e o tempo estimado de leitura. Esse conteúdo é limpo, removendo scripts, estilos e elementos que não fazem parte do texto principal.

Todas essas informações são armazenadas em uma lista de dicionários. Após coletar os dados de todas as páginas, o scraper converte essa lista em uma tabela usando pandas e salva em um arquivo CSV, facilitando a análise posterior dos dados.

Durante o processo, o scraper faz pausas entre as requisições para evitar sobrecarregar o servidor da BBC, respeitando boas práticas de web scraping.
