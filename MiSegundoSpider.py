from scrapy import Spider, Selector
from scrapy.item import Field, Item

# Definimos un Item llamado 'Pregunta' que contiene dos campos: 'pregunta' y 'id'
class Pregunta(Item):
    pregunta = Field()  # Este campo almacenará el texto de la pregunta
    id = Field()  # Este campo almacenará el enlace o ID de la pregunta

# Definimos el Spider que se encargará de rastrear la página de StackOverflow
class StackOverflowSpider(Spider):
    name = 'MiSegundoSpider'  # Nombre del Spider
    start_urls = ['https://stackoverflow.com/questions']  # Lista de URLs de inicio para el Spider

    # Función principal del Spider, se ejecuta cada vez que se descarga una página
    def parse(self, response):
        sel = Selector(response)  # Creamos un Selector para analizar el contenido de la página

        # Seleccionamos los elementos que contienen las preguntas utilizando XPath
        # Se seleccionan todos los enlaces <a> con la clase 's-link' dentro del div con id 'questions'
        preguntas = sel.xpath('//*[@id="questions"]//a[@class="s-link"]')

        # Recorremos cada una de las preguntas encontradas
        for pregunta in preguntas:
            # Extraemos el texto dentro del enlace (que es el título de la pregunta)
            texto_pregunta = pregunta.xpath('.//text()').get()

            # Extraemos el enlace (href) de la pregunta, que puede ser usado como ID o identificador
            id_pregunta = pregunta.xpath('.//@href').get()

            # Imprimimos en la consola el título de la pregunta y su enlace
            print(f"Pregunta: {texto_pregunta} - ID/Link: {id_pregunta}")

            # Retornamos el ítem 'Pregunta' con los datos extraídos (título e ID)
            yield Pregunta(pregunta=texto_pregunta, id=id_pregunta)
             #almacenar en csv pondremos por terminal :
            # scrapy runspider MiSegundoSpider.py -o preguntas2.csv -t csv