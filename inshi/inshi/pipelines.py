# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from inshi.items import Product


class ProductPipeline:
    def process_item(self, product: Product, spider):
        product.description = self.clean_description(product.description)
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