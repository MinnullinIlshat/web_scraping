from bs4 import BeautifulSoup
from lxml import html 
from urllib.request import urlretrieve
from requests.sessions import Session 
import time 


def get_html_obj(url, session: Session):
    '''возвращает текстовый html объект'''
    try: 
        return session.get(url).text
    except Exception:
        return None


def get_bs(html_obj: str) -> BeautifulSoup:
    '''принимает html файд в виде строки и возвращает объект BeautifulSoup'''
    try:
        return BeautifulSoup(html_obj, 'lxml')
    except Exception:
        return None


def safe_get_str(bs: BeautifulSoup, code: str) -> str:
    try:
        return eval(code)
    except Exception:
        return ''


class Product: 
    def __init__(self, url, session: Session):
        self.session = session 
        self.url = url
        self.html = get_html_obj(url, self.sessoin)
        self.bs = get_bs(self.html)
        self.name = ''
        self.path = ''
        self.images = [] # ссылки на изображения
        self.description = '' # описание товара
        self.vendor_code = '' # артикул 
        self.price = ''
        self.old_price = '' # старая цена, если она есть


class Category:
    def __init__(self, name, url, session: Session):
        self.session = session
        self.name = name 
        self.url = url 
        self.html = get_html_obj(url, self.session)
        self.pages = self.get_pages()
        self.product_urls = self.get_product_urls()

    def get_pages(self) -> list[str]:
        '''создает url для каждой страницы категории'''
        pages = [self.url]
        res = html.fromstring(self.html)
        last = res.xpath('//a[@class="pagination-link page "]')[-1].text_content()
        link = self.url.rsplit('/', 1)[0]
        for i in range(1, int(last)):
            pages.append(f'{link}/{i}')
        return pages

    def get_product_urls(self) -> list[str]:
        '''загружает каждую старницу категории, собирает все ссылки
        на товары из каждой старницы в список, и возвращает его'''
        product_urls = [] 
        for page in self.pages:
            print('PAGE:', page[-1])
            time.sleep(1)
            html_obj = get_html_obj(page)
            bs = get_bs(html_obj)
            for item in bs.find_all(class_="product__brief"):
                product_url = item.a.get('href').strip()
                product_urls.append(product_url)
        return product_urls      

    def save_to_csv(self):
        '''Создает файл csv, в который извлекает и записывает всю инфорамцию
        по каждому продукту входяещему в категорию (category)'''
        self.products = [Product(url, self.session) for url in self.pages] 
        '''
        
        ! ! ! НАДО ДОПИСАТЬ ФУНКЦИЮ ! ! !
        
        '''


def main():
    session = Session()
    perfumery_url = 'https://chudodey.com/catalog/parfyumeriya/filters/filter10/filter_type/SG/filters/filter10/filter_name/%D0%B2%20%D0%BD%D0%B0%D0%BB%D0%B8%D1%87%D0%B8%D0%B8%20%D0%B8%20%D0%BF%D0%BE%D0%B4%20%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7/filters/filter10/values/sort/field_name/title/sort/sort_type/%D0%B2%D0%BE%D0%B7%D1%80%D0%B0%D1%81%D1%82%D0%B0%D0%BD%D0%B8%D0%B5/pager/page_number/0'
    perfumery = Category('perfumery', perfumery_url, session)
    perfumery.save_to_csv()

if __name__ == '__main__':
    main()