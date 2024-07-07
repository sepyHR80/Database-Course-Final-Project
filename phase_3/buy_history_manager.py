import sqlite3

conn = sqlite3.connect('store_1.db')
cursor = conn.cursor()

def save_order_history(order_id):
    try:
        cursor.execute("""
            INSERT INTO OrderHistory (OrderID, UserID, OrderDate, ProductID, Quantity, Price)
            SELECT Orders.OrderID, Orders.UserID, Orders.OrderDate, OrderDetails.ProductID, OrderDetails.Quantity, Products.Price
            FROM Orders
            JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
            JOIN Products ON OrderDetails.ProductID = Products.ProductID
            WHERE Orders.OrderID = ?
        """, (order_id,))
        
        conn.commit()
        print("Order history saved successfully")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def view_user_order_history(user_id):
    try:
        cursor.execute("""
            SELECT OrderHistory.OrderID, OrderHistory.OrderDate, Products.ProductName, OrderHistory.Quantity, OrderHistory.Price
            FROM OrderHistory
            JOIN Products ON OrderHistory.ProductID = Products.ProductID
            WHERE OrderHistory.UserID = ?
        """, (user_id,))
        
        order_history = cursor.fetchall()
        
        if order_history:
            print("Order History:")
            for history in order_history:
                print(history)
        else:
            print("No order history found for the user")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def view_all_order_history():
    try:
        cursor.execute("""
            SELECT OrderHistory.OrderID, OrderHistory.OrderDate, Users.Username, Products.ProductName, OrderHistory.Quantity, OrderHistory.Price
            FROM OrderHistory
            JOIN Users ON OrderHistory.UserID = Users.UserID
            JOIN Products ON OrderHistory.ProductID = Products.ProductID
        """)
        
        order_history = cursor.fetchall()
        
        if order_history:
            print("All Order History:")
            for history in order_history:
                print(history)
        else:
            print("No order history found")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def place_order(user_id, order_date, products):
    try:
        cursor.execute("""
            INSERT INTO Orders (UserID, OrderDate) 
            VALUES (?, ?)
        """, (user_id, order_date))
        
        order_id = cursor.lastrowid

        for product_id, quantity in products.items():
            cursor.execute("""
                SELECT Price FROM Products WHERE ProductID = ?
            """, (product_id,))
            result = cursor.fetchone()
            if result:
                price = result[0]
                cursor.execute("""
                    INSERT INTO OrderDetails (OrderID, ProductID, Quantity) 
                    VALUES (?, ?, ?)
                """, (order_id, product_id, quantity))
            else:
                print(f"Product with ID {product_id} does not exist.")
        
        conn.commit()
        save_order_history(order_id)
        print("Order placed successfully")
        return order_id
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None

# Add order history table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS OrderHistory (
        OrderHistoryID INTEGER PRIMARY KEY,
        OrderID INTEGER,
        UserID INTEGER,
        OrderDate DATE,
        ProductID INTEGER,
        Quantity INTEGER,
        Price DECIMAL(10,2),
        FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
        FOREIGN KEY (UserID) REFERENCES Users(UserID),
        FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
    )
""")

# Place a sample order and save to history
order_id = place_order(
    user_id=1, 
    order_date="2024-07-07",
    products={1: 2, 2: 1}  # {product_id: quantity}
)

# View order history for a specific user
view_user_order_history(user_id=1)

# View all order history
view_all_order_history()

conn.close()