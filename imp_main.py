from imperative_imp import stock_management_imperative

def main():
    stock_management_imperative.initialize_db()
    add_product(1, "Product A", 50.0, 100)
    add_product(2, "Product B", 30.0, 50)
    update_stock(1, -10)
    process_order(1, 20)
    low_stock = generate_low_stock_report(30)
    print("Low Stock Items:", low_stock)
    total_value = generate_inventory_value_report()
    print("Total Inventory Value:", total_value)

if __name__ == "__main__":
    main()
