# Password Generator

import random
import string

def generate_password(length=12):
    if length < 4:
        raise ValueError("Password length should be at least 4")

    letters = string.ascii_letters  # a-zA-Z
    digits = string.digits          # 0-9
    symbols = string.punctuation    # !@#$%^&*()_+ etc.

    password = [
        random.choice(letters),
        random.choice(digits),
       random.choice(symbols),
        random.choice(letters.upper())
    ]
    all_chars = letters + digits + symbols
    password += random.choices(all_chars, k=length - 4)

    random.shuffle(password)

    return ''.join(password)

print("Generated Password:", generate_password(12))
