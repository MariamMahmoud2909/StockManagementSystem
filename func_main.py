from db_manager import DBManager

def add_product(inventory, product_id, name, price, quantity):
    new_product = {"name": name, "price": price, "quantity": quantity}
    return {**inventory, product_id: new_product}

def update_product(inventory, product_id, name=None, price=None, quantity=None):
    if product_id not in inventory:
        return inventory
    product = inventory[product_id]
    updated_product = {
        "name": name or product["name"],
        "price": price if price is not None else product["price"],
        "quantity": quantity if quantity is not None else product["quantity"]
    }
    return {**inventory, product_id: updated_product}

def delete_product(inventory, product_id):
    return {key: val for key, val in inventory.items() if key != product_id}

def generate_low_stock_report(inventory, threshold):
    return {k: v for k, v in inventory.items() if v["quantity"] < threshold}

def process_order(inventory, product_id, order_quantity):
    if product_id not in inventory or inventory[product_id]["quantity"] < order_quantity:
        return "Insufficient stock", inventory
    product = inventory[product_id]
    total_cost = product["price"] * order_quantity
    updated_inventory = update_product(inventory, product_id, quantity=product["quantity"] - order_quantity)
    return total_cost, updated_inventory

def main():
    inventory = {}
    db_manager = DBManager("server_name", "database_name", "username", "password")

    while True:
        print("\n1. Add Product")
        print("2. Update Product")
        print("3. Delete Product")
        print("4. Generate Low Stock Report")
        print("5. Process Order")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            product_id = int(input("Enter Product ID: "))
            name = input("Enter Product Name: ")
            price = float(input("Enter Product Price: "))
            quantity = int(input("Enter Product Quantity: "))
            inventory = add_product(inventory, product_id, name, price, quantity)

        elif choice == "2":
            product_id = int(input("Enter Product ID: "))
            name = input("Enter New Name (Leave blank to skip): ")
            price = input("Enter New Price (Leave blank to skip): ")
            quantity = input("Enter New Quantity (Leave blank to skip): ")
            inventory = update_product(inventory, product_id, name or None, float(price) if price else None, int(quantity) if quantity else None)

        elif choice == "3":
            product_id = int(input("Enter Product ID: "))
            inventory = delete_product(inventory, product_id)

        elif choice == "4":
            threshold = int(input("Enter Low Stock Threshold: "))
            report = generate_low_stock_report(inventory, threshold)
            for product_id, details in report.items():
                print(product_id, details)

        elif choice == "5":
            product_id = int(input("Enter Product ID: "))
            order_quantity = int(input("Enter Order Quantity: "))
            total_cost, inventory = process_order(inventory, product_id, order_quantity)
            print(f"Total cost: {total_cost}")

        elif choice == "6":
            db_manager.close()
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
