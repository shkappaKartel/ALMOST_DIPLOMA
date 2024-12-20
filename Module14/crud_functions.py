import sqlite3

def initiate_db():
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL,
            image_url TEXT
        )
    ''')
    connection.commit()
    connection.close()

def add_product(title, description, price, image_url):
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO Products (title, description, price, image_url) 
        VALUES (?, ?, ?, ?)
    ''', (title, description, price, image_url))
    connection.commit()
    connection.close()

def get_all_products():
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    cursor.execute('SELECT title, description, price, image_url FROM Products')
    products = cursor.fetchall()
    connection.close()
    return products

initiate_db()