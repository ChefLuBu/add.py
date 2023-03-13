class Height(object):
    def __init__(self, feet, inches):
        self.feet = feet
        self.inches = inches
#str overloading
    def __str__(self):
        output = str(self.feet) + ' feet, ' + str(self.inches) + ' inches'
        return output
    
#greater than overloading
    def __gt__(self, other):
        height_inches_A = self.feet * 12 + self.inches
        height_inches_B = other.feet * 12 + other.inches
        return height_inches_A > height_inches_B

#greater than or equal to overloading
    def __ge__(self, other):
        height_inches_A = self.feet * 12 + self.inches
        height_inches_B = other.feet * 12 + other.inches
        return height_inches_A >= height_inches_B

#not equal to overloading
    def __ne__(self, other):
        height_inches_A = self.feet * 12 + self.inches
        height_inches_B = other.feet * 12 + other.inches
        return height_inches_A != height_inches_B

#Height is the class that we print from
print(Height(4, 6) > Height(4, 5))
print(Height(4, 5) >= Height(4, 5))
print(Height(5, 9) != Height(5, 10))