import sqlite3

db = None
cursor = None

def db_open():
    global db, cursor
    db = sqlite3.connect("shop.db")
    cursor = db.cursor()
    cursor.execute("""PRAGMA foreign_keys=on""")

def db_close():
    db.commit()
    cursor.close()
    db.close()

def db_create():
    db_open()
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS user(
                        id INTEGER PRIMARY KEY,
                        name VARCHAR,
                        login VARCHAR,
                        password VARCHAR,
                        mail VARCHAR
                   )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS category(
                        id INTEGER PRIMARY KEY,
                        title VARCHAR
                   )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS product(
                        id INTEGER PRIMARY KEY,
                        title VARCHAR,
                        info VARCHAR,
                        prise VARCHAR,
                        id_category INTEGER,
                        FOREIGN KEY (id_category) REFERENCES category(id)
                   )""")
    
    db_close()
 
def db_del():
    db_open()
    cursor.execute("""DROP TABLE user""")
    cursor.execute("""DROP TABLE product""")
    cursor.execute("""DROP TABLE category""")
    db_close()

#===================================== user =====================================================
def reg_user(name:str, login:str, password:str, mail:str):
    """login_user -> [id]"""
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

def login_user(login:str, password:str):
    """login_user -> [id]"""
    db_open()
    cursor.execute("""SELECT id
                        FROM user
                        WHERE login == ? 
                            AND password == ?
                    """,(login,password))
    data = cursor.fetchone()
    db_close()
    return data

def get_user(id:int):
    """get_user -> [name, login, mail]"""
    db_open()
    cursor.execute("""SELECT name, login, mail
                        FROM user
                        WHERE id == ? 
                    """,(id,))
    data = cursor.fetchone()
    db_close()
    return data
#===================================== category =================================================
def add_category(title:str):
    "return id"
    db_open()
    cursor.execute("""INSERT INTO category(title)
                            VALUES (?)  
                   """,(title,))
    last_id = cursor.lastrowid
    db_close()
    return last_id

def get_category(id:int):
    "id, title"
    db_open()
    cursor.execute("""SELECT id, title
                        FROM category
                        WHERE id == ?  
                   """,(id,))
    data = cursor.fetchone()
    db_close()
    return data

def get_all_category():
    "id, title"
    db_open()
    cursor.execute("""SELECT id, title
                        FROM category
                   """)
    data = cursor.fetchall()
    db_close()
    return data
#===================================== product ==================================================
def add_product(title:str, info:str, prise:float, id_category:int):
    "add_product -> id"
    db_open()
    cursor.execute("""INSERT INTO product(title, info, prise, id_category)
                            VALUES (?,?,?,?) 
                   """,(title,info,prise,id_category,))
    last_id = cursor.lastrowid
    db_close()
    return last_id

def get_product(id:int):
    " get_product -> [id, title, info, prise, category] "
    db_open()
    cursor.execute("""SELECT product.id, product.title, product.info, product.prise, category.title
                        FROM product, category
                        WHERE product.id_category == category.id
                            AND product.id == ?  
                   """,(id,))
    data = cursor.fetchall()
    db_close()
    return data

def get_all_product():
    " get_all_product -> [(id, title, info, prise, id_category), ...] "
    db_open()
    cursor.execute("""SELECT id, title, info, prise, id_category
                        FROM product
                   """)
    data = cursor.fetchall()
    db_close()
    return data

def get_form_category_product(id_category:int):
    "get_form_category_product -> [(id, title, info, prise, id_category), ...] "
    db_open()
    cursor.execute("""SELECT *
                        FROM product
                        WHERE id_category == ?  
                   """,(id_category,))
    data = cursor.fetchall()
    db_close()
    return data
#===================================== create ===================================================
if __name__ == "__main__":
    db_del()
    db_create()
    if True:
        reg_user("name1", "login1", "1111", "name1@gmail.com")
        reg_user("name2", "login2", "2222", "name2@gmail.com")
        reg_user("name3", "login3", "3333", "name3@gmail.com")

        add_category("ТЕЛЕФОНЫ") # id = 1
        add_category("НОУТБУКИ") # id = 2
        add_category("МОНИТОРЫ") # id = 3

        add_product("Samsung Galaxy A24", """Екран (6.5", Super AMOLED, 2340x1080) / Mediatek Helio G99 (2 x 2.6 ГГц + 6 x 2.0 ГГц) / основна потрійна камера: 50 Мп + 5 Мп + 2 Мп, фронтальна камера: 13 Мп / RAM 6 ГБ / 128 ГБ вбудованої пам'яті + microSD (до 1 ТБ) / 3G / LTE / GPS / ГЛОНАСС / BDS / підтримка 2х SIM-карток (Nano-SIM) / Android 13 / 5000 мА*год""", 7599.00, 1)
        add_product("Apple iPhone 15 Pro Max", """Екран (6.7", OLED (Super Retina XDR), 2796x1290) / Apple A17 Pro / основна потрійна камера: 48 Мп + 12 Мп + 12 Мп, фронтальна камера: 12 Мп / 256 ГБ вбудованої пам'яті / 3G / LTE / 5G / GPS / Nano-SIM / iOS 17 """, 52999.00, 1)
        add_product("Motorola G54 Power", """Екран (6.5", IPS, 2400x1080) / MediaTek Dimensity 7020 (2.2 ГГц + 2.0 ГГц) / подвійна основна камера: 50 Мп + 8 Мп, фронтальна камера: 16 Мп / RAM 12 ГБ / 256 ГБ вбудованої памʼяті + microSD (до 1 ТБ) / 3G / LTE / 5G / GPS / Nano-SIM + eSIM / Android 13 / 6000 мА*год""", 8888.00, 1)

        add_product("ASUS TUF Gaming A15", """Екран 15.6" IPS (1920x1080) Full HD 144 Гц, матовий / AMD Ryzen 5 7535HS (3.3 - 4.55 ГГц) / RAM 16 ГБ / SSD 1 ТБ / NVIDIA GeForce RTX 3050, 4 ГБ / без ОД / Wi-Fi / Bluetooth / веб-камера / без ОС / 2.3 кг / чорний""", 34999.00, 2)
        add_product("Apple MacBook Air 13", """Екран 13.3" Retina (2560x1600) WQXGA, глянсовий / Apple M1 / RAM 8 ГБ / SSD 256 ГБ / Apple M1 Graphics / Wi-Fi / Bluetooth / macOS Big Sur / 1.29 кг / сірий""", 31999.00, 2)
        add_product("HP Pavilion 15-eh1106ua", """Екран 15.6" IPS (1920x1080) Full HD, матовий / AMD Ryzen 5 5500U (2.1 — 4.0 ГГц) / RAM 16 ГБ / SSD 512 ГБ / AMD Radeon Graphics / без ОД / Wi-Fi / Bluetooth / вебкамера / DOS / 1.75 кг / сріблястий""", 19999.00, 2)

        add_product("Samsung Odyssey AG50", """Діагональ дисплея: 27"
    Максимальна роздільна здатність дисплея: 2560x1440 (2K QHD)
    Час реакції матриці: 1 мс (GTG)
    Тип матриці: IPS""", 9999.00, 3)
        add_product("Asus VG249QL3A", """Діагональ дисплея: 23.8"
    Максимальна роздільна здатність дисплея: 1920x1080 (FullHD)
    Час реакції матриці: 1 мс (GTG)
    Тип матриці: IPS""", 6599.00, 3)
        add_product("Acer EK271EBI", """Діагональ дисплея: 27"
    Максимальна роздільна здатність дисплея: 1920x1080 (FullHD)
    Час реакції матриці: 1 ms (VRB) / 4 ms (GTG)
    Тип матриці: IPS""", 4499.00, 3)

    print("login_user",login_user("login2","password2"))
    print("get_user",get_user(3))

    print("get_category",get_category(2))

    print("get_product",get_product(3))
    print("get_form_category_product",get_form_category_product(2))


