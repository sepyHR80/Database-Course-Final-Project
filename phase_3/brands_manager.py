import sqlite3

conn = sqlite3.connect('store_1.db')
cursor = conn.cursor()

def add_brand(brand_name):
    try:
        cursor.execute("""
            INSERT INTO Brands (BrandName) 
            VALUES (?)
        """, (brand_name,))
        
        conn.commit()
        print("Brand added successfully")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def update_brand(brand_id, brand_name):
    try:
        cursor.execute("""
            UPDATE Brands SET BrandName = ? WHERE BrandID = ?
        """, (brand_name, brand_id))
        
        conn.commit()
        print("Brand updated successfully")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def delete_brand(brand_id):
    try:
        cursor.execute("""
            DELETE FROM Brands WHERE BrandID = ?
        """, (brand_id,))
        
        conn.commit()
        print("Brand deleted successfully")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

add_brand("New Brand")
update_brand(brand_id=1, brand_name="Updated Brand")
delete_brand(brand_id=1)

conn.close()