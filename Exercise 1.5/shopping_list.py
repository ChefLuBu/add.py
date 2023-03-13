#Class is a blueprint for creating objects
class ShoppingList(object):
    def __init__(self, list_name):
        shopping_list = []
        self.list_name = list_name
        self.shopping_list = shopping_list
#self is a reference to the current instance of the class
#and is used to access variables that belong to the class
#self.shopping_list is a list of items
#self.list_name is the name of the list
#self.item is the item being added or removed from the list

    def add_item(self, item):
        self.item = item
        if (item in self.shopping_list):
            print("Item already in list")
        else:
            self.shopping_list.append(item)
            print("Item added to list")

    def remove_item(self, item):
        self.item = item
        if (item in self.shopping_list):
            self.shopping_list.remove(self.item)
            print("Item removed from list")
        else:
            print("Item not in list")
        
        
    def view_list(self):
        print(self.shopping_list)
        for item in self.shopping_list:
            print(item)

pet_store_list = ShoppingList("Pet Store Shopping List")

pet_store_list.add_item("Dog Food")
pet_store_list.add_item("Collars")
pet_store_list.add_item("Flea Collars")
pet_store_list.add_item("Frisbee")
pet_store_list.add_item("Bowl")

pet_store_list.remove_item("Flea Collars")

pet_store_list.add_item("Frisbee")

pet_store_list.view_list()
