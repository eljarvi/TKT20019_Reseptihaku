from db import db
from sqlalchemy.sql import text


def add_recipe(user_id, name, desc, time, priv, ingr, inst):
    sql = "INSERT INTO Recipes (user_id, name, description, time, privacy, visible) \
            VALUES (:user_id, :name, :desc, :time, :priv, true) RETURNING id"
    recipe_id = db.session.execute(
        text(sql),
        {"user_id": user_id, "name":name, "desc":desc, "time": time, "priv": priv}
        ).fetchone()[0]

    for ingredient in ingr:
        sql = "INSERT INTO Ingredients (recipe_id, name, quantity, visible) \
            VALUES (:recipe_id, :name, :quantity, true)"
        db.session.execute(
            text(sql),
            {"recipe_id": recipe_id, "name": ingredient[0], "quantity": ingredient[1]}
            )
    sql = "INSERT INTO Instructions (recipe_id, instruction, visible) \
            VALUES (:recipe_id, :instruction, true)"
    db.session.execute(text(sql), {"recipe_id": recipe_id, "instruction": inst})
    db.session.commit()

def add_ingredient(recipe_id, name, quantity):
    sql = "INSERT INTO Ingredients (recipe_id, name, quantity, visible) \
            VALUES (:recipe_id, :name, :quantity, true)"
    db.session.execute(text(sql), {"recipe_id": recipe_id, "name": name, "quantity": quantity})
    db.session.commit()

def recipe_properties(recipe_id):
    sql = "SELECT id, user_id, name, description, time,  \
            privacy FROM Recipes WHERE id = :recipe_id AND visible"
    return db.session.execute(text(sql), {"recipe_id": recipe_id}).fetchone()

def recipe_ingredients(recipe_id):
    sql = "SELECT name, quantity, id FROM Ingredients WHERE recipe_id = :recipe_id AND visible"
    return db.session.execute(text(sql), {"recipe_id": recipe_id}).fetchall()

def recipe_instructions(recipe_id):
    sql = "SELECT instruction FROM Instructions WHERE recipe_id = :recipe_id AND visible"
    return db.session.execute(text(sql), {"recipe_id": recipe_id}).fetchone()[0]

def users_recipes(user_id):
    sql = "SELECT id FROM Recipes WHERE user_id = :user_id AND visible"
    result = db.session.execute(text(sql), {"user_id": user_id}).fetchall()
    return [row[0] for row in result]

def all_recipes():
    sql = "SELECT id FROM Recipes WHERE privacy = FALSE AND visible"
    result = db.session.execute(text(sql)).fetchall()
    return [row[0] for row in result]

def remove_recipe(recipe_id):
    sql = "UPDATE Recipes SET visible = FALSE WHERE id = :recipe_id"
    db.session.execute(text(sql), {"recipe_id": recipe_id})
    sql = "UPDATE Ingredients SET visible = FALSE WHERE recipe_id = :recipe_id"
    db.session.execute(text(sql), {"recipe_id": recipe_id})
    sql = "UPDATE Instructions SET visible = FALSE WHERE recipe_id = :recipe_id"
    db.session.execute(text(sql), {"recipe_id": recipe_id})
    db.session.commit()

def change_recipe_properties(recipe_id, name, desc, time, priv):
    sql = "UPDATE Recipes SET name = :name WHERE id = :recipe_id"
    db.session.execute(text(sql), {"recipe_id": recipe_id, "name": name})
    sql = "UPDATE Recipes SET description = :desc WHERE id = :recipe_id"
    db.session.execute(text(sql), {"recipe_id": recipe_id, "desc": desc})
    sql = "UPDATE Recipes SET time = :time WHERE id = :recipe_id"
    db.session.execute(text(sql), {"recipe_id": recipe_id, "time": time})
    sql = "UPDATE Recipes SET privacy = :priv WHERE id = :recipe_id"
    db.session.execute(text(sql), {"recipe_id": recipe_id, "priv": priv})
    db.session.commit()

def change_recipe_instructions(recipe_id, instructions):
    sql = "UPDATE Instructions SET instruction = :instructions WHERE recipe_id = :recipe_id"
    db.session.execute(text(sql), {"recipe_id": recipe_id, "instructions": instructions})
    db.session.commit()

def remove_ingredient(ingredient_id):
    sql = "UPDATE Ingredients SET visible = false WHERE id =:ingredient_id"
    db.session.execute(text(sql), {"ingredient_id": ingredient_id})
    db.session.commit()

def search_recipes(name, maxtime, ingredient):
    sql = "SELECT DISTINCT R.id FROM Recipes R, Ingredients I \
            WHERE R.id = I.recipe_id AND LOWER(R.name) LIKE :name \
            AND R.time <= :maxtime AND I.visible AND NOT R.privacy \
            AND LOWER(I.name) LIKE :ingredient"
    result = db.session.execute(
            text(sql),
            {"maxtime": maxtime, "name": name, "ingredient": ingredient}
            ).fetchall()
    return [row[0] for row in result]
        