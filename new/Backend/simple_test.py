#!/usr/bin/env python3
"""
Simple API test for Bank Loan Portal Backend
Run this while the Flask server is running on port 5001
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5001/api"

def test_endpoints():
    print("🏛️  Testing Bank Loan Portal API")
    print("=" * 50)
    
    # Test 1: Health Check
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health Check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health Check Failed: {e}")
        return
    
    # Test 2: Register User
    user_data = {
        "fullName": "Test User",
        "email": "test@example.com",
        "phone": "9876543210",
        "aadhaar": "123456789012",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        print(f"Registration: {response.status_code} - {response.json()}")
        if response.status_code != 201:
            print("Registration failed, trying to continue with login...")
    except Exception as e:
        print(f"Registration Failed: {e}")
    
    # Test 3: Login User
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"Login: {response.status_code} - {response.json()}")
        
        if response.status_code == 200:
            token = response.json().get('token')
            print(f"JWT Token: {token[:50]}...")
            
            # Test 4: Submit Loan Application
            loan_data = {
                "personal": {
                    "name": "Test User",
                    "age": 30,
                    "gender": "male",
                    "location": "Mumbai",
                    "contact": "9876543210"
                },
                "employment": {
                    "status": "salaried",
                    "income": 75000,
                    "creditScore": 750
                },
                "loan": {
                    "type": "home",
                    "amount": 2500000,
                    "tenure": "20 years"
                },
                "metadata": {
                    "submittedAt": datetime.now().isoformat() + "Z",
                    "applicationId": "LOAN-TEST-123",
                    "source": "test-script"
                }
            }
            
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            try:
                response = requests.post(f"{BASE_URL}/loan-applications", json=loan_data, headers=headers)
                print(f"Loan Submission: {response.status_code} - {response.json()}")
                
                if response.status_code == 201:
                    print("✅ Loan application submitted successfully!")
                else:
                    print("❌ Loan application submission failed!")
            except Exception as e:
                print(f"Loan Submission Failed: {e}")
            
            # Test 5: Get Loan Applications
            try:
                response = requests.get(f"{BASE_URL}/loan-applications", headers=headers)
                print(f"Get Applications: {response.status_code} - {response.json()}")
                
                if response.status_code == 200:
                    print("✅ Retrieved loan applications successfully!")
                else:
                    print("❌ Failed to retrieve loan applications!")
            except Exception as e:
                print(f"Get Applications Failed: {e}")
            
        else:
            print("❌ Login failed, cannot test authenticated endpoints")
            
    except Exception as e:
        print(f"Login Failed: {e}")

if __name__ == "__main__":
    test_endpoints()
