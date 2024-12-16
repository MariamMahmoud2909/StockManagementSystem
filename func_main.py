from functional_imp import *

def main():
    inventory = {}
    sales_records = []  

    print("STOCK MANAGEMENT SYSTEM")

    while True:
        print("\n1. Product Management")
        print("2. Order Management")
        print("3. Inventory Tracking")
        print("4. Inventory Reports")
        print("5. Exit")

        choice = int(input("\nChoose an option: "))

        if choice == 1:
            print("\n1. Add Product")
            print("2. Update Product")
            print("3. Delete Product")

            operation = int(input("\nChoose an option: "))

            if operation == 1:
                name = input("Enter Product Name: ")
                price = float(input("Enter Product Price: "))
                quantity = int(input("Enter Product Quantity: "))
                product_id = len(inventory) + 1  
                inventory = add_product(inventory, product_id, name, price, quantity)
                print("Product added successfully!")

            elif operation == 2:
                product_id = int(input("Enter Product ID: "))
                name = input("Enter New Name (Leave blank to skip): ")
                price = input("Enter New Price (Leave blank to skip): ")
                quantity = input("Enter New Quantity (Leave blank to skip): ")
                inventory = update_product(
                    inventory,
                    product_id,
                    name=name or None,
                    price=float(price) if price else None,
                    quantity=int(quantity) if quantity else None,
                )
                print("Product updated successfully!")

            elif operation == 3:
                product_id = int(input("Enter Product ID: "))
                inventory = delete_product(inventory, product_id)
                print("Product deleted successfully!")

            else:
                print("Invalid choice. Try again.")

        elif choice == 2:
            print("\n1. Process Order")
            print("2. Check Product Availability")

            operation = int(input("\nChoose an option: "))

            if operation == 1:
                order_details = []
                print("Enter items for the order (Enter -1 to stop):")
                while True:
                    product_id = int(input("Enter Product ID: "))
                    if product_id == -1:
                        break
                    order_quantity = int(input("Enter Order Quantity: "))
                    order_details.append((product_id, order_quantity))

                updated_inventory, errors = process_order(inventory, order_details)
                if errors:
                    print("Some items could not be processed:")
                    for error in errors:
                        print(error)
                else:
                    inventory = updated_inventory
                    total_cost = sum(inventory[product_id]["price"] * quantity for product_id, quantity in order_details)
                    sales_records.append({"order_details": order_details, "total_price": total_cost})
                    print(f"Total cost of the order: {total_cost}")
                    print("Order processed successfully!")

            elif operation == 2:
                product_id = int(input("Enter Product ID: "))
                is_available = check_product_availability(inventory, product_id, 1)
                print(f"Product is {'available' if is_available else 'not available'}.")

            else:
                print("Invalid choice. Try again.")

        elif choice == 3:
            threshold = int(input("Enter Low Stock Threshold: "))
            report = generate_low_stock_report(inventory, threshold)
            print(f"Low Stock Items (Threshold: {threshold}):")
            print("Product ID | Name | Quantity")
            for product_id, details in report.items():
                print(f"{product_id} | {details['name']} | {details['quantity']}")

        elif choice == 4:
            print("\n1. Generate Low Stock Report")
            print("2. Generate Total Sales Report")
            print("3. Generate Inventory Value Report")

            operation = int(input("\nChoose an option: "))

            if operation == 1:
                threshold = int(input("Enter Low Stock Threshold: "))
                report = generate_low_stock_report(inventory, threshold)
                print("Low Stock Items:")
                print("Product ID | Name | Quantity")
                for product_id, details in report.items():
                    print(f"{product_id} | {details['name']} | {details['quantity']}")

            elif operation == 2:
                total_sales = calculate_total_sales(sales_records)
                print(f"Total Sales: {total_sales}")

            elif operation == 3:
                total_value = calculate_total_inventory_value(inventory)
                print(f"Total Inventory Value: {total_value}")

            else:
                print("Invalid choice. Try again.")

        elif choice == 5:
            print("Thanks For Using Our Stock Management System <3")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
