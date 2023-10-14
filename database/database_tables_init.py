from database.database_connection import open_connection


def create_users():
    db_connection, db_cursor = open_connection()
    db_cursor.execute("""CREATE TABLE IF NOT EXISTS users(
         id integer [primary key],
         username text,
         created_at timestamp
      )""")
    db_connection.close()


def create_recipes():
    db_connection, db_cursor = open_connection()
    db_cursor.execute("""CREATE TABLE IF NOT EXISTS recipes(
         id integer [primary key],
         author_user_id integer,
         name text,
         description text,
         ingredients text,
         like_count integer,
         created_at timestamp
      )""")
    db_connection.close()


def create_tags():
    db_connection, db_cursor = open_connection()
    db_cursor.execute("""CREATE TABLE IF NOT EXISTS tags(
         id integer [primary key],
         name text
      )""")
    db_connection.close()


def create_recipe_tags():
    db_connection, db_cursor = open_connection()
    db_cursor.execute("""CREATE TABLE IF NOT EXISTS recipe_tags(
         recipe_id integer,
         tag_id integer
      )""")
    db_connection.close()