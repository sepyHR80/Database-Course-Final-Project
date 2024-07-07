import sqlite3

conn = sqlite3.connect('store_1.db')
cursor = conn.cursor()

def add_category(category_name):
    try:
        cursor.execute("""
            INSERT INTO Categories (CategoryName) 
            VALUES (?)
        """, (category_name,))
        
        conn.commit()
        print("Category added successfully")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def update_category(category_id, category_name):
    try:
        cursor.execute("""
            UPDATE Categories SET CategoryName = ? WHERE CategoryID = ?
        """, (category_name, category_id))
        
        conn.commit()
        print("Category updated successfully")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def delete_category(category_id):
    try:
        cursor.execute("""
            DELETE FROM Categories WHERE CategoryID = ?
        """, (category_id,))
        
        conn.commit()
        print("Category deleted successfully")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

add_category("Electronics")
update_category(category_id=1, category_name="Updated Electronics")
delete_category(category_id=1)

conn.close()