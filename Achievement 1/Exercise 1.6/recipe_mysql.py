import mysql.connector
#requires install of mysql.connector via pip install mysql-connector-python

conn = mysql.connector.connect(
    host="localhost", user='cf-python', passwd='password')
#user and password are created in mysql workbench

cursor = conn.cursor()
#cursor is used to execute SQL queries

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
#creates database if a database with the specified name does not exist

cursor.execute("USE task_database")

cursor.execute('''CREATE TABLE IF NOT EXISTS recipes (
id INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(50),
ingredients VARCHAR(255),
cooking_time INT,
difficulty VARCHAR(20)
)''')
#creates table if a table with the specified name does not exist
#id is the primary key and is auto incremented
#name is a varchar with a max length of 50
#ingredients is a varchar with a max length of 255
#cooking_time is an integer
#difficulty is a varchar with a max length of 20

def main_menu(conn, cursor):
    choice = ''
    while (choice != 'Quit'):
        print("What action would you like to perform?")
        print("1. Create recipe")
        print("2. Search recipe")
        print("3. Modify recipe")
        print("4. Delete recipe")
        print("5. Quit")
        print("\n Type Quit to exit the program")
        choice = input("Enter choice: ")
        if choice == '1':
            create_recipe(conn, cursor)
        elif choice == '2':
            search_recipe(cursor)
        elif choice == '3':
            modify_recipe(conn, cursor)
        elif choice == '4':
            delete_recipe(conn, cursor)
        elif choice == '5':
            print('returning to main menu')
#as long as the user does not enter quit, the program will continue to run

def create_recipe(conn, cursor):
    recipe_ingredients = []
    name = str(input('Enter recipe name: '))
    cooking_time = int(input('Enter cooking time: '))
    ingredients = input('Enter ingredients: ')
    recipe_ingredients.append(ingredients)
    recipe_ingredients_str = ', '.join(recipe_ingredients)
    difficulty = calc_difficulty(cooking_time, recipe_ingredients)
    sql = "INSERT INTO recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
    val = (name, recipe_ingredients_str, cooking_time, difficulty)
    cursor.execute(sql, val)
    conn.commit()
    print("Recipe added")
#creates a recipe and adds it to the database
#the difficulty is calculated using the calc_difficulty function
#the ingredients are added to a list and then converted to a string
#the string is then added to the database
#the database is then committed
#the user is then notified that the recipe has been added

def calc_difficulty(cooking_time, recipe_ingredients):
    if (cooking_time < 10) and (len(recipe_ingredients) < 4):
        difficulty = "easy"
    elif (cooking_time < 10) and (len(recipe_ingredients) > 4):
        difficulty = "medium"
    elif (cooking_time >= 10) and (len(recipe_ingredients) < 4):
        difficulty = "intermediate"
    elif (cooking_time >= 10) and (len(recipe_ingredients) >= 4):
        difficulty = "hard"
    else:
        print("An error occured")

    print("Difficulty: " + difficulty)
    return difficulty
#calculates the difficulty of the recipe based on the cooking time and number of ingredients

def search_recipe(cursor):
    all_ingredients = []
    cursor.execute("SELECT ingredients FROM recipes")
    results = cursor.fetchall()
    for recipe_ingredients_list in results:
        for recipe_ingredients in recipe_ingredients_list:
            recipe_ingredient_split = recipe_ingredients.split(", ")
            all_ingredients.extend(recipe_ingredient_split)
    all_ingredients = list(dict.fromkeys(all_ingredients))
    all_ingredients_list = list(enumerate(all_ingredients))
#searches the database for a specific ingredient
#When the user enters an ingredient, the program searches the database for recipes that contain that ingredient
#it then prints the recipes that contain that ingredient
    
    print("Ingredients:")

    for index, tup in enumerate(all_ingredients_list):
        print(str(tup[0]+1) + "." + tup[1])
