#!/usr/bin/env python3
"""
Script to create an admin user for the Bank Loan Portal
Run this script to create the first admin user
"""

from app import app
from models import db, User

def create_admin():
    with app.app_context():
        # Check if admin already exists
        admin_exists = User.query.filter_by(role='admin').first()
        
        if admin_exists:
            print("Admin user already exists!")
            print(f"Admin: {admin_exists.full_name} ({admin_exists.email})")
            return
        
        # Create admin user
        admin = User(
            full_name="System Administrator",
            email="admin@bankloanportal.com",
            phone="9999999999",
            aadhaar="999999999999",
            role="admin"
        )
        admin.set_password("admin123")  # Change this password!
        
        try:
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created successfully!")
            print(f"Email: {admin.email}")
            print(f"Password: admin123")
            print("⚠️  Please change the default password after first login!")
        except Exception as e:
            print(f"❌ Failed to create admin user: {e}")
            db.session.rollback()

if __name__ == "__main__":
    create_admin()
