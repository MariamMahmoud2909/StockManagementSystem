from db_manager import DBManager
from imperative_imp import Inventory, Product

def main():
    
    db_manager = DBManager("DESKTOP-9UUO4AR", "StockManagement")
    inventory = Inventory(db_manager)
    
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
                quantity = input("Enter Product Quantity: ")
                product = Product(name, price, quantity)
                inventory.add_product(product)

            elif operation == 2:
                product_id = input("Enter Product ID: ")
                name = input("Enter New Name (Leave blank to skip): ")
                price = input("Enter New Price (Leave blank to skip): ")
                quantity = input("Enter New Quantity (Leave blank to skip): ")
                inventory.update_product(product_id, name or None, float(price) if price else None, int(quantity) if quantity else None)

            elif operation == 3:
                product_name = input("Enter Product Name: ")
                inventory.delete_product(product_name)

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
                
                total_cost, errors = inventory.process_order(order_details)
                
                if errors:
                    print("Some items could not be processed:")
                    for error in errors:
                        print(error)
                
                print(f"Total cost of the order: {total_cost}")
                print("Order processed successfully!")
                
            elif operation ==2:
                product_name = input("Please Enter Product Name: ")
                inventory.check_product_availability(product_name)
            
            else:
                print("Invalid choice. Try again.")
                        
        elif choice == 3:
            threshold = input("Enter Low Stock Threshold: ")
            inventory.update_threshold(threshold)
            report = inventory.generate_low_stock_items_report()
            print(f"Take Care!! The Following Products Fell Below the Predefined Threshold[{threshold}]")
            print("Product ID | Name | Quantity")
            for row in report:
                print(row)
            
        elif choice == 4:
            
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
        
        elif choice == 5:
            db_manager.close()
            print("Thanks For Using Our Stock Managemet System <3")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
