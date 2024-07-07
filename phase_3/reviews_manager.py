import sqlite3

conn = sqlite3.connect('store_1.db')
cursor = conn.cursor()

def add_review(user_id, product_id, rating, comment, review_date):
    try:
        cursor.execute("""
            INSERT INTO Reviews (UserID, ProductID, Rating, Comment, ReviewDate) 
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, product_id, rating, comment, review_date))
        
        conn.commit()
        print("Review added successfully")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def view_reviews(product_id):
    try:
        cursor.execute("""
            SELECT Users.Username, Reviews.Rating, Reviews.Comment, Reviews.ReviewDate
            FROM Reviews
            JOIN Users ON Reviews.UserID = Users.UserID
            WHERE Reviews.ProductID = ?
        """, (product_id,))
        
        reviews = cursor.fetchall()
        
        if reviews:
            print(f"Reviews for product {product_id}:")
            for review in reviews:
                print(review)
        else:
            print("No reviews found for this product")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def delete_review(review_id):
    try:
        cursor.execute("""
            DELETE FROM Reviews 
            WHERE ReviewID = ?
        """, (review_id,))
        
        conn.commit()
        print("Review deleted successfully")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

# Create Reviews table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Reviews (
        ReviewID INTEGER PRIMARY KEY,
        UserID INTEGER,
        ProductID INTEGER,
        Rating INTEGER,
        Comment TEXT,
        ReviewDate DATE,
        FOREIGN KEY (UserID) REFERENCES Users(UserID),
        FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
    )
""")

# Add a sample review
add_review(
    user_id=1, 
    product_id=1, 
    rating=5, 
    comment="Great product!", 
    review_date="2024-07-07"
)

# View reviews for a product
view_reviews(product_id=1)

# Delete a review
delete_review(review_id=1)

conn.close()