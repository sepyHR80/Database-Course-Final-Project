import sqlite3

conn = sqlite3.connect('store_1.db')
cursor = conn.cursor()

def add_discount(product_id, discount_percentage, start_date, end_date):
    try:
        cursor.execute("""
            INSERT INTO Discounts (ProductID, DiscountPercentage, StartDate, EndDate) 
            VALUES (?, ?, ?, ?)
        """, (product_id, discount_percentage, start_date, end_date))
        
        conn.commit()
        print("Discount added successfully")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def update_discount(discount_id, discount_percentage=None, start_date=None, end_date=None):
    try:
        if discount_percentage:
            cursor.execute("""
                UPDATE Discounts SET DiscountPercentage = ? WHERE DiscountID = ?
            """, (discount_percentage, discount_id))
        
        if start_date:
            cursor.execute("""
                UPDATE Discounts SET StartDate = ? WHERE DiscountID = ?
            """, (start_date, discount_id))
        
        if end_date:
            cursor.execute("""
                UPDATE Discounts SET EndDate = ? WHERE DiscountID = ?
            """, (end_date, discount_id))
        
        conn.commit()
        print("Discount updated successfully")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def apply_discounts():
    try:
        cursor.execute("""
            SELECT Products.ProductID, Products.Price, Discounts.DiscountPercentage, Discounts.StartDate, Discounts.EndDate
            FROM Products
            JOIN Discounts ON Products.ProductID = Discounts.ProductID
            WHERE Discounts.StartDate <= DATE('now') AND Discounts.EndDate >= DATE('now')
        """)
        
        discounts = cursor.fetchall()
        
        for discount in discounts:
            product_id, price, discount_percentage, start_date, end_date = discount
            discounted_price = price - (price * (discount_percentage / 100))
            print(f"Product ID: {product_id}, Original Price: {price}, Discounted Price: {discounted_price}")
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Discounts (
        DiscountID INTEGER PRIMARY KEY,
        ProductID INTEGER,
        DiscountPercentage DECIMAL(5,2),
        StartDate DATE,
        EndDate DATE,
        FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
    )
""")

add_discount(
    product_id=1,
    discount_percentage=20.0,
    start_date="2024-07-01",
    end_date="2024-07-31"
)

update_discount(
    discount_id=1,
    discount_percentage=25.0,
    end_date="2024-08-15"
)

apply_discounts()

conn.close()