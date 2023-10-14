from database.database_connection import open_connection

def create_users():
    db_connection, db_cursor = open_connection()
    #db_cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    #    id TEXT)""")
    db_connection.close()

def add_user(id):
    db_connection, db_cursor = open_connection()
    try:
        users = get_users()
        for user in users:
            if int(user[0]) == int(id):
                raise Exception('Users is already in the database')
    except :
        return 'Users is already in the database'
    
    #db_cursor.execute("""INSERT INTO users(
    #    id,
    #    ) VALUES(
    #    ?,
    #    )""", [id])
    db_connection.commit()
    db_connection.close()

def get_users():
    db_connection, db_cursor = open_connection()
    users = db_cursor.execute("SELECT * FROM users").fetchall()
    db_connection.close()    
    return users