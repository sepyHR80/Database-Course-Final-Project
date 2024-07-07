import sqlite3

conn = sqlite3.connect('store_1.db')
cursor = conn.cursor()

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
        print("Order placed successfully")
        return order_id
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None

def track_order_status(order_id):
    try:
        cursor.execute("""
            SELECT Orders.OrderID, Orders.OrderDate, ShippingInfo.Carrier, ShippingInfo.TrackingNumber, 
                   ShippingInfo.ShippingDate, ShippingInfo.DeliveryDate
            FROM Orders
            LEFT JOIN ShippingInfo ON Orders.OrderID = ShippingInfo.OrderID
            WHERE Orders.OrderID = ?
        """, (order_id,))
        
        order_status = cursor.fetchone()
        
        if order_status:
            print("Order Status:", order_status)
        else:
            print("Order not found")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def view_order_details(order_id):
    try:
        cursor.execute("""
            SELECT Orders.OrderID, Orders.OrderDate, Users.Username, Products.ProductName, OrderDetails.Quantity, Products.Price
            FROM Orders
            JOIN Users ON Orders.UserID = Users.UserID
            JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
            JOIN Products ON OrderDetails.ProductID = Products.ProductID
            WHERE Orders.OrderID = ?
        """, (order_id,))
        
        order_details = cursor.fetchall()
        
        if order_details:
            for detail in order_details:
                print("Order Details:", detail)
        else:
            print("Order not found")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

order_id = place_order(
    user_id=1, 
    order_date="2024-07-07",
    products={1: 2, 2: 1}  # {product_id: quantity}
)

track_order_status(order_id)
view_order_details(order_id)

conn.close()