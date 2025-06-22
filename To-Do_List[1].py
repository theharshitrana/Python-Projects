# To Do List

tasks = []

while True:
    print("\n1. Add task")
    print("2. Show tasks")
    print("3. Exit")
    choice = input("Choose an option: ")

    if choice == '1':
        task = input("Enter task: ")
        tasks.append(task)
        print("Task added!")
    elif choice == '2':
        if not tasks:
            print("No tasks yet.")
        else:
            print("Your tasks:")
            for i, t in enumerate(tasks, 1):
                print(f"{i}. {t}")
    elif choice == '3':
        print("Goodbye!")
        break
    else:
        print("Invalid choice, try again.")