import sqlite3

conn = sqlite3.connect('store_1.db')
cursor = conn.cursor()

def add_product(product_name, brand_id, price, stock_quantity, description):
    try:
        cursor.execute("""
            INSERT INTO Products (ProductName, BrandID, Price, StockQuantity, Description) 
            VALUES (?, ?, ?, ?, ?)
        """, (product_name, brand_id, price, stock_quantity, description))
        
        conn.commit()
        print("Product added successfully")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def update_product(product_id, product_name=None, brand_id=None, price=None, stock_quantity=None, description=None):
    try:
        if product_name:
            cursor.execute("""
                UPDATE Products SET ProductName = ? WHERE ProductID = ?
            """, (product_name, product_id))
        
        if brand_id:
            cursor.execute("""
                UPDATE Products SET BrandID = ? WHERE ProductID = ?
            """, (brand_id, product_id))
        
        if price:
            cursor.execute("""
                UPDATE Products SET Price = ? WHERE ProductID = ?
            """, (price, product_id))
        
        if stock_quantity:
            cursor.execute("""
                UPDATE Products SET StockQuantity = ? WHERE ProductID = ?
            """, (stock_quantity, product_id))
        
        if description:
            cursor.execute("""
                UPDATE Products SET Description = ? WHERE ProductID = ?
            """, (description, product_id))
        
        conn.commit()
        print("Product updated successfully")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def delete_product(product_id):
    try:
        cursor.execute("""
            DELETE FROM Products WHERE ProductID = ?
        """, (product_id,))
        
        conn.commit()
        print("Product deleted successfully")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

add_product(
    product_name="New Product",
    brand_id=1,
    price=99.99,
    stock_quantity=100,
    description="This is a new product."
)

update_product(
    product_id=1,
    product_name="Updated Product",
    price=79.99,
    stock_quantity=150
)

delete_product(product_id=1)

conn.close()