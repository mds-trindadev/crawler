import scrapy
from scrapy.item import Item, Field
from scrapy.http import FormRequest
from scrapy_splash import SplashRequest
from scrapy.linkextractors import LinkExtractor
import re

##################################################################
## BUSCAR DADOS REFERENTES AS DISCIPLINAS
class QuotesSpider(scrapy.Spider):
    # Nome do Scrapy
    name = "quotes"

    # Flags de configuracao para captura
    allowed_domains = ['sig.unb.br']
    extractor = LinkExtractor(allow=allowed_domains)

    Funcao principal
    def start_requests(self):
        # Metodos responsaveis por realizar a consulta no formulario e listar as disciplinas disponiveis por unidade academica
        script = """
        function main(splash)
            splash:go('https://sig.unb.br/sigaa/public/componentes/busca_componentes.jsf')
                
            splash:runjs("document.forms['form']['form:nivel'].selectedIndex = 1")

            splash:runjs("document.forms['form']['form:tipo'].selectedIndex = 1")
            splash:runjs("document.forms['form']['form:checkTipo'].checked = true")

            splash:runjs("document.forms['form']['form:unidades'].selectedIndex = 87")
            splash:runjs("document.forms['form']['form:checkUnidade'].checked = true")

            splash:runjs("document.getElementById('form:btnBuscarComponentes').click()")
            splash:wait(1)
            return splash:html()
        end
        """
        yield scrapy.Request('https://sig.unb.br/sigaa/public/componentes/busca_componentes.jsf', self.parseJavaScript, meta={
            'splash': {
                'args': {'lua_source': script},
                'endpoint': 'execute',
            }
        })

    # Funcao responsavel por entrar em cada pagina referentes as disciplinas
    def parseJavaScript(self, response):

        # Gera os dados para serem salvos no arquivo "quotes.xml"
        for quote in response.css('form#formListagemComponentes'):
            yield {
                'par': quote.css("table.listagem tbody tr.linhaPar td a::attr(onclick)").getall(),
                'impar': quote.css("table.listagem tbody tr.linhaImpar td a::attr(onclick)").getall(),
            }

        # Abre o arquivo com a lista de disciplinas disponiveis na unidade
        f = open('./quotes.xml', 'r')
        temp = ' ' + f.read()
        f.close()

        # Extrai apenas as funcoes javascript
        regex = r"""(jsfcljs\(document.getElementById\((.[^\}])+'public'\},''\);)"""

        # Armazena as funcoes em uma lista
        lista = re.findall(regex, temp)

        # Percorre a lista executando cada funcao javascript e pega os dados contendo os detalhes de cada disciplina
        for i in lista:
            newscript = """
                function main(splash)
                    splash:go('https://sig.unb.br/sigaa/public/componentes/busca_componentes.jsf')
                    
                    splash:runjs("document.forms['form']['form:nivel'].selectedIndex = 1")

                    splash:runjs("document.forms['form']['form:tipo'].selectedIndex = 1")
                    splash:runjs("document.forms['form']['form:checkTipo'].checked = true")

                    splash:runjs("document.forms['form']['form:unidades'].selectedIndex = 87")
                    splash:runjs("document.forms['form']['form:checkUnidade'].checked = true")

                    splash:runjs("document.getElementById('form:btnBuscarComponentes').click()")
                    splash:wait(2)

                    splash:runjs(" """ + i[0] + """ ")
                    splash:wait(4)

                    return splash:html()
                end
            """
            yield scrapy.Request('https://sig.unb.br/sigaa/public/componentes/busca_componentes.jsf', self.formatData, meta={
                'splash': {
                    'args': {'lua_source': newscript},
                    'endpoint': 'execute',
                }
            })

    # Salva os dados com detalhes de cada disciplina no arquivo "quotes.xml"
    def formatData(self, response):
        for quote in response.css('body'):
            yield {
                'divPrincipal': quote.css("div#corpo").get(),
            }



##################################################################
## BUSCAR DADOS REFERENTES AS TURMAS
# class QuotesSpider(scrapy.Spider):
#     # Nome do Scrapy
#     name = "quotes"

#     # Flags de configuracao para captura
#     allowed_domains = ['sig.unb.br']
#     extractor = LinkExtractor(allow=allowed_domains)

