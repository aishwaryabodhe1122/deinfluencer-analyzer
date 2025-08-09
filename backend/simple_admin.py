#!/usr/bin/env python3
"""
Simple admin user creation script without complex imports
"""

import os
import sqlite3
from dotenv import load_dotenv
from passlib.context import CryptContext

# Load environment variables
load_dotenv()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin_simple():
    """Create admin user directly in SQLite database"""
    
    # Get admin credentials from .env
    admin_email = os.getenv('ADMIN_EMAIL', 'aishwaryabodhe1122@gmail.com')
    admin_password = os.getenv('ADMIN_PASSWORD', 'Aishu@11')
    admin_name = os.getenv('ADMIN_NAME', 'Admin User')
    admin_username = os.getenv('ADMIN_USERNAME', 'admin')
    
    print(f"🔧 Creating admin user with simple approach...")
    print(f"📧 Email: {admin_email}")
    print(f"🔑 Password: {admin_password}")
    print(f"👤 Name: {admin_name}")
    print(f"🏷️ Username: {admin_username}")
    print("-" * 50)
    
    # Hash the password
    hashed_password = pwd_context.hash(admin_password)
    print(f"🔐 Password hashed successfully")
    
    # Connect to SQLite database
    db_path = "nexora.db"  # Adjust if your database file has a different name
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if admin user already exists
        cursor.execute("SELECT id, email FROM users WHERE email = ?", (admin_email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            print(f"👤 Updating existing admin user (ID: {existing_user[0]})")
            # Update existing user
            cursor.execute("""
                UPDATE users 
                SET hashed_password = ?, full_name = ?, username = ?, role = ?, is_active = 1, is_verified = 1
                WHERE email = ?
            """, (hashed_password, admin_name, admin_username, "admin", admin_email))
        else:
            print(f"👤 Creating new admin user")
            # Create new user
            cursor.execute("""
                INSERT INTO users (email, username, hashed_password, full_name, role, is_active, is_verified, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, 1, 1, datetime('now'), datetime('now'))
            """, (admin_email, admin_username, hashed_password, admin_name, "admin"))
        
        # Commit changes
        conn.commit()
        
        # Verify the user was created/updated
        cursor.execute("SELECT id, email, username, role FROM users WHERE email = ?", (admin_email,))
        user = cursor.fetchone()
        
        if user:
            print("✅ Admin user created/updated successfully!")
            print(f"   ID: {user[0]}")
            print(f"   Email: {user[1]}")
            print(f"   Username: {user[2]}")
            print(f"   Role: {user[3]}")
            print("-" * 50)
            print("🎉 You can now login with:")
            print(f"   Email: {admin_email}")
            print(f"   Password: {admin_password}")
            return True
        else:
            print("❌ Failed to create/update admin user")
            return False
            
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("🔧 Simple Admin User Creation Tool")
    print("=" * 50)
    create_admin_simple()
