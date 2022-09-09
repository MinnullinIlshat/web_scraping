from urllib.request import urlopen
from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup 
import re 

class Contacts:
    def __init__(self, home_url):
        self.home_url = home_url 
        self.phone_numbers = []
        self.social_links = []
        self.emails = []
        self.internal_links = get_internal_links(home_url)
    
    def update_data(self):
        '''обновляет конактные данные'''
        pass

    def get_phone_numbers(self, bs):
        '''собирает все номера телефонов'''
        pass

    def get_social_links(self, bs):
        '''собирает ссылки на соц. сети'''
        pass 

    def get_emails(self, bs):
        '''собирает почты'''
        pass


def get_bsoup(url):
    '''возращает объект BeautifulSoup / при неудаче None'''
    try:
        html = urlopen(url)
        return BeautifulSoup(html, 'html.parser')
    except:
        print(f'Any error with {url}.')
        return None


def is_link_to_file(url):
    '''если это ссылка на файл - True, иначе False'''
    p = urlsplit(url).path
    if any((re.match(r'.*(?<=\.\w{3})$', p), re.match(r'.*(?<=\.\w{4})$', p))):
        if not p.endswith('.html'):
            return True
    return False 


def get_home_url(url):
    '''возвращает только schema и netloc: https://site.com/'''
    return urlsplit(url)._replace(path='', query='', fragment='').geturl()


def clean_internal_links(d, url):
    '''убирает ссылки имеющие другой hostname(попали по ошибке)'''
    return {key: val for key, val in d.items() if key.startswith(f'{url}') and val}

def get_internal_links(url, l=None):
    ''' собирает все внутренние ссылки сайта в словарь и возвращает его
        ключ словаря - ссылка, значение - объект BeautifulSoup >> {url:bs}'''
    internal_links = dict() if not l else l
    if len(internal_links) > 100:                 # ограничим кол-во страниц, экономим время
        return internal_links
    if not (bs:= get_bsoup(url)):                 # если bs не получен - останавливаем функцию
        print(f'URL {url} can\'t be checked.')
        internal_links[url] = None                # не обращаемся повторно к недоступным страницам
        return None
    print(url)
    internal_links[url] = bs                      # если bs получен, добавляем url и bs в словврь {url:bs}

    home_url = get_home_url(url) # format: https://site.com/
    href1 = re.compile(r'^(/)((?!@).)*(?<!\.\w{3})$')  
    href2 = re.compile(rf'^{home_url}.*(?<!\.\w{3})$')

    for link in bs.find_all('a', {'href': {href1, href2}}):
        link = urljoin(home_url, link.attrs['href'])
        if link not in internal_links and not is_link_to_file(link):
            get_internal_links(link, internal_links)

    return clean_internal_links(internal_links, url) if not l else None


if __name__ == '__main__':
    int_links = get_internal_links('')
    if int_links:
        for link in int_links.keys():
            print(link)
        print(len(int_links))