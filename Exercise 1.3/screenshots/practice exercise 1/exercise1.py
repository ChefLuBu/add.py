math = input("Enter a number: ")
math2 = input("Enter another number to be combined to the first: ")
math3 = input("choose an operator: ")
if math3 == "+":
    print("the sum of the two numbers is", int(math)+int(math2))
elif math3 == "-":
    print("the difference of the two numbers is", int(math)-int(math2))
else:
    print("Unknown operator")