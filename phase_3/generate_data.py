import sqlite3
from faker import Faker
import random

# Initialize Faker
fake = Faker()

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('store_1.db')
cursor = conn.cursor()

for _ in range(10):
    cursor.execute("INSERT INTO Admins (Username, Password, Email) VALUES (?, ?, ?)",
                   (fake.user_name(), fake.password(), fake.email()))

# Insert fake records into Users table
for _ in range(50):
    cursor.execute("INSERT INTO Users (Username, Password, Email, PhoneNumber) VALUES (?, ?, ?, ?)",
                   (fake.user_name(), fake.password(), fake.email(), fake.phone_number()))

# Insert fake records into Addresses table
for _ in range(100):
    cursor.execute("INSERT INTO Addresses (UserID, Street, City, State, PostalCode, Country) VALUES (?, ?, ?, ?, ?, ?)",
                   (random.randint(1, 50), fake.street_address(), fake.city(), fake.state(), fake.postcode(), fake.country()))

# Insert fake records into Cart table
for _ in range(50):
    cursor.execute("INSERT INTO Cart (UserID) VALUES (?)", (random.randint(1, 50),))

# Insert fake records into CartItems table
for _ in range(200):
    cursor.execute("INSERT INTO CartItems (CartID, ProductID, Quantity) VALUES (?, ?, ?)",
                   (random.randint(1, 50), random.randint(1, 100), random.randint(1, 10)))

# Insert fake records into Orders table
for _ in range(100):
    cursor.execute("INSERT INTO Orders (UserID, OrderDate) VALUES (?, ?)",
                   (random.randint(1, 50), fake.date_between(start_date='-1y', end_date='today')))

# Insert fake records into OrderDetails table
for _ in range(200):
    cursor.execute("INSERT INTO OrderDetails (OrderID, ProductID, Quantity) VALUES (?, ?, ?)",
                   (random.randint(1, 100), random.randint(1, 100), random.randint(1, 10)))

# Insert fake records into ShippingInfo table
for _ in range(100):
    order_date = fake.date_between(start_date='-1y', end_date='today')
    cursor.execute("INSERT INTO ShippingInfo (OrderID, Carrier, TrackingNumber, ShippingDate, DeliveryDate) VALUES (?, ?, ?, ?, ?)",
                   (random.randint(1, 100), fake.company(), fake.uuid4(), order_date, fake.date_between(start_date=order_date, end_date='+30d')))

# Insert fake records into Products table
for _ in range(100):
    cursor.execute("INSERT INTO Products (ProductName, BrandID, Price, StockQuantity, Description) VALUES (?, ?, ?, ?, ?)",
                   (fake.word(), random.randint(1, 10), round(random.uniform(10.0, 1000.0), 2), random.randint(0, 1000), fake.text()))

# Insert fake records into Categories table
for _ in range(20):
    cursor.execute("INSERT INTO Categories (CategoryName) VALUES (?)", (fake.word(),))

# Insert fake records into ProductCategories table with duplicate check
existing_combinations = set()
for _ in range(200):
    product_id = random.randint(1, 100)
    category_id = random.randint(1, 20)
    if (product_id, category_id) not in existing_combinations:
        cursor.execute("INSERT INTO ProductCategories (ProductID, CategoryID) VALUES (?, ?)",
                       (product_id, category_id))
        existing_combinations.add((product_id, category_id))

# Insert fake records into Brands table
for _ in range(10):
    cursor.execute("INSERT INTO Brands (BrandName) VALUES (?)", (fake.company(),))

# Insert fake records into Reviews table
for _ in range(200):
    cursor.execute("INSERT INTO Reviews (UserID, ProductID, Rating, Comment, ReviewDate) VALUES (?, ?, ?, ?, ?)",
                   (random.randint(1, 50), random.randint(1, 100), random.randint(1, 5), fake.text(), fake.date_between(start_date='-1y', end_date='today')))

# Insert fake records into Discounts table
for _ in range(50):
    start_date = fake.date_between(start_date='-1y', end_date='today')
    cursor.execute("INSERT INTO Discounts (ProductID, DiscountPercentage, StartDate, EndDate) VALUES (?, ?, ?, ?)",
                   (random.randint(1, 100), round(random.uniform(5.0, 50.0), 2), start_date, fake.date_between(start_date=start_date, end_date='+30d')))

# Commit the changes and close the connection
conn.commit()
conn.close()