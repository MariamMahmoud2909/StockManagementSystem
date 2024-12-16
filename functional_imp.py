from functools import reduce

# Helper function for pattern matching
def get_value(d, key):
    return d[key] if key in d else None

# Custom functions to replace built-in functionalities
def custom_merge(dict1, dict2):
    """Merge two dictionaries into a new dictionary."""
    if not dict1:
        return dict2
    if not dict2:
        return dict1
    key, *remaining_keys = list(dict2.keys())
    merged = {key: dict2[key]}
    return custom_merge({**dict1, **merged}, {k: dict2[k] for k in remaining_keys})

def custom_filter(predicate, iterable):
    """Filter items based on a custom predicate."""
    if not iterable:
        return {}
    key, value = next(iter(iterable.items()))
    rest = {k: v for k, v in iterable.items() if k != key}
    if predicate(key, value):
        return {key: value, **custom_filter(predicate, rest)}
    return custom_filter(predicate, rest)

def custom_reduce(func, iterable, initializer):
    """Reduce function using recursion."""
    if not iterable:
        return initializer
    first, *rest = iterable
    return custom_reduce(func, rest, func(initializer, first))

# Functional Inventory Management
def add_product(inventory, product_id, name, price, quantity):
    new_product = {"name": name, "price": price, "quantity": quantity}
    return custom_merge(inventory, {product_id: new_product})

def update_product(inventory, product_id, name=None, price=None, quantity=None):
    if product_id not in inventory:
        return inventory

    def update_field(field_name):
        return (
            get_value(inventory[product_id], field_name)
            if get_value(locals(), field_name) is None
            else get_value(locals(), field_name)
        )

    updated_product = {
        product_id: {
            "name": update_field("name"),
            "price": update_field("price"),
            "quantity": update_field("quantity"),
        }
    }
    return custom_merge(inventory, updated_product)

def delete_product(inventory, product_id):
    def exclude_key(key, _):
        return key != product_id

    return custom_filter(exclude_key, inventory)

def check_product_availability(inventory, product_id, required_quantity):
    product = get_value(inventory, product_id)
    return product is not None and product["quantity"] >= required_quantity

def generate_low_stock_report(inventory, threshold):
    def is_low_stock(_, details):
        return details["quantity"] < threshold

    return custom_filter(is_low_stock, inventory)

def process_order(inventory, order_details):
    if not order_details:
        return inventory, []

    product_id, order_quantity = order_details[0]
    updated_inventory, errors = process_order(inventory, order_details[1:])

    product = get_value(inventory, product_id)
    if product is None:
        return updated_inventory, [*errors, f"Product ID {product_id} does not exist"]
    if product["quantity"] < order_quantity:
        return updated_inventory, [*errors, f"Insufficient stock for Product ID {product_id}"]

    updated_inventory = update_product(
        updated_inventory, product_id, quantity=product["quantity"] - order_quantity
    )
    return updated_inventory, errors

def calculate_total_inventory_value(inventory):
    def calculate_value(total, item):
        return total + (item["price"] * item["quantity"])

    items = list(inventory.values())
    return custom_reduce(calculate_value, items, 0)

def calculate_total_sales(sales_records):
    def calculate_sales(total, sale):
        return total + sale["total_price"]

    return custom_reduce(calculate_sales, sales_records, 0)

def set_threshold(thresholds, product_id, threshold):
    return custom_merge(thresholds, {product_id: threshold})