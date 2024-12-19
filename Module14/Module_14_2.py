import sqlite3
from itertools import count

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

cursor.execute("DELETE FROM Users")

for i in range(1,11):
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                   (f"User{i}", f"example{i}@gmail.com", "i*10", "1000"))

cursor.execute("SELECT id FROM Users")
user_ids = [row[0] for row in cursor.fetchall()]
for i, user_id in enumerate(user_ids):
    if i % 2 == 0:
        cursor.execute("UPDATE Users SET balance = ? WHERE id = ?", (500, user_id))

cursor.execute("SELECT id FROM Users")
user_ids =[row[0] for row in cursor.fetchall()]
for i, user_id in enumerate(user_ids):
    if (i+1)%3==0:
        cursor.execute("DELETE FROM Users WHERE id = ?", (user_id,))

cursor.execute("SELECT username, email, age, balance FROM Users WHERE age != 60")
rows = cursor.fetchall()

for row in rows:
    print(f"Имя: {row[0]} | Эл. адрес: {row[1]} | Возраст: {row[2]} | Баланс: {row[3]}:)")

cursor.execute("DELETE FROM Users WHERE id = ?", (6,))

cursor.execute("SELECT COUNT(*) FROM Users")
total_users = cursor.fetchone()[0]

cursor.execute("SELECT SUM(balance) FROM Users")
all_balances = cursor.fetchone()[0]

print(all_balances / total_users)

connection.commit()
connection.close()