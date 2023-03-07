text = input("Enter a string: ")
chars = ['Uppercase' if c.isupper() else 'Lowercase' if c.islower() else 'Other' for c in text]