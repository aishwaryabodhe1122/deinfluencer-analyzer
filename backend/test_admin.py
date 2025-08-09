#!/usr/bin/env python3
"""
Simple admin user creation for testing
"""

from sqlalchemy.orm import Session
from database import SessionLocal, User
from auth import get_password_hash

def create_test_admin():
    """Create a test admin user for testing purposes"""
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.email == "admin@nexora.com").first()
        if existing_admin:
            print("✅ Admin user already exists!")
            print(f"   Email: admin@nexora.com")
            print(f"   Username: {existing_admin.username}")
            print(f"   Role: {existing_admin.role}")
            print(f"   Status: {'Active' if existing_admin.is_active else 'Inactive'}")
            return True
        
        # Create new admin user
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
        
        print("🎉 Test admin user created successfully!")
        print(f"   Email: admin@nexora.com")
        print(f"   Password: admin123")
        print(f"   Username: admin")
        print(f"   Role: admin")
        print("")
        print("🔧 You can now test the admin panel features!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
        return False
        
    finally:
        db.close()

if __name__ == "__main__":
    print("🔧 Creating test admin user...")
    print("-" * 40)
    create_test_admin()
