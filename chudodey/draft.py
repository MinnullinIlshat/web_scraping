from bs4 import BeautifulSoup
from lxml import html 
from urllib.request import urlopen 


def get_html_obj(url):
    '''возвращает текстовый html объект'''
    try: 
        return urlopen(url).read()
    except Exception:
        return None


def get_bs(html_obj: str) -> BeautifulSoup:
    '''принимает html файд в виде строки и возвращает объект BeautifulSoup'''
    try:
        return BeautifulSoup(html_obj, 'lxml')
    except Exception:
        return None


def get_pages(html_obj, url) -> list[str]:
    '''создает url для каждой страницы категории'''
    pages = [url]
    res = html.fromstring(html_obj)
    last = res.xpath('//a[@class="pagination-link page "]')[-1].text_content()
    link = url.rsplit('/', 1)[0]
    for i in range(1, int(last)):
        pages.append(f'{link}/{i}')
    return pages


def get_product_urls(pages: list) -> list[str]:
    product_urls = [] 
    for page in self.pages:
        pass

#########################################################################
with open('perfumery.html') as file: 
    html_obj = file.read()

url = 'https://chudodey.com/catalog/parfyumeriya/filters/filter10/filter_type/SG/filters/filter10/filter_name/%D0%B2%20%D0%BD%D0%B0%D0%BB%D0%B8%D1%87%D0%B8%D0%B8%20%D0%B8%20%D0%BF%D0%BE%D0%B4%20%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7/filters/filter10/values/sort/field_name/title/sort/sort_type/%D0%B2%D0%BE%D0%B7%D1%80%D0%B0%D1%81%D1%82%D0%B0%D0%BD%D0%B8%D0%B5/pager/page_number/0'
pages = get_pages(html_obj, url)

bs = get_bs(html_obj)

for item in bs.find_all(class_="product__brief"):
    url = item.a.get('href').strip()
    print('URL:  ', url)
    print()