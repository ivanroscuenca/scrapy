from scrapy import Spider, Selector
from scrapy.item import Field, Item

# Definimos un Item llamado 'Pregunta' que contiene dos campos: 'pregunta' y 'id'
class Pregunta(Item):
    pregunta = Field()  # Este campo almacenará el texto de la pregunta
    id = Field()  # Este campo almacenará el número de la pregunta

# Definimos el Spider que se encargará de rastrear la página de StackOverflow
class StackOverflowSpider(Spider):
    name = 'MiPrimerSpider'  # Nombre del Spider
    start_urls = ['https://stackoverflow.com/questions']  # Lista de URLs de inicio para el Spider

    # Función principal del Spider, se ejecuta cada vez que se descarga una página
    def parse(self, response):
        sel = Selector(response)  # Creamos un Selector para analizar el contenido de la página

        # Seleccionamos los elementos que contienen las preguntas utilizando XPath
        # Se seleccionan todos los enlaces <a> con la clase 's-link' dentro del div con id 'questions'
        preguntas = sel.xpath('//*[@id="questions"]//a[@class="s-link"]')

        # Recorremos cada una de las preguntas encontradas
        for index, pregunta in enumerate(preguntas, start=1):
            # Extraemos el texto de la pregunta
            texto_pregunta = pregunta.xpath('.//text()').get()

            # Imprimimos en la consola el título de la pregunta y su enlace
            print(f"Pregunta: {texto_pregunta}")

            # Creamos un ítem 'Pregunta' con el texto de la pregunta y su número
            yield Pregunta(pregunta=texto_pregunta, id=index)
            #almacenar en csv pondremos por terminal :
            # scrapy runspider MiPrimerSpider.py -o preguntas.csv -t csv