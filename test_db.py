from database.database_commands import *

if __name__ == '__main__':
    create_database()
    add_user(-1, 'hello')
    print(get_users())
    print(get_all_tags())
    add_recipe(-1, 'Маффин', 'oh nooo', [])
    print(get_recipes())
