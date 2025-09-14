#!/usr/bin/env python3
"""
Manual Hub download with authentication for Prism
"""

import requests
import json
import os
import platform
import getpass

# Prism server details
SERVER_URL = "https://service.prism-pipeline.com"
HUB_URL = SERVER_URL + "/api/service/links/plugins/hub"
INTERNALS_URL = SERVER_URL + "/api/service/links/plugins/prisminternals"

def get_credentials():
    """Get login credentials from user"""
    print("Prism Login Credentials Required")
    print("-" * 40)
    username = input("Username/Email: ")
    password = getpass.getpass("Password: ")
    return username, password

def authenticate(username, password):
    """Try to authenticate with Prism service"""
    auth_url = SERVER_URL + "/api/service/auth/login"
    
    auth_data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(auth_url, json=auth_data)
        if response.status_code == 200:
            result = response.json()
            if "token" in result:
                print("✓ Authentication successful!")
                return result["token"]
            else:
                print("✗ No token in response:", result)
                return None
        else:
            print(f"✗ Authentication failed. Status: {response.status_code}")
            try:
                error_info = response.json()
                print(f"Error details: {error_info}")
            except:
                print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"✗ Authentication error: {e}")
        return None

def download_with_auth(url, plugin_name, auth_token=None):
    """Download plugin with optional authentication"""
    data = {
        "key": plugin_name,
        "origin": "prismOss", 
        "prism_version": "v2.0.17",
        "opsystem": platform.system(),
    }
    
    headers = {}
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"
        # or try different auth header formats:
        # headers["X-Auth-Token"] = auth_token
        # headers["token"] = auth_token
    
    try:
        print(f"Requesting {plugin_name} download...")
        response = requests.get(url, params=data, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}...")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Response received for {plugin_name}")
            return result
        else:
            print(f"✗ Download failed for {plugin_name}")
            return None
            
    except Exception as e:
        print(f"✗ Error downloading {plugin_name}: {e}")
        return None

def main():
    print("Prism Hub Manual Download Tool")
    print("=" * 50)
    
    # Try without authentication first
    print("\n1. Trying without authentication...")
    hub_result = download_with_auth(HUB_URL, "Hub")
    internals_result = download_with_auth(INTERNALS_URL, "PrismInternals")
    
    if (hub_result and "error" not in hub_result) and (internals_result and "error" not in internals_result):
        print("✓ Downloads work without authentication!")
        return
    
    # Try with authentication
    print("\n2. Downloads require authentication. Please login:")
    username, password = get_credentials()
    
    print("\n3. Authenticating...")
    token = authenticate(username, password)
    
    if not token:
        print("\nAuthentication failed. Possible solutions:")
        print("1. Check your username/password")
        print("2. Contact Prism support for correct login procedure")
        print("3. Check if there's a web portal where you can download plugins manually")
        return
    
    print("\n4. Downloading with authentication...")
    hub_result = download_with_auth(HUB_URL, "Hub", token)
    internals_result = download_with_auth(INTERNALS_URL, "PrismInternals", token)
    
    if hub_result and "files" in hub_result:
        print("✓ Hub download links obtained!")
        print("Files available:", [f["url"] for f in hub_result["files"]])
    
    if internals_result and "files" in internals_result:
        print("✓ PrismInternals download links obtained!")
        print("Files available:", [f["url"] for f in internals_result["files"]])

if __name__ == "__main__":
    main()