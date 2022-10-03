from urllib.request import urlopen 
from bs4 import BeautifulSoup
import csv 


def get_bs(url):
    try: 
        html = urlopen(url)
        return BeautifulSoup(html.read(), 'lxml')
    except Exception:
        return None 

class Good:

    def __init__(self, price_item: BeautifulSoup):
        self.price_item = price_item
        self.text = self.get_text()
        self.name = self.get_name()
        self.category = self.text[1]
        self.get_quantity_and_cost_price()
        self.get_weight_and_price_per_kg()
        self.price = self.get_price()

    def get_text(self):
        text = self.price_item.find(class_='text-muted').get_text().split('•')
        text = [w.strip() for w in text]
        return [w.replace('\xa0', '') for w in text]

    def get_name(self):
        return self.price_item.find(class_='price_good_title').get_text()

    def get_quantity_and_cost_price(self):
        if self.text[2].startswith('~'):
            self.quantity =  self.text[2].split('по')[0].strip()
            self.cost_price = self.text[2].split('по')[1].strip()
        elif self.text[3].startswith('~'):
            self.quantity = self.text[3].split('по')[0].strip()
            self.cost_price = self.text[3].split('по')[1].strip()
        else: 
            self.quantity = ''
            self.cost_price= ''

    def get_weight_and_price_per_kg(self):
        if self.text[-2].startswith('('):
            self.weight = self.text[-2].split(' по')[0].lstrip('(')
            price_per_kg = self.text[-2].split(' по')[1].strip(') ').split()
            self.price_per_kg = price_per_kg[0] if len(price_per_kg) == 1 else price_per_kg[1]
        else: 
            self.weight = ''
            self.price_per_kg = ''

    def get_price(self):
        price = self.price_item.find(class_="price_costs d-none d-sm-none d-md-table-cell").text
        price = price.split('₽')[0].replace('\xa0', '') + '₽'
        return price


def main(): 
    bs = get_bs('https://optof.biz/price/')
    if not bs: return
    price_items = bs.find_all('tr', class_='price_item')
    goods = [Good(item) for item in price_items]
    with open('optof_price.csv', 'w') as file: 
        writer = csv.writer(file)
        writer.writerow(['Наименование', 'Категория', 'Единиц в мешке', 
            'Вес мешка', 'Цена за ед.', 'Цена мешка', 'Цена за 1 кг'])
        for good in goods: 
            writer.writerow((good.name, good.category, good.quantity,
                good.weight, good.cost_price, good.price, good.price_per_kg))

if __name__ == '__main__':
    main()