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

internal_links = []

def get_internal_links(url, l=None):
    # проходит по всем страницам сайта и собираеет внутренние ссылки
    internal_links = [] if not l else l
    internal_links.append(url)
    print(f"\n LENGTH: {len(internal_links)} \n")
    html = urlopen(url)
    print('url', url)
    bs = BeautifulSoup(html, 'html.parser')

    home_url = urlsplit(url)._replace(path='', query='', fragment='').geturl()
    for link in bs.find_all('a', href=re.compile(r'^(/)((?!@).)*[^(jpg)(gif)(png)(jpeg)]$')):
        print('1 href', link.attrs['href'])
        link = urljoin(home_url, link.attrs['href'])
        if link not in internal_links:
            print('1 link', link)
            get_internal_links(link, internal_links)

    for link in bs.find_all('a', href=re.compile(rf'^{home_url}.*[^(jpg)(gif)(png)(jpeg)]$')):
        print('2 href', link.attrs['href'])
        if (link:= urljoin(home_url, link.attrs['href'])) not in internal_links:
            print('2', link)
            get_internal_links(link, internal_links)
    return internal_links if not l else None