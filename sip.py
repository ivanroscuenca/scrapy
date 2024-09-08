from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class SipSpider(CrawlSpider):
    name = 'sip'
    start_urls = ['http://sipwhiskey.com/']
    allowed_domains = ['sipwhiskey.com']  # Es una lista, no un string

    rules = (
        Rule(LinkExtractor(allow='collections', deny='products')),  # Sigue enlaces de 'collections' pero no de 'products'
        Rule(LinkExtractor(allow='products'), callback='parse_item'),  # Sigue enlaces de 'products' y llama a 'parse_item'
    )

    def parse_item(self, response):
        yield {
            'brand': response.css('div.vendor a::text').get(),
            'name': response.css('h1.title::text').get(),
            'price': response.css('span.price::text').get(),
        }


        # truco para saber css , usando scrapy shell por terminal
        # scrapy shell 'https://sipwhiskey.com/collections/japanese-whisky/products/nikka-coffey-malt-whisky'

        # ejecutar y guardar en csv
        # scrapy runspider sip.py -o productos.csv