#enumerates the ingredients and prints them to the screen
#the user is then prompted to enter the number of the ingredient they want to search for

    try:
        ingredient_searched_nber = input(
            "Enter the number of the ingredient you want to search: ")
        ingredient_searched_index = int(ingredient_searched_nber) - 1
        ingredient_searched = all_ingredients_list[ingredient_searched_index][1]
        print("You searched for: " + ingredient_searched)
#the user input is converted to an integer and then used to index the list of ingredients
#the ingredient is then printed to the screen

    except:
        print("No ingredient found")

    else:
        print("Recipes with " + ingredient_searched + ":")
#the program then searches the database for recipes that contain the ingredient

        cursor.execute("SELECT * FROM recipes WHERE ingredients LIKE %s",
                       ('%'+ingredient_searched+'%',))
#the % is used to search for the ingredient anywhere in the string

        results_recipes_with_ingredient = cursor.fetchall()
        for row in results_recipes_with_ingredient:
            print("id: ",  row[0])
            print("name: ",  row[1])
            print("ingredients: ",  row[2])
            print("cooking_time: ",  row[3])
            print("difficulty: ",  row[4])
#the results are then printed to the screen
#containing the id, name, ingredients, cooking time, and difficulty
#the row[0] is the id, row[1] is the name, etc.


def modify_recipe(conn, cursor):
    recipe_id_for_update = int(
        input("Enter the id of the recipe you want to update: "))
    column_to_update = str(
        input("Select either name, Ingredients, or Cooking Time to update: "))
    updated_value = (input("Enter the recipes new value: "))
    print("You selected to update the " + column_to_update +
          " of recipe " + str(recipe_id_for_update) + " to " + updated_value)
#the user is prompted to enter the id of the recipe they want to update
#the user is then prompted to enter the column they want to update
#either name, ingredients, or cooking time
#the user is then prompted to enter the new value for the column
#the user is then notified of the changes they are about to make
#difficulty is not included because it is calculated based on the cooking time and ingredients

    if column_to_update == "Name":
        cursor.execute("UPDATE recipes SET name = %s WHERE id = %s",
                       (updated_value, recipe_id_for_update))
        print("Recipe name updated")

    elif column_to_update == "Cooking Time":
        cursor.execute("UPDATE recipes SET cooking_time = %s WHERE id = %s",
                       (updated_value, recipe_id_for_update))
        cursor.execute("SELECT * FROM recipes WHERE id = %s",
                       (recipe_id_for_update, ))
        print("Recipe updated")
        result_recipe_for_update = cursor.fetchall()

        name = result_recipe_for_update[0][1]
        recipe_ingredients = tuple(result_recipe_for_update[0][2].split(','))
        cooking_time = result_recipe_for_update[0][3]

    elif column_to_update == "Ingredients":
        cursor.execute("UPDATE recipes SET ingredients = %s WHERE id = %s",
                       (updated_value, recipe_id_for_update))
        cursor.execute("SELECT * FROM recipes WHERE id = %s",
                       (recipe_id_for_update, ))
        result_recipe_for_update = cursor.fetchall()
        print("Recipe ingredients updated")

        name = result_recipe_for_update[0][1]
        recipe_ingredients = tuple(result_recipe_for_update[0][2].split(", "))
        cooking_time = result_recipe_for_update[0][3]
        difficulty = result_recipe_for_update[0][4]

        updated_difficulty = calc_difficulty(cooking_time, recipe_ingredients)
        print("Updated difficulty: " + updated_difficulty)
        cursor.execute("UPDATE recipes SET difficulty = %s WHERE id = %s",
                       (updated_difficulty, recipe_id_for_update))
        print("Difficulty updated")

    conn.commit()


def delete_recipe(conn, cursor):
    recipe_id_for_deletion = (
        input("\nEnter the ID of the recipe you want to delete: "))
    cursor.execute("DELETE FROM Recipes WHERE id = (%s)",
                   (recipe_id_for_deletion, ))

    conn.commit()
    print("\nRecipe deleted.")


main_menu(conn, cursor)
print("Goodbye\n")
