from scrapy.linkextractors import LinkExtractor 
from scrapy.spiders import CrawlSpider, Rule

class ArticleSpider(CrawlSpider):
    name = 'articles'
    allowed_domains = ['wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/'
        'Benevolent_dictator_for_life']
    rules = [
        Rule(LinkExtractor(allow=r'^(/wiki/)((?!:).)*$'),
            callback='parse_items', follow=True,
            cb_kwargs={'is_article': True}),
        Rule(LinkExtractor(allow=r'^(https://en.wikipedia.org/wiki/)((?!:).)*$'),
            callback='parse_items', follow=True,
            cb_kwargs={'is_article': True}),
        Rule(LinkExtractor(allow=r'.*'), callback='parse_items',
            cb_kwargs={'is_article': False})
    ]

    def parse_items(self, response, is_article):
        print(response.url)
        title = response.xpath('//*[@id="mw-content-text"]/div[1]/p[2]/b[1]/text()').get()
        if is_article:
            url = response.url 
            text = response.xpath('//div[@id="mw-content-text"]/'
                'div[@class="mw-parser-output"]/p/text()').getall()
            last_updated = response.css('li#footer-info-lastmod'
                '::text').get() 
            last_updated = last_updated.replace('This page was '
                'last edited on ', '')
            print(f'URL is: {url}')
            print(f'Title is: {title}')
            print(f'text is: {text}')
        else: 
            print(f'This is not an article: {title}')

        