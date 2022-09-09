import requests 
from bs4 import BeautifulSoup


class Content:
    '''базовый класс для статей и страниц'''
    def __init__(self, topic, url, title, body):
        self.topic = topic 
        self.url = url 
        self.title = title 
        self.body = body 

    def print(self):
        print(f'New article found for topic: {self.topic}')
        print(f'TITLE: {self.title}')
        print(f'BODY:\n{self.body}')
        print(f'URL: {self.url}')


class Website:
    '''содержит информацию о структуре сайта'''
    def __init__(self, name, url, search_url, result_listing,
        result_url, absolute_url, title_tag, body_tag):
        self.name = name 
        self.url = url 
        self.search_url = search_url 
        self.result_listing = result_listing 
        self.result_url = result_url 
        self.absolute_url = absolute_url
        self.title_tag = title_tag 
        self.body_tag = body_tag 


class Crawler:

    def get_page(self, url):
        try: 
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None 
        return BeautifulSoup(req.text, 'html.parser')

    def safe_get(self, page_obj, selector):
        child_obj = page_obj.select_one(selector)
        if child_obj:
            return child_obj.get_text() 
        return '' 

    def search(self, topic, site):
        '''ищет тему topic на сайте site и сохранаяет результаты'''
        bs = self.get_page(site.search_url + topic)
        search_results = bs.select(site.result_listing)
        for result in search_results:
            url = result.select_one(site.result_url).attrs['href']
            if not site.absolute_url:
                url = site.url + url
            bs = self.get_page(url)
            if not bs:
                print("Something was wrong with that page or URL. Skipping!")
                return 
            title = self.safe_get(bs, site.title_tag)
            body = self.safe_get(bs, site.body_tag)
            if title and body: 
                content = Content(topic, title, body, url)
                content.print() 

crawler = Crawler() 

site_data = [
    ['O\'Reilly Media', 'http://oreilly.com',
    'https://ssearch.oreilly.com/?q=','article.product-result',
    'p.title a', True, 'h1', 'section#product-description'],
    ['Reuters', 'http://reuters.com',
    'http://www.reuters.com/search/news?blob=',
    'div.search-result-content','h3.search-result-title a',
    False, 'h1', 'div.StandardArticleBody_body_1gnLA'],
    ['Brookings', 'http://www.brookings.edu',
    'https://www.brookings.edu/search/?s=',
    'div.list-content article', 'h4.title a', True, 'h1',
    'div.post-body']
]
sites = [] 
for row in site_data:
    sites.append(Website(*row))

topics = ['python', 'data science']
for topic in topics:
    print('GETTING INFO ABOUT: ' + topic)
    for target_site in sites:
        crawler.search(topic, target_site)

