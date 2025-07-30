import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import time
import re

def scrape_bbc_news(max_pages=3, output_file='bbc_news.csv'):
    """
    Scraper para coletar notícias do site internacional da BBC News
    
    Args:
        max_pages (int): Número máximo de páginas para raspar
        output_file (str): Nome do arquivo de saída CSV
    """
    base_url = "https://www.bbc.com"
    news_url = urljoin(base_url, "news")
    
    all_news = []
    
    for page in range(1, max_pages + 1):
        print(f"Coletando dados da página {page}...")
        
        # Construir URL da página atual (a BBC usa paginação diferente)
        if page > 1:
            current_url = f"{news_url}?page={page}"
        else:
            current_url = news_url
        
        try:
            # Fazer requisição HTTP com headers para parecer um navegador
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(current_url, headers=headers)
            response.raise_for_status()  # Verificar se a requisição foi bem-sucedida
            
            # Parsear o HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Encontrar todos os elementos de notícia
            news_items = soup.find_all('div', {'data-testid': 'edinburgh-card'})
            
            if not news_items:
                print("Nenhuma notícia encontrada na página. Parando...")
                break
                
            # Extrair dados de cada notícia
            for item in news_items:
                title_elem = item.find('h2')
                if not title_elem:
                    continue
                    
                title = title_elem.get_text(strip=True)
                link = urljoin(base_url, title_elem.find_parent('a')['href']) if title_elem.find_parent('a') else ''
                
                summary_elem = item.find('p')
                summary = summary_elem.get_text(strip=True) if summary_elem else ''
                
                date_elem = item.find('time')
                date = date_elem['datetime'] if date_elem and 'datetime' in date_elem.attrs else ''
                
                # Coletar dados adicionais da página da notícia
                if link:
                    news_details = scrape_news_details(link)
                else:
                    news_details = {}
                
                # Adicionar ao dataset
                all_news.append({
                    'titulo': title,
                    'link': link,
                    'resumo': summary,
                    'data_publicacao': date,
                    'conteudo': news_details.get('conteudo', ''),
                    'autor': news_details.get('autor', ''),
                    'categoria': news_details.get('categoria', ''),
                    'tempo_leitura': news_details.get('tempo_leitura', '')
                })
            
            # Esperar um pouco entre requisições para não sobrecarregar o servidor
            time.sleep(3)
            
        except Exception as e:
            print(f"Erro ao processar página {page}: {e}")
            continue
    
    # Salvar os dados em um CSV
    if all_news:
        df = pd.DataFrame(all_news)
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"Dados salvos com sucesso em {output_file}")
        print(f"Total de notícias coletadas: {len(all_news)}")
    else:
        print("Nenhum dado foi coletado.")

def scrape_news_details(news_url):
    """Coleta detalhes adicionais da página individual da notícia"""
    details = {}
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(news_url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Conteúdo completo
        content = soup.find('main', {'role': 'main'})
        if content:
            # Remover scripts e elementos indesejados
            for element in content(['script', 'style', 'aside', 'nav', 'footer']):
                element.decompose()
            details['conteudo'] = ' '.join(content.get_text(strip=True).split())
        else:
            details['conteudo'] = ''
        
        # Autor
        author = soup.find('div', {'data-testid': 'byline'})
        details['autor'] = author.get_text(strip=True) if author else ''
        
        # Categoria
        category = soup.find('a', {'data-testid': 'BreadcrumbItem'})
        details['categoria'] = category.get_text(strip=True) if category else ''
        
        # Tempo de leitura
        reading_time = soup.find('div', {'data-testid': 'timestamp'})
        details['tempo_leitura'] = reading_time.get_text(strip=True) if reading_time else ''
            
    except Exception as e:
        print(f"Erro ao coletar detalhes de {news_url}: {e}")
    
    return details

if __name__ == "__main__":
    scrape_bbc_news(max_pages=2, output_file='bbc_news_internacional.csv')