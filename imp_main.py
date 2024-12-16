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

                choice = int(input("\nChoose an option: "))

                if choice == 1:
                    try:
                        print("\n1. Add Product")
                        print("2. Update Product")
                        print("3. Delete Product")

                        operation = int(input("\nChoose an option: "))

                        if operation == 1:
                            name = input("Enter Product Name: ")
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

                        elif operation == 2:
                            product_id = input("Enter Product ID: ")
                            name = input("Enter New Name (Leave blank to skip): ")
                            price = input("Enter New Price (Leave blank to skip): ")
                            quantity = input("Enter New Quantity (Leave blank to skip): ")
                            inventory.update_product(product_id, name or None, float(price) if price else None, int(quantity) if quantity else None)
                            print("Product updated successfully!")

                        elif operation == 3:
                            product_name = input("Enter Product Name: ")
                            inventory.delete_product(product_name)
                            print("Product deleted successfully!")

                        else:
                            print("Invalid choice. Try again.")
                    except ValueError as ve:
                        print(f"Invalid input: {ve}")
                    except KeyError as ke:
                        print(f"Product not found: {ke}")
                    except Exception as e:
                        print(f"An unexpected error occurred: {e}")

                elif choice == 2:
                    try:
                        print("\n1. Process Order")
                        print("2. Check Product Availability")

                        operation = int(input("\nChoose an option: "))

                        if operation == 1:
                            order_details = []
                            print("Enter items for the order (Enter -1 to stop):")
                            while True:
                                try:
                                    product_id = int(input("Enter Product ID: "))
                                    if product_id == -1:
                                        break
                                    if product_id <= 0:
                                        print("Product ID must be greater than 0. Please try again.")
                                        continue
                                except ValueError:
                                    print("Invalid input. Please enter a valid integer for the product ID.")
                                    continue
                                
                                while True:
                                    try:
                                        order_quantity = int(input("Enter Order Quantity: "))
                                        if order_quantity <= 0:
                                            print("Order quantity must be greater than 0. Please try again.")
                                            continue
                                        break
                                    except ValueError:
                                        print("Invalid input. Please enter a valid integer for the quantity.")
                                        continue
                                    
                                order_details.append((product_id, order_quantity))
                            
                            total_cost, errors = inventory.process_order(order_details)
                            
                            if errors:
                                print("Some items could not be processed:")
                                for error in errors:
                                    print(error)
                            
                            print(f"Total cost of the order: {total_cost}")
                            print("Order processed successfully!")

                        elif operation == 2:
                            product_name = input("Please Enter Product Name: ")
                            inventory.check_product_availability(product_name)

                        else:
                            print("Invalid choice. Try again.")
                    except ValueError as ve:
                        print(f"Invalid input: {ve}")
                    except KeyError as ke:
                        print(f"Product not found: {ke}")
                    except Exception as e:
                        print(f"An unexpected error occurred: {e}")

                elif choice == 3:
                    try:
                        threshold = input("Enter Low Stock Threshold: ")
                        if not threshold.isdigit():
                            print("Invalid threshold value. Please enter a valid number.")
                            continue
                        inventory.update_threshold(int(threshold))
                        report = inventory.generate_low_stock_items_report()
                        print(f"Take Care!! The Following Products Fell Below the Predefined Threshold[{threshold}]")
                        print("Product ID | Name | Quantity")
                        for row in report:
                            print(row)

                    except ValueError as ve:
                        print(f"Invalid threshold value: {ve}")
                    except Exception as e:
                        print(f"An unexpected error occurred: {e}")

                elif choice == 4:
                    try:
                        print("\n1. Generate Low Stock Report")
                        print("2. Generate Total Sales Report")
                        print("3. Generate Inventory Value Report")

                        operation = int(input("\nChoose an option: "))

                        if operation == 1:
                            report = inventory.generate_low_stock_items_report()
                            print("Low Stock Items:")
                            print("Product ID | Name | Quantity \n")
                            for row in report:
                                print(row)

                        elif operation == 2:
                            value = inventory.calculate_total_sales()
                            print("Total Sales:", value)

                        elif operation == 3:
                            value = inventory.calculate_total_inventory_value()
                            print("Total Inventory Value: ", value)

                        else:
                            print("Invalid choice. Try again.")
                    except ValueError as ve:
                        print(f"Invalid input: {ve}")
                    except Exception as e:
                        print(f"An unexpected error occurred: {e}")

                elif choice == 5:
                    db_manager.close()
                    print("Thanks For Using Our Stock Management System <3")
                    break

                else:
                    print("Invalid choice. Try again.")
            except ValueError as ve:
                print(f"Invalid input: {ve}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    except Exception as e:
        print(f"An error occurred while initializing the system: {e}")

if __name__ == "__main__":
    main()
