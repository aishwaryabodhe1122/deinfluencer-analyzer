#!/usr/bin/env python3
"""
Debug script to check admin authentication
"""

import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from database import SessionLocal, User
from auth import verify_password, get_password_hash, authenticate_user

def debug_admin_auth():
    """Debug admin authentication"""
    
    # Load environment variables
    load_dotenv()
    
    # Get admin credentials from .env
    admin_email = os.getenv('ADMIN_EMAIL', 'aishwaryabodhe1122@gmail.com')
    admin_password = os.getenv('ADMIN_PASSWORD', 'your-secure-admin-password')
    
    print(f"🔍 Debugging admin authentication...")
    print(f"📧 Admin Email: {admin_email}")
    print(f"🔑 Admin Password from .env: {admin_password}")
    print("-" * 50)
    
    # Create database session
    db: Session = SessionLocal()
    
    try:
        # Check if admin user exists
        user = db.query(User).filter(User.email == admin_email).first()
        
        if not user:
            print("❌ Admin user not found in database!")
            print("   Try running: python create_admin.py")
            return False
        
        print(f"✅ Admin user found:")
        print(f"   ID: {user.id}")
        print(f"   Email: {user.email}")
        print(f"   Username: {user.username}")
        print(f"   Role: {user.role}")
        print(f"   Is Active: {user.is_active}")
        print(f"   Hashed Password: {user.hashed_password[:20]}...")
        print("-" * 50)
        
        # Test password verification
        print("🔍 Testing password verification...")
        is_valid = verify_password(admin_password, user.hashed_password)
        print(f"   Password verification result: {is_valid}")
        
        if not is_valid:
            print("❌ Password verification failed!")
            print("   This means the password in .env doesn't match the hashed password in database")
            
            # Test with common passwords
            test_passwords = ['admin', 'password', 'admin123', 'your-secure-admin-password']
            print("\n🔍 Testing common passwords:")
            for test_pwd in test_passwords:
                if verify_password(test_pwd, user.hashed_password):
                    print(f"   ✅ Password '{test_pwd}' works!")
                    return True
                else:
                    print(f"   ❌ Password '{test_pwd}' failed")
        else:
            print("✅ Password verification successful!")
            
            # Test full authentication
            print("\n🔍 Testing full authentication...")
            auth_user = authenticate_user(db, admin_email, admin_password)
            if auth_user:
                print("✅ Full authentication successful!")
                return True
            else:
                print("❌ Full authentication failed!")
                return False
        
    except Exception as e:
        print(f"❌ Error during authentication debug: {str(e)}")
        return False
    finally:
        db.close()
    
    return False

if __name__ == "__main__":
    print("🔧 Admin Authentication Debug Tool")
    print("=" * 50)
    debug_admin_auth()
