#  “recipe_search.py” accesses the binary file and lists all the 
#  ingredients that are available. The user enters an ingredient,
# and thescript displays every recipe containing that specific ingredient.
import pickle 

def display_recipe(recipe):
    with open('recipe_binary.bin', 'rb') as my_file:
        recipe = pickle.load(my_file)
    print("Recipe details - ")
    print('Ingredient Name: ',','.join(recipe['ingredients']))
    # print("Ingredient Name:  " + recipe['ingredients']) 
    # print(recipe['ingredients']) 
    print("Cooking time: " + recipe['Cooking Time'])
    print("Difficulty:  " + recipe['Difficulty'])

def search_ingredient(data):
    ingredients_list = data['ingredients_list']
    indexed_ingredients_list = list(enumerate(ingredients_list, 1))
    for ingredient in indexed_ingredients_list:
        print('No.', ingredient[0], ' - ', ingredient[1])

# First, it shows the user all the available ingredients 
# contained in data, under the key all_ingredients.
# Each ingredient is displayed with a number (take the index
# of each ingredient for this purpose using the enumerate() function).
# The user enters the number of the ingredient he wants to search for.

 

    try:
        chosen_num = int(input("Enter the number of the ingredient you want to search for: "))
        index = chosen_num - 1
        ingredient_searched = ingredients_list[index]
        ingredient_searched = ingredient_searched.lower()

# The Try block asks the user to enter the number of the ingredient
# The number is stored in the variable chosen_num.
# It then retrieves the ingredient from the list of ingredients
# using the index variable. The ingredient is stored in the variable  



    except IndexError:
        print("The number you entered is not in the list.")
    except:
        print('An error occurred. Please try again.')
    else:
        for recipe in data['recipes_list']:
            for recipe_ing in recipe['ingredients']:
                if (recipe_ing == ingredient_searched):
                    print('Recipe Name: ', recipe['name'])
                    display_recipe(recipe)


filename = input('Enter the name of the desired recipe file: ')
try:
    recipe_file = open(filename, 'rb')
    data=pickle.load(recipe_file)

except FileNotFoundError:
    print("The file you entered does not exist.")   
    data = {'recipes_list': [], 'all_ingredients': []}
except:
    print('An error occurred. Please try again.')
    data = {'recipes_list': [], 'all_ingredients': []}
else:
    print("The following ingredients are available: ")
    search_ingredient(data)
finally:
    recipe_file.close()
