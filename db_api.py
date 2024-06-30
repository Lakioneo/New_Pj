import sqlite3

name = "data.db"
db = None
cursor = None

#======================== DB ========================================
def db_open(): 
    global db,cursor
    db = sqlite3.connect(name)
    cursor = db.cursor()
#-----------------------------------------------------------------
def db_close():
    db.commit()
    cursor.close()
    db.close()    
#-----------------------------------------------------------------
def db_clear():
    ''' удаляет все таблицы '''
    db_open()
    cursor.execute('''DROP TABLE IF EXISTS shop''')
    cursor.execute('''DROP TABLE IF EXISTS user''')
    cursor.execute('''DROP TABLE IF EXISTS category''')
    db_close()
#-----------------------------------------------------------------   
def create():
    db_open()
    cursor.execute('''PRAGMA foreign_keys=on''')

    cursor.execute("""CREATE TABLE IF NOT EXISTS user (
                        id INTEGER PRIMARY KEY,
                        name VARCHAR,
                        login VARCHAR,
                        password VARCHAR,
                        mail VARCHAR
                            )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS category (
                        id INTEGER PRIMARY KEY,
                        title VARCHAR
                   )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS product (
                        id INTEGER PRIMARY KEY,
                        title VARCHAR,
                        info VARCHAR,
                        id_category INTEGER,
                        id_user INTEGER,
                        FOREIGN KEY (id_category) REFERENCES category(id),
                        FOREIGN KEY (id_user) REFERENCES user(id)
                   )""")


    db_close()

#======================== user ========================================
def reg_user(name:str, login:str, password:str, mail:str):
    last_id = None

    db_open()
    
    cursor.execute("""SELECT login, mail
                        FROM user
                        WHERE login == ? 
                            OR mail == ?
                    """,(login, mail))
    data = cursor.fetchall()

    if data == None or len(data) == 0:
        cursor.execute("""INSERT INTO user(name, login, password, mail)
                            VALUES (?, ?, ?, ?) 
                        """,(name, login, password, mail))
        last_id = cursor.lastrowid

    db_close()
    
    return last_id
#-----------------------------------------------------------------
def login_user(login:str, password:str):
    db_open()
    cursor.execute("""SELECT id
                        FROM user
                        WHERE login == ? 
                            OR password == ?
                    """,(login,password))
    data = cursor.fetchone()
    db_close()
    return data
#-----------------------------------------------------------------
def get_user(id:int):
    db_open()
    cursor.execute("""SELECT name, login, mail
                        FROM user
                        WHERE id == ? 
                    """,(id,))
    data = cursor.fetchone()
    db_close()
    return data

#========================== category ======================================
def add_category(title:str):
    db_open()
    cursor.execute("""INSERT INTO category(title) 
                   VALUE (?)
                   """,(title,))
    last_id = cursor.lastrowid
    db_close()
    return last_id
#-----------------------------------------------------------------
def get_category(id:int):
    """get_category -> [id, title]"""
    db_open()
    cursor.execute("""SELECT id, title
                        FROM category
                        WHERE id == ?
                   """,(id,))
    data = cursor.fetchone()
    db_close()
    return data
#-----------------------------------------------------------------
def get_all_category():
    """get_all_category -> [(id, title), ...]"""
    db_open()
    cursor.execute("""SELECT id, title
                        FROM category
                   """)
    data = cursor.fetchall()
    db_close()
    return data

#============================= product ===================================
def add_product(title:str,info:str,id_category:int,id_user:int):
    db_open()
    cursor.execute("""INSERT INTO product(title,info,id_category,id_user) 
                   VALUE (?,?,?,?)
                   """,(title,info,id_category,id_user))
    last_id = cursor.lastrowid
    db_close()
    return last_id
#-----------------------------------------------------------------
def get_product(id:int):
    """get_category -> [id, title, info, id_category, id_user]"""
    db_open()
    cursor.execute("""SELECT id, title, info, id_category, id_user
                        FROM product
                        WHERE id == ?
                   """,(id,))
    data = cursor.fetchone()
    db_close()
    return data
#-----------------------------------------------------------------
def get_all_product():
    """get_category -> [(id, title, info, id_category, id_user), ...]"""
    db_open()
    cursor.execute("""SELECT id, title, info, id_category, id_user
                        FROM product
                   """)
    data = cursor.fetchall()
    db_close()
    return data
#-----------------------------------------------------------------
def get_from_category_product(id_category:int):
    """get_category -> [(id, title, info, id_category, id_user), ...]"""
    db_open()
    cursor.execute("""SELECT id, title, info, id_category, id_user
                        FROM product
                        WHERE id_category == ?
                   """,(id_category,))
    data = cursor.fetchall()
    db_close()
    return data
#================================================================

if __name__ == "__main__":
    db_clear()
    create()
    
    reg_user("nam1","log1","1111","pp1@gmail.com")
    reg_user("name2","log2","1111","pp2@gmail.com")
    reg_user("name3","log3","1111","pp3@gmail.com")






