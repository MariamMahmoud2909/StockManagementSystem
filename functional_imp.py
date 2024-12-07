# Implements the functional approach with immutable data and recursive transformations.
from config import db_config

class stock_management_functional:
    
    def initialize_db():
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Products' AND xtype='U')
        CREATE TABLE Products (
            id INT PRIMARY KEY,
            name NVARCHAR(50),
            price FLOAT,
            quantity INT
        )
        """)
        conn.commit()
        conn.close()

    def add_product(products, product):
        if not products:
            return [product]
        if products[0]['id'] == product['id']:
            print("Product already exists!")
            return products
        return [products[0]] + add_product(products[1:], product)

    def update_stock(products, product_id, quantity_change):
        if not products:
            return []
        product = products[0]
        if product['id'] == product_id:
            updated_product = {**product, 'quantity': product['quantity'] + quantity_change}
            return [updated_product] + products[1:]
        return [product] + update_stock(products[1:], product_id, quantity_change)

    def process_order(products, product_id, order_quantity):
        if not products:
            print("Product not found!")
            return products, 0
        product = products[0]
        if product['id'] == product_id:
            if product['quantity'] < order_quantity:
                print("Insufficient stock!")
                return products, 0
            updated_product = {**product, 'quantity': product['quantity'] - order_quantity}
            return [updated_product] + products[1:], product['price'] * order_quantity
        updated_products, total_cost = process_order(products[1:], product_id, order_quantity)
        return [product] + updated_products, total_cost

    def generate_low_stock_report(products, threshold):
        if not products:
            return []
        product = products[0]
        if product['quantity'] < threshold:
            return [product] + generate_low_stock_report(products[1:], threshold)
        return generate_low_stock_report(products[1:], threshold)

    def generate_inventory_value(products):
        if not products:
            return 0
        product = products[0]
        return product['price'] * product['quantity'] + generate_inventory_value(products[1:])
