#!/usr/bin/env python3
"""
Local development server for AI Quiz Generator
Run this file to start the application locally
"""

import os
import sys
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def load_env_file():
    """Load environment variables from .env file"""
    env_file = current_dir / '.env'
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
        print("Loaded environment variables from .env file")
    else:
        print("Warning: .env file not found. Please create one with your GEMINI_API_KEY")

def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        'flask',
        'flask_cors', 
        'google.genai',
        'fitz',  # PyMuPDF
        'docx',  # python-docx
        'pydantic'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            if package == 'google.genai':
                import google.genai
            elif package == 'fitz':
                import fitz
            elif package == 'docx':
                import docx
            elif package == 'flask_cors':
                import flask_cors
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        print("Please install them using:")
        print("pip install flask flask-cors google-genai pymupdf python-docx pydantic")
        return False
    
    return True

def main():
    """Main function to start the local server"""
    print("AI Quiz Generator - Local Development Server")
    print("=" * 50)
    
    # Load environment variables
    load_env_file()
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check for API key
    if not os.environ.get('GEMINI_API_KEY'):
        print("Error: GEMINI_API_KEY not found in environment variables")
        print("Please add it to your .env file or set it as an environment variable")
        sys.exit(1)
    
    # Import and run the Flask app
    try:
        from app import app
        print("Starting Flask development server...")
        print("Access the application at: http://localhost:5000")
        print("Press Ctrl+C to stop the server")
        print("-" * 50)
        
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()