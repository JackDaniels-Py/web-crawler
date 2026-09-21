import bs4
import requests
from urllib.parse import urljoin, urlparse
import time
import logging

# Configurações de logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s [%(levelname)s] %(message)s'
)

# URL base, lista de links a visitar, set de sites já visitados
# dominio base: "books.toscrape.com"
base_url = "http://books.toscrape.com"
lista_links_visitar = [base_url]
set_links_visitados = set()
set_links_na_fila = {base_url}
dominio_base = urlparse(base_url).netloc
contador = 0
internos = set()
externos = set()

logging.info("Crawler iniciado...")
while lista_links_visitar and contador < 10:
    url = lista_links_visitar.pop(0)

    if url in set_links_visitados:
        logger.warning(f"URL duplicada ignorada: {url}")
        continue
    
    logger.debug(f"Processando URL: {url}")

    try:
        # Fazer Requisição
        logger.debug(f"Requisição GET iniciada: {url}")
        requests_url = requests.get(url, timeout=5)

    except requests.exceptions.RequestException as erro:
        logger.exception(f"Falha na requisição para: {url}")
        continue
    
    if requests_url.status_code == requests.codes.ok:
        logger.info(f"Requisição bem-sucedida: {url}")
        logger.debug(f"Status code: {requests_url.status_code}")
    else:
        logger.warning(f"Requisição falhou para {url} [Status: {requests_url.status_code}]")
        continue

    # Adicionar url aos visitados
    set_links_visitados.add(url)
    contador += 1

    # Criar Objeto Soup com URL
    soup = bs4.BeautifulSoup(requests_url.text, "html.parser")

    # Extrair Headers
    info_headers = requests_url.headers
    logger.debug(f"Total de headers extraídos: {len(info_headers)}")

    print("\n" + "<-- Headers -->".center(50))
    for info in info_headers:
        print(f"{info}: {info_headers[info]}".center(50))
    print(" ")

    # Extrair title
    titlePage = soup.find("title").getText(strip=True)
    logger.debug(f"Title extraído: {titlePage}")
    print(f"\n" + "<-- Title -->".center(50) + "\n" + f"{titlePage}".center(50) + "\n")

    
    # Extrair todas as tags <meta> e exibir name e content.
    headTags = soup.select("head > meta")
    logger.debug(f"Total de tags meta extraídas: {len(headTags)}")

    print("\n" + "<-- Name/http_equiv e Content -->".center(50))
    for tag in headTags:
        name = tag.get("name")
        http_equiv = tag.get("http-equiv")
        content = tag.get("content", "").strip()

        identifier = name if name else http_equiv
        conteudo = content if content else "Sem conteúdo"
        print(f"Name: {identifier:<10} | Conteúdo: {conteudo}")
    print(" ")

    # Extrair links, e separar entre links internos e externos
    links = soup.select('a[href]')

    for link in links:
        href = link.get("href")

        if not href or href.startswith("#") or href.startswith("javascript:"):
            continue

        url_absoluta = urljoin(url, href)
        dominio_link = urlparse(url_absoluta).netloc

        if dominio_link == dominio_base:
            internos.add(url_absoluta)
        else:
            externos.add(url_absoluta)

    logger.info(f"Links encontrados - Externos: {len(externos)}, Internos: {len(internos)}")
    logger.debug(f"URLs externas: {externos}")
    logger.debug(f"URLs internas: {internos}")

    # Exibir externos
    print("\n" + "<-- Externos -->".center(50))
    if not externos:
        print("Nenhum link externo encontrado".center(50))
    for link_externo in externos:
        print(link_externo)

    # Exibir internos
    print("\n" + "<-- Internos -->".center(50))
    if not internos:
        print("Nenhum link interno encontrado".center(50))
    for link_interno in internos:
        print(link_interno)

        # Verificar se link interno não está no set de visitados
        # Se não estiver ele é adicionado na lista de sites a visitar
        if (
            link_interno not in set_links_visitados and 
            link_interno not in set_links_na_fila
        ):
            lista_links_visitar.append(link_interno)
            set_links_na_fila.add(link_interno)
    print(" ")

    # Encontrar todos os forms da página
    forms_pagina = soup.select("form")
    logging.debug(f"Forms encontrados {len(forms_pagina)}")
    logging.debug(f"Forms: {forms_pagina}")
    print(" ")
    
    
    # Exibir method e action
    print("<-- Method e Action -->".center(50))
    for form in forms_pagina:
        method = form.get("method", "NÃO ESPECIFICADO").upper()
        action = form.get("action", "NÃO ESPECIFICADO").strip()
        print(f"Method: {method} - Action: {action}")

    # Pegar todos os campos <input>, <textarea>, <select>
        campos = form.select("input, textarea, select, button")
        if not campos:
            logging.debug(f"Nenhum dos campos foi encontrado, campos: {campos}")

        # Extrair Hidden
        hidden = form.select('input[type="hidden"]')
        print(f"Hidden: {hidden}" if hidden else 'Atributo hidden não encontrado')
        
        # Em cada campo extrair e exibir name e type
        for campo in campos:
            name = campo.get("name", "N/A")
            type_ = campo.get("type", "N/A")
            tag = campo.name
            print(f"Tag: {tag} | name: {name} | type: {type_}")
        
    time.sleep(0.5)