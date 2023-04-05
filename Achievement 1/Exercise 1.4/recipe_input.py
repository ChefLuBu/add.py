import pickle

recipes_list = []
ingredients_list = []


def take_recipe():
    recipe_name = input("Enter the name of the recipe: ")
    recipe_ingredients = input("Enter the ingredients of the recipe: ").split(", ")
    cooking_time = int(input("Enter the cooking time of the recipe: "))
    recipe = {"name": recipe_name, "ingredients": recipe_ingredients,
              "cooking_time": cooking_time}
    recipe['Difficulty']= calc_difficulty(recipe)
    return recipe

def calc_difficulty(recipe):
    for recipe in recipes_list:
        if recipe['cooking_time'] < 10 and len(recipe['ingredients']) < 4:
            difficulty = "easy"
        elif recipe['cooking_time'] < 10 and len(recipe['ingredients']) <= 4:
            difficulty = "medium"
        elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) < 4:
            difficulty = "intermediate"
        elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) >= 4:
            difficulty = "hard"
            return difficulty

n = int(input("Enter the number of recipes: "))

for number in range(n):
    recipe = take_recipe()
    for ingredient in recipe['ingredients']:
        if ingredient in ingredients_list:
            print("This ingredient is already in the list")
        else:
            ingredients_list.append(ingredient)
    recipes_list.append(recipe)


filename = input("Enter the filename where you've stored your recipes:")
try:
    file = open(filename, 'rb')
    data=pickle.load(file)
except FileNotFoundError:
    print("File not found")
except:
    print("Oops, we've stumbled on some unexpected error.") 
else:
    file.close()
finally:
    print("Goodbye!")

data = {'recipes_list': recipes_list, 'ingredients_list': ingredients_list}

new_file_name = input("Enter the name of the new file: ")
with open(new_file_name, 'wb') as file:
    pickle.dump(data, file)


