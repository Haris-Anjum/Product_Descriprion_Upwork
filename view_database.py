import sqlite3

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('product_descriptions.db')
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

# Function to display the contents of a table
def display_table(cursor, table_name):
    cursor.execute(f'SELECT * FROM {table_name}')
    rows = cursor.fetchall()
    
    print(f"\n--- {table_name} Table ---")
    if rows:
        # Print the column names
        col_names = [description[0] for description in cursor.description]
        print(" | ".join(col_names))
        print("-" * len(" | ".join(col_names)))
        
        # Print the rows
        for row in rows:
            print(" | ".join(str(row[col]) for col in col_names))
    else:
        print(f"No data found in {table_name} table.")

# Main function to display all tables
def main():
    conn = get_db_connection()
    cursor = conn.cursor()

    # List of tables you want to display
    tables = ['products', 'attributes', 'usps', 'descriptions']

    for table in tables:
        display_table(cursor, table)

    conn.close()

if __name__ == "__main__":
    main()
