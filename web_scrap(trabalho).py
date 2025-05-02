from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from time import sleep
import re

# Primeiro acesso à OLX pra coletar os links
driver = webdriver.Firefox()
url = 'https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-es/norte-do-espirito-santo?me=40000&pe=60000&rs=65'
driver.get(url)

# Espera os anúncios carregarem
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "olx-adcard__link"))
)

# Coleta todos os links dos anúncios
elements = driver.find_elements(By.CLASS_NAME, "olx-adcard__link")
links = [elem.get_attribute('href') for elem in elements]
driver.quit()  # Fecha o navegador depois de pegar os links

# Armazena o HTML de cada página de anúncio
htmls = []

# Agora, para cada link, abre e fecha o navegador separadamente e definindo uma quantidade pra ele colocando um limite de 10
for i, link in enumerate(links[:2]):
    driver = webdriver.Firefox()
    driver.get(link)
    sleep(2)  # tempo de carregamento da página
    html = driver.page_source
    htmls.append(html)
    print(f"{i+1} capturado")
    driver.quit()

todos_detalhes = []

# Insere espaço entre letra minúscula seguida de maiúscula, ou entre letra e número
def separar_palavras(texto):
    return re.sub(r'(?<=[a-záéíóúãõç])(?=[A-Z0-9])', ' ', texto)

# Lista de palavras indesejadas
palavras_indesejadas = [
    "Quilometragem",
    "Potência do motor",
    "Possui Kit GNV",
    "Portas",
    "Final de placa",
    "Direção",
    "Tipo de direção"
]

# Passa por todas as páginas
for i, html in enumerate(htmls, 1):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Pega o preço do carro
    preco = soup.find('span', class_='olx-text olx-text--title-large olx-text--block')

    # Pega todas as descrições do carro de acordo coma classe
    descricao = soup.find_all('div', class_='ad__sc-2h9gkk-1 bdpQSX olx-d-flex olx-ai-flex-start olx-fd-column olx-flex')

    #Pega o municipio
    municipio = soup.find('div', class_='ad__sc-o5hdud-1 jvsEyX olx-d-flex olx-ai-center')
    
    # Extrai os textos da descricao e usa a função para separar os texto que acabam vindo junto
    infoCarro = [separar_palavras(d.text.strip()) for d in descricao]

    # Filtra apenas as informações desejadas (remove as indesejadas)
    infoCarro = [info for info in infoCarro if not any(info.startswith(palavra) for palavra in palavras_indesejadas)]

    # Adiciona o preço na lista
    infoCarro.append(separar_palavras(f"Preço {preco.text.strip()}"))

    # Adiciona o municipio na lista
    infoCarro.append(separar_palavras(f"Municipio {municipio.text.strip()}"))

    # Salva os detalhes de cada carro
    todos_detalhes.append(infoCarro)

# Mostra os detalhes capturados
for i, detalhes in enumerate(todos_detalhes, 1):
    print(f"\nInformações do carro {i}:")
    for info in detalhes:
        print(f"- {info}")

print( )
print(todos_detalhes)






#-------------------------------- SEGUNDA PARTE -----------------------------------

driver = webdriver.Firefox()
url2 = 'http://weka.inf.ufes.br/IFESTP/login.php'
driver.get(url2)

#procura os elementos na pagina
username = driver.find_element(By.NAME, 'username')
password = driver.find_element(By.NAME, 'password')

#coloca a senha nos elementos enccontrados e aperta enter
username.send_keys('dhon')
password.send_keys('dhon')
password.send_keys(Keys.RETURN)

sleep(2)
for detalhes in todos_detalhes:
    # Clica no botão 'inserir'
    botao = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/button')
    botao.click()
    sleep(2)

    # Converte lista em dicionário
    dados = {}
    for item in detalhes:
        chave, valor = item.split(" ", 1)
        dados[chave.strip()] = valor.strip()

    # Marca
    marca = driver.find_element(By.NAME, 'marca')
    marca.send_keys(dados.get("Marca", ""))

    # Modelo
    modelo = driver.find_element(By.NAME, 'modelo')
    modelo.send_keys(dados.get("Modelo", ""))

    # Ano
    ano = driver.find_element(By.NAME, 'ano')
    ano.send_keys(dados.get("Ano", ""))

    sleep(2)
    # Câmbio automático
    if dados.get("Câmbio", "").lower() == "automático":
        cambio = driver.find_element(By.NAME, 'cambioAutomatico')
        cambio.click()

    sleep(2)
    # Tipo de veículo
    tipo_valor = dados.get("Tipo", "").lower()
    if "hatch" in tipo_valor:
        tipoVeiculo = driver.find_element(By.ID, 'c_hatch')
        tipoVeiculo.click()
    elif "sedan" in tipo_valor:
        tipoVeiculo = driver.find_element(By.ID, 'c_sedan')
        tipoVeiculo.click()

    sleep(2)
    # Cor
    cor_select = Select(driver.find_element(By.ID, 'cor'))
    cor_desejada = dados.get("Cor", "").lower()
    if "branco" in cor_desejada:
        cor_select.select_by_value("branco")
    elif "preto" in cor_desejada:
        cor_select.select_by_value("preto")
    elif "prata" in cor_desejada:
        cor_select.select_by_value("prata")
    elif "vermelho" in cor_desejada:
        cor_select.select_by_value("vermelho")
    elif "verde" in cor_desejada:
        cor_select.select_by_value("verde")
    elif "azul" in cor_desejada:
        cor_select.select_by_value("azul")
    elif "rosa" in cor_desejada:
        cor_select.select_by_value("rosa")
    else:
        cor_select.select_by_value("outro")

    # Valor
    valor = driver.find_element(By.NAME, 'valor')
    valor_str = dados.get("Preço", "").replace("R$", "").replace(".", "").replace(",", ".").strip()
    valor.send_keys(valor_str)

    # Cidade
    cidade = driver.find_element(By.NAME, 'municipio')
    cidade.send_keys(dados.get("Municipio", ""))
    cidade.send_keys(Keys.RETURN)
    
    # Espera antes de ir para o próximo
    sleep(5)