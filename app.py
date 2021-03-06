
from collections import OrderedDict
import sys
import csv
import datetime
import os

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
# Reads, cleans and installs the csv data into a list.
# Learned how to change dollars to cents from this site: https://codereview.stackexchange.com/questions/121074/safely-convert-dollars-to-cents/121077
# Reminded me about how to strip the $: https://stackoverflow.com/questions/3887469/python-how-to-convert-currency-to-decimal
    with open('inventory.csv') as csvfile:
        store_list = csv.DictReader(csvfile, delimiter=',')
        rows = list(store_list)
        for row in rows:
            row['product_name'] = row['product_name']
            row['product_price'] = float(row['product_price'].replace('$','')) * 100
            row['product_quantity'] = int(row['product_quantity'])
            row['date_updated'] = datetime.datetime.strptime(row['date_updated'], '%m/%d/%Y')
            try:
                Product.create(
                product_name=row['product_name'], 
                product_price=row['product_price'], 
                product_quantity=row['product_quantity'], 
                date_updated=row['date_updated']
                ).save()

            except IntegrityError:
                product_list = Product.get(product_name=row['product_name'])

                if product_list.date_updated <= row['date_updated']:
                    product_list.product_price = row['product_price']
                    product_list.product_quantity = row['product_quantity']
                    product_list.date_updated = row['date_updated']
                    product_list.save()


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

    
def view_menu():
# Using OrderedDict to create, view and access the inventory's menu.
    result = None    
    while True:
        print('\n','=== MENU OPTIONS ===','\n')
        for key,value in menu.items():
            print('{}) {}'.format(key, value.__doc__))           
        result = input('Enter your choice here:  ').lower().strip()
        print('\n')
        
        if result in menu:
            clear()
            menu[result]()

        elif result not in menu:
            print('\n','Please try an option from the menu.')
   

def display_products():
    """Display inventory items.""" 
# Displays the inventory 1 product at a time.
    product_entry = Product.select().order_by(Product.product_id.desc())               
    for product in product_entry:
        clear()
        print('\n')
        print(' ID:', product.product_id, '\n',
        'Product:', product.product_name,'\n',
        'Price: $', product.product_price/100, '\n',
        'Quantity:', product.product_quantity, '\n',
        'Last updated:', product.date_updated.strftime('%m/%d/%Y'),
        '\n', '\n')       
       
        print('q) Return to main menu.')
        print('d) Delete product')
        print('Or press enter to see the next product.','\n')  
    
        choice = input('Enter your choice here:  ').lower().strip()
        print('\n')
        if choice == 'q':
            clear()
            break
        elif choice == 'd':
            delete_product(product)


def delete_product(product):
    if input('Delete product? (y/n)  ').lower() == 'y':
        Product.delete_instance(product)
        print('Product deleted.')


def search_product():
    """Search for product by ID#."""   
# Allows user to search products by the inventory id#.
# Recieved assistance from Jennifer Nordell to use and utilize the get_by_id function. 
    while True:
        try:
            search = int(input('Enter the product ID you wish to search for:  ')) 
        except ValueError:
            print('Invalid character, please try again.')           
        else:
            try:
                item = Product.get_by_id(search)
            except Product.DoesNotExist:   
                print('Invalid ID, please try again.')
            else:
                clear()
                print('\n')
                print(' ID:', item.product_id, '\n',
                'Product:', item.product_name,'\n',
                'Price: $', item.product_price/100, '\n',
                'Quantity:', item.product_quantity, '\n',
                'Last updated:', item.date_updated.strftime('%m/%d/%Y'),
                '\n', '\n') 
                break
                                       

def new_product_name():
    new = Product()
    while True:
        try:    
            new.name = input('Enter product name:  ')

        except ValueError:
            print('Invalid character, please try again.')
            continue
        else:
            break
    return new.name


def new_product_price():
    new = Product()
    while True:
        try:
            new.price = float(input('Enter product price:$  '))
            new.price = int(new.price * 100)
        
        except ValueError:
            print('Invalid character, please try again.')
            continue
        else:
            break
    return new.price


def new_product_quantity():
    new = Product()
    while True:
        try:
            new.quantity = int(input('Enter product quantity:  '))

        except ValueError:
            print('Invalid character, please try again.')
            continue
        else:
            break
    return new.quantity


def add_product():
    """Add a product to inventory."""
# Collects data from the users and inputs a new product into the inventory.   
    new_name = new_product_name()
    new_price = new_product_price()
    new_quantity = new_product_quantity()
        
    if input('Would you like to save this product? (y/n)  ').lower() != 'n': 
        try:
            Product.create(
            product_name = new_name, 
            product_price = new_price, 
            product_quantity = new_quantity).save()
            print('Product saved.')

        except IntegrityError:
            product_list = Product.get(product_name=new_name)
            product_list.product_name = new_name
            product_list.product_price = new_price
            product_list.product_quantity = new_quantity        
            product_list.save()


def backup_csv():
    """Backup inventory.""" 
# Creates a backup inventory.
    
    with open('backup.csv', 'w', newline='') as csvfile:
        fieldnames = ['product_name', 'product_price', 'product_quantity', 'date_updated']
        inventorywriter = csv.DictWriter(csvfile, fieldnames=fieldnames)

        inventorywriter.writeheader() 
        backup = Product.select().order_by(Product.product_id.asc())            
        for product in backup:
            inventorywriter.writerow({
            'product_name': product.product_name, 
            'product_price': '$' + '{}'.format(product.product_price / 100), 
            'product_quantity': product.product_quantity,     
            'date_updated': product.date_updated.strftime('%m/%d/%Y')}) 
        print('Successfully updated!')   


def quit_inventory():
    """Quit."""
    sys.exit('Have a great day!')


menu = OrderedDict([
    ('v', search_product),
    ('d', display_products),
    ('a', add_product),
    ('b', backup_csv),
    ('q', quit_inventory)
    ])


if __name__ == '__main__':
    initialize()
    csv_data()
    view_menu()
