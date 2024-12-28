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
        ) bb
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL,
            balance INTEGER DEFAULT 1000
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
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, description, price, image_url FROM Products")
    products = cursor.fetchall()

    conn.close()
    return products

def add_user(username, email, age):
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO Users (username, email, age, balance)
        VALUES (?, ?, ?, 1000)
    ''', (username, email, age))
    connection.commit()
    connection.close()

def is_included(username):
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM Users WHERE username = ?', (username,))
    exists = cursor.fetchone()[0] > 0
    connection.close()
    return exists

initiate_db()