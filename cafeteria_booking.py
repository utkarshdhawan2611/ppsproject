import os
import datetime

def display_menu():
    print("=== Cafeteria Menu ===")
    print("1. Coffee - $2.50")
    print("2. Sandwich - $5.00")
    print("3. Salad - $4.50")
    print("4. Pasta - $7.00")

def order_food():
    order = {}
    
    while True:
        choice = input("Enter the number of the item you want to order (0 to finish): ")
        
        if choice == '0':
            break

        item_name = ""
        if choice == '1':
            item_name = "Coffee"
        elif choice == '2':
            item_name = "Sandwich"
        elif choice == '3':
            item_name = "Salad"
        elif choice == '4':
            item_name = "Pasta"
        else:
            print("Invalid choice. Please enter a valid item number.")
            continue

        quantity = int(input(f"How many {item_name}s do you want to order? "))
        order[item_name] = quantity

    return order

def calculate_total(order):
    total = sum(get_item_price(item) * quantity for item, quantity in order.items())
    return total

def calculate_gst(total):
    gst_rate = 0.18  # 18% GST
    gst_amount = total * gst_rate
    return gst_amount

def make_receipt(customer_name, order):
    # Calculate total cost
    total_cost = calculate_total(order)

    # Calculate GST
    gst_amount = calculate_gst(total_cost)

    # Get current date and time
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Find the next available receipt number
    receipt_number = 1
    while os.path.exists(f"receipt{receipt_number}.txt"):
        receipt_number += 1

    receipt_file = f"receipt{receipt_number}.txt"

    # Print receipt
    print("\n=== Receipt ===")
    print(f"Customer Name: {customer_name}")
    print("-" * 40)
    print("{:<20} {:<10} {:<10}".format("Item", "Quantity", "Cost"))
    print("-" * 40)
    for item, quantity in order.items():
        cost = quantity * get_item_price(item)
        print("{:<20} {:<10} ${:<10.2f}".format(item, quantity, cost))
    
    print("-" * 40)
    print("{:<20} {:<10} ${:<10.2f}".format("Total (before GST)", "", total_cost))
    print("{:<20} {:<10} ${:<10.2f}".format("GST (18%)", "", gst_amount))
    total_with_gst = total_cost + gst_amount
    print("{:<20} {:<10} ${:<10.2f}".format("Total (after GST)", "", total_with_gst))
    print("-" * 40)
    print(f"Date and Time: {current_datetime}")

    # Save receipt to a file
    save_receipt(receipt_file, customer_name, order, total_with_gst, current_datetime)

    print(f"Receipt saved to '{receipt_file}'")

def delete_receipt():
    # Get the list of available receipts
    receipt_files = [file for file in os.listdir() if file.startswith("receipt") and file.endswith(".txt")]

    if not receipt_files:
        print("No receipts found.")
        return

    print("Available Receipts:")
    for i, receipt_file in enumerate(receipt_files, start=1):
        print(f"{i}. {receipt_file}")

    choice = input("Enter the number of the receipt you want to delete: ")

    try:
        choice = int(choice)
        selected_receipt = receipt_files[choice - 1]
        os.remove(selected_receipt)
        print(f"Receipt '{selected_receipt}' deleted successfully.")
    except (ValueError, IndexError):
        print("Invalid choice. Please enter a valid number.")

def extract_old_receipt():
    # Get the list of available receipts
    receipt_files = [file for file in os.listdir() if file.startswith("receipt") and file.endswith(".txt")]

    if not receipt_files:
        print("No receipts found.")
        return

    print("Available Receipts:")
    for i, receipt_file in enumerate(receipt_files, start=1):
        print(f"{i}. {receipt_file}")

    choice = input("Enter the number of the receipt you want to extract: ")

    try:
        choice = int(choice)
        selected_receipt = receipt_files[choice - 1]

        with open(selected_receipt, 'r') as file:
            content = file.read()
            print("\n=== Extracted Receipt ===\n")
            print(content)
    except (ValueError, IndexError):
        print("Invalid choice. Please enter a valid number.")

def get_item_price(item):
    prices = {"Coffee": 2.50, "Sandwich": 5.00, "Salad": 4.50, "Pasta": 7.00}
    return prices.get(item, 0)

def save_receipt(receipt_file, customer_name, order, total_cost, current_datetime):
    with open(receipt_file, "w") as file:
        file.write("=== Receipt ===\n")
        file.write(f"Customer Name: {customer_name}\n")
        file.write("-" * 40 + "\n")
        file.write("{:<20} {:<10} {:<10}\n".format("Item", "Quantity", "Cost"))
        file.write("-" * 40 + "\n")
        for item, quantity in order.items():
            cost = quantity * get_item_price(item)
            file.write("{:<20} {:<10} ${:<10.2f}\n".format(item, quantity, cost))
        
        file.write("-" * 40 + "\n")
        file.write("{:<20} {:<10} ${:<10.2f}\n".format("Total (before GST)", "", total_cost))
        gst_amount = calculate_gst(total_cost)
        file.write("{:<20} {:<10} ${:<10.2f}\n".format("GST (18%)", "", gst_amount))
        total_with_gst = total_cost + gst_amount
        file.write("{:<20} {:<10} ${:<10.2f}\n".format("Total (after GST)", "", total_with_gst))
        file.write("-" * 40 + "\n")
        file.write(f"Date and Time: {current_datetime}")

def view_menu_and_order_option1():
    display_menu()
    want_to_order = input("Do you want to place an order? (y/n): ").lower()

    if want_to_order == 'y'or'Y':
        customer_name = input("Enter your name: ")
        order = order_food()
        make_receipt(customer_name, order)
    else:
        print("Thank you for visiting. Goodbye!")

def view_menu_and_order_option2():
    display_menu()
    customer_name = input("Enter your name: ")
    order = order_food()
    make_receipt(customer_name, order)

def main():
    print("=== Welcome to the Cafeteria ===")
    print("1. View the Menu")
    print("2. Place an order")
    print("3. Review an old order")
    print("4. Delete an order receipt")

    choice = input("Enter your choice (1, 2, 3, or 4): ")

    if choice == '1':
        view_menu_and_order_option1()
    elif choice == '2':
        view_menu_and_order_option2()
    elif choice == '3':
        extract_old_receipt()
    elif choice == '4':
        delete_receipt()
    else:
        print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
