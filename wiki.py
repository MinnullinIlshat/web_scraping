from urllib.request import urlopen 
from bs4 import BeautifulSoup 
import re 


pages = set()
def get_links(page_url):
    global pages 
    html = urlopen(f'http://en.wikipedia.org{page_url}')
    bs = BeautifulSoup(html, 'html.parser')
    try:
        print(bs.h1.get_text())
        print(bs.find(id='mw-content-text').find_all('p')[0])
        print(bs.find(id='ca-edit').find('span').find('a').attrs['href'])
    except AttributeError:
        print('This page is missing something! Continuing.')
    for link in bs.find_all('a', href=re.compile(r'^(/wiki/)')):
        if 'href' in link.attrs:
            if (new_page:=link.attrs['href']) not in pages:
                # мы нашли новую страницу 
                print('-'*20)
                print(new_page)
                pages.add(new_page)
                get_links(new_page)

get_links('')