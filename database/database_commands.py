from database.database_connection import open_connection
from database.database_tables_init import create_recipe_tags, create_recipes, create_tags, create_users
from datetime import datetime

def create_database():
    create_users()
    create_tags()
    create_recipes()
    create_recipe_tags()
    print('Database initialized')


def search(search_state, query):
    match search_state:
        case 'recipe':
            return list(filter(lambda recipe: query.lower() in recipe[2].lower(), get_recipes()))
        case 'tags':
            return list(filter(lambda tag: query.lower() in tag[2].lower(), get_all_tags()))


def add_user(id: int, username: str):
    db_connection, db_cursor = open_connection()
    try:
        users = get_users()
        for user in users:
            if int(user[0]) == int(id):
                raise Exception('Users is already in the database')
    except:
        return 'Users is already in the database'

    db_cursor.execute("""INSERT INTO users(
            id,
            username,
            search_state,
            created_at
        ) VALUES(?,?,?,?)""", [
            id,
            username,
            'None',
            datetime.now()
    ])
    db_connection.commit()
    db_connection.close()


def get_users():
    db_connection, db_cursor = open_connection()
    users = db_cursor.execute("SELECT * FROM users").fetchall()
    db_connection.close()
    return users

def get_user(id):
    users = get_users()
    for user in users:
        if user[0] == id:
            return user
    return None


def change_search_state(id, new_state):
    user = get_user(id)
    if user == None:
        return
    user = list(user)
    
    db_connection, db_cursor = open_connection()
    user[2] = new_state
    db_cursor.execute("""UPDATE users SET search_state=? WHERE id=?""", [new_state, id])
    db_connection.commit()
    db_connection.close()        
    

def get_all_tags():
    db_connection, db_cursor = open_connection()
    tags = db_cursor.execute("SELECT * FROM tags").fetchall()
    db_connection.close()
    return tags


def get_recipes():
    db_connection, db_cursor = open_connection()
    recipes = db_cursor.execute("SELECT * FROM recipes").fetchall()
    db_connection.close()
    return recipes


def add_recipe_tags(recipe_id: int, tag_id: int):
    db_connection, db_cursor = open_connection()
    db_cursor.execute("""INSERT INTO recipe_tags(
        recipe_id,
        tag_id
    ) VALUES(?,?)""", [
        recipe_id,
        tag_id
    ])
    db_connection.commit()
    db_connection.close()


def add_recipe(author_user_id: int, name: str, description: str, tags: list[int]):
    last_id = 0
    try:
        last_id = get_recipes()[-1][0]
    except IndexError:
        print('This is the first Recipe!')
    
    db_connection, db_cursor = open_connection()
    db_cursor.execute("""INSERT INTO recipes(
            id,
            author_user_id,
            name,
            description,
            like_count,
            created_at
        ) VALUES(?,?,?,?,?,?)""", [
            last_id + 1,
            author_user_id,
            name,
            description,
            0,
            datetime.now()
        ])
    db_connection.commit()
    
    all_tags = get_all_tags()
    for i in range(len(tags)):
        for j in range(len(all_tags)):
            if tags[i] == all_tags[j][0]:
                add_recipe_tags(tags[i], all_tags[j][0]) 
                continue
    
    db_connection.close()