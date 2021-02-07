#!/usr/bin/env python3 

from collections import OrderedDict
import csv
import datetime

from peewee import *


db = SqliteDatabase('inventory.db')




class Product(Model):
    product_id = PrimaryKeyField()
    product_name = CharField(max_length=100, unique=True)
    product_quanity = IntegerField()
    product_price = IntegerField()
    date_updated = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


def initialize():
    db.connect()
    db.create_tables([Product], safe=True)


def csv_data():
# Learned how to change dollars to cents from this site: https://codereview.stackexchange.com/questions/121074/safely-convert-dollars-to-cents/121077
# Reminded me about how to strip the $: https://stackoverflow.com/questions/3887469/python-how-to-convert-currency-to-decimal
    with open('inventory.csv', newline=' ') as csvfile:
        store_list = csv.DictReader(csvfile, delimiter=',')
        rows = list(store_list)
        for row in rows:
            row['product_id'] = primary_key
            row['product_quanity'] = int(row['product_quanity'])
            row['product_price'] = float(row['product_price' * 100].strip('$'))
            row['date_updated'] = datetime.datetime.strptime(row['date_updated'])
        try:
            Product.create(product_name=row['product_name'], 
            product_quanity=row['product_quanity'], 
            product_price=row['product_price'], 
            date_updated=row['date_updated']).save()

        except IntegrityError:
            product_list = Product.get(product_name=row['product_name'])
            product_list.product_quanity = row['product_quanity']
            product_list.product_price = row['product_price']
            product_list.date_updated = row['date_updated']
            product_list.save()

def view_menu():
    result = None
    
    while choice != 'q':
        print('Enter q to quit.')
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
            result = input('Enter your choice here:  ').lower().strip()

            if result in menu:
                menu[result]()

    

def display_product():
    """Find and display item by it's product id."""
    pass

def add_product():
    """Add a new product."""
    try:
        print('Enter your product name:   ')
    except IntegrityError:
        product_list = Product.get(product_name=row['product_name'])
        if product_list.date_updated == datetime.datetime.now:
            product_list.product.name = row('product_name')
            product_list.product_quanity = row['product_quanity']
            product_list.product_price = row['product_price']
            product_list.save()
    pass

def back_up_csv():
   """Back up this file.""" 



menu = OrderedDict([
    ('v', display_product),
    ('a', add_product),
    ('b', back_up_csv)
    ])


if __name__ == '__main__':
    initialize()
    csv_data()
    view_menu()