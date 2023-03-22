import mysql.connector

conn = mysql.connector.connect(
    host="localhost", user='cf-python', passwd='password')

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

cursor.execute("USE task_database")

cursor.execute('''CREATE TABLE IF NOT EXISTS recipes (
id INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(50),
ingredients VARCHAR(255),
cooking_time INT,
difficulty VARCHAR(20)
)''')


def main_menu(conn, cursor):
    choice = ''
    while (choice != 'quit'):
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
            search_recipe(conn, cursor)
        elif choice == '3':
            modify_recipe(conn, cursor)
        elif choice == '4':
            delete_recipe(conn, cursor)
        elif choice == '5':
            print('returning to main menu')


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


def search_recipe(conn, cursor):
    all_ingredients = []
    cursor.execute("SELECT * FROM recipes")
    results = cursor.fetchall()
    for recipe_ingredients_list in results:
        for recipe_ingredients in recipe_ingredients_list:
            recipe_ingredient_split = recipe_ingredients.split(", ")
            all_ingredients.extend(recipe_ingredient_split)
    all_ingredients = list(dict.fromkeys(all_ingredients))
    all_ingredients_list = list(enumerate(all_ingredients))

    print("Ingredients:")

    for index, tup in enumerate(all_ingredients_list):
        print(str(tup[0]+1) + "." + tup[1])

    try:
        ingredient_searched_nber = input(
            "Enter the number of the ingredient you want to search: ")
        ingredient_searched_index = int(ingredient_searched_nber) - 1
        ingredient_searched = all_ingredients_list[ingredient_searched_index][1]
        print("You searched for: " + ingredient_searched)

    except:
        print("No ingredient found")

    else:
        print("Recipes with " + ingredient_searched + ":")

        cursor.execute("SELECT * FROM recipes WHERE ingredients LIKE %s",
                       ('%'+ingredient_searched+'%',))

        results_recipes_with_ingredient = cursor.fetchall()
        for row in results_recipes_with_ingredient:
            print("id: " + row[0])
            print("name: " + row[1])
            print("ingredients: " + row[2])
            print("cooking_time: " + row[3])
            print("difficulty: " + row[4])


def modify_recipe(conn, cursor):
    recipe_id_for_update = int(
        input("Enter the id of the recipe you want to update: "))
    column_to_update = str(
        input("Select either name, Ingredients, or Cooking Time to update: "))
    updated_value = (input("Enter the recipes new value: "))
    print("You selected to update the " + column_to_update +
          " of recipe " + str(recipe_id_for_update) + " to " + updated_value)

    if column_to_update == "name":
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
