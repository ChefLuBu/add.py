from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql://cf-python:password@localhost/my_database")

Base = declarative_base()

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
#Engine is the vehicle that connects to the database
#Session is the bridge that connects the engine to the database
#Base is the base class that all classes inherit from

class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return (
            "< Recipe ID: "
            + str(self.id)
            + "-"
            + self.name
            + ", Difficulty: "
            + self.difficulty
            + ">"
        )
#__repr__ is a special method that returns a string representation 
# of the object

def calc_difficulty(cooking_time, recipe_ingredients):
    if (cooking_time < 10) and (len(recipe_ingredients) < 4):
        difficulty = "easy"
    elif (cooking_time < 10) and (len(recipe_ingredients) >= 4):
        difficulty = "medium"
    elif (cooking_time >= 10) and (len(recipe_ingredients) < 4):
        difficulty = "intermediate"
    elif (cooking_time >= 10) and (len(recipe_ingredients) >= 4):
        difficulty = "hard"
    else:
        print("An error occured")

    print("Difficulty: " + difficulty)
    return difficulty


def return_ingredients_as_list():
    recipes_list = session.query(Recipe).all()
    for recipe in recipes_list:
        print("Recipe: ", recipe)
        print("recipe.ingredients = ", recipe.ingredients)
        recipe_ingredints_list = recipe.ingredients.split(", ")
        print("recipe_ingredints_list = ", recipe_ingredints_list)
#.split(", ") is splitting the string into a list

def create_recipe():
    recipe_ingredients = []
    valid_name = False
    while valid_name == False:
        name = str(input("Enter recipe name: "))
        if len(name) < 50:
            if type(name)==str:
                valid_name = True
#This was a better catch than isalpha() because it allows for spaces
# but still catches numbers 
            else:
                print("Please enter a valid name")
        else:
            print("This program only accepts names with less than 50 characters")
    valid_cooking_time = False
    while valid_cooking_time == False:
        cooking_time = input("Enter cooking time in minutes: ")
        if cooking_time.isnumeric() == True:
            valid_cooking_time = True
##isnumeric() is a method that returns True if all characters 
# in the string are numeric
        else:
            print("Please enter a valid cooking time")
    valid_ingredient_number = False
    while valid_ingredient_number == False:
        ingredient_number = input("Enter number of ingredients: ")
        if ingredient_number.isnumeric() == True:
            valid_ingredient_number = True
            for _ in range(int(ingredient_number)):
##The underscore is a dummy variable that is used to iterate through a loop
                ingredient = input("Enter ingredient: ")
                if ingredient.isalpha():
                    recipe_ingredients.append(ingredient)
                else:
                    print("Please enter a valid ingredients, delete your mistakes and try again")
                    break
##This is a break statement that breaks out of the loop if the user enters
# an invalid ingredient, such as multiple ingredients or a number 
# or special character. It currently will still create the recipe, however
# it will not add the ingredients to the recipe, so it should be deleted
        else:
            valid_ingredient_number = False
            print("Please enter a valid number of ingredients")
    recipe_ingredients_str = ", ".join(recipe_ingredients)
    print(recipe_ingredients_str)
#.join() is a method that joins the elements of an 
# iterable to the end of the string
    difficulty = calc_difficulty(int(cooking_time), recipe_ingredients)

    recipe_format = Recipe(
        name=name,
        cooking_time=int(cooking_time),
        ingredients=recipe_ingredients_str,
        difficulty=difficulty,
    )

    print(recipe_format)

    session.add(recipe_format)
    session.commit()
#This is the method that adds the recipe to the database


def view_all_recipes():
    all_recipes = []
    all_recipes = session.query(Recipe).all()
    if len(all_recipes)==0:
        print("There are no recipes in the database")
        return None
    else:
        print("Here are all the recipes in the database: ")
        print("\n")
        for recipe in all_recipes:
            print(recipe)
#This is a method that returns all the recipes in the database
#len() is a method that returns the length of an object
#for recipe in all_recipes is a for loop that iterates through the list


def search_by_ingredients():
    if session.query(Recipe.ingredients).count() == 0:
        print("There are no recipes in the database")
        return None
    else:
        results = session.query(Recipe.ingredients).all()
        all_ingredients = []
        for recipe_ingredients_list in results:
            for recipe_ingredient in recipe_ingredients_list:
                recipe_ingredients = recipe_ingredient.split(", ")
                all_ingredients.extend(recipe_ingredients)
#.split(", ") is splitting the string into a list
#extend() is a method that adds all the elements 
# of an iterable to the end of the list

        all_ingredients = list(dict.fromkeys(all_ingredients))
        all_ingredients_list = list(enumerate(all_ingredients))
#dict.fromkeys() is a method that returns a dictionary with the 
# specified keys and values. enumerate() is a method that takes a
# collection (e.g. a tuple) and returns it as an enumerate object

        print("All ingredients list: ")

        for index, tup in enumerate(all_ingredients_list):
            print(str(tup[0] + 1) + ". " + tup[1])
