import sqlite3

# Connect to SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect('product_descriptions.db')

# Create a cursor object
cursor = conn.cursor()


# Create products table
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
''')

# Create attributes table
cursor.execute('''
CREATE TABLE IF NOT EXISTS attributes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    attribute TEXT,
    FOREIGN KEY (product_id) REFERENCES products (id)
)
''')

# Create usps (Unique Selling Propositions) table
cursor.execute('''
CREATE TABLE IF NOT EXISTS usps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    usp TEXT,
    FOREIGN KEY (product_id) REFERENCES products (id)
)
''')

# Create descriptions table
cursor.execute('''
CREATE TABLE IF NOT EXISTS descriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    long_description TEXT,
    short_description_bullets TEXT,
    short_description_paragraph TEXT,
    FOREIGN KEY (product_id) REFERENCES products (id)
)
''')

# Commit changes and close the connection
conn.commit()
conn.close()




# # deleting rows

# import sqlite3

# def clear_all_tables():
#     conn = sqlite3.connect('product_descriptions.db')
#     cursor = conn.cursor()

#     try:
#         # List of tables to clear
#         tables = ['products', 'attributes', 'usps', 'descriptions']

#         for table in tables:
#             cursor.execute(f'DELETE FROM {table}')
#             print(f"Data cleared from table: {table}")

#         conn.commit()
#         print("All tables have been cleared.")
#     except sqlite3.Error as e:
#         print(f"Error: {e}")
#     finally:
#         conn.close()

# # Run the function to clear data from all tables
# clear_all_tables()
