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
        product['name'] = response.xpath('//div[@class="col-md-12 text-center"]/h1/text()').get()
        price_pack = response.xpath('//select[@class="js-pack form-control"]')
        if price_pack:
            product["price"], product['fasovka'] = self.get_prices(price_pack)
        else: 
            product['price'] = response.xpath('//p[@class="normal-price"]/text()').get().strip()
            product['fasovka'] = response.xpath('//p[@class="ppack"]/text()').get().strip()
        product["description"] = response.xpath('//*[@class="prod-desc js-product"]/hr/following-sibling::*//text()').getall()
        product['url'] = response.url
        product['file_urls'] = self.get_file_urls(response)
        return product

    def get_file_urls(self, response):
        file_urls = []
        for link in response.xpath('//@src | //@href').getall():
            if self.is_valid_url(link):
                file_urls.append(link)
        file_urls = ['https://inshi.by/' + l for l in file_urls if 's_' not in l]
        return '\n'.join(file_urls)

    def is_valid_url(self, url: str):
        if 'templates' in url or 'cache' in url:
            return False 
        if not url.startswith('assets'):
            return False 
        return True

    def get_prices(self, price_pack):
        price = '\n'.join([item.get().strip() for item in price_pack.xpath('//option/@value')])
        fasovka = '\n'.join([item.get().strip() for item in price_pack.xpath('//option/text()')])
        return price, fasovka