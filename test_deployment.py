#!/usr/bin/env python3
"""
Test script to verify the AI Quiz Generator deployment
Run this script to test the application endpoints and functionality
"""

import requests
import json
import sys
import os
from pathlib import Path

def test_health_endpoint(base_url):
    """Test the health check endpoint"""
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Health check passed: {data['service']} v{data['version']}")
            return True
        else:
            print(f"✗ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Health check error: {e}")
        return False

def test_main_page(base_url):
    """Test the main page loads"""
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200 and "AI Quiz Generator" in response.text:
            print("✓ Main page loads successfully")
            return True
        else:
            print(f"✗ Main page failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Main page error: {e}")
        return False

def test_quiz_history(base_url):
    """Test the quiz history endpoint"""
    try:
        response = requests.get(f"{base_url}/quizzes", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Quiz history endpoint working: {len(data.get('quizzes', []))} quizzes")
            return True
        else:
            print(f"✗ Quiz history failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Quiz history error: {e}")
        return False

def create_test_file():
    """Create a test text file for upload testing"""
    test_content = """
    Machine Learning Fundamentals
    
    Machine learning is a subset of artificial intelligence that focuses on algorithms 
    and statistical models that enable computer systems to improve their performance 
    on a specific task through experience. Instead of being explicitly programmed 
    to perform a task, machine learning algorithms build mathematical models based 
    on training data to make predictions or decisions.
    
    Neural networks are computing systems inspired by biological neural networks 
    that constitute animal brains. They consist of interconnected nodes (neurons) 
    that process information using a connectionist approach to computation.
    
    Deep learning is a subset of machine learning that uses neural networks with 
    multiple layers (deep neural networks) to progressively extract higher-level 
    features from raw input.
    """
    
    with open('test_document.txt', 'w') as f:
        f.write(test_content)
    
    return 'test_document.txt'

def test_file_upload(base_url):
    """Test file upload functionality (requires a test file)"""
    test_file = create_test_file()
    
    try:
        # Note: This will fail with .txt file due to validation
        # but tests the endpoint structure
        with open(test_file, 'rb') as f:
            files = {'file': (test_file, f, 'text/plain')}
            response = requests.post(f"{base_url}/upload", files=files, timeout=30)
        
        # Clean up test file
        os.remove(test_file)
        
        if response.status_code == 400:
            data = response.json()
            if "File type not supported" in data.get('error', ''):
                print("✓ File upload validation working (correctly rejected .txt file)")
                return True
        
        print(f"✗ File upload test unexpected result: {response.status_code}")
        return False
        
    except Exception as e:
        # Clean up test file
        if os.path.exists(test_file):
            os.remove(test_file)
        print(f"✗ File upload error: {e}")
        return False

def run_deployment_tests(base_url=None):
    """Run all deployment tests"""
    if not base_url:
        base_url = input("Enter your deployment URL (e.g., https://your-app.onrender.com): ").strip()
        if not base_url:
            base_url = "http://localhost:5000"
    
    # Remove trailing slash
    base_url = base_url.rstrip('/')
    
    print(f"Testing deployment at: {base_url}")
    print("=" * 50)
    
    tests = [
        ("Health Check", lambda: test_health_endpoint(base_url)),
        ("Main Page", lambda: test_main_page(base_url)),
        ("Quiz History", lambda: test_quiz_history(base_url)),
        ("File Upload", lambda: test_file_upload(base_url))
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"  Test failed: {test_name}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your deployment is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Check the logs and configuration.")
        return False

if __name__ == '__main__':
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = None
    
    success = run_deployment_tests(url)
    sys.exit(0 if success else 1)