 # Bill Spliter App

def calculate_split_bill(total, people, tip_percent):
    tip = total * (tip_percent / 100)
    final_amount = total + tip
    return final_amount / people

def main():
    try:
        total = float(input("Enter the total bill amount: ₹"))
        people = int(input("Enter number of people: "))
        tip_percent = float(input("Enter tip percentage (e.g., 10 for 10%): "))

        if people <= 0:
            print(" Number of people must be greater than 0.")
            return

        amount_per_person = calculate_split_bill(total, people, tip_percent)
        print(f"\nEach person should pay: ₹{amount_per_person:.2f}")

    except ValueError:
        print("❌ Invalid input. Please enter numeric values.")

main()

