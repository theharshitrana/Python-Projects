# mini_pos_rupee.py

# Sample inventory with prices in Indian Rupees (₹)
inventory = {
    '1001': {'name': 'Milk', 'price': 55},
    '1002': {'name': 'Bread', 'price': 40},
    '1003': {'name': 'Eggs (dozen)', 'price': 70},
    '1004': {'name': 'Apple (kg)', 'price': 120},
}

cart = {}

def show_inventory():
    print("\n--- 🛒 Available Items ---")
    print("Code | Item           | Price (₹)")
    for code, item in inventory.items():
        print(f"{code} | {item['name']:<14} | ₹{item['price']}")
    print()

def add_to_cart():
    code = input("Enter item code: ")
    if code in inventory:
        try:
            qty = int(input("Enter quantity: "))
            if qty <= 0:
                print("Quantity must be positive.\n")
                return
        except ValueError:
            print("Invalid quantity.\n")
            return

        if code in cart:
            cart[code]['qty'] += qty
        else:
            cart[code] = {
                'name': inventory[code]['name'],
                'price': inventory[code]['price'],
                'qty': qty
            }
        print(f"✅ Added {qty} x {inventory[code]['name']} to cart.\n")
    else:
        print("❌ Invalid item code.\n")

def view_cart():
    if not cart:
        print("🛒 Cart is empty.\n")
        return

    print("\n--- 🧾 Your Cart ---")
    total = 0
    print("Item           | Qty | Unit Price | Total (₹)")
    print("----------------------------------------------")
    for item in cart.values():
        line_total = item['qty'] * item['price']
        total += line_total
        print(f"{item['name']:<14} | {item['qty']}   | ₹{item['price']}       | ₹{line_total}")
    print("----------------------------------------------")
    print(f"🧾 Total Amount: ₹{total}\n")

def checkout():
    view_cart()
    print("✅ Checkout complete.\n🙏 Thank you for shopping with us!\n")
    cart.clear()

def menu():
    while True:
        print("===== MINI POS BILLING SYSTEM (₹) =====")
        print("1. Show Inventory")
        print("2. Add Item to Cart")
        print("3. View Cart")
        print("4. Checkout")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            show_inventory()
        elif choice == '2':
            add_to_cart()
        elif choice == '3':
            view_cart()
        elif choice == '4':
            checkout()
        elif choice == '5':
            print("👋 Exiting POS System. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.\n")

# Run the program
if __name__ == "__main__":
    menu()
