# User manager
#********************************************#
import sqlite3
from hashlib import sha256

conn = sqlite3.connect('store_1.db')
cursor = conn.cursor()

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def register_user(username, password, email, phone_number, street, city, state, postal_code, country):
    try:
        cursor.execute("""
            INSERT INTO Users (Username, Password, Email, PhoneNumber) 
            VALUES (?, ?, ?, ?)
        """, (username, hash_password(password), email, phone_number))
        
        user_id = cursor.lastrowid
        
        cursor.execute("""
            INSERT INTO Addresses (UserID, Street, City, State, PostalCode, Country) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, street, city, state, postal_code, country))
        
        conn.commit()
        print("User registered successfully")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def login_user(username, password):
    cursor.execute("""
        SELECT UserID FROM Users 
        WHERE Username = ? AND Password = ?
    """, (username, hash_password(password)))
    
    user = cursor.fetchone()
    
    if user:
        print("Login successful")
        return user[0]
    else:
        print("Invalid username or password")
        return None

def update_user_profile(user_id, name=None, email=None, phone_number=None, street=None, city=None, state=None, postal_code=None, country=None):
    try:
        if name:
            cursor.execute("""
                UPDATE Users SET Username = ? WHERE UserID = ?
            """, (name, user_id))
        
        if email:
            cursor.execute("""
                UPDATE Users SET Email = ? WHERE UserID = ?
            """, (email, user_id))
        
        if phone_number:
            cursor.execute("""
                UPDATE Users SET PhoneNumber = ? WHERE UserID = ?
            """, (phone_number, user_id))
        
        if street or city or state or postal_code or country:
            cursor.execute("""
                UPDATE Addresses SET Street = ?, City = ?, State = ?, PostalCode = ?, Country = ? 
                WHERE UserID = ?
            """, (street, city, state, postal_code, country, user_id))
        
        conn.commit()
        print("User profile updated successfully")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

register_user(
    username="john_doe",
    password="securepassword",
    email="john@example.com",
    phone_number="1234567890",
    street="123 Elm Street",
    city="Springfield",
    state="IL",
    postal_code="62701",
    country="USA"
)

user_id = login_user("john_doe", "securepassword")

if user_id:
    update_user_profile(
        user_id,
        name="john_updated",
        email="john_updated@example.com",
        phone_number="0987654321",
        street="456 Oak Street",
        city="Springfield",
        state="IL",
        postal_code="62701",
        country="USA"
    )

conn.close()

