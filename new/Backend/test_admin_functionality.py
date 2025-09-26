#!/usr/bin/env python3
"""
Comprehensive test script for the Bank Loan Portal with admin functionality
Tests email notifications, admin routes, and application filtering
"""

import requests
import json
from datetime import datetime
import time

BASE_URL = 'http://localhost:5001/api'

def test_admin_functionality():
    print('🏛️  Testing Bank Loan Portal - Admin Functionality')
    print('=' * 60)
    
    # Test data
    admin_data = {
        'fullName': 'Test Admin',
        'email': 'admin@test.com',
        'phone': '1111111111',
        'aadhaar': '111111111111',
        'password': 'admin123',
        'role': 'admin'
    }
    
    user_data = {
        'fullName': 'Test User',
        'email': 'user@test.com',
        'phone': '2222222222',
        'aadhaar': '222222222222',
        'password': 'user123'
    }
    
    try:
        # 1. Register admin
        print('1. Registering admin user...')
        response = requests.post(f'{BASE_URL}/auth/register', json=admin_data)
        print(f'   Status: {response.status_code}')
        if response.status_code == 400:
            print('   Admin already exists, proceeding...')
        
        # 2. Register regular user
        print('2. Registering regular user...')
        response = requests.post(f'{BASE_URL}/auth/register', json=user_data)
        print(f'   Status: {response.status_code}')
        if response.status_code == 400:
            print('   User already exists, proceeding...')
        
        # 3. Login as admin
        print('3. Logging in as admin...')
        admin_login = {'email': admin_data['email'], 'password': admin_data['password']}
        response = requests.post(f'{BASE_URL}/auth/login', json=admin_login)
        print(f'   Status: {response.status_code}')
        
        if response.status_code != 200:
            print('❌ Admin login failed')
            return
        
        admin_token = response.json()['token']
        admin_headers = {'Authorization': f'Bearer {admin_token}', 'Content-Type': 'application/json'}
        print('   ✅ Admin logged in successfully')
        
        # 4. Login as user
        print('4. Logging in as user...')
        user_login = {'email': user_data['email'], 'password': user_data['password']}
        response = requests.post(f'{BASE_URL}/auth/login', json=user_login)
        print(f'   Status: {response.status_code}')
        
        if response.status_code != 200:
            print('❌ User login failed')
            return
        
        user_token = response.json()['token']
        user_headers = {'Authorization': f'Bearer {user_token}', 'Content-Type': 'application/json'}
        print('   ✅ User logged in successfully')
        
        # 5. Submit loan application as user
        print('5. Submitting loan application as user...')
        loan_data = {
            'personal': {'name': 'Test User', 'age': 30, 'gender': 'male', 'location': 'Mumbai', 'contact': '2222222222'},
            'employment': {'status': 'employed', 'income': 60000, 'creditScore': 750},
            'loan': {'type': 'home', 'amount': 2000000, 'tenure': '15 years'},
            'metadata': {'submittedAt': datetime.now().isoformat() + 'Z', 'applicationId': 'LOAN-ADMIN-TEST', 'source': 'admin-test'}
        }
        
        response = requests.post(f'{BASE_URL}/loan-applications', json=loan_data, headers=user_headers)
        print(f'   Status: {response.status_code}')
        
        if response.status_code != 201:
            print('❌ Loan application submission failed')
            return
        
        application_id = response.json()['application']['id']
        print(f'   ✅ Loan application submitted (ID: {application_id})')
        
        # 6. Test admin dashboard stats
        print('6. Testing admin dashboard stats...')
        response = requests.get(f'{BASE_URL}/admin/dashboard-stats', headers=admin_headers)
        print(f'   Status: {response.status_code}')
        
        if response.status_code == 200:
            stats = response.json()
            print(f'   ✅ Total applications: {stats["total_applications"]}')
            print(f'   ✅ Pending applications: {stats["pending_applications"]}')
        else:
            print('❌ Failed to get dashboard stats')
        
        # 7. Test admin view all applications
        print('7. Testing admin view all applications...')
        response = requests.get(f'{BASE_URL}/admin/applications', headers=admin_headers)
        print(f'   Status: {response.status_code}')
        
        if response.status_code == 200:
            apps = response.json()['applications']
            print(f'   ✅ Admin can view {len(apps)} applications')
        else:
            print('❌ Failed to get all applications')
        
        # 8. Test admin request documents
        print('8. Testing admin document request...')
        doc_request = {
            'documents_required': 'Please upload:\n- Salary slips (last 3 months)\n- Bank statements (last 6 months)\n- Identity proof',
            'admin_notes': 'Additional documents required for loan verification'
        }
        
        response = requests.post(f'{BASE_URL}/admin/applications/{application_id}/request-documents', 
                               json=doc_request, headers=admin_headers)
        print(f'   Status: {response.status_code}')
        
        if response.status_code == 200:
            print('   ✅ Document request sent successfully')
        else:
            print('❌ Failed to send document request')
        
        # 9. Test admin approve application
        print('9. Testing admin approve application...')
        approval_data = {
            'status': 'approved',
            'admin_notes': 'Application approved after reviewing all documents and credit score.'
        }
        
        response = requests.post(f'{BASE_URL}/admin/applications/{application_id}/approve', 
                               json=approval_data, headers=admin_headers)
        print(f'   Status: {response.status_code}')
        
        if response.status_code == 200:
            print('   ✅ Application approved successfully')
        else:
            print('❌ Failed to approve application')
        
        # 10. Test filtering (get approved applications)
        print('10. Testing application filtering...')
        response = requests.get(f'{BASE_URL}/admin/applications?status=approved', headers=admin_headers)
        print(f'    Status: {response.status_code}')
        
        if response.status_code == 200:
            apps = response.json()['applications']
            print(f'    ✅ Found {len(apps)} approved applications')
        else:
            print('❌ Failed to filter applications')
        
        # 11. Test user access (should only see own applications)
        print('11. Testing user access restrictions...')
        response = requests.get(f'{BASE_URL}/loan-applications', headers=user_headers)
        print(f'    Status: {response.status_code}')
        
        if response.status_code == 200:
            apps = response.json()['applications']
            print(f'    ✅ User can see {len(apps)} own applications')
        else:
            print('❌ Failed to get user applications')
        
        # 12. Test user cannot access admin routes
        print('12. Testing user cannot access admin routes...')
        response = requests.get(f'{BASE_URL}/admin/applications', headers=user_headers)
        print(f'    Status: {response.status_code}')
        
        if response.status_code == 403:
            print('    ✅ User correctly denied admin access')
        else:
            print('❌ User should not have admin access')
        
        print('\n🎉 All tests completed!')
        
    except Exception as e:
        print(f'❌ Test error: {e}')

if __name__ == "__main__":
    test_admin_functionality()
