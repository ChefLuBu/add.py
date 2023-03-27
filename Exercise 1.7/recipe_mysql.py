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

class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return "<Recipe ID: " + str(self.id) + "-" + self.name + "Difficulty: " + self.difficulty + ">"

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


def return_ingredients_as_list():
    recipes_list = session.query(Recipe).all()
    for recipe in recipes_list:
        print("Recipe: ", recipe)
        print("recipe.ingredients = ", recipe.ingredients)
        recipe_ingredints_list = recipe.ingredients.split(", ")
        print("recipe_ingredints_list = ", recipe_ingredints_list)
    

def create_recipe():
    recipe_ingredients = []
    valid_name = False
    while valid_name == False:
        name = str(input('Enter recipe name: '))
        if len(name) < 50:
            if name.isalpha():
                valid_name = True
            else:
                print("Please enter a valid name")
    else:
        print("This program only accepts names with less than 50 characters")
    valid_cooking_time = False
    while valid_cooking_time == False:
        cooking_time = input('Enter cooking time: ')
        if cooking_time.isnumeric() == True:
            valid_cooking_time = True
        else:
            print("Please enter a valid cooking time")
    valid_ingredient_number = False
    while valid_ingredient_number == False:
        ingredient_number = input('Enter number of ingredients: ')
        if ingredient_number.isnumeric() == True:
            valid_ingredient_number = True
            for i in range(int(ingredient_number)):
                ingredient = input('Enter ingredient: ')
                recipe_ingredients.append(ingredient)
        else:
            valid_ingredient_number = False
            print("Please enter a valid number of ingredients")
    recipe_ingredients_str = ', '.join(recipe_ingredients)
    print(recipe_ingredients_str)

    difficulty = calc_difficulty(cooking_time, recipe_ingredients)
    
    recipe_format = Recipe(
        name = name,
        cooking_time=int(cooking_time),
        ingredients=recipe_ingredients_str,
        difficulty=difficulty
    )

    print(recipe_format)

    session.add(recipe_format)
    session.commit()

def view_all_recipes():
    recipes_list = session.query(Recipe).all()
    for recipe in recipes_list:
        print("Recipe: ", recipe)
        print("recipe.ingredients = ", recipe.ingredients)
        recipe_ingredints_list = recipe.ingredients.split(", ")
        print("recipe_ingredints_list = ", recipe_ingredints_list)
        if recipe in recipes_list == []:
            print("There are no recipes in the database")
            return None
        
def search_by_ingredients():
    if session.query(Recipe.ingredients).count() == 0:
        print("There are no recipes in the database")
        return None
    else:
        results = session.query(Recipe.ingredients).all()
        print("results = ", results)
        all_ingredients = []
        for result in results:
            recipe_ingredients = result.ingredients.split(", ")
            all_ingredients.extend(recipe_ingredients)

        print("all_ingredients = ", all_ingredients)
        all_ingredients=list(dict.fromkeys(all_ingredients))
        all_ingredients_list = list(enumerate(all_ingredients))

        print("All ingredients list = ")
        for index, tup in enumerate(all_ingredients_list):
            print(str(tup[0]+1) + ". " + tup[1])

        try:
            ingredient_index = int(input("Enter ingredient index number: "))
            index_search = ingredient_index.split(", ")

            index_searched_ingredients = []
            for ingredient_index in index_search:
                ingredient_index_minus_one = int(ingredient_index) - 1
                search_complete = all_ingredients_list[ingredient_index_minus_one][1]
                index_searched_ingredients.append(search_complete)
            print("Here are the results of your search: ", index_searched_ingredients)


            conditions = []
            for ingredient in index_searched_ingredients:
                like_term = "%" + ingredient + "%"
                condition = Recipe.ingredients.like(like_term)
                conditions.append(condition)
            print("conditions = ", conditions)
            searched_recipes = session.query(Recipe).filter(*conditions).all()
            
            print(searched_recipes)

        except:
                print("Please enter a valid index number")
        else:
            print("searched_recipes:")
        for recipe in searched_recipes:
            print(recipe)

def delete_recipe():
    if session.query(Recipe).count() == 0:
        print("There are no recipes in the database")
        return None
    
    else:
        results = session.query(Recipe).with_entities(
            Recipe.id, Recipe.name).all()
        print("results = ", results)
        for recipe in results:
            print("Id:", recipe[0])
            print("Name:", recipe[1])
            recipe_id_delete = (
                input("Enter the id of the recipe you want to delete:")
            )

            if recipe_id_delete.isnumeric() == True:
                recipe_id_delete = int(recipe_id_delete)
                recipe_to_delete = session.query(Recipe).filter_by(
                    id=recipe_id_delete).first()
                session.delete(recipe_to_delete)
                session.commit()
                print("Recipe deleted")
            else:
                print("Please enter a valid id")
                return None
            
def modify_recipe():
    if session.query(Recipe).count() == 0:
        print("There are no recipes in the database")
        return None
    else:
        results = session.query(Recipe).with_entities(
            Recipe.id, Recipe.name).all()
        print("results = ", results)
        print("Here are the recipes in the database:")
        for recipe in results:
            print("Id:", recipe[0])
            print("Name:", recipe[1])

        recipe_id_edit = int("Enter the id of the recipe you want to edit:")
        print(session.query(Recipe).with_entities(Recipe.id).all())

        recipes_list = session.query(Recipe).with_entities(Recipe.id).all()
        recipe_id_list = []

        for recipe_tuple in recipe_id_edit:
            print(recipe_tuple[0])
            recipes_list.append(recipe_tuple[0])
        
        print(recipe_id_list)

        if recipe_id_edit not in recipe_id_list:
            print("Please enter a valid id")
        else:   print("Please, continue with the edit process")
        edited_recipe = session.query(Recipe).filter_by(id=recipe_id_edit).one()
        print("edited_recipe = ", edited_recipe)
        column_for_update = int(input("Enter the data you want to update. 1 = Name, 2 = Cooking time, 3 = Ingredients"))
        updated_data = (input("Enter the new data:"))
        print("Updated data = ", updated_data)

        if column_for_update == 1:
            print("You've selected to update the name")
            session.query(Recipe).filter(Recipe.id == recipe_id_edit).update({Recipe.name: updated_data})
            session.commit()

        elif column_for_update == 2:
            print("You've selected to update the cooking time")
            session.query(Recipe).filter(Recipe.id == recipe_id_edit).update({Recipe.cooking_time: updated_data})
            session.commit()
        
        elif column_for_update == 3:
            print("You've selected to update the ingredients")
            session.query(Recipe).filter(Recipe.id == recipe_id_edit).update({Recipe.ingredients: updated_data})
            session.commit()

        else:
            print("Please enter a valid number")
        update_difficulty = calc_difficulty(edited_recipe.cooking_time, edited_recipe.ingredients)
        print("Difficulty has been updated to: ", update_difficulty)
        edited_recipe.difficulty = update_difficulty
        session.commit()
        print("Recipe updated")



def main_menu():
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
            create_recipe()
        elif choice == '2':
            search_by_ingredients()
        elif choice == '3':
            modify_recipe()
        elif choice == '4':
            delete_recipe()
        elif choice == '5':
            print('returning to main menu')
        else:
            if choice == 'Quit':
                print("Goodbye")
                break
            else:
                print("Please enter a valid choice")

main_menu()
session.close()