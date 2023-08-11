import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin



def imprimir_csv(data):     # Função para armazenar em um txt todas as URLs
    contador2 = 0
    filename = "todas_urls.csv"  # Nome do arquivo
    with open(filename, 'w') as file:
        # Escrever cabeçalho (opcional)
        file.write("URL, Título\n")

        # Escrever os dados em formato CSV
        for site in data:
            contador2 = contador2 + 1
            url = site.replace(",", "")  # Remover vírgulas das URLs
            titulo = contador2  # Remover vírgulas dos títulos
            file.write(f"{url}, {titulo}\n")

    print(f"Os dados foram gravados no arquivo '{filename}'.") 


def find_all_urls(
    url_site: str,
    base_url: str,
    vetor_sites: list = list(),
    url_site_total: list = list()):

    try:
        url_site_total.append(url_site)

        #  Fazendo a requisição para o site
        response = requests.get(url_site)

        #  Extraindo o conteúdo HTML da página
        soup = BeautifulSoup(response.content, "html.parser")


        #  Encontrando todas as tags "a"
        links = soup.find_all("a")

        #  Extraindo as URLs e títulos dos links
        urls_and_titles = [(link.get("href"), link.text.replace("\n","")) for link in links]

        #   For que criará a verificação para adquirir apenas sites de valor
        for url , title in urls_and_titles:
            
            if url is not None and url not in vetor_sites:
                if "Category" in url or "Special" in url or "?":    # Excluindo URL sem valor
                    continue
            
                elif isinstance(url, str) and url.startswith(base_url):     # Verificando se a URL começa com a base
                    primeira_ocorrencia = url.find(":")
                    letra = url.find(":", primeira_ocorrencia + 1)     # Cortando possiveis variações de uma mesma URL
                    if letra != -1:
                        url = url[:letra]
                    if url not in vetor_sites:
                        vetor_sites.append(url)
                    else:
                        continue
            
                elif isinstance(url, str) and url.startswith("/wiki"):      # Verificando se a URL começa com "/wiki" e adicionando a base
                    url = urljoin(base_url, url)
                    primeira_ocorrencia = url.find(":")
                    letra = url.find(":", primeira_ocorrencia + 1)          # Cortando possiveis variações de uma mesma URL
                    if letra != -1:
                        url = url[:letra]
                    if url not in vetor_sites:
                        vetor_sites.append(url)
                    else:
                        continue

            for site in vetor_sites:        # For que irá chamar a segunda função e armazenará todas as possiveis URLs de um site 
                if site not in url_site_total:
                    find_all_urls2(
                        url_site= site,
                        base_url = base_url,
                        vetor_sites=vetor_sites,
                        url_site_total=url_site_total

                    )
    except requests.exceptions.RequestException as e:
        print("Erro na solicitação:", e)
                    
    return
                





def find_all_urls2(                     # Função igual a de outra, entretanto, sem o ultimo "for"
    url_site: str,
    base_url: str,
    vetor_sites: list = list(),
    url_site_total: list = list()):

    url_site_total.append(url_site)

 #  Fazendo a requisição para o site
    response = requests.get(url_site)

    #  Extraindo o conteúdo HTML da página
    soup = BeautifulSoup(response.content, "html.parser")


    #  Encontrando todas as tags "a"
    links = soup.find_all("a")

    #  Extraindo as URLs e títulos dos links
    urls_and_titles = [(link.get("href"), link.text.replace("\n","")) for link in links]
    for url , title in urls_and_titles:
        
        if url is not None and url not in vetor_sites:
            if "Category" in url or "Special" in url:
                continue
            elif "?" in url:
                continue
        
            elif isinstance(url, str) and url.startswith(base_url):
                primeira_ocorrencia = url.find(":")
                letra = url.find(":", primeira_ocorrencia + 1)
                if letra != -1:
                    url = url[:letra]
                if url not in vetor_sites:
                    vetor_sites.append(url)
                else:
                    continue
        
            elif isinstance(url, str) and url.startswith("/wiki"):
                url = urljoin(base_url, url)
                primeira_ocorrencia = url.find(":")
                letra = url.find(":", primeira_ocorrencia + 1)
                if letra != -1:
                    url = url[:letra]
                if url not in vetor_sites:
                    vetor_sites.append(url)
                else:
                    continue

    return


base_url = "https://basketball.fandom.com" #Base da URL
site_url = "https://basketball.fandom.com/wiki/Basketball_Wiki" #Site principal da onde sairá todos os sites
all_urls = []
url_site_total = []

vetor_sites = []  #Armazena a struct site

all_urls = find_all_urls(site_url,base_url,vetor_sites, url_site_total) #Chamando função recursiva

imprimir_csv(vetor_sites)