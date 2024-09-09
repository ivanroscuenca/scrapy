import scrapy
from bs4 import BeautifulSoup
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Item, Field


# Clase para definir el contenedor de los datos extraídos
class LeMondeItem(Item):
    # Campo para el título del artículo
    titulo = Field()
    # Campo para el contenido del artículo
    contenido = Field()


# Clase principal del spider que rastrea el sitio
class LeMondeCrawler(CrawlSpider):
    # Nombre del spider
    name = 'lemondecrawler'
    # Dominios permitidos para evitar que el spider siga enlaces fuera de Le Monde
    allowed_domains = ['lemonde.fr']
    # URL de inicio donde comienza el rastreo
    start_urls = ['https://www.lemonde.fr/euro-2016/']

    # Definición de las reglas para el rastreo
    rules = (
        # Regla horizontal: sigue enlaces que contienen '/euro-2016/' seguido de dígitos
        Rule(LinkExtractor(allow=r'/euro-2016/\d+'), follow=True),
        # Regla vertical: sigue enlaces que contienen '/euro-2016/article' y llama a 'parse_items' para extraer los datos
        Rule(LinkExtractor(allow=r'/euro-2016/article'), follow=True, callback='parse_items'),
    )

    # Función que se ejecuta cuando el spider encuentra una página de artículo
    def parse_items(self, response):
        # Crear un cargador de ítems para almacenar los datos extraídos
        item = ItemLoader(LeMondeItem(), response)

        # Extraer el título del artículo usando XPath y el elemento <h1>
        item.add_xpath('titulo', '//h1/text()')

        # Usar BeautifulSoup para analizar el contenido HTML de la página
        soup = BeautifulSoup(response.body, 'html.parser')

        # Buscar el contenido del artículo dentro del elemento con ID 'habillagepub'
        article = soup.find(id='habillagepub')

        # Si el artículo existe (evitar errores si no se encuentra), extraer el contenido
        if article:
            # Extraer el texto del artículo, eliminando espacios innecesarios
            contenido = article.get_text(strip=True)

            # Reemplazar caracteres no deseados, como '&nbsp;' (espacio no separable) con un espacio normal
            contenido_limpio = contenido.replace(u'\xa0', ' ')

            # Añadir el contenido limpio al cargador de ítems
            item.add_value('contenido', contenido_limpio)

        # Devolver el ítem cargado para que Scrapy lo procese y lo almacene
        yield item.load_item()

# correr el spider con :
# scrapy runspider leMondeVideo.py -o resumen.csv -t csv
