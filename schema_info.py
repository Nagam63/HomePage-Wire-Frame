import sqlite3

conn = sqlite3.connect('instance/soroban_circle.db')
cursor = conn.cursor()

# Categories
cursor.execute("SELECT * FROM categories;")
print("Categories:")
print(cursor.fetchall())

# Campaigns
cursor.execute("SELECT * FROM campaigns;")
print("Campaigns:")
print(cursor.fetchall())

# Users
cursor.execute("SELECT * FROM users;")
print("Users:")
print(cursor.fetchall())

# Articles
cursor.execute("SELECT * FROM articles;")
print("Articles:")
print(cursor.fetchall())

# Contents
cursor.execute("SELECT * FROM contents;")
print("Contents:")
print(cursor.fetchall())

conn.close()
