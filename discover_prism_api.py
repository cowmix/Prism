#!/usr/bin/env python3
"""
Discover Prism's API endpoints and authentication methods
"""

import requests
import json

SERVER_URL = "https://service.prism-pipeline.com"

def test_endpoint(path, method="GET", data=None):
    """Test an API endpoint"""
    url = SERVER_URL + path
    try:
        if method == "GET":
            response = requests.get(url, params=data, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        
        print(f"{method} {path} - Status: {response.status_code}")
        if response.status_code != 404:
            content = response.text[:200]
            if len(response.text) > 200:
                content += "..."
            print(f"  Response: {content}")
        return response
    except Exception as e:
        print(f"{method} {path} - Error: {e}")
        return None

def main():
    print("Discovering Prism API Structure")
    print("=" * 50)
    
    # Test common API paths
    endpoints_to_test = [
        "/api",
        "/api/v1",
        "/api/v2", 
        "/api/auth",
        "/api/auth/login",
        "/api/user/login",
        "/api/service",
        "/api/service/auth",
        "/api/service/user",
        "/login",
        "/auth/login",
        "/user/login",
    ]
    
    print("\n1. Testing common endpoints:")
    for endpoint in endpoints_to_test:
        test_endpoint(endpoint)
    
    print("\n2. Testing with credentials in different ways:")
    
    # Test basic auth (DEMO - don't use real password)
    print("Basic Auth test - SKIPPED (would need real credentials)")
    
    # Test with credentials in data (DEMO - don't use real password) 
    print("Credentials in params test - SKIPPED (would need real credentials)")
    print("NOTE: You can test these manually by editing this script with your real password")

    print("\n3. Check if there's a web login portal:")
    try:
        response = requests.get(SERVER_URL, timeout=10)
        print(f"Main site - Status: {response.status_code}")
        if "login" in response.text.lower():
            print("  ✓ Login form found on main page")
        if "hub" in response.text.lower():
            print("  ✓ Hub mentioned on main page")
        if "download" in response.text.lower():
            print("  ✓ Download links might be available")
    except Exception as e:
        print(f"Main site - Error: {e}")

    print("\n" + "=" * 50)
    print("RECOMMENDATIONS:")
    print("1. Check https://service.prism-pipeline.com in a browser")
    print("2. Look for a customer/user login portal")
    print("3. Contact Prism support with your exact error messages")
    print("4. Ask them for the correct authentication method for Linux")
    print("5. Request manual download links for Hub plugin")

if __name__ == "__main__":
    main()