import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('ecommerce.db')
cursor = conn.cursor()

# Define the queries
queries = [
    # Simple Queries
    {
        "description": "Retrieve all products with their prices and stock quantities",
        "query": "SELECT ProductName, Price, StockQuantity FROM Products;"
    },
    {
        "description": "List all categories",
        "query": "SELECT CategoryName FROM Categories;"
    },
    # Medium Queries
    {
        "description": "Fetch user details who placed an order on a specific date",
        "query": "SELECT Users.Username, Users.Email, Orders.OrderDate FROM Users JOIN Orders ON Users.UserID = Orders.UserID WHERE Orders.OrderDate = '2024-07-07';"
    },
    {
        "description": "Get the list of products with discounts currently active",
        "query": "SELECT Products.ProductName, Discounts.DiscountPercentage, Discounts.StartDate, Discounts.EndDate FROM Products JOIN Discounts ON Products.ProductID = Discounts.ProductID WHERE DATE('now') BETWEEN Discounts.StartDate AND Discounts.EndDate;"
    },
    {
        "description": "Retrieve all reviews for a specific product",
        "query": "SELECT Users.Username, Reviews.Rating, Reviews.Comment, Reviews.ReviewDate FROM Reviews JOIN Users ON Reviews.UserID = Users.UserID WHERE Reviews.ProductID = 1;"
    },
    {
        "description": "List all users with their corresponding addresses",
        "query": "SELECT Users.Username, Users.Email, Addresses.Street, Addresses.City, Addresses.State, Addresses.PostalCode, Addresses.Country FROM Users JOIN Addresses ON Users.UserID = Addresses.UserID;"
    },
    # Complex Queries
    {
        "description": "Retrieve the total amount spent by each user on all their orders",
        "query": "SELECT Users.Username, SUM(OrderDetails.Quantity * Products.Price) AS TotalSpent FROM Users JOIN Orders ON Users.UserID = Orders.UserID JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID JOIN Products ON OrderDetails.ProductID = Products.ProductID GROUP BY Users.Username;"
    },
    {
        "description": "Get the order history with detailed product information for a specific user",
        "query": "SELECT Orders.OrderID, Orders.OrderDate, Products.ProductName, OrderDetails.Quantity, (OrderDetails.Quantity * Products.Price) AS TotalPrice FROM Orders JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID JOIN Products ON OrderDetails.ProductID = Products.ProductID WHERE Orders.UserID = 1 ORDER BY Orders.OrderDate DESC;"
    },
    {
        "description": "List products along with the total number of times they have been ordered",
        "query": "SELECT Products.ProductName, SUM(OrderDetails.Quantity) AS TotalOrdered FROM Products JOIN OrderDetails ON Products.ProductID = OrderDetails.ProductID GROUP BY Products.ProductName ORDER BY TotalOrdered DESC;"
    },
    {
        "description": "Retrieve all users who have not placed any orders",
        "query": "SELECT Users.Username, Users.Email FROM Users LEFT JOIN Orders ON Users.UserID = Orders.UserID WHERE Orders.UserID IS NULL;"
    }
]

# Write the queries to a .sql file
with open('queries.sql', 'w') as file:
    for q in queries:
        file.write(f"-- {q['description']}\n")
        file.write(f"{q['query']}\n\n")

# Execute the queries and print the results
for q in queries:
    print(f"Executing: {q['description']}")
    cursor.execute(q['query'])
    results = cursor.fetchall()
    for row in results:
        print(row)
    print("\n")

# Commit and close the database connection
conn.commit()
conn.close()