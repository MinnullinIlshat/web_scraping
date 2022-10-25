from bs4 import BeautifulSoup 
from urllib.request import urlopen, urlretrieve 

with open('perfumery.html') as file: 
    bs = BeautifulSoup(file.read(), 'lxml')

class Product: 
    def __init__(self):
        self.name = '' 
        self.path = ''
        self.images = [] # ссылки на изображения
        self.description = '' # описание товара
        self.vendor_code = '' # артикул 
        self.price = '' 
        self.old_price = '' # старая цена, если она есть

class Category:
    def __init__(self, url):
        self.pages_count = 0 
        self.products: list[Product] = []