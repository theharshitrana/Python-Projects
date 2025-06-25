# Initialize the list of reminders
reminders = []

def add_reminder():
    title = input("Enter the title of the reminder: ")
    
    # Add the reminder to the list
    reminders.append({"title": title})
    print(f"✅ Reminder '{title}' added.\n")

def view_reminders():
    if not reminders:
        print("You have no reminders set.\n")
        return
    
    print("\n--- Your Reminders ---")
    for i, reminder in enumerate(reminders, 1):
        print(f"{i}. {reminder['title']}")
    print()

def delete_reminder():
    if not reminders:
        print("You have no reminders to delete.\n")
        return

    view_reminders()
    try:
        reminder_number = int(input("Enter the number of the reminder to delete: "))
        if reminder_number < 1 or reminder_number > len(reminders):
            print("Invalid reminder number.")
            return
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return
    
    deleted_reminder = reminders.pop(reminder_number - 1)
    print(f"✅ Reminder '{deleted_reminder['title']}' deleted.\n")

def menu():
    while True:
        print("==== Simple Reminder App (No Time) ====")
        print("1. Add Reminder")
        print("2. View Reminders")
        print("3. Delete Reminder")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            add_reminder()
        elif choice == '2':
            view_reminders()
        elif choice == '3':
            delete_reminder()
        elif choice == '4':
            print("Exiting Reminder App. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")

# Run the app
if __name__ == "__main__":
    menu()