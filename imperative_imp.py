# Implements the imperative approach with mutable global state and step-by-step logic.
from config import db_config
class stock_management_imperative:
        
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

    def add_product(product_id, name, price, quantity):
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Products (id, name, price, quantity) VALUES (?, ?, ?, ?)", 
                    (product_id, name, price, quantity))
        conn.commit()
        conn.close()

    def update_stock(product_id, quantity_change):
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT quantity FROM Products WHERE id = ?", (product_id,))
        result = cursor.fetchone()
        if not result:
            print("Product not found!")
            return
        new_quantity = result[0] + quantity_change
        cursor.execute("UPDATE Products SET quantity = ? WHERE id = ?", (new_quantity, product_id))
        conn.commit()
        conn.close()

    def process_order(product_id, order_quantity):
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT price, quantity FROM Products WHERE id = ?", (product_id,))
        result = cursor.fetchone()
        if not result:
            print("Product not found!")
            return
        price, quantity = result
        if quantity < order_quantity:
            print("Insufficient stock!")
            return
        total_cost = price * order_quantity
        new_quantity = quantity - order_quantity
        cursor.execute("UPDATE Products SET quantity = ? WHERE id = ?", (new_quantity, product_id))
        conn.commit()
        conn.close()
        print(f"Order processed. Total cost: {total_cost}")

    def generate_low_stock_report(threshold):
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Products WHERE quantity < ?", (threshold,))
        result = cursor.fetchall()
        conn.close()
        return result

    def generate_inventory_value_report():
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(price * quantity) FROM Products")
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0
