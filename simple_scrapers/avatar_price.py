from bs4 import BeautifulSoup
from urllib.request import urlopen
from bs4.element import Tag
import csv


def get_bs(url) -> BeautifulSoup:
    '''открывает страницу и возвращает объект BeautifulSoup'''
    print(url)
    try: 
        html = urlopen(url)
        return BeautifulSoup(html.read(), 'lxml')
    except Exception:
        return None 

def get_exchange_rate_and_data(bs: BeautifulSoup) -> tuple:
    '''возвращает дату и текущий курс евро'''
    try:
        course = bs.select_one('.catalog-course').get_text()
        data, course = course.split(' | ')
        return data, course
    except Exception:
        return ('', '')

def get_items(bs: BeautifulSoup) -> list:
    '''принимает объект bs, и возвращает все объекты Item со страницы'''
    items = bs.select('.line > .right')[1:]
    item_urls = [get_url_from_item(item) for item in items]
    return [Item(url) for url in item_urls]

def get_url_from_item(item: Tag) -> str:
    '''принимает Tag который содержит информацию об обном объекте из прайса
    и возвращает ссылку на него'''
    return "https://tdavatar.ru" + item.find(class_='block size2').a.attrs['href']

class Item:
    def __init__(self, item_url: str):
        self.info = get_bs(item_url).select_one('.catalog-detail__info')
        self.name = self.safe_get("self.info.select_one('.catalog-detail__category').text")
        self.country = self.safe_get("self.info.find('span', text='Страна:').next_sibling.next_sibling.text")
        self.category = self.safe_get("self.info.find('span', text='Категория:').next_sibling.next_sibling.text")
        self.weight = self.safe_get("self.info.find('span', text='Вес:').next_sibling.next_sibling.text")
        self.price = self.safe_get("self.info.select_one('.product-item-detail-info-container > "
            "div:nth-of-type(2)').text.replace('\xa0', '').strip()")
        self.price_per_kg = self.safe_get("self.info.select('.catalog-detail-price__value')[1].text.strip()")

    def safe_get(self, code: str) -> str:
        try:
            return eval(code)
        except Exception:
            return ''


def main():
    items = []
    for page in range(1, int(input("How many pages are there on the price?\n> "))+1):
        url = f'https://tdavatar.ru/price/filter/city_avail-is-sankt-peterburg-or-moskva-or-nizhniy-novgorod-or-kirov-or-chelyabinsk/apply/?PAGEN_1={page}'
        items.extend(get_items(bs:= get_bs(url)))
    with open('avatar_price.csv', 'w') as file: 
        writer = csv.writer(file)
        writer.writerow(get_exchange_rate_and_data(bs))
        writer.writerow(('Наименование', 'Страна', 'Категория', 'Вес мешка', 'Цена мешка', 'Цена за кг'))
        for item in items:
            writer.writerow((item.name, item.country, item.category, 
                item.weight, item.price, item.price_per_kg))
    

if __name__ == '__main__':
    main()