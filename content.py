import requests 
from bs4 import BeautifulSoup
from urllib.request import urlopen


class Crawler:
    def get_page(self, url):
        try: 
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None 
        return BeautifulSoup(req.text, 'html.parser')

    def safe_get(self, page_obj, selector):
        '''функция используется для получения получения строки
        содержимого из объека bs и селектора. Если объект
        селектора не найдет, возвращает пустую строку'''
        selected_elems = page_obj.select(selector)
        if selected_elems:
            return '\n'.join([elem.get_text() for elem in selected_elems])
        return '' 

    def parse(self, site, url):
        '''извлекает содержимое страницы с заданным URL'''
        bs = self.get_page(url)
        if bs:
            title = self.safe_get(bs, site.title_tag)
            body = self.safe_get(bs, site.body_tag)
        if title and body:
            content = Content(url, title, body)
            content.print()
            

class Content:
    def __init__(self, url, title, body):
        self.url = url 
        self.title = title
        self.body = body 

    def print(self):
        print(f'URL: {self.url}')
        print(f'TITLE: {self.title}')
        print(f'BODY\n{self.body}')


class Website:
    def __init__(self, name, url, title_tag, body_tag):
        self.name = name 
        self.url = url 
        self.title_tag = title_tag 
        self.body_tag = body_tag 

crawler = Crawler()

site_data = [
    ['O\'Reilly Media', 'http://oreilly.com',
    'h1', 'section#product-description'],
    ['Reuters', 'http://reuters.com', 'h1',
    'div.StandardArticleBody_body_1gnLA'],
    ['Brookings', 'http://www.brookings.edu',
    'h1', 'div.post-body'],
    ['New York Times', 'http://nytimes.com',
    'h1', 'p.story-content']
]

websites = []

for row in site_data:
    websites.append(Website(*row))

crawler.parse(websites[0], 'http://shop.oreilly.com/product/'\
    '0636920028154.do')
crawler.parse(websites[1], 'http://www.reuters.com/article/'\
    'us-usa-epa-pruitt-idUSKBN19W2D0')
crawler.parse(websites[2], 'https://www.brookings.edu/blog/'\
    'techtank/2016/03/01/idea-to-retire-old-methods-of-policy-education/')
crawler.parse(websites[3], 'https://www.nytimes.com/2018/01/'\
    '28/business/energy-environment/oil-boom.html')