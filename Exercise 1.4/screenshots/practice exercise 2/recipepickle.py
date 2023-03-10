import pickle

with open('recipe_binary.bin', 'rb') as my_file:
    recipe = pickle.load(my_file)

print("Recipe details - ")
print("Ingredient Name:  " + recipe['Ingredient Name']) 
print(recipe['Ingredients']) 
print("Cooking time: " + recipe['Cooking Time'])
print("Difficulty:  " + recipe['Difficulty'])