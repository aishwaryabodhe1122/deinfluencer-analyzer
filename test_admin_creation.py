#!/usr/bin/env python3
"""
Test script to create admin user for testing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.database import get_db, User
from backend.auth import get_password_hash
from sqlalchemy.orm import Session

def create_test_admin():
    """Create a test admin user"""
    db = next(get_db())
    
    # Check if admin already exists
    existing_admin = db.query(User).filter(User.email == "admin@nexora.com").first()
    if existing_admin:
        print("✅ Admin user already exists!")
        print(f"Email: admin@nexora.com")
        print(f"Username: {existing_admin.username}")
        print(f"Role: {existing_admin.role}")
        return
    
    # Create admin user
    admin_user = User(
        email="admin@nexora.com",
        username="admin",
        full_name="System Administrator",
        hashed_password=get_password_hash("admin123"),
        role="admin",
        is_active=True,
        is_verified=True
    )
    
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    
    print("✅ Test admin user created successfully!")
    print(f"Email: admin@nexora.com")
    print(f"Password: admin123")
    print(f"Username: admin")
    print(f"Role: admin")

if __name__ == "__main__":
    create_test_admin()
