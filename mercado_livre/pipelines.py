# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

from itemadapter import ItemAdapter


class MercadoLivrePipeline:
    def __init__(self):
        print("Initializing database connection...")
        uri = "mongodb+srv://uptotaskcompany:R4Os7kZODtHg68BP@mercadolivrecluster.ujh7tr3.mongodb.net/?retryWrites=true&w=majority&appName=mercadoLivreCluster"

        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client.mercado_livre

    def process_item(self, item, spider):
        print("Processing item...")
        current_time = datetime.now()
        product = {
            '_id': item['id'],
            'name': item['name'],
            'url': item['url'],
            'rating_number': item['rating_number'],
            'rating_amount': item['rating_amount'],
            'price':item['price'],
            'create_at': current_time,
        }
        product_prices = {
            'product_id': item['id'],
            'price': item['price'],
            'price_date': current_time
        }

        result = self.db.products.update_one(
            {"_id": product["_id"]},  # Query to find the document
            {"$set": product},        # Data to insert or update
            upsert=True
        )
        if result.upserted_id:
             print(f"Product {product['_id']} inserted into database.")
        else:
            print(f"Product {product['_id']} updated in database.")

        self.db.product_prices.insert_one(product_prices)
        print(f"Product price {product_prices['price']} inserted into database.")
        
        return item

    def close_spider(self, spider):
        print("Closing spider...")
        self.client.close()
        print("Database connection closed.")
