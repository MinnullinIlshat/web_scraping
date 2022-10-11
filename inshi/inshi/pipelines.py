# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from inshi.items import Product
from urllib.request import urlretrieve 
import os 


class InshiPipeline:
    def process_item(self, product: Product, spider):
        product['description'] = self.clean_description(product['description'])
        file_urls = product['file_urls'].split('\n')
        self.save_files(product, file_urls)
        return product

    def clean_description(self, description):
        words = []
        for word in description:
            if word.startswith('Оставить отзыв') or word.startswith('Техническое описание'):
                break 
            words.append(word)
        words = ''.join(words)
        words = words.strip(' \r\n\t\xa0')
        return words

    def save_files(self, product: Product, file_urls: list):
        '''принимает продукт, извлекает из него url и создает папку для продукта.
        скачивает все изображения и файлы pdf (принимает их как список file_urls)'''
        path = self.get_path(product['url'], 'files')
        for url in file_urls:
            if path and url: 
                filename = url.split('/')[-1]
                urlretrieve(url, path+'/'+filename)

    def get_path(self, url: str, download_path) -> str:
        '''принимает url товара, и создает соответствующую папку если её не существует.
        возвращает путь папки'''
        path = url.replace('https://inshi.by', download_path)
        if not os.path.exists(path):
            os.makedirs(path)
        return path 