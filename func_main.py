from functional_imp import *

def main():
    inventory = {}
    sales_records = []

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
                        #Handle if the product already exist 
                        existing_product = next((product for product in inventory.values() if product['name'].lower() == name.lower()), None)
                        if existing_product:
                            print(f"A product with the name '{name}' already exists (Product ID: {existing_product['id']}).")
                            continue
                        while True:
                           try:
                              price = float(input("Enter Product Price: "))
                             #Handle if the product price 0 or negative
                              if price <= 0:
                                  print("Price cannot be negative or zero. Please enter a valid price.")
                                  continue
                              break
                           except ValueError:
                                print("Invalid input. Please enter a valid number for the price.")
                       
                        while True:
                            try:
                                quantity = int(input("Enter Product Quantity: "))
                                #Handle if the product quantity 0 or negative
                                if quantity <= 0:
                                    print("Quantity cannot be negative  or zero. Please enter a valid quantity.")
                                    continue
                                break
                            except ValueError:
                                print("Invalid input. Please enter a valid integer for the quantity.")
                        product_id = len(inventory) + 1
                        inventory = add_product(inventory, product_id, name, price, quantity)
                        print("Product added successfully!")

                    elif operation == 2:
                        product_id = int(input("Enter Product ID: "))
                        name = input("Enter New Name (Leave blank to skip): ")
                        while True:
                           try:
                              price = float(input("Enter New Price (Leave blank to skip): "))
                             #Handle if the product price 0 or negative
                              if price <= 0:
                                  print("Price cannot be negative or zero. Please enter a valid price.")
                                  continue
                              break
                           except ValueError:
                                print("Invalid input. Please enter a valid number for the price.")
                       
                        while True:
                            try:
                                quantity = int(input("Enter New Quantity (Leave blank to skip): "))
                                #Handle if the product quantity 0 or negative
                                if quantity <= 0:
                                    print("Quantity cannot be negative  or zero. Please enter a valid quantity.")
                                    continue
                                break
                            except ValueError:
                                print("Invalid input. Please enter a valid integer for the quantity.")
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
                            product_id = int(input("Enter Product ID: "))
                            if product_id == -1:
                                break
                            #Handle if the product user want to order is not in the inventory
                            if product_id not in inventory:
                                print(f"Product ID {product_id} does not exist. Please enter a valid Product ID.")
                                continue
                            order_quantity = int(input("Enter Order Quantity: "))
                            #Handle if the product user want to order is not in the inventory
                            if order_quantity <= 0:
                                print("Order quantity must be greater than 0. Please try again.")
                                continue
                             #Handle if the order quantity exceeds available quantity in inventory 
                            available_quantity = inventory[product_id]["quantity"]
                            if order_quantity > available_quantity:
                               print(f"Insufficient stock for Product ID {product_id}. Available quantity: {available_quantity}. Please adjust your order.")
                               continue
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
                except ValueError as ve:
                    print(f"Invalid input: {ve}")
                except KeyError as ke:
                    print(f"Product not found: {ke}")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")

            elif choice == 3:
                try:
                    threshold = int(input("Enter Low Stock Threshold: "))
                    report = generate_low_stock_report(inventory, threshold)
                    # handle if report is empty
                    if not report:  
                       print(f"No products are below the threshold of {threshold}.")
                    else:
                       print(f"Low Stock Items (Threshold: {threshold}):")
                       print("Product ID | Name | Quantity")
                       for product_id, details in report.items():
                           print(f"{product_id} | {details['name']} | {details['quantity']}")
                except ValueError as ve:
                    print(f"Invalid threshold value: {ve}")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                

            elif choice == 4:
                try:
                    if not inventory:
                        print("The inventory is empty. Please add products before generating reports.")
                        continue
                    print("\n1. Generate Low Stock Report")
                    print("2. Generate Total Sales Report")
                    print("3. Generate Inventory Value Report")

                    operation = int(input("\nChoose an option: "))

                    if operation == 1:
                        threshold = int(input("Enter Low Stock Threshold: "))
                        report = generate_low_stock_report(inventory, threshold)
                        #Handle if no product below the threshold
                        if not report:
                           print(f"No products below the threshold of {threshold}.")
                        else:
                           print("Low Stock Items:")
                           print("Product ID | Name | Quantity")
                           for product_id, details in report.items():
                              print(f"{product_id} | {details['name']} | {details['quantity']}")

                    elif operation == 2:
                        #Handle if no sales records to show
                        if not sales_records:
                           print("No sales records found. Please process orders to generate sales reports.")
                        else:
                           total_sales = calculate_total_sales(sales_records)
                           print(f"Total Sales: {total_sales}")

                    elif operation == 3:
                        total_value = calculate_total_inventory_value(inventory)
                        print(f"Total Inventory Value: {total_value}")

                    else:
                        print("Invalid choice. Try again.")
                except ValueError as ve:
                    print(f"Invalid input: {ve}")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")

            elif choice == 5:
                print("Thanks For Using Our Stock Management System <3")
                break

            else:
                print("Invalid choice. Try again.")
        except ValueError as ve:
            print(f"Invalid input: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