#index is the index number of the ingredient
#tup is the tuple of the ingredient
#tup[0] is the index number of the ingredient + 1, so 
# that the index number starts at 1
        try:
            ingredient_index = int(input("Enter ingredient index number"))
            index_searched_ingredients = []
            for ingredient in all_ingredients:
                index_searched_ingredients.append(all_ingredients[(ingredient_index - 1)])
                
#append is adding all_ingredients[(ingredient_index - 1)] to 
# the index_searched_ingredients

            conditions = []
            for ingredient in index_searched_ingredients:
                like_term = "%" + ingredient + "%"
                condition = Recipe.ingredients.like(like_term)
                conditions.append(condition)
            searched_recipes = session.query(Recipe).filter(*conditions).all()

  
#conditions is taking the index_searched_ingredients and adding it 
# to the like_term
#like_term is adding the % to the index_searched_ingredients
#searched_recipes is adding the conditions to the 
# session.query(Recipe).filter(*conditions).all()

        except:
            print("Please enter a valid index number")
        else:
            print("searched_recipes: ")
            print("\n")
            for recipe in searched_recipes: 
                print(recipe)
                print("\n")


def delete_recipe():
    if session.query(Recipe).count() == 0:
        print("There are no recipes in the database")
        return None

    else:
        results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()
        print("results = ", results)
        for recipe in results:
            print("Id:", recipe[0])
            print("Name:", recipe[1])
            recipe_id_delete = input(
                "Enter the id of the recipe you want to delete or press enter to return to main menu:"
            )

            if recipe_id_delete.isnumeric() == True:
                recipe_id_delete = int(recipe_id_delete)
                recipe_to_delete = (
                    session.query(Recipe).filter_by(id=recipe_id_delete).first()
                )
                session.delete(recipe_to_delete)
                session.commit()
                print("Recipe deleted")
            else:
                print("Please enter a valid id")
                return None
#simple delete function that deletes a recipe from the database

def modify_recipe():
    if session.query(Recipe).count() == 0:
        print("There are no recipes in the database")
        return None
    else:
        results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()
        print("Here are the recipes in the database:")
        for recipe in results:
            print("Id:", recipe[0])
            print("Name:", recipe[1])

        recipe_id_edit = int(input("Enter the id of the recipe you want to edit:"))
        print(session.query(Recipe).with_entities(Recipe.id).all())
#with_entities() is a method that returns a list of tuples

        recipes_list = session.query(Recipe).with_entities(Recipe.id).all()
        recipe_id_list = []

#recipes_list is a list of tuples containing the recipe ids
        for recipe_tuple in recipes_list:
            print(recipe_tuple[0])
            recipe_id_list.append(recipe_tuple[0])
#append is adding the recipe_tuple[0] to the recipe_id_list
#the tuple contains the recipe id

        print(recipe_id_list)

        if recipe_id_edit not in recipe_id_list:
            print("Please enter a valid id")
        else:
            print("Please, continue with the edit process")
        edited_recipe = session.query(Recipe).filter_by(id=recipe_id_edit).one()
        print("edited_recipe = ", edited_recipe)
        column_for_update = int(
            input(
                "Enter the data you want to update. 1 = Name, 2 = Cooking time, 3 = Ingredients"
            )
#column_for_update is the column that the user wants to update
        )
        updated_data = input("Enter the new data:")
        print("Updated data = ", updated_data)

        if column_for_update == 1:
            print("You've selected to update the name")
            session.query(Recipe).filter(Recipe.id == recipe_id_edit).update(
                {Recipe.name: updated_data}
            )
            session.commit()

        elif column_for_update == 2:
            print("You've selected to update the cooking time")
            session.query(Recipe).filter(Recipe.id == recipe_id_edit).update(
                {Recipe.cooking_time: updated_data}
            )
            session.commit()

        elif column_for_update == 3:
            print("You've selected to update the ingredients")
            session.query(Recipe).filter(Recipe.id == recipe_id_edit).update(
                {Recipe.ingredients: updated_data}
            )
            session.commit()

        else:
            print("Please enter a valid number")
        update_difficulty = calc_difficulty(
            edited_recipe.cooking_time, edited_recipe.ingredients
        )
        print("Difficulty has been updated to: ", update_difficulty)
        edited_recipe.difficulty = update_difficulty
        session.commit()
        print("Recipe updated")


def main_menu():
    choice = ""
    while choice != "Quit":
        print("What action would you like to perform?")
        print("1. Create recipe")
        print("2. Search recipe")
        print("3. Modify recipe")
        print("4. Delete recipe")
        print("5. View all recipes")
        print("\n Type Quit to exit the program")
        choice = input("Enter choice: ")
        if choice == "1":
            create_recipe()
        elif choice == "2":
            search_by_ingredients()
        elif choice == "3":
            modify_recipe()
        elif choice == "4":
            delete_recipe()
        elif choice == "5":
            view_all_recipes()
        else:
            if choice == "Quit":
                print("Goodbye")
                break
            else:
                print("Please enter a valid choice")


main_menu()
session.close()
