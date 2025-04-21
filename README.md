Web Scraper OLX - Carros ES (com Filtro de Atributos)
Este projeto é um web scraper em Python que coleta informações de anúncios de carros no site da OLX, focado na região norte do Espírito Santo, com faixa de preço entre R$ 40.000 e R$ 60.000.

O script utiliza as bibliotecas Selenium e BeautifulSoup para automação e extração dos dados, com destaque para:

✅ Funcionalidades
Acessa a OLX e coleta os links dos anúncios de carros;

Abre individualmente cada anúncio para capturar os detalhes completos;

Extrai informações relevantes do veículo como:
-Marca
-Modelo
-Ano
-Tipo de câmbio
-Cor
-Tipo de veículo
-Preço
-Município

Remove automaticamente informações desnecessárias como:
-Quilometragem
-Potência do motor
-Número de portas
-Direção
-Final de placa

Aplica formatação com espaços automáticos entre palavras que estão coladas no HTML (ex: TipoDeVeiculo → Tipo De Veiculo).

🛠️ Tecnologias Utilizadas
Python 3
Selenium
BeautifulSoup
Regex (para separação de palavras)
Firefox + Geckodriver

Feito por: Dhonathas Goofins Alves de Lima Filho, Luiz Gabriel Maifredi Brits
