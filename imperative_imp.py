class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

class Inventory:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_product(self, product):
        query = f"""
        INSERT INTO Products (name, price, quantity)
        VALUES ('{product.name}', {product.price}, {product.quantity})
        """
        self.db_manager.execute_query(query)

    def update_product(self, product_id, name=None, price=None, quantity=None):
        updates = []
        if name:
            updates.append(f"name = '{name}'")
        if price is not None:
            updates.append(f"price = {price}")
        if quantity is not None:
            updates.append(f"quantity = {quantity}")
        update_query = ", ".join(updates)
        query = f"UPDATE Products SET {update_query} WHERE product_id = {product_id}"
        self.db_manager.execute_query(query)

    def delete_product(self, product_name):
        query = f"DELETE FROM Products WHERE name = '{product_name}'"
        self.db_manager.execute_query(query)
        
    def check_product_availability(self, product_name):
        query = f"SELECT price, quantity FROM Products WHERE name = '{product_name}'"
        result = self.db_manager.fetch_all(query)
        if not result:
            print("Product Not Found!") 
        else :
            print("Product Available") 
        
    def generate_low_stock_items_report(self):
        query = f"SELECT product_id,name,quantity FROM Products WHERE quantity < threshold"
        return self.db_manager.fetch_all(query)
    
    def update_threshold(self, threshold):
        query = f"UPDATE Products SET threshold = {threshold}"
        return self.db_manager.execute_query(query)
    
    def calculate_total_sales(self):
        query = f"SELECT SUM(total_price) from orders"
        return self.db_manager.fetch_all(query)
    
    def calculate_total_inventory_value(self):
        query = f"SELECT SUM(quantity) from Products"
        return self.db_manager.fetch_all(query)
    
    def process_order(self, order_details):
        total_cost = 0
        errors = []

        for product_id, order_quantity in order_details:
            # Check if the product exists in the database
            query = f"SELECT price, quantity FROM Products WHERE product_id = {product_id}"
            result = self.db_manager.fetch_all(query)
            
            if not result:
                errors.append(f"Product ID {product_id} does not exist.")
                continue
            
            price, quantity = result[0]
            
            # Check stock availability
            if quantity < order_quantity:
                errors.append(f"Insufficient stock for Product ID {product_id}. Available: {quantity}.")
                continue
            
            # Calculate total cost for this product
            item_cost = price * order_quantity
            total_cost += item_cost

            # Update the inventory in the database
            new_quantity = quantity - order_quantity
            update_query = f"UPDATE Products SET quantity = {new_quantity} WHERE product_id = {product_id}"
            self.db_manager.execute_query(update_query)

            # Add the order to the Orders table
            insert_query = f"""
                INSERT INTO Orders (product_id, quantity, total_price)
                VALUES ({product_id}, {order_quantity}, {item_cost})
            """
            self.db_manager.execute_query(insert_query)

        return total_cost, errors
