from scrapy.linkextractors import LinkExtractor 
from scrapy.spiders import CrawlSpider, Rule 
from wikiSpider.items import Article 

class ArticleSpider(CrawlSpider):
    name = 'article_items'
    allowed_domains = ['wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Game_of_Thrones']
    rules = [
        Rule(LinkExtractor(allow=r'^(/wiki/)((?!:).)*$'),
            callback='parse_items', follow=True),
        Rule(LinkExtractor(
            allow=r'^(https://en.wikipedia.org/wiki/)((?!:).)*$'),
            callback='parse_items', follow=True),
    ]

    def parse_items(self, response):
        article = Article() 
        article['url'] = response.url
        article['title'] = response.xpath(
            '//*[@id="mw-content-text"]/div[1]/p[2]/b[1]/text()').get()
        article['text'] = response.xpath(
            '//div[@id="mw-content-text"]/'
            'div[@class="mw-parser-output"]/p/text()').getall()
        article['last_updated'] = response.css(
            'li#footer-info-lastmod::text').get()
        return article 