#     # Funcao principal
#     def start_requests(self):

#         # Metodos responsaveis por realizar a consulta no formulario e listar as disciplinas disponiveis por unidade academica
#         script = """
#         function main(splash)
#             splash:go('https://sig.unb.br/sigaa/public/turmas/listar.jsf')
                
#             splash:runjs("document.forms['formTurma']['formTurma:inputNivel'].selectedIndex = 2")
#             splash:runjs("document.forms['formTurma']['formTurma:inputDepto'].selectedIndex = 90") 
#             splash:runjs("document.forms['formTurma']['formTurma:inputPeriodo'].selectedIndex = 0")

#             splash:runjs("document.forms['formTurma']['formTurma:j_id_jsp_1370969402_11'].click()")
#             splash:wait(3)
#             return splash:html()
#         end
#         """
#         yield scrapy.Request('https://sig.unb.br/sigaa/public/turmas/listar.jsf', self.parseJavaScript, meta={
#             'splash': {
#                 'args': {'lua_source': script},
#                 'endpoint': 'execute',
#             }
#         })

#     def parseJavaScript(self, response):
#         # Gera os dados para serem salvos no arquivo "quotes.xml"
#         for quote in response.css('div#turmasAbertas'):
#             yield {
#                 'disciplina': quote.css("table.listagem tbody").getall(),
#             }
#         

##################################################################
## BUSCAR DADOS REFERENTES AS PAGINAS DE FLUXOS
# class QuotesSpider(scrapy.Spider):
#     # Nome do Scrapy
#     name = "quotes"

#     # Flags de configuracao para captura
#     allowed_domains = ['sig.unb.br']
#     extractor = LinkExtractor(allow=allowed_domains)

#     # Funcao principal
#     def start_requests(self):
#         f = open('./tutorial/listaIdFluxo', 'r')
        
#         for i in f:
#             i = i[:-1]
#             newscript = """
#                 function main(splash)
#                     splash:go('https://sig.unb.br/sigaa/public/curso/curriculo.jsf?lc=pt_BR&id="""+ i +"""')
#                     splash:wait(2)

#                     return splash:html()
#                 end
#             """
#             yield scrapy.Request('https://sig.unb.br/sigaa/public/componentes/busca_componentes.jsf', self.parseJavaScript, meta={
#                 'splash': {
#                     'args': {'lua_source': newscript},
#                     'endpoint': 'execute',
#                 }
#             })

#         f.close()

#     def parseJavaScript(self, response):
#         for quote in response.css('div#conteudo'):
#             yield {
#                 'funcao': quote.css("a::attr(onclick)").get(),
#             }

##################################################################
## BUSCAR DADOS REFERENTES AOS DADOS DOS FLUXOS
# class QuotesSpider(scrapy.Spider):
#     # Nome do Scrapy
#     name = "quotes"

#     # Flags de configuracao para captura
#     allowed_domains = ['sig.unb.br']
#     extractor = LinkExtractor(allow=allowed_domains)

#     # Funcao principal
#     def start_requests(self):
#         f = open('./tutorial/listaIdFluxo', 'r')
#         g = open('./tutorial/listaJavascriptFluxo', 'r')

#         cont = 0
#         cont2 = 0
#         funcao = ''

#         for i in f:
#             i = i[:-1]
#             cont2 = 0
#             for j in g:
#                 cont2 += 1
#                 funcao = j[:-1]
#                 if cont2 > cont:
#                     break;

#             newscript = """
#                     function main(splash)
#                         splash:go('https://sig.unb.br/sigaa/public/curso/curriculo.jsf?lc=pt_BR&id="""+ i +"""')
#                         splash:wait(2)

#                         splash:runjs(" """ + funcao + """ ")
#                         splash:wait(2)

#                         return splash:html()
#                     end
#             """
#             yield scrapy.Request('https://sig.unb.br/sigaa/public/componentes/busca_componentes.jsf', self.parseJavaScript, meta={
#                 'splash': {
#                     'args': {'lua_source': newscript},
#                     'endpoint': 'execute',
#                 }
#             })
#             cont += 1

#         f.close()

#     def parseJavaScript(self, response):
#         for quote in response.css('body'):
#             yield {
#                 'funcao': quote.css("div#container").get(),
#             }