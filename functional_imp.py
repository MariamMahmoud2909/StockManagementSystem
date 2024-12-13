from functools import reduce

def add_product(inventory, product_id, name, price, quantity):
    new_product = {"name": name, "price": price, "quantity": quantity}
    return {**inventory, product_id: new_product}

def update_product(inventory, product_id, name=None, price=None, quantity=None):
    if product_id not in inventory:
        return inventory
    updated_inventory = {
        product_id: {
            "name": name or inventory[product_id]["name"],
            "price": price if price is not None else inventory[product_id]["price"],
            "quantity": quantity if quantity is not None else inventory[product_id]["quantity"]
        }
    }
    return {**inventory, **updated_inventory}

def delete_product(inventory, product_id):
    return {key: value for key, value in inventory.items() if key != product_id}

def check_product_availability(inventory, product_id, required_quantity):
    product = inventory.get(product_id)
    return product is not None and product["quantity"] >= required_quantity

def generate_low_stock_report(inventory, threshold):
    return {product_id: details for product_id, details in inventory.items() if details["quantity"] < threshold}

def process_order(inventory, order_details):
    def process_item(inventory, product_id, order_quantity):
        if product_id not in inventory:
            return inventory, f"Product ID {product_id} does not exist"
        if inventory[product_id]["quantity"] < order_quantity:
            return inventory, f"Insufficient stock for Product ID {product_id}"
        
        updated_inventory = update_product(
            inventory, product_id, quantity=inventory[product_id]["quantity"] - order_quantity
        )
        return updated_inventory, None

    errors = []
    updated_inventory = inventory
    for product_id, order_quantity in order_details:
        updated_inventory, error = process_item(updated_inventory, product_id, order_quantity)
        if error:
            errors.append(error)

    return updated_inventory, errors

def calculate_total_inventory_value(inventory):
    return reduce(lambda total, item: total + (item["price"] * item["quantity"]), inventory.values(), 0)

def calculate_total_sales(sales_records):
    return reduce(lambda total, sale: total + sale["total_price"], sales_records, 0)

def set_threshold(thresholds, product_id, threshold):
    return {**thresholds, product_id: threshold}