import sqlite3

conn = sqlite3.connect('store_1.db')
cursor = conn.cursor()

def create_cart(user_id):
    try:
        cursor.execute("""
            INSERT INTO Cart (UserID) 
            VALUES (?)
        """, (user_id,))
        
        conn.commit()
        print("Cart created successfully")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def add_item_to_cart(cart_id, product_id, quantity):
    try:
        cursor.execute("""
            INSERT INTO CartItems (CartID, ProductID, Quantity) 
            VALUES (?, ?, ?)
        """, (cart_id, product_id, quantity))
        
        conn.commit()
        print("Item added to cart successfully")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def remove_item_from_cart(cart_id, product_id):
    try:
        cursor.execute("""
            DELETE FROM CartItems 
            WHERE CartID = ? AND ProductID = ?
        """, (cart_id, product_id))
        
        conn.commit()
        print("Item removed from cart successfully")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def update_item_quantity(cart_id, product_id, quantity):
    try:
        cursor.execute("""
            UPDATE CartItems 
            SET Quantity = ? 
            WHERE CartID = ? AND ProductID = ?
        """, (quantity, cart_id, product_id))
        
        conn.commit()
        print("Item quantity updated successfully")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def calculate_cart_total(cart_id):
    try:
        cursor.execute("""
            SELECT SUM(Products.Price * CartItems.Quantity) as Total
            FROM CartItems
            JOIN Products ON CartItems.ProductID = Products.ProductID
            WHERE CartItems.CartID = ?
        """, (cart_id,))
        
        total = cursor.fetchone()[0]
        
        if total:
            print(f"Cart total: {total}")
            return total
        else:
            print("Cart is empty or not found")
            return 0
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return 0

create_cart(user_id=1)

add_item_to_cart(cart_id=1, product_id=1, quantity=2)
add_item_to_cart(cart_id=1, product_id=2, quantity=1)

update_item_quantity(cart_id=1, product_id=1, quantity=3)

remove_item_from_cart(cart_id=1, product_id=2)

total = calculate_cart_total(cart_id=1)

conn.close()