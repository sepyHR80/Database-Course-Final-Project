# Managers manager
#********************************************#
import sqlite3
from hashlib import sha256

conn = sqlite3.connect('store_1.db')
cursor = conn.cursor()

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def register_admin(username, password, email):
    try:
        cursor.execute("""
            INSERT INTO Admins (Username, Password, Email) 
            VALUES (?, ?, ?)
        """, (username, hash_password(password), email))
        
        conn.commit()
        print("Admin registered successfully")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def login_admin(username, password):
    cursor.execute("""
        SELECT AdminID FROM Admins 
        WHERE Username = ? AND Password = ?
    """, (username, hash_password(password)))
    
    admin = cursor.fetchone()
    
    if admin:
        print("Login successful")
        return admin[0]
    else:
        print("Invalid username or password")
        return None

def update_admin_profile(admin_id, username=None, email=None):
    try:
        if username:
            cursor.execute("""
                UPDATE Admins SET Username = ? WHERE AdminID = ?
            """, (username, admin_id))
        
        if email:
            cursor.execute("""
                UPDATE Admins SET Email = ? WHERE AdminID = ?
            """, (email, admin_id))
        
        conn.commit()
        print("Admin profile updated successfully")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

register_admin(
    username="admin_john",
    password="secureadminpassword",
    email="admin_john@example.com"
)

admin_id = login_admin("admin_john", "secureadminpassword")
if admin_id:
    update_admin_profile(
        admin_id,
        username="admin_john_updated",
        email="admin_john_updated@example.com"
    )

conn.close()
