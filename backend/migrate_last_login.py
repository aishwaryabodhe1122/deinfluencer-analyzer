#!/usr/bin/env python3
"""
Database migration script to add last_login column to users table
Run this script to update the database schema: python migrate_last_login.py
"""

import sqlite3
import os
from datetime import datetime

def migrate_database():
    """Add last_login column to users table"""
    
    db_path = "deinfluencer.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Database file {db_path} not found!")
        return False
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if last_login column already exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'last_login' in columns:
            print("✅ last_login column already exists in users table")
            return True
        
        # Add last_login column
        print("🔧 Adding last_login column to users table...")
        cursor.execute("ALTER TABLE users ADD COLUMN last_login DATETIME")
        
        # Commit changes
        conn.commit()
        
        # Verify the column was added
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'last_login' in columns:
            print("✅ Successfully added last_login column to users table")
            
            # Show current table structure
            print("\n📋 Updated users table structure:")
            cursor.execute("PRAGMA table_info(users)")
            for column in cursor.fetchall():
                print(f"   - {column[1]} ({column[2]})")
            
            return True
        else:
            print("❌ Failed to add last_login column")
            return False
            
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
        
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("🔧 Database Migration: Adding last_login column")
    print("-" * 50)
    
    success = migrate_database()
    
    print("-" * 50)
    if success:
        print("🎉 Database migration completed successfully!")
        print("\nThe users table now includes the last_login field.")
        print("You can now restart the backend server to use the updated schema.")
    else:
        print("❌ Database migration failed!")
        print("Please check the error messages above and try again.")
