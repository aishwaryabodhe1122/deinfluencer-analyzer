#!/usr/bin/env python3
"""
Script to create an admin user using credentials from .env file
Run this script to create the admin user: python create_admin.py
"""

import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from database import SessionLocal, User
from auth import get_password_hash

def create_admin_user():
    """Create admin user from .env credentials"""
    
    # Load environment variables
    load_dotenv()
    
    # Get admin credentials from .env
    admin_email = os.getenv('ADMIN_EMAIL')
    admin_password = os.getenv('ADMIN_PASSWORD')
    admin_name = os.getenv('ADMIN_NAME')
    admin_username = os.getenv('ADMIN_USERNAME')
    
    if not all([admin_email, admin_password, admin_name, admin_username]):
        print("❌ Error: Missing admin credentials in .env file")
        print("Required variables: ADMIN_EMAIL, ADMIN_PASSWORD, ADMIN_NAME, ADMIN_USERNAME")
        return False
    
    # Create database session
    db: Session = SessionLocal()
    
    try:
        # Check if admin user already exists
        existing_user = db.query(User).filter(
            (User.email == admin_email) | (User.username == admin_username)
        ).first()
        
        if existing_user:
            print(f"⚠️  Admin user already exists:")
            print(f"   Email: {existing_user.email}")
            print(f"   Username: {existing_user.username}")
            print(f"   Role: {existing_user.role}")
            
            # Update existing user to admin role if needed
            if existing_user.role != 'admin':
                existing_user.role = 'admin'
                db.commit()
                print("✅ Updated existing user to admin role")
            else:
                print("✅ User already has admin role")
            return True
        
        # Create new admin user
        hashed_password = get_password_hash(admin_password)
        
        admin_user = User(
            email=admin_email,
            username=admin_username,
            full_name=admin_name,
            hashed_password=hashed_password,
            role='admin',
            is_active=True,
            avatar_url=None,
            notification_preferences='{"analysis_updates": true, "system_alerts": true}'
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("✅ Admin user created successfully!")
        print(f"   Email: {admin_user.email}")
        print(f"   Username: {admin_user.username}")
        print(f"   Full Name: {admin_user.full_name}")
        print(f"   Role: {admin_user.role}")
        print(f"   User ID: {admin_user.id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating admin user: {str(e)}")
        db.rollback()
        return False
        
    finally:
        db.close()

if __name__ == "__main__":
    print("🔧 Creating admin user from .env credentials...")
    print("-" * 50)
    
    success = create_admin_user()
    
    print("-" * 50)
    if success:
        print("🎉 Admin user setup complete!")
        print("\nYou can now login with:")
        print(f"   Email: {os.getenv('ADMIN_EMAIL')}")
        print(f"   Password: {os.getenv('ADMIN_PASSWORD')}")
    else:
        print("❌ Admin user setup failed!")
