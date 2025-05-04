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




def preencher_formulario(todos_detalhes):
    driver = webdriver.Firefox()
    url2 = 'http://weka.inf.ufes.br/IFESTP/login.php'
    driver.get(url2)

    username = driver.find_element(By.NAME, 'username')
    password = driver.find_element(By.NAME, 'password')
    username.send_keys('dhon')
    password.send_keys('dhon')
    password.send_keys(Keys.RETURN)

    sleep(2)

    for detalhes in todos_detalhes:
        dados = {
            "modelo": "",
            "marca": "",
            "tipo": "",
            "ano": "",
            "cambio": "",
            "cor": "",
            "valor": "",
            "municipio": ""
        }

        for item in detalhes:
            item = item.strip().lower()
            if item.startswith("modelo"):
                dados["modelo"] = item.replace("modelo", "").strip()
            elif item.startswith("marca"):
                dados["marca"] = item.replace("marca", "").strip()
            elif item.startswith("tipo de veículo") or item.startswith("tipo"):
                dados["tipo"] = item.replace("tipo de veículo", "").replace("tipo", "").strip()
            elif item.startswith("ano"):
                dados["ano"] = item.replace("ano", "").strip()
            elif item.startswith("câmbio") or item.startswith("cambio"):
                dados["cambio"] = item.replace("câmbio", "").replace("cambio", "").strip()
            elif item.startswith("cor"):
                dados["cor"] = item.replace("cor", "").strip()
            elif item.startswith("preço"):
                dados["valor"] = item.replace("preço", "").replace("r$", "").strip()
            elif item.startswith("municipio"):
                dados["municipio"] = item.replace("municipio", "").strip()

        # Abre o formulário
        cadastrar = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/button')
        cadastrar.click()
        sleep(2)

        # Preenche os campos
        driver.find_element(By.NAME, 'marca').send_keys(dados["marca"])
        driver.find_element(By.NAME, 'modelo').send_keys(dados["modelo"])
        driver.find_element(By.NAME, 'ano').send_keys(dados["ano"])

        if dados["cambio"] == "automático":
            driver.find_element(By.NAME, 'cambioAutomatico').click()

        tipo = dados["tipo"]
        if "hatch" in tipo:
            driver.find_element(By.ID, 'c_hatch').click()
        elif "sedã" in tipo or "sedan" in tipo:
            driver.find_element(By.ID, 'c_sedan').click()

        cores_possiveis = ["branco", "preto", "prata", "vermelho", "verde", "azul", "rosa"]
        cor_select = Select(driver.find_element(By.ID, 'cor'))
        if dados["cor"] in cores_possiveis:
            cor_select.select_by_value(dados["cor"])
        else:
            cor_select.select_by_value("outro")

        driver.find_element(By.NAME, 'valor').send_keys(dados["valor"])
        driver.find_element(By.NAME, 'municipio').send_keys(dados["municipio"])

        sleep(2)
        inserir = driver.find_element(By.XPATH, '/html/body/div[1]/div/form/div[4]/div[3]/input')
        inserir.click()

        sleep(5)

    driver.quit()


if __name__ == "__main__":
    preencher_formulario(todos_detalhes)