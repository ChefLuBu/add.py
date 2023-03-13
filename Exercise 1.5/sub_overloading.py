class Height(object):
    def __init__(self, feet, inches):
        self.feet = feet
        self.inches = inches

# __str__ is a special method that is called when you try to print an object
    def __str__(self):
        output = str(self.feet) + " feet, " + str(self.inches) + " inches"
        return output
    
#subtraction overloading    
# __sub__ is a special method that is called when you try to subtract two objects
    def __sub__(self, other):
        height_A_inches = self.feet * 12 - self.inches
        height_B_inches = other.feet * 12 - other.inches

        total_height_inches = height_A_inches - height_B_inches

        output_feet = total_height_inches // 12

        output_inches = total_height_inches - (output_feet * 12)

        return Height(output_feet, output_inches)

person_A_height = Height(3, 9)
person_B_height = Height(5, 10)
height_sum = person_A_height - person_B_height

print("Total height:", height_sum)