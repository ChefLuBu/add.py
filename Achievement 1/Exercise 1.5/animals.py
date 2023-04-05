class Animal(object):
    def __init__(self, age):
        self.age = age
        self.name = None

    def get_age(self):
        return self.age

    def get_name(self):
        return self.name

    def set_age(self, age):
        self.age = age

    def set_name(self, name):
        self.name = name

    def __str__(self):
        output = "\nClass: Animal\nName: " + str(self.name) + \
            "\nAge: " + str(self.age)
        return output
        
    #cat and dog are subclasses of animal
    #they inherit the methods of animal
class Cat(Animal):
    #pass the parent class into the child class's arguments
    
    # Introducing a new method where it speaks
    def speak(self):
        print("Meow")

    # Another neat string representation for cats
    def __str__(self):
        output = "\nClass: Cat\nName: " + str(self.name) + \
            "\nAge: " + str(self.age)
        return output


class Dog(Animal):
 # Implementing another speak() method for dogs
    def speak(self):
        print("Woof!")

    # String representation for dogs
    def __str__(self):
        output = "\nClass: Cat\nName: " + str(self.name) + \
            "\nAge: " + str(self.age)
        return output
    


class Human(Animal):
    # Making its own initialization method
    def __init__(self, name, age):
        # Calling the parent class' init method to initialize
        # other attributes like 'name' and 'age'
        Animal.__init__(self, age)

        # Setting a name, since humans must have names
        self.set_name(name)

        # Our new attribute for humans, 'friends'!
        self.friends = []

    # Adding another method to add friends
    def add_friend(self, friend_name):
        self.friends.append(friend_name)

    # A method to display friends
    def show_friends(self):
        for friend in self.friends:
            print(friend)

    # Humans can speak sentences!
    def speak(self):
        print("Hello, my name's " + self.name + "!")

    # We'll modify the string representation to include friends as well.
    def __str__(self):
        output = "\nClass: Human\nName: " + str(self.name) + \
            "\nAge: " + str(self.age) + "\nFriends list: \n"
        for friend in self.friends:
            output += friend + "\n"
        return output

#create the objects cat and dog
cat = Cat(5)
dog = Dog(3)
human = Human("Bob",46)

human.add_friend("Tom")
human.add_friend("Ron")
human.add_friend("Mike")
human.add_friend("Jenny")
human.add_friend("Sam")
human.add_friend("Reb")
human.add_friend("Jill")

#set the name of the cat and dog
cat.set_name("Kitty")
dog.set_name("Doggy")

#print the cat and dog
print(cat)
print(dog)
print(human)

cat.speak()
dog.speak()
human.speak()