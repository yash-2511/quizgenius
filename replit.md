# AI Quiz Generator from Notes

## Overview

This is an AI-powered web application that extracts text from uploaded documents (PDF, DOCX) and generates interactive multiple-choice quizzes using Google Gemini AI. The application provides a clean, responsive interface for users to upload documents, generate quizzes, and interact with the generated questions.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a traditional client-server architecture with a Flask backend and vanilla JavaScript frontend:

### Frontend Architecture
- **Technology**: Vanilla JavaScript with Bootstrap 5 for UI components
- **Theme**: Dark theme implementation using Bootstrap's dark mode
- **Responsiveness**: Mobile-first responsive design
- **Interaction**: Real-time quiz interaction with immediate feedback
- **File Handling**: Drag-and-drop file upload with visual feedback

### Backend Architecture
- **Framework**: Flask web framework with CORS enabled
- **File Processing**: Modular design with separate processors for different file types
- **AI Integration**: Dedicated service layer for Google Gemini API interactions
- **Storage**: In-memory storage for MVP (quiz and file data)
- **Error Handling**: Comprehensive logging and exception handling

## Key Components

### 1. File Processing System (`file_processor.py`)
- **Purpose**: Extract text from PDF and DOCX files
- **PDF Processing**: Uses PyMuPDF (fitz) for robust text extraction
- **DOCX Processing**: Uses python-docx library for document parsing
- **Error Handling**: Graceful fallbacks when libraries are unavailable

### 2. AI Quiz Generation (`gemini_service.py`)
- **Purpose**: Generate structured quizzes from extracted text
- **API Integration**: Google Gemini API for natural language processing
- **Data Validation**: Pydantic models for structured quiz responses
- **Content Management**: Text truncation for API token limits

### 3. Web Interface (`app.py`)
- **Purpose**: Main Flask application handling HTTP requests
- **File Upload**: Secure file handling with size and type restrictions
- **API Endpoints**: RESTful endpoints for file upload and quiz generation
- **Session Management**: Basic session handling for user interactions

### 4. Frontend Interface (`static/` directory)
- **Purpose**: Client-side quiz interaction and file upload
- **Styling**: Custom CSS with Bootstrap integration
- **JavaScript**: QuizGenerator class for managing quiz state and interactions
- **Template**: Single-page application design with dynamic content sections

## Data Flow

1. **File Upload**: User uploads PDF/DOCX → Server validates and saves file
2. **Text Extraction**: File processor extracts raw text from document
3. **Quiz Generation**: Gemini AI processes text → Generates structured quiz questions
4. **Quiz Display**: Frontend receives quiz data → Renders interactive interface
5. **User Interaction**: User answers questions → Client tracks responses
6. **Results**: Immediate feedback with explanations for correct answers

## External Dependencies

### Required Services
- **Google Gemini API**: Core AI functionality for quiz generation
  - Requires API key configuration
  - Used for natural language processing and question generation

### Python Libraries
- **Flask**: Web framework and routing
- **Flask-CORS**: Cross-origin resource sharing
- **PyMuPDF**: PDF text extraction (optional fallback handling)
- **python-docx**: DOCX document processing (optional fallback handling)
- **google-genai**: Google Gemini API client
- **Werkzeug**: File handling utilities
- **Pydantic**: Data validation and serialization

### Frontend Dependencies
- **Bootstrap 5**: UI framework with dark theme support
- **Font Awesome**: Icon library for enhanced UI
- **CDN-based**: No local JavaScript dependencies

## Deployment Strategy

### Current Setup (Development)
- **Environment**: Development server with debug mode enabled
- **Storage**: In-memory storage for MVP functionality
- **File Management**: Local file system storage in 'uploads' directory
- **Configuration**: Environment variables for API keys and secrets

### Production Considerations
- **Database**: Ready for database integration (Drizzle ORM compatible)
- **File Storage**: Can be extended to cloud storage solutions
- **Scaling**: Stateless design allows for horizontal scaling
- **Security**: CORS enabled, file validation, and secure filename handling

### Environment Configuration
- `GEMINI_API_KEY`: Required for AI functionality
- `SESSION_SECRET`: For session management (falls back to dev key)
- File upload limits: 16MB maximum file size
- Supported formats: PDF and DOCX only

### Architectural Decisions

1. **In-Memory Storage**: Chosen for MVP simplicity, easily replaceable with persistent storage
2. **Modular File Processing**: Separate processors allow for easy extension to new file types
3. **Pydantic Validation**: Ensures consistent AI response structure and type safety
4. **Single-Page Application**: Provides smooth user experience without page reloads
5. **Bootstrap Integration**: Rapid UI development with consistent dark theme
6. **Flask Framework**: Lightweight, flexible framework suitable for the application's scope
7. **Configuration Management**: Centralized config system supporting development/production environments
8. **Local Development Setup**: Automated setup scripts and environment management for easy local deployment

### Recent Changes (July 16, 2025)

- **Added Configuration System**: Created `config.py` with environment-based configuration management
- **Local Development Support**: Added `run_local.py` for easy local server startup with environment setup
- **Setup Automation**: Created `local_setup.py` script for automated dependency installation and directory creation  
- **Enhanced Documentation**: Updated README.md with comprehensive local setup instructions and troubleshooting
- **Improved Error Handling**: Fixed JavaScript error handling for better user feedback
- **Environment Management**: Enhanced .env file support with automatic loading and validation
- **Render Deployment Ready**: Added all necessary deployment files and configuration for Render platform
- **Production Optimization**: Added health endpoint, logging configuration, and deployment testing tools
- **Deployment Documentation**: Created comprehensive deployment guide and checklist for Render deployment