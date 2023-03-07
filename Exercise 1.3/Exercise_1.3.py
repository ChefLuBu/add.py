recipes_list = []
ingredients_list = []

def take_recipe():
    recipe_name = input("Enter the name of the recipe: ")
    recipe_ingredients = input("Enter the ingredients of the recipe: ")
    recipes_list.append(recipe_name)
    ingredients_list.append(recipe_ingredients)
    cooking_time = int(input("Enter the cooking time of the recipe: "))
    recipe={"name":recipe_name,"ingredients":recipe_ingredients,"cooking_time":cooking_time}
    return recipe

n = int(input("Enter the number of recipes: "))
# recipe = {}
for number in range(n):
    recipe = take_recipe()
    for ingredient in recipe['ingredients']:
        if ingredient in ingredients_list:
            print("This ingredient is already in the list")
        else:
            ingredients_list.append(ingredient)
    recipes_list.append(recipe)

for recipe in recipes_list:
    if recipe['cooking_time'] < 10 and len(recipe['ingredient']) < 4:
        recipe['difficulty'] = "easy"
    elif recipe['cooking_time'] < 10 and len(recipe['ingredient']) <= 4:
       recipe['difficulty'] = "medium"
    elif recipe['cooking_time'] >= 10 and len(recipe['ingredient']) < 4:
       recipe['difficulty'] = "intermediate"
    elif recipe['cooking_time'] >= 10 and len(recipe['ingredient']) >= 4:
       recipe['difficulty'] = "hard"

for recipe in recipes_list:
    print("Recipe name: ", recipe["name"])
    print("Ingredients: ", recipe["ingredients"])
    print("Cooking time: ", recipe["cooking_time"])
    print("Difficulty: ", recipe["difficulty"])

    def print_ingredients():
        ingredients_list.sort()
        print('All Ingredients')
        print('_______________')
        for ingredient in ingredients_list:
            print(ingredient)

print_ingredients()