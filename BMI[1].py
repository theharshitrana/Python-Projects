# Bmi Calculator

 def calculate_bmi(height, weight):
    return weight / (height ** 2)
    return bmi

height = float(input("Enter your height in meters: "))
weight = float(input("Enter your weight in kilograms: "))

bmi = calculate_bmi(height, weight)

print(f"Your BMI is: {bmi:.2f}")
