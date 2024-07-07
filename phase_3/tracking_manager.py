import sqlite3

conn = sqlite3.connect('store_1.db')
cursor = conn.cursor()

def add_shipping_info(order_id, carrier, tracking_number, shipping_date, delivery_date):
    try:
        cursor.execute("""
            INSERT INTO ShippingInfo (OrderID, Carrier, TrackingNumber, ShippingDate, DeliveryDate) 
            VALUES (?, ?, ?, ?, ?)
        """, (order_id, carrier, tracking_number, shipping_date, delivery_date))
        
        conn.commit()
        print("Shipping information added successfully")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def track_shipping(order_id):
    try:
        cursor.execute("""
            SELECT Carrier, TrackingNumber, ShippingDate, DeliveryDate
            FROM ShippingInfo
            WHERE OrderID = ?
        """, (order_id,))
        
        shipping_info = cursor.fetchone()
        
        if shipping_info:
            print(f"Shipping Information for order {order_id}: {shipping_info}")
        else:
            print("No shipping information found for this order")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS ShippingInfo (
        ShippingID INTEGER PRIMARY KEY,
        OrderID INTEGER,
        Carrier TEXT,
        TrackingNumber TEXT,
        ShippingDate DATE,
        DeliveryDate DATE,
        FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
    )
""")


add_shipping_info(
    order_id=1,
    carrier="FedEx",
    tracking_number="123456789",
    shipping_date="2024-07-07",
    delivery_date="2024-07-10"
)


track_shipping(order_id=1)

conn.close()