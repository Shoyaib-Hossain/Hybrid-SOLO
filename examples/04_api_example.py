#!/usr/bin/env python3
"""
Example 4: Making API Requests
===============================

This demonstrates:
- Making GET requests
- Making POST requests
- Handling JSON data
- Error handling
- Working with response data
"""

import requests
import json

def example_1_simple_get():
    """Simple GET request to a public API."""
    print("\n" + "="*60)
    print("Example 1: Simple GET Request")
    print("="*60)
    
    # Make GET request to GitHub API
    url = "https://api.github.com/users/github"
    
    print(f"Requesting: {url}")
    response = requests.get(url)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Username: {data['login']}")
        print(f"Name: {data.get('name', 'N/A')}")
        print(f"Bio: {data.get('bio', 'N/A')}")
        print(f"Public Repos: {data['public_repos']}")
        print(f"Followers: {data['followers']}")
    else:
        print(f"Error: {response.status_code}")

def example_2_get_with_parameters():
    """GET request with query parameters."""
    print("\n" + "="*60)
    print("Example 2: GET with Parameters")
    print("="*60)
    
    # Search GitHub repositories
    url = "https://api.github.com/search/repositories"
    
    params = {
        'q': 'flask',
        'sort': 'stars',
        'order': 'desc',
        'per_page': 5
    }
    
    print(f"Searching for: {params['q']}")
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print(f"Total found: {data['total_count']}")
        print("\nTop 5 repositories:")
        
        for i, repo in enumerate(data['items'], 1):
            print(f"{i}. {repo['name']}")
            print(f"   Stars: {repo['stargazers_count']}")
            print(f"   Description: {repo['description'][:60] if repo['description'] else 'N/A'}...")

def example_3_post_request():
    """POST request to send data."""
    print("\n" + "="*60)
    print("Example 3: POST Request")
    print("="*60)
    
    # Example POST to a test API
    url = "https://httpbin.org/post"
    
    # Data to send
    data = {
        'username': 'alice',
        'email': 'alice@example.com',
        'message': 'Hello from Python!'
    }
    
    print(f"Sending data: {json.dumps(data, indent=2)}")
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        result = response.json()
        print("\nResponse from server:")
        print(f"Received data: {result['json']}")
        print(f"Headers: {result['headers']['Content-Type']}")

def example_4_error_handling():
    """Demonstrate error handling."""
    print("\n" + "="*60)
    print("Example 4: Error Handling")
    print("="*60)
    
    # Try multiple requests with error handling
    urls = [
        "https://api.github.com/users/github",  # Valid
        "https://api.github.com/users/this-user-definitely-does-not-exist-12345",  # 404
        "http://localhost:9999/api/test",  # Connection error
    ]
    
    for url in urls:
        print(f"\nTrying: {url}")
        
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # Raise exception for 4xx/5xx
            
            print(f"✅ Success! Status: {response.status_code}")
            
        except requests.exceptions.Timeout:
            print("❌ Timeout: Request took too long")
            
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error: Could not reach server")
            
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP Error: {e}")
            print(f"   Status Code: {response.status_code}")
            
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

def example_5_headers_and_auth():
    """Request with custom headers."""
    print("\n" + "="*60)
    print("Example 5: Custom Headers")
    print("="*60)
    
    url = "https://httpbin.org/headers"
    
    headers = {
        'User-Agent': 'My-Python-App/1.0',
        'Accept': 'application/json',
        'Custom-Header': 'Hello from Python'
    }
    
    print("Sending custom headers...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print("\nServer received these headers:")
        for key, value in result['headers'].items():
            print(f"  {key}: {value}")

def main():
    """Run all examples."""
    print("🌐 API Request Examples")
    print("="*60)
    
    # Run each example
    example_1_simple_get()
    example_2_get_with_parameters()
    example_3_post_request()
    example_4_error_handling()
    example_5_headers_and_auth()
    
    print("\n" + "="*60)
    print("✅ All examples completed!")

if __name__ == '__main__':
    main()

"""
Try running this:
    python3 examples/04_api_example.py

Exercise:
1. Create a function to fetch weather data from a weather API
2. Make a POST request that sends multiple fields
3. Add retry logic for failed requests
4. Parse and display specific fields from JSON response
5. Create a function that caches API responses

Note: Some examples require internet connection.
If you get SSL errors, try adding: verify=False to requests.get()
(but only for learning purposes!)
"""
