#!/usr/bin/env python3
"""
Local setup script for AI Quiz Generator
Creates necessary directories and configuration files for local development
"""

import os
import sys

def create_directories():
    """Create necessary directories"""
    directories = [
        'uploads',
        'templates', 
        'static'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")
        else:
            print(f"Directory already exists: {directory}")

def create_env_file():
    """Create .env file from example if it doesn't exist"""
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("Created .env file from .env.example")
            print("Please edit .env file and add your GEMINI_API_KEY")
        else:
            with open('.env', 'w') as f:
                f.write("""# Google Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Flask Configuration  
SESSION_SECRET=your_secure_session_secret_here

# Development Settings
FLASK_ENV=development
FLASK_DEBUG=True
""")
            print("Created .env file")
            print("Please edit .env file and add your GEMINI_API_KEY")
    else:
        print(".env file already exists")

def install_requirements():
    """Install required packages"""
    packages = [
        'flask==3.0.0',
        'flask-cors==4.0.0', 
        'google-genai==0.8.0',
        'pymupdf==1.23.14',
        'python-docx==1.1.0',
        'pydantic==2.5.2',
        'werkzeug==3.0.1'
    ]
    
    print("Installing required packages...")
    for package in packages:
        os.system(f'pip install {package}')
    
    print("All packages installed!")

def main():
    """Main setup function"""
    print("Setting up AI Quiz Generator for local development...")
    
    create_directories()
    create_env_file()
    
    if '--install-deps' in sys.argv:
        install_requirements()
    
    print("\nSetup complete!")
    print("\nNext steps:")
    print("1. Edit .env file and add your GEMINI_API_KEY")
    print("2. Run: python main.py")
    print("3. Open http://localhost:5000 in your browser")

if __name__ == '__main__':
    main()