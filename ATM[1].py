# ATM

def atm():
  balance = 2000  # Initial balance

  def check_balance():
    print(f"Your current balance is: ${balance}")

  def deposit(amount):
    nonlocal balance
    if amount > 0:
      balance += amount
      print(f"${amount} has been deposited. Your new balance is: ${balance}")
    else:
      print("Invalid deposit amount.")

  def withdraw(amount):
    nonlocal balance
    if 0 < amount <= balance:
      balance -= amount
      print(f"${amount} has been withdrawn. Your new balance is: ${balance}")
    elif amount > balance:
      print("Insufficient funds.")
    else:
      print("Invalid withdrawal amount.")

  while True:
    print("\nWelcome to the ATM!")
    print("1. Check Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == '1':
      check_balance()
    elif choice == '2':
      try:
        amount = float(input("Enter amount to deposit: $"))
        deposit(amount)
      except ValueError:
        print("Invalid input. Please enter a number.")
    elif choice == '3':
      try:
        amount = float(input("Enter amount to withdraw: $"))
        withdraw(amount)
      except ValueError:
        print("Invalid input. Please enter a number.")
    elif choice == '4':
      print("Thank you for using the ATM. Goodbye!")
      break
    else:
      print("Invalid choice. Please try again.")