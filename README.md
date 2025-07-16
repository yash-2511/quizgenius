# AI Quiz Generator from Notes

An AI-powered web application that extracts text from uploaded documents (PDF, DOCX) and generates interactive multiple-choice quizzes using Google Gemini AI.

## Features

- **Document Upload**: Support for PDF and DOCX file formats
- **AI-Powered Quiz Generation**: Uses Google Gemini API to create meaningful MCQ questions
- **Interactive Quiz Interface**: Clean, responsive design with real-time feedback
- **Answer Validation**: Immediate results with explanations for correct answers
- **Quiz History**: View and retake previously generated quizzes
- **File Processing**: Robust text extraction from various document formats

## Tech Stack

### Backend
- **Flask**: Web framework
- **Flask-CORS**: Cross-origin resource sharing
- **PyMuPDF**: PDF text extraction
- **python-docx**: DOCX text extraction
- **google-genai**: Google Gemini AI integration
- **Werkzeug**: File handling utilities

### Frontend
- **HTML5**: Modern markup
- **Bootstrap 5**: Responsive UI framework with dark theme
- **Vanilla JavaScript**: Client-side functionality
- **Font Awesome**: Icons

## Setup Instructions

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Google Gemini API Key** (get it from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone or create the project directory**:
   ```bash
   mkdir ai-quiz-generator
   cd ai-quiz-generator
   