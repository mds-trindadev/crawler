# Crawler
Responsável por buscar os dados referentes as disciplinas da UnB.

## Instalação
Splash
- pip install scrapy-splash

Scrapy
- pip install Scrapy

## Execução
Para executar o splash
- Para executar o Splash execute o comando "sudo docker run -p 8050:8050 scrapinghub/splash"

Para compilar o programa e salvar a saída no arquivo quotes.xml
- Execute o comando "scrapy crawl quotes -O quotes.xml"