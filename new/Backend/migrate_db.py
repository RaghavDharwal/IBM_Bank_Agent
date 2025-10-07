#!/usr/bin/env python3
"""
Database migration script to add missing columns to existing database
Run this when you've added new columns to the models but have an existing database
"""

import sqlite3
from app import app
from models import db

def migrate_database():
    """Add missing columns to existing database"""
    with app.app_context():
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        
        # Handle relative paths
        if not db_path.startswith('/'):
            db_path = f"instance/{db_path}"
        
        print(f"Migrating database: {db_path}")
        
        # Connect directly to SQLite
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        try:
            # Check if role column exists in users table
            cursor.execute("PRAGMA table_info(users)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'role' not in columns:
                print("Adding 'role' column to users table...")
                cursor.execute("ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user'")
                print("✅ Added 'role' column")
            else:
                print("'role' column already exists")
            
            # Check if new columns exist in loan_applications table
            cursor.execute("PRAGMA table_info(loan_applications)")
            columns = [column[1] for column in cursor.fetchall()]
            
            new_columns = [
                ('admin_notes', 'TEXT'),
                ('documents_required', 'TEXT'),
                ('documents_uploaded', 'BOOLEAN DEFAULT 0'),
                ('reviewed_by', 'INTEGER'),
                ('reviewed_at', 'DATETIME')
            ]
            
            for col_name, col_type in new_columns:
                if col_name not in columns:
                    print(f"Adding '{col_name}' column to loan_applications table...")
                    cursor.execute(f"ALTER TABLE loan_applications ADD COLUMN {col_name} {col_type}")
                    print(f"✅ Added '{col_name}' column")
                else:
                    print(f"'{col_name}' column already exists")
            
            # Commit the changes
            conn.commit()
            print("✅ Database migration completed successfully!")
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            conn.rollback()
        finally:
            conn.close()

if __name__ == "__main__":
    migrate_database()
