from urllib.request import urlopen
from urllib.parse import urlparse, urlsplit, urljoin
from bs4 import BeautifulSoup 
import re 

class ContactSearcher(BeautifulSoup):
    # создает объект bs и ищет все контакты на странице
    def get_phone_numbers(self):
        # собирает все номера телефонов
        pass

    def get_social_links(self):
        # собирает ссылки на соц сети 
        pass 

    def get_emails(self):
        # собирает emails
        pass


def get_internal_links(url, l=None):
    # проходит по всем страницам сайта и собираеет внутренние ссылки
    internal_links = [] if not l else l
    internal_links.append(url)
    print(f"\n LENGTH: {len(internal_links)} \n")
    html = urlopen(url)
    print('url', url)
    bs = BeautifulSoup(html, 'html.parser')

    home_url = urlsplit(url)._replace(path='', query='', fragment='').geturl()

    href1 = re.compile(r'^(/)((?!@).)*(?<!\.\w{3})$')
    href2 = re.compile(rf'^{home_url}.*(?<!\.\w{3})$')

    for link in bs.find_all('a', {'href': {href1, href2}}):
        print('1 href', link.attrs['href'])
        link = urljoin(home_url, link.attrs['href'])
        if link not in internal_links:
            print('1 link', link)
            get_internal_links(link, internal_links)

    return internal_links if not l else None


'''
from base64 import urlsafe_b64decode
from urllib.request import urlopen
from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup 
import re 


def get_bsoup(url):
    try:
        html = urlopen(url)
        return BeautifulSoup(html, 'html.parser')
    except:
        print(f'Any error with {url}.')
        return None

def get_internal_links(url, l=None):
    # проходит по всем страницам сайта и собираеет внутренние ссылки
    internal_links = dict() if not l else l
    if len(internal_links) > 50:                 # не собираем слишком много страниц, экономим время
        return internal_links
    bs = get_bsoup(url)
    if not bs:                                   # если bs не получен - останавливаем функцию
        print(f'URL {url} can\'t be checked.')
        return None
    internal_links[url] = bs                     # если bs получен, добавляем url и bs в словврь {url:bs}

    home_url = urlsplit(url)._replace(path='', query='', fragment='').geturl()
    href1 = re.compile(r'^(/)((?!@).)*(?<!\.\w{3})$')
    href2 = re.compile(rf'^{home_url}.*(?<!\.\w{3})$')

    for link in bs.find_all('a', {'href': {href1, href2}}):
        print('\nHREF:', link.attrs['href'])
        link = urljoin(home_url, link.attrs['href'])
        if link not in internal_links:
            print('link', link)
            get_internal_links(link, internal_links)

    return internal_links if not l else None

int_links = get_internal_links('https://autlet.ru/')

for key in int_links.keys():
    print(key)

print(len(int_links))'''