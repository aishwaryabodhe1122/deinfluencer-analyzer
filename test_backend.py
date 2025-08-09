#!/usr/bin/env python3
"""
Simple test script to check backend API response
"""
import requests
import json

def test_backend_api():
    """Test the backend API endpoint"""
    url = "http://localhost:8000/api/analyze"
    
    # Test data
    test_data = {
        "username": "justinbieber",
        "platform": "twitter",
        "deep_analysis": True
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("Testing backend API...")
        print(f"URL: {url}")
        print(f"Data: {json.dumps(test_data, indent=2)}")
        print("-" * 50)
        
        response = requests.post(url, json=test_data, headers=headers, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Raw Response: {response.text[:500]}...")
        
        if response.status_code == 200:
            try:
                json_data = response.json()
                print("✅ JSON parsing successful!")
                print(f"Profile username: {json_data.get('profile', {}).get('username', 'N/A')}")
                print(f"Follower count: {json_data.get('profile', {}).get('follower_count', 'N/A')}")
                print(f"Overall score: {json_data.get('authenticity_score', {}).get('overall_score', 'N/A')}")
            except json.JSONDecodeError as e:
                print(f"❌ JSON parsing failed: {e}")
                print(f"Response content: {response.text}")
        else:
            print(f"❌ API request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - Backend server may not be running")
    except requests.exceptions.Timeout:
        print("❌ Request timed out - Backend may be hanging")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_backend_api()
