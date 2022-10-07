from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from inshi.items import Product

class CatalogueSpider(CrawlSpider): 
    name='catalog_spider'
    start_urls = ["https://inshi.by/katalog/instrument", "https://inshi.by/katalog/remmers"]
    allowed_domains = ["inshi.by"]
    rules = [Rule(LinkExtractor(allow=r'^.*inshi.by\/katalog\/remmers\/[\w-]+\/[\w-]+\/.*$'), 
        callback='parse_items', follow=False), # <- товары remmers
        Rule(LinkExtractor(allow=r'^.*inshi.by\/katalog\/instrument\/[\w-]+\/.*$'),
            callback='parse_items', follow=False)] # <- товары instruments

    def parse_items(self, response):
        product = Product()
        product["description"] = response.xpath('//*[@class="prod-desc js-product"]/hr/following-sibling::*//text()').getall()
        price_pack = response.xpath('//select[@class="js-pack form-control"]')
        if price_pack:
            product["price"], product['fasovka'] = self.get_prices(price_pack)
        else: 
            product['price'] = response.xpath('//p[@class="normal-price"]/text()').get().strip()
            product['fasovka'] = response.xpath('//p[@class="ppack"]/text()').get().strip()
        product['name'] = response.xpath('//div[@class="col-md-12 text-center"]/h1/text()').get()
        return product

    def save_files(self, response):
        pdf_url = response.xpath('//strong[text()="Техническое описание: "]/following-sibling::a[1]/@href').get()
        path = ''

    def get_prices(self, price_pack):
        price = '\n'.join([item.get().strip() for item in price_pack.xpath('//option/@value')])
        fasovka = '\n'.join([item.get().strip() for item in price_pack.xpath('//option/text()')])
        return price, fasovka