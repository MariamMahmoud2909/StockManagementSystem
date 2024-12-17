from db_manager import DBManager
from imperative_imp import Inventory, Product

def main():
    try:
        db_manager = DBManager("DESKTOP-9UUO4AR", "StockManagement")
        inventory = Inventory(db_manager)

        print("STOCK MANAGEMENT SYSTEM")

        while True:
            try:
                print("\n1. Product Management")
                print("2. Order Management")
                print("3. Inventory Tracking")
                print("4. Inventory Reports")
                print("5. Exit")

                choice = input("\nChoose an option: ").strip()
                if not choice.isdigit():
                    print("Invalid input. Please enter a number between 1 and 5.")
                    continue
                choice = int(choice)
                
                if choice == 1:
                    try:
                        print("\n1. Add Product")
                        print("2. Update Product")
                        print("3. Delete Product")

                        operation = input("\nChoose an option: ").strip()

                        if not operation.isdigit():
                            print("Invalid input. Please enter a number between 1 and 3.")
                            continue
                        operation = int(operation)
                        
                        if operation == 1:
                            name = input("Enter Product Name: ")
                            try:
                                # Check if product already exists
                                existing_product = db_manager.get_product_by_name(name)
                                if existing_product:
                                    print(f"Product '{name}' already exists in the inventory with ID {existing_product[0]}.")
                                else:
                                    while True:
                                        try:
                                            price = float(input("Enter Product Price: "))
                                            if price <= 0:
                                                print("Price must be greater than zero. Please enter a valid price.")
                                                continue
                                            break
                                        except ValueError:
                                            print("Invalid input. Please enter a valid number for the price.")

                                    while True:
                                        try:
                                            quantity = int(input("Enter Product Quantity: "))
                                            if quantity <= 0:
                                                print("Quantity must be greater than zero. Please enter a valid quantity.")
                                                continue
                                            break
                                        except ValueError:
                                            print("Invalid input. Please enter a valid integer for the quantity.")
                                    
                                    product = Product(name, price, quantity)
                                    inventory.add_product(product)
                                    print("Product added successfully!")
                            except KeyError:
                                print("Error retrieving product. Please try again.")
                            except Exception as e:
                                print(f"An unexpected error occurred: {e}")

                        elif operation == 2:
                            try:
                                product_id = int(input("Enter Product ID: ").strip())
                                name = input("Enter New Name (Leave blank to skip): ").strip()
                                price_input = input("Enter New Price (Leave blank to skip): ").strip()
                                quantity_input = input("Enter New Quantity (Leave blank to skip): ").strip()

                                # Validate price input
                                price = None
                                if price_input:
                                    try:
                                        price = float(price_input)
                                        if price <= 0:
                                            print("Price must be greater than zero.")
                                            continue
                                    except ValueError:
                                        print("Invalid input for price.")
                                        continue

                                quantity = None
                                if quantity_input:
                                    try:
                                        quantity = int(quantity_input)
                                        if quantity <= 0:
                                            print("Quantity must be greater than zero.")
                                            continue
                                    except ValueError:
                                        print("Invalid input for quantity.")
                                        continue

                                inventory.update_product(product_id, name or None, price, quantity)
                                print("Product updated successfully!")
                            except ValueError:
                                print("Invalid input. Product ID must be an integer.")

                        elif operation == 3:
                            product_name = input("Enter Product Name: ").strip()
                            if not product_name:
                                print("Product name cannot be empty.")
                                continue
                            inventory.delete_product(product_name)
                            print("Product deleted successfully!")

                        else:
                            print("Invalid choice. Please try again.")
                    except Exception as e:
                        print(f"Error in Product Management: {e}")

                elif choice == 2:
                    try:
                        print("\n1. Process Order")
                        print("2. Check Product Availability")

                        operation = input("\nChoose an option: ").strip()

                        if not operation.isdigit():
                            print("Invalid input. Please enter a number between 1 and 2.")
                            continue
                        operation = int(operation)

                        if operation == 1:
                            order_details = []
                            print("Enter items for the order (Enter -1 to stop):")

                            while True:
                                try:
                                    product_id = int(input("Enter Product ID: ").strip())
                                    if product_id == -1:
                                        break
                                    if product_id <= 0:
                                        print("Product ID must be greater than 0. Please try again.")
                                        continue

                                    order_quantity = int(input("Enter Order Quantity: ").strip())
                                    if order_quantity <= 0:
                                        print("Order quantity must be greater than 0. Please try again.")
                                        continue

                                    order_details.append((product_id, order_quantity))
                                except ValueError:
                                    print("Invalid input. Please enter valid integers for Product ID and Quantity.")

                            total_cost, errors = inventory.process_order(order_details)

                            if errors:
                                print("Some items could not be processed:")
                                for error in errors:
                                    print(error)
                            print(f"Total cost of the order: {total_cost}")
                            print("Order processed successfully!")

                        elif operation == 2:
                            product_name = input("Enter Product Name: ").strip()
                            inventory.check_product_availability(product_name)
                        else:
                            print("Invalid choice. Please try again.")
                    except Exception as e:
                        print(f"Error in Order Management: {e}")

                elif choice == 3:
                    try:
                        threshold = input("Enter Low Stock Threshold: ").strip()
                        if not threshold.isdigit():
                            print("Invalid threshold value. Please enter a valid number.")
                            continue

                        threshold = int(threshold)
                        inventory.update_threshold(threshold)
                        report = inventory.generate_low_stock_items_report()

                        if not report:
                            print(f"No products below the threshold of {threshold}.")
                        else:
                            print(f"Products below the threshold ({threshold}):")
                            print("Product ID | Name | Quantity")
                            for row in report:
                                print(row)
                    except Exception as e:
                        print(f"Error in Inventory Tracking: {e}")

                elif choice == 4:
                    try:
                        print("\n1. Generate Low Stock Report")
                        print("2. Generate Total Sales Report")
                        print("3. Generate Inventory Value Report")

                        operation = input("\nChoose an option: ").strip()
                        if not operation.isdigit():
                            print("Invalid input. Please enter a valid option.")
                            continue
                        operation = int(operation)

                        if operation == 1:
                            report = inventory.generate_low_stock_items_report()
                            print("Low Stock Items:")
                            print("Product ID | Name | Quantity")
                            for row in report:
                                print(row)

                        elif operation == 2:
                            total_sales = inventory.calculate_total_sales()
                            print("Total Sales: ", total_sales)

                        elif operation == 3:
                            total_value = inventory.calculate_total_inventory_value()
                            print("Total Inventory Value: ", total_value)

                        else:
                            print("Invalid choice. Please try again.")
                    except Exception as e:
                        print(f"Error in Inventory Reports: {e}")

                elif choice == 5:
                    db_manager.close()
                    print("Thanks for using the Stock Management System! Goodbye.")
                    break

                else:
                    print("Invalid choice. Please choose a valid option.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    except Exception as e:
        print(f"An error occurred while initializing the system: {e}")

if __name__ == "__main__":
    main()
