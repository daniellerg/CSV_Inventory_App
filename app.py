
from collections import OrderedDict
import sys
import csv
import datetime

from peewee import *


db = SqliteDatabase('inventory.db')


class Product(Model):
    product_id = PrimaryKeyField()
    product_name = CharField(max_length=100, unique=True)
    product_price = IntegerField()
    product_quantity = IntegerField()
    date_updated = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


def initialize():
    db.connect()
    db.create_tables([Product], safe=True)
    db.close


def csv_data():
# Learned how to change dollars to cents from this site: https://codereview.stackexchange.com/questions/121074/safely-convert-dollars-to-cents/121077
# Reminded me about how to strip the $: https://stackoverflow.com/questions/3887469/python-how-to-convert-currency-to-decimal
    with open('inventory.csv') as csvfile:
        store_list = csv.DictReader(csvfile, delimiter=',')
        rows = list(store_list)
        for row in rows:
            row['product_name'] = row['product_name']
            row['product_price'] = int(float(row['product_price'].strip('$'))) * 100
            row['product_quantity'] = int(row['product_quantity'])
            row['date_updated'] = datetime.datetime.strptime(row['date_updated'], '%m/%d/%Y')
        try:
            Product.create(product_name=row['product_name'], 
            product_price=row['product_price'], 
            product_quantity=row['product_quantity'], 
            date_updated=row['date_updated'])

        except IntegrityError:
            product_list = Product.get(product_name=row['product_name'])
            product_list.product_price = row['product_price']
            product_list.product_quantity = row['product_quantity']
            product_list.date_updated = row['date_updated']
            product_list.save()


def view_menu():
    result = None    
    while True:
        print('\n','=== MENU OPTIONS ===','\n')
        for key,value in menu.items():
            print('{}) {}'.format(key, value.__doc__))           
        result = input('Enter your choice here:  ').lower().strip()
        
        if result in menu:
            menu[result]()

        elif result not in menu:
            print('\n','Please try an option from the menu.')

   

def display_product(search_query=None):
    """Find an inventory item."""  
    product_entry = Product.select().order_by(Product.product_id.desc())

    if search_query:
        product_entry = Product.select().where(Product.product_id==search_query)
        
    for product in product_entry:
        print(product)  
        print('Press enter to see next product.')  
        print('q) return to main menu.')
        print('d) delete product')

        choice = input('Enter your choice here:  '.lower().strip())

        if choice == 'q':
            break

        elif choice == 'd':
            delete_product(product)


def delete_product(product):
    if input("Delete product? (y/n)  ").lower() == 'y':
        Product.delete_instance()
        print('Product deleted.')


def search_product():
    while True:
        try:
            search_query = display_product(int(input('Enter the product id you wish to search:  '.strip())))
            if search_query != Product.product_id:
                raise ValueError

        except ValueError:
            print('Product id does not exist.')
            search_query = display_product(int(input('Enter the product id you wish to search:  '.strip())))


def add_product():
    """Add a product to inventory."""
    add_item = Product()

    try:
        add_item.product_name = input('Enter product name:  ')
        add_item.product_price = input('Enter product price:  ')
        add_item.product_quantity = input('Enter product quantity:  ')
        save = input('Would you like to save this product? (y/n)  '.lower())

        if save != 'n':
            add_item.save()
            print('Product saved.')

    except IntegrityError:
        product_list = Product.get(product_name=row['product_name'])
        if product_list.date_updated == datetime.datetime.now:
            product_list.product.name = row('product_name')
            product_list.product_price = row['product_price']
            product_list.product_quantity = row['product_quantity']          
            product_list.save()
    

def back_up_csv():
   """Backup inventory.""" 
   with open('new_inventory.csv', 'a') as csvfile:
       fieldnames = ['product_name', 'product_price', 'product_quantity', 'date_updated']
       inventorywriter = csv.DictWriter(csvfile, fieldnames=fieldnames)

       inventorywriter.writeheader()
       #inventorywriter.writerow()


def quit_inventory():
    """Quit."""
    sys.exit('Have a great day!')


menu = OrderedDict([
    ('v', display_product),
    ('a', add_product),
    ('b', back_up_csv),
    ('q', quit_inventory)
    ])


if __name__ == '__main__':
    initialize()
    csv_data()
    view_menu()