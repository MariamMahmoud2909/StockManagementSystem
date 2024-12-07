from functional_imp import stock_management_functional

def main():
    initialize_db()
    products = []
    products = add_product(products, {'id': 1, 'name': "Product A", 'price': 50.0, 'quantity': 100})
    products = add_product(products, {'id': 2, 'name': "Product B", 'price': 30.0, 'quantity': 50})
    products = update_stock(products, 1, -10)
    products, total_cost = process_order(products, 1, 20)
    print("Low Stock Items:", generate_low_stock_report(products, 30))
    print("Total Inventory Value:", generate_inventory_value(products))

if __name__ == "__main__":
    main()